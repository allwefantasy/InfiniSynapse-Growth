---
name: web-ui-review-skill
description: 用本机 agent-browser CLI 对任意 Web 页面做完整的端到端自动化体验——覆盖 UI review（找溢出/断裂/交互坑）、功能链路演练（创建/提交/执行/验证）、以及把整个体验过程写成教程文档。当用户说"体验一下这个页面"、"看看这个站有没有交互问题"、"UI review"、"在界面上走一遍 xxx 流程"、"用浏览器操作一下然后写教程"、"截图分析界面"、"把这次操作整理成文档"时使用。
---

# 浏览器自动化体验 Skill

一套基于 `agent-browser` CLI 的**可复现工作流**，把"人去打开浏览器、动手体验、截图记录、写报告"这个过程**完全程式化**，让 Agent 能独立完成。

## 本 skill 覆盖的 3 类任务

| 任务类型 | 示例 | 对应工作流 |
|---|---|---|
| **UI/UX 审查** | "Dashboard 有没有交互上的问题？" | 工作流 A —— 详见 [workflows.md § A](workflows.md#a-uiux-审查工作流) |
| **功能链路体验** | "创建一个需求、运行、等完成、再拖到已完成" | 工作流 B —— 详见 [workflows.md § B](workflows.md#b-功能链路体验工作流) |
| **体验 → 写教程** | "体验完顺便写份用户教程文档" | 工作流 C —— 详见 [workflows.md § C](workflows.md#c-体验写教程工作流) |

这三类任务在 agent-browser 层面**共享同一套基础命令**，只是组合策略和收敛产物不同。本文件只讲**公共基础**和**决策路径**，具体命令串在 `workflows.md` 里展开。

---

## 决策树：进来之后先问自己 3 个问题

```
Q1. 用户的最终产物是？
    ├─ "找 bug / 提改进建议" ───────────▶ 用 工作流 A（UI/UX 审查）
    ├─ "把某条流程跑通 + 留截图证据" ──▶ 用 工作流 B（功能链路）
    └─ "教别人怎么用" ─────────────────▶ 用 工作流 C（体验 → 写教程）

Q2. 页面是否需要登录？
    ├─ 是 ─▶ 先截登录页，然后 ask 用户手动登录（daemon 是 headed）
    └─ 否 ─▶ 直接往下走

Q3. 本次体验需要"真实提交数据"吗？（创建订单、写入数据库、发消息等）
    ├─ 是 ─▶ 选"小而美 + 可回滚"的示例数据（比如改 README 一行文本）
    └─ 否 ─▶ 随便填，但保持语义清晰
```

---

## 工具前提

- 全局 Cursor Rule `use-agent-browser-for-web.mdc` 已开启 → **浏览器相关操作必须走 `agent-browser`**；禁止用 WebFetch/curl/临时搭 Puppeteer。
- 本机路径：`~/.auto-coder/.autocodertools/agent-browser`
- 查命令速览：`agent-browser --help`；查 AI 完整指南：`agent-browser --skill`；查站点专属技巧：`agent-browser site-skills --name <domain>`
- 配套规则：输出 PDF 时用 `use-markdown2pdf-for-pdf.mdc` → `~/.auto-coder/.autocodertools/markdown2pdf convert report.md`

---

## 8 个通用基础动作（所有工作流的"原子操作"）

### 1. 准备工作目录 + 启动 daemon

```bash
mkdir -p /tmp/<task-name> && cd /tmp/<task-name>
~/.auto-coder/.autocodertools/agent-browser daemon status
# 没跑就：agent-browser daemon start
```

`daemon` 带持久 profile（`~/.agent-browser/profile`），**登录态跨会话保留**，是 agent-browser 最爽的能力，不要走 `--cdp` 那种老路。

### 2. 打开目标 URL + 等待加载

```bash
~/.auto-coder/.autocodertools/agent-browser open <URL>
~/.auto-coder/.autocodertools/agent-browser wait --load networkidle
~/.auto-coder/.autocodertools/agent-browser get url    # 验证有没有被重定向
~/.auto-coder/.autocodertools/agent-browser get title
```

**大坑提醒**：很多现代页面（含 WebSocket / SSE / 长轮询）**永远不进 networkidle**，`wait --load networkidle` 会在 10 秒后**超时**。这是**正常现象**不是失败，页面其实已经能用了。处理方式：

- 超时后直接 `wait 2000` 补一个固定时长 + 截图看
- 或者 `wait --text "某个肯定会出现的关键文本"`
- 或者 `wait <selector>` 等关键元素出现

### 3. 三件套素材（每个关键画面都拿）

```bash
~/.auto-coder/.autocodertools/agent-browser screenshot ./NN-viewport.png         # 首屏
~/.auto-coder/.autocodertools/agent-browser screenshot --full ./NN-full.png      # 整页
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c                       # 仅交互元素，紧凑
```

**读图**：只用 Cursor 的 Read 工具读 PNG（会直接渲染图像）；**不要** `cat` / `base64`。

**命名**：用 `NN-<动作>-<状态>.png` 格式，例如 `01-login.png` → `02-dashboard.png` → `03-new-form.png`，教程复用时更直观。

### 4. 找溢出容器（UI review 必做）

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const hits = [...document.querySelectorAll('*')].filter(n => {
    const s = getComputedStyle(n);
    return (s.overflowX === 'auto' || s.overflowX === 'scroll')
        && n.scrollWidth > n.clientWidth + 10;
  }).slice(0, 5).map(n => ({
    tag: n.tagName,
    cls: (n.className || '').toString().slice(0, 120),
    sw: n.scrollWidth, cw: n.clientWidth, diff: n.scrollWidth - n.clientWidth
  }));
  return JSON.stringify(hits);
})()"
```

找到溢出容器后**强制滚到底**再截图看尾部：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const el = document.querySelector('<上一步拿到的 selector>');
  el.scrollLeft = el.scrollWidth;
  return el.scrollLeft + '/' + (el.scrollWidth - el.clientWidth);
})()"
~/.auto-coder/.autocodertools/agent-browser screenshot ./NN-scrolled.png
```

### 5. 定位 + 点击元素

**优先级**（稳定性从高到低）：

1. `click --text "精确文字"` —— 有稳定文案时首选
2. `find role button click --name "提交"` —— 语义定位
3. `click @e<N>` —— 用 snapshot 给的 ref（ref 会随 DOM 变化失效，别跨 snapshot 复用）
4. `click <CSS selector>` —— 兜底

```bash
~/.auto-coder/.autocodertools/agent-browser click --text "新建需求"
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser screenshot ./NN-after-click.png
```

**陷阱**：`find text` 是**模糊匹配**，容易误击到左侧栏同名链接。如果多个地方都叫同一个词（比如"新建需求"在 Tab 和模态按钮上都有），加 `--exact` 或者改用 ref。

### 6. 填表单（text / textarea / contenteditable 三种）

```bash
# 普通 input / textarea
~/.auto-coder/.autocodertools/agent-browser fill @e41 "需求标题"

# 多行（验收标准等）— \n 需要真实换行，shell 字符串用双引号 + 真换行
~/.auto-coder/.autocodertools/agent-browser fill @e45 "- 条件 1
- 条件 2
- 条件 3"

# 富文本编辑器（ProseMirror / Tiptap / Slate 等）
~/.auto-coder/.autocodertools/agent-browser fill @e60 "内容"   # fill 会自动 fallback
# 或：~/.auto-coder/.autocodertools/agent-browser inserttext "内容"
```

填完**先检查按钮是否启用**再点：

```bash
~/.auto-coder/.autocodertools/agent-browser is enabled @e62
~/.auto-coder/.autocodertools/agent-browser click @e62
```

### 7. 切视口（验证响应式）

```bash
~/.auto-coder/.autocodertools/agent-browser set viewport 1440 900    # 笔记本
~/.auto-coder/.autocodertools/agent-browser set viewport 1024 768    # 小笔记本/平板
~/.auto-coder/.autocodertools/agent-browser set viewport 414 896     # 手机
```

切完必 `wait 500` 让布局重排再截图。

### 8. 拖拽（HTML5 DnD 的特殊处理）⚠️

这是**最容易翻车**的动作。

- `agent-browser drag <src> <dst>` 和 `mouse down/move/up` **对基于 HTML5 DnD（`draggable="true"`）的页面无效**，因为 Playwright 的真实鼠标事件不会触发合成的 `dragstart/dragover/drop`
- 大部分现代 React 看板（dnd-kit / react-dnd / 手写 draggable）都吃这个亏
- **正确做法**：用 `eval` 手动 `dispatchEvent`：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const src = document.querySelector('<源元素 selector>');
  const dst = document.querySelector('<目标容器 selector>');
  if (!src || !dst) return 'missing';
  const dt = new DataTransfer();
  const sr = src.getBoundingClientRect();
  const dr = dst.getBoundingClientRect();
  const fire = (el, type, x, y) => el.dispatchEvent(new DragEvent(type, {
    bubbles: true, cancelable: true, clientX: x, clientY: y, dataTransfer: dt
  }));
  fire(src, 'dragstart', sr.x + sr.width/2, sr.y + sr.height/2);
  fire(dst, 'dragenter', dr.x + dr.width/2, dr.y + 100);
  fire(dst, 'dragover',  dr.x + dr.width/2, dr.y + 100);
  fire(dst, 'drop',      dr.x + dr.width/2, dr.y + 100);
  fire(src, 'dragend',   dr.x + dr.width/2, dr.y + 100);
  return 'dispatched';
})()"
```

> 先试一次真实 `mouse` 操作，**如果卡片纹丝不动** = HTML5 DnD = 切到 dispatchEvent 方案。

拖完一定要 **刷新页面 + 再截图** 验证状态**真的持久化**到了后端（否则可能只是前端状态）。

---

## 常见 UI 问题 → 对应验证动作

| 问题类型 | 怎么验证 |
|---|---|
| 看板/表格横向溢出 | 基础动作 4（找溢出）+ `scrollLeft = scrollWidth` 强滚到底截图 |
| 骨架屏/loading 一直不消失 | `wait --load networkidle` 之后仍 `is visible <skeleton>` 为真 |
| 按钮点了没反应 | 点前 `get url` → 点击 → `wait 1500` → `get url` + `snapshot -i -c` 前后对比 |
| 模态关不掉 | `find text "close" click` / `press Escape` 后 `snapshot` 看模态是否消失 |
| 深色模式下对比度差 | `set media dark` 后重新截图对比 |
| 小屏断裂 | 基础动作 7 切到 `414 896` + 全页截图 |
| 刷新后数据丢 | `reload` + `wait 2000` + 再截图对比是否一致 |
| 拖拽不生效 | 基础动作 8 的 HTML5 DnD dispatchEvent 方案 |

---

## 产物收敛模板

### 模板 1：UI 审查报告（工作流 A 末尾）

```markdown
## UI 体验报告：<页面名>

### 环境
- URL: <最终 URL>
- 视口: 1440×900 / 1024×768
- 截图目录: <路径>

### 发现的问题
1. **<问题标题>**（严重度：高/中/低）
   - 现象：一句话描述
   - 截图：`NN-xxx.png`
   - 触发条件：<视口宽度 / 某个操作 / 数据量>
   - 证据：`eval` 输出里的 scrollWidth/clientWidth 等硬数据
   - 建议：修改方向（非代码级别）

### 值得表扬的地方
- （可选）顺手说一两个设计得不错的点
```

### 模板 2：链路体验总结（工作流 B 末尾）

```markdown
## <功能> 链路体验记录

### 执行步骤
| 步骤 | 动作 | 预期 | 实际 | 截图 |
|---|---|---|---|---|
| 1 | 进入 Dashboard | 看到 5 列看板 | ✅ 看到 5 列 | `01.png` |
| 2 | 点"新建" | 弹表单 | ✅ | `02.png` |
| ... |

### 关键验证点
- [ ] 后端持久化：刷新后状态保留
- [ ] 副作用正确：`git diff` 只改目标文件
- [ ] 顺带发现的 bug：<列表>
```

### 模板 3：教程文档目录（工作流 C 产物）

```
<topic-tutorial>/
├── README.md            # 主教程，节号 1~N
└── images/
    ├── 01-<step>.png
    ├── 02-<step>.png
    └── ...
```

文件放在 `~/projects/william-docs/产品/<产品名>/文章/<topic>-tutorial/`。

---

## 反模式（见到就阻止自己）

1. ❌ 点击没有等待就截图 → **必然**截到 loading 态，看不到真实界面
2. ❌ 跨 snapshot 复用 `@eN` ref → ref 随 DOM 重绘失效，先重新 snapshot
3. ❌ 真实鼠标拖 HTML5 DnD 拖不动就放弃 → 改 dispatchEvent
4. ❌ 用 `cat` 输出 PNG → 屏幕上一堆乱码且毫无意义
5. ❌ 多视口测试只测 1 种 → 漏掉的都是用户真实报 bug 的宽度
6. ❌ 拖拽完成后不刷新验证 → 可能只是前端状态，没写后端
7. ❌ 截图文件混在项目根或 `/tmp` 根 → 下次任务无法复用，先建 `/tmp/<task-name>/`

---

## 工作流分派

三类任务的**完整命令串 + 真实案例**见配套文件：

- **[workflows.md § A — UI/UX 审查工作流](workflows.md#a-uiux-审查工作流)**：7 步闭环
- **[workflows.md § B — 功能链路体验工作流](workflows.md#b-功能链路体验工作流)**：以"auto-coder.chat 看板创建并运行需求"为例，10 步完整操作
- **[workflows.md § C — 体验 → 写教程工作流](workflows.md#c-体验写教程工作流)**：从素材到 Markdown 教程的结构化模板

---

## 与其他 skill / rule 的关系

- **前置规则**：`~/.cursor/rules/use-agent-browser-for-web.mdc`（或项目级副本）—— 决定"所有浏览器操作走 agent-browser"
- **姊妹规则**：`~/.cursor/rules/use-markdown2pdf-for-pdf.mdc` —— 教程/报告要导 PDF 时配合使用
- **同项目其他 skill**：
  - `open-project-skill` — 理解目标项目背景，用于功能链路体验前做 context 准备
  - `md2pdf-skill` — 教程完成后转 PDF 分发

---

*本 skill 的每一条实践都来自真实工作流验证，后续遇到新坑请直接更新此文件。*
