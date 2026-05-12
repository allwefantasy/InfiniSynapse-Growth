---
name: infinisynapse-app-skill
description: 用 agent-browser CLI 在 InfiniSynapse SaaS 控制台（app.infinisynapse.com / .cn）里跑完整自动化流程的操作手册——覆盖 URL 路由、侧边栏结构、关键选择器、提交问题、5 阶段任务轮询、滚动进入对话内容（双 .overflow-auto 容器陷阱）、三点菜单（Save to memory / Move to Project / Delete）、记忆库召回的 prompt 写法、antd 弹窗按钮中文带空格（"取 消" / "确 认" / "确 定"）的 JS 修法、Modal vs Popconfirm 的容器区分、订阅生命周期三层状态 + 真正取消订阅的隐藏入口、**`.compact-tool-row` 执行明细面板（点步骤行→右侧弹 SQL+数据表/图表查看器，含最大化按钮，录屏神器）**、**"文件" tab 的产物下载（单文件 / 批量 zip，及 daemon 不落盘的 `URL.createObjectURL` monkeypatch workaround）**、以及把这些组合起来跑一个端到端业务流程或录屏 demo。当用户说"在 InfiniSynapse 里问一句"、"用 app.infinisynapse 跑一个分析"、"把会话存进记忆库"、"在 InfiniSynapse 控制台体验/截图/写教程"、"录一段 InfiniSynapse demo"、"订阅一个数据集"、"调用 RAG 召回上次的分析"、"展示 AI 跑了什么 SQL / 看每步明细 / 把 SQL 或图表放大显示"、"把 InfiniSynapse 生成的 SVG / CSV / 文件下载到本地"时使用。这是配合 web-ui-review-skill 的站点专属增量手册——基础动作走 web-ui-review-skill，本 skill 只补 InfiniSynapse 控制台的特异性。**录屏 demo 联用 screen-subtitled-recording-skill 时务必先读 §3.3 §3.4 §4.1 §5.2 §5.3 §8.3**，那几节是 antd 选择器陷阱 + 执行明细面板 + 文件下载能力的全部修法。
---

# InfiniSynapse 控制台（app.infinisynapse.com）操作 Skill

一份**站点专属的反复踩坑手册**：把"用 agent-browser 驱动 `app.infinisynapse.com` 完成数据分析任务"程式化。

和姊妹 skill 的分工：

- [`web-ui-review-skill`](../web-ui-review-skill/SKILL.md) —— 通用浏览器自动化基础（8 个原子动作、ProseMirror 坑、HTML5 DnD 等），本 skill **直接复用**，不重复写。
- [`winclaw-infinisynapse-skill`](../winclaw-infinisynapse-skill/SKILL.md) —— 把 InfiniSynapse 接进 **WinClaw 本机（127.0.0.1:9199）**，通过 `agent_infini` Command Tool 在 WinClaw 里调起远端能力。**本 skill 走的是反向**：直接驱动 InfiniSynapse 自己的 Web 控制台。

---

## 何时用本 skill

| 用户说法 | 走 |
|---|---|
| "在 InfiniSynapse 里问一下 XXX" | 直接 → §3 提问 |
| "把这个会话存进记忆库" | →§5 记忆库写入 |
| "新开一个会话接着昨天那个分析" | → §6 记忆库召回 |
| "登录后看不到内容 / 让我手动登录" | → §1 登录态预检 |
| "InfiniSynapse 这个页面有没有 bug" | 套 web-ui-review-skill 工作流 A，本 skill 给路由 + 选择器 |
| "把控制台体验过程写成教程" | 套 web-ui-review-skill 工作流 C，本 skill 提供截图清单 |
| "展示 AI 跑了什么 SQL / 看每步明细 / 演示执行过程" | → §5.2 `.compact-tool-row` 执行明细面板（最大化截图）|
| "把 InfiniSynapse 生成的 SVG / 数据文件下载下来" | → §5.3 "文件" tab + monkeypatch createObjectURL workaround |
| "把 InfiniSynapse 接进 WinClaw" | ❌ 不走本 skill，走 `winclaw-infinisynapse-skill` |

---

## 0. 域名口径

- **主域名**：`app.infinisynapse.com`（本 skill 默认用这个）
- **国内同源**：`app.infinisynapse.cn`（行为基本一致，路由相同；`winclaw-infinisynapse-skill` 用的是这个）
- 两个域名**登录态独立**——daemon profile 里的 cookie 是按 origin 存的，第一次跑哪个就在哪个上扫码登录。
- 用户没特别指定就用 `.com`；如果说"国内 / .cn"再切。

---

## 1. 登录态预检（每次会话开头）

```bash
# 0) daemon 在跑且 viewport 设了
~/.auto-coder/.autocodertools/agent-browser daemon status     # 没起就 daemon start
~/.auto-coder/.autocodertools/agent-browser set viewport 1440 900

# 1) 打开任务首页，看是否已登录
~/.auto-coder/.autocodertools/agent-browser open "https://app.infinisynapse.com/tasks"
~/.auto-coder/.autocodertools/agent-browser wait 2500
~/.auto-coder/.autocodertools/agent-browser get url
# 已登录 → URL 保持在 /tasks
# 未登录 → 会被重定向到登录页，URL 含 /login 之类
```

**判定登录的硬信号**：截图首屏能看到大字 **"What can I do for you?"** + 输入框 + 右上角配额（如 `99,999.95`）+ 头像。看不到就让用户手动扫码。

---

## 2. URL 路由地图（直接 `open` 跳过点菜单）

| 页面 | URL | 说明 |
|---|---|---|
| 任务首页（New Task） | `/` 或 `/tasks` | 默认主页，有"What can I do for you?"输入框 |
| 具体任务详情 | `/tasks?taskId=<uuid>` | 提交问题后会自动跳到这里 |
| 我的数据源（数据库） | `/database/private` | "My Data → Data Source" |
| 我的知识库（RAG） | `/rag/private` | "My Data → Knowledge Base" |
| 订阅的知识库 | `/rag/my` | "My Subscriptions → Subscribed Knowledge Base" |
| API Key 管理 | `/ai/apikey` | 左下齿轮里 |
| 仪表盘（Dashboard） | `/dashboard` 系列 | 顶部菜单 |
| 搜索（Search） | `/search` | 顶部菜单 |

**直跳省事**：`agent-browser open <url>` 比"点菜单 → 等待 → 点子菜单"稳得多。

---

## 3. 侧边栏结构 + 选择器

侧边栏是 `.manus-sidebar.expanded`，从上到下：

```
.manus-sidebar.expanded
├── (顶) New Task / Search / Dashboard
├── My Subscriptions ▼   .sidebar-section  (展开后含 Subscribed Data / Subscribed Knowledge Base)
├── My Data ▼            .sidebar-section  (展开后含 Data Source / Knowledge Base)
├── PROJECTS ▼           .sidebar-section
└── ALL TASKS ▼          .tasks-section
    └── .task-list
        └── .task-item[.active]
            ├── .task-status-icon (✓ 绿圈)
            ├── .task-name        ← 任务标题（截断）
            └── .task-more-btn.ant-dropdown-trigger ← 三点菜单 ⭐
```

### 3.1 重名陷阱（必须 `--exact`）

| 文案 | 重复出现的位置 | 处理 |
|---|---|---|
| `"Data Source"` | 侧边栏菜单 + 首页 Data Marketplace 段落正文 | 必须 `click --text "Data Source" --exact` |
| `"New Task"` | 单独按钮，无重复，可直接 click 但加 `--exact` 更稳 | `click --text "New Task" --exact` |
| `"My Data"` | 单独，但是个**展开标签**——点一次展开，再点一次会折叠 | 直接 `open /database/private` 更稳 |

**经验**：能用 URL 直跳就别点菜单，省一类陷阱。

### 3.2 三点菜单（任务列表行）

每个 `.task-item` 末尾的 `.task-more-btn.ant-dropdown-trigger` 就是 ··· 菜单触发器。**默认隐藏直到 hover**，但 selector 直接 click 也能触发：

```bash
# 当前激活的任务（侧边栏左边那条带高亮的）
~/.auto-coder/.autocodertools/agent-browser click ".task-item.active .task-more-btn"
~/.auto-coder/.autocodertools/agent-browser wait 1000
```

弹出的下拉菜单选项（按现版本顺序）：

1. **Save to memory** —— 把整个会话沉淀进账号级隐性记忆库
2. **Move to Project** —— 归入侧边栏 PROJECTS 下的某个项目
3. **Delete** —— 删除任务

### 3.3 antd 弹窗按钮的"中文空格"陷阱 ⭐⭐⭐ 最容易翻车

InfiniSynapse 控制台用 ant design 4.x，**`Modal.confirm` / `Popconfirm` 这类内置弹窗的中文按钮，文案里会被自动塞一个空格**：`确 认` 而不是 `确认`、`取 消` 而不是 `取消`、`确 定` 而不是 `确定`。这是 antd 的 letter-spacing 渲染逻辑，DOM 里的 `textContent` 真的就是带空格的。

**翻车现场**：

```bash
# ❌ 卡 10 秒超时, 永远找不到
~/.auto-coder/.autocodertools/agent-browser click --text "确认" --exact
# locator.click: Timeout 10000ms exceeded
#   - waiting for getByText('确认', { exact: true })

# ❌ 不加 --exact 也不行 (因为还有别的元素含 "确认" 子串)
~/.auto-coder/.autocodertools/agent-browser click --text "确认"

# ✅ 必须用 JS, textContent 去空格再比
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const modals = [...document.querySelectorAll('.ant-modal, .ant-popover, .ant-popconfirm')]
    .filter(m => m.offsetParent && m.getBoundingClientRect().height > 50);
  for (const m of modals) {
    const btn = [...m.querySelectorAll('button, [role=button]')].find(b =>
      b.textContent.replace(/\s/g,'') === '确认');
    if (btn) { btn.click(); return 'clicked'; }
  }
  return 'not-found';
})()"
```

**双重打击**：除了文案带空格，**`agent-browser snapshot` 还不输出 modal 内的按钮**。snapshot 只列页面顶层的 interactive elements，弹窗里的 "取 消 / 确 认" 完全不在输出里，所以你不知道它的 ref，也不知道它文案有空格——只能靠 click 超时报错才发现。

**自定义按钮 ≠ antd 内置按钮，文案规则不同**：

| 按钮来源 | 文案样式 | 例子 |
|---|---|---|
| 自定义 `<button>` (卡片/列表里的"订阅 / 取消 / 查看") | **没空格** | `订阅` / `取消` / `查看` |
| antd `Modal.confirm` / `Popconfirm` 弹窗按钮 | **带空格** | `取 消` / `确 认` / `确 定` |
| antd `Button type="primary"` 普通按钮（页面正文里） | **看具体 wrapper** | 多数无空格，但建议用 JS 验证 |

**通用稳妥做法**：所有"点 antd 弹窗按钮"的场景都用 JS 选择器，`textContent.replace(/\s/g,'') === '<目标文案>'`。**别用 `--text` / `--exact`**，它们对 antd 中文带空格按钮一律不灵。

### 3.4 三类"看着像确认弹"的容器，类名不同 ⚠️

点了某个"危险动作"按钮后跳出的小框，可能是三种不同 DOM 结构之一，**选择器要全覆盖**：

| 容器类 | 触发场景 | 形态 | 关闭方式 |
|---|---|---|---|
| `.ant-modal` | `Modal.confirm()` / `<Modal>` | 居中遮罩 + 标题 + 正文 + 底部按钮 | 顶部 X (`.ant-modal-close`) 或底部按钮 |
| `.ant-popover` / `.ant-popconfirm` | `<Popconfirm>` 行内确认 | 紧贴触发按钮的小气泡 | 只有内部"确 定 / 取 消"按钮 |
| `.ant-dropdown` | 下拉菜单（如三点菜单） | 紧贴触发按钮的菜单列表 | 点外部或选项 |

**判断技巧**：截图看尺寸 / 位置——居中遮罩是 Modal，紧贴某个按钮的气泡是 Popconfirm，竖排菜单是 Dropdown。**写选择器时三个 class 都加上保险**：

```js
const containers = [...document.querySelectorAll(
  '.ant-modal, .ant-popover, .ant-popconfirm, [class*=Dropdown]'
)].filter(c => c.offsetParent && c.getBoundingClientRect().height > 30);
```

特别注意 **Popconfirm 的"确 定"是 `确 定` 不是 `确 认`**——一字之差但 antd 默认两个不同弹窗用不同文案：

- `Modal.confirm({ okText: ..., cancelText: ... })` → 默认 "确 认 / 取 消"
- `Popconfirm` → 默认 "确 定 / 取 消"

最稳的 JS 模式：

```js
const ok = ['确认', '确定', '是', '同意'];
const btn = [...container.querySelectorAll('button')].find(b =>
  ok.includes(b.textContent.replace(/\s/g, '')));
```

---

## 4. 提交问题：输入框 + 发送按钮 ⚠️

进 `/tasks` 之后跑 snapshot 看到的典型布局：

```
- textbox "Please enter your question..." [ref=e1]   ← 主输入框
- button "plus"          [ref=e2]
- button "picture"       [ref=e3]
- button "Database"      [ref=e4]
- button "cloud-server"  [ref=e5]
- button "chrome"        [ref=e6]
- button "∞ Agent "      [ref=e7]                    ← 模式切换
- button ""              [ref=e8]                    ← 🟢 发送按钮（label 是空的！）
- button " openai/gpt-5.4" [ref=e9]                  ← 模型选择
- textbox "Search data..." [ref=e10]
```

### 4.0 任务详情页 vs 首页输入框 ⭐⭐ (2026-05-05 v9 实战补)

InfiniSynapse 的输入框在两个地方**底层实现完全不同**, 选择器不能复用:

| 位置 | DOM 结构 | placeholder | fill 方式 |
|---|---|---|---|
| **首页** `/tasks` (新建任务) | `textarea[placeholder*="问题"]` | "请输入您的问题..." | React setter (HTMLTextAreaElement.value) + dispatch input |
| **任务详情页** `/tasks?taskId=...` (追问) | `div.cib-editable[contenteditable=true]` | 兄弟节点 DIV 的文字 "输入消息..." | `document.execCommand('insertText', false, txt)` |

**任务详情页 fill 的标准写法**:

```js
const editor = document.querySelector('div.cib-editable[contenteditable=true]');
editor.focus();
// 清空
const range = document.createRange();
range.selectNodeContents(editor);
const sel = window.getSelection();
sel.removeAllRanges();
sel.addRange(range);
document.execCommand('delete', false, null);
// 插入
document.execCommand('insertText', false, '你的追问内容');
editor.dispatchEvent(new InputEvent('input', { bubbles: true }));
```

**为什么不能用 React setter?** cib-editable 是富文本 contenteditable, 不是 textarea. `tb.value=...` 不存在; 直接改 innerHTML 不会触发 React 的状态同步. **execCommand('insertText') 是 contenteditable 的官方插入接口**, 兼容 React.

**Bash 里传中文文本**: 用 base64 避免 shell escape 灾难:

```bash
B64=$(printf '%s' "$TXT" | base64 | tr -d '\n')
$AGENT eval "(() => {
  const bytes = Uint8Array.from(atob('${B64}'), c => c.charCodeAt(0));
  const txt = new TextDecoder('utf-8').decode(bytes);
  // ... fill ...
})()"
```

### 4.1 发送按钮的"空 label"陷阱 ⭐

`button "" [ref=e8]` —— **label 是空字符串**，因为它就是个图标按钮。所以：

- ❌ `click --text "Send"` —— 找不到
- ❌ `find role button --name "Send"` —— 名字是空，匹配不上
- ✅ **当场 snapshot 拿 ref**（首选，但每次操作后 DOM 可能重排，ref 会变）
- ✅ 或者按 Enter 提交：`fill @e1 "..."` + `press Enter`（次选，有时会被 textarea 吃掉换行）
- ✅ **JS 选择器（最稳，不依赖 ref）**：见 §4.1.2

**标准串（基于 snapshot ref）**：

```bash
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | head -10
# 抽出 textbox 的 ref 和发送按钮的 ref
~/.auto-coder/.autocodertools/agent-browser fill @e1 "<your question>"
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser click @e8       # 紧贴发送按钮 ref
~/.auto-coder/.autocodertools/agent-browser wait 4000
~/.auto-coder/.autocodertools/agent-browser get url         # 应该跳到 /tasks?taskId=<uuid>
```

#### 4.1.1 用 awk/grep 抽 send ref 的常见挂法

跑长脚本时常见这种写法："grep snapshot 输出抽 ref → 拼成 `@eN` → click"。**坑很多**：

```bash
# ❌ awk match()/RSTART/RLENGTH 在 BSD/GNU awk 上行为不一致
SEND_REF=$(snapshot | awk '/button ""/{ match($0, /ref=e[0-9]+/); print substr(...) }')
# 实际跑出来 SEND_REF="" 是常见结果, 然后 click @ 报 "Unexpected token @"

# ✅ 用 grep -oE, 简单稳定
SEND_REF=$($AGENT snapshot -i -c | grep -E '^- button "" \[ref=' | head -1 | grep -oE 'ref=e[0-9]+' | sed 's/ref=//')
echo "[debug] SEND_REF=$SEND_REF"     # 一定要 echo 确认拿到了再 click
[[ -z "$SEND_REF" ]] && { echo "ERROR: send ref empty"; exit 2; }
$AGENT click "@$SEND_REF"
```

**调试纪律**：所有"snapshot 抽 ref → 后续 click" 之前都 `echo` 一下，**空字符串就立刻退出**，别让脚本继续跑成"click @"语法错误。

#### 4.1.2 完全不依赖 ref 的 JS click（推荐用于自动化录屏 / CI）

发送按钮的稳定特征：
1. 在 textarea 容器内
2. 文本为空（`textContent.trim() === ''`）
3. 没有 `anticon-*` 子元素（区别于 plus / picture / database / cloud-server / chrome / ellipsis 这些 icon 按钮）
4. 可见（`width × height ≥ 20 × 20`）
5. **位置最靠右**（textarea 容器内 x 最大的那个）

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const tb = document.querySelector('textarea[placeholder*=\"问题\"], textarea[placeholder*=\"question\"]');
  if (!tb) return 'no-textbox';
  let container = tb;
  for (let i = 0; i < 6 && container; i++) container = container.parentElement;
  const candidates = [...container.querySelectorAll('button')].filter(b => {
    if (b.textContent.trim()) return false;
    const r = b.getBoundingClientRect();
    if (r.width < 20 || r.height < 20) return false;
    if (b.querySelector('[class*=anticon]')) return false;
    return true;
  });
  candidates.sort((a,b) => b.getBoundingClientRect().x - a.getBoundingClientRect().x);
  if (candidates.length) {
    candidates[0].click();
    const r = candidates[0].getBoundingClientRect();
    return JSON.stringify({clicked: true, x: r.x|0, y: r.y|0});
  }
  return 'no-send-btn';
})()"
```

实测 2026-05-04 在 `app.infinisynapse.cn` 上稳定命中 (1140, 331) 那个 button——它正是 send 按钮。这种写法 **完全不依赖 ref**，DOM 怎么重排都不怕。

#### 4.1.3 textbox fill 的 JS fallback (绕开 actionability 检查)

`agent-browser fill @eN` 走 Playwright，会做 actionability 检查（element 必须可见且不被遮挡）。**有时弹窗刚关闭还在动画过程中，fill 会超时失败**。fallback 方案：用 React 兼容的 setter 直接注入，再触发 onChange：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const tb = document.querySelector('textarea[placeholder*=\"问题\"]');
  if (!tb) return 'no-tb';
  // React 控制的 textarea 不能直接 tb.value=..., 必须用原型链上的 setter
  const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  setter.call(tb, '你的问题文字...');
  tb.dispatchEvent(new Event('input', {bubbles: true}));
  return JSON.stringify({value: tb.value, len: tb.value.length});
})()"
```

清空 textbox 同样用这套（setter.call(tb, '')）。

### 4.2 提交后的状态切换 ⭐⭐ (2026-05-05 v9 实战修正)

**之前版本说"红色方块的停止按钮"是错的** —— 实测 send 按钮在生成中变成 **`bg=rgb(30, 30, 30)` 黑色**, 不是红色. 颜色检测**完全不可靠**, 别用.

**最稳的"在跑"信号: 进度数字 N/M, N<M 即在跑** (见 §7.1.1 综合信号检测).

**提交是否成功的快速验证**:
- send 之前: editor.innerText 有内容
- send 之后 1-3s: editor.innerText 被清空 (变 `\u200b` 零宽空格或空)
- 如果 send 后 editor 仍有原文 → **send 被吞掉了**, 任务可能已卡死, 后续追问大概率失败

**任务卡死的征兆 (见到要 abort)**:
- last_prog 卡在某个 N/M (比如 1/2) 持续 10+ 分钟不动
- 页面文本里出现 "API 请求已取消" / "暂无数据" 但任务没标完成
- 此时新追问的 textbox 会被清空但 send 不真生效

**对策**: 直接 `open /tasks` 开新会话, 别在卡死的任务页死磕.

---

## 5. 任务执行：5 阶段计划 + 类型标签

InfiniSynapse 的 Agent 提交后会**自己规划阶段**（一般 3~6 个），每个阶段有：

- **进度图标**：`▶`（当前在跑）/ `✓`（完成）/ `○`（pending）
- **阶段名**：自然语言（如 "Discover relevant registration tables and schema"）
- **阶段类型 tag**（关键诊断信号）：

| 类型标签 | 含义 |
|---|---|
| **Data Analysis** | 在数据源上跑 SQL / 查询 / 计算 |
| **RAG Research** | **去知识库或记忆库做检索** ⭐ |
| **Technical Writing** | 整理最终回答（Markdown / 表格 / 总结句） |

**"RAG Research" 出现在 Phase 1 是记忆库被命中的硬证据**——见 §6.3。

### 5.1 阶段进度的 DOM 抓取

底部那条状态条文案可以从 `body.innerText` 末 500 字符直接读：

```bash
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const txt = document.body.innerText;
  return JSON.stringify({ text_len: txt.length, last_500: txt.slice(-500) });
})()"
```

末尾通常是 `...<阶段名>\n<i>/<N>\nType a message...\n<model>\n∞\nAgent\n...`，可以用正则抠 `(\d+)\/(\d+)` 拿到当前阶段进度。

### 5.2 执行明细面板：`.compact-tool-row` 是可点步骤行 ⭐⭐⭐ 录屏 / 写教程必用

任务详情页 Agent 跑动过程中，每一个工具调用（SQL 查询 / 探索表结构 / 加载文档 / 绘图 等）都会渲染成一行紧凑的"工具行"，class 是 **`.compact-tool-row`**，cursor:pointer。**点一下就在右侧弹出"任务查看"面板**，把这一步背后的 SQL 代码 / 数据表（带分页）/ 图表 全部展开给你看——演示 AI 工作过程的核心抓手。

#### 5.2.1 触发器特征

```
.compact-tool-row    ← cursor:pointer
├── (icon ⊞ 表格图标，有时其它形状)
└── 文本：<步骤名> + <时间戳>，例如 "用数值排序键正确排序16-24岁失业率趋势  2026/5/5 11:25:29"
```

行外层包裹 span (cursor:pointer)，整行都可点。**所以 click `.compact-tool-row` 本身即可，不用打到 icon 上**。

#### 5.2.2 面板形态：默认半屏（右侧）/ 最大化（占满主区域）

打开后右上角会出现 tab：`当前会话 / 文件 / 任务查看 ✕`（前两个常驻；第三个仅当面板打开时存在）。面板内容自动按所点步骤切换：

| 步骤类型 | 面板显示 |
|---|---|
| 数据查询（SQL） | 顶部 SQL 代码框（macOS 风格红黄绿圆点 + "复制代码"按钮）+ 底部数据表（分页 N/M、总条数） |
| 绘图（chart） | SQL 代码 + 完整图表 SVG |
| 表结构探索（schema） | schema 信息 / 字段列表 |
| 加载文档 | 文档片段 |

**关键操作按钮（右上角）**：

| 状态 | 图标 class | 作用 |
|---|---|---|
| 半屏 | `.anticon-expand` | 最大化（变全屏，遮住对话区） |
| 最大化 | `.anticon-compress` | 还原回半屏 |
| 任意 | `.anticon-close` | 关闭面板，回到对话视图 |
| 顶部 tab 上 | `.anticon-close`（小） | 同上，关闭"任务查看" tab |

**最大化态特别适合录屏 / 截图**——SQL 字号变大、数据表全列展开、图表满幅，比半屏看清晰多了。**用户用了红框框这个能力就是想强调它的演示价值**——后续做 InfiniSynapse demo / 写教程时只要涉及"展示 AI 写了什么 SQL / 跑出了什么数据 / 画了什么图"，**默认就走"点 .compact-tool-row → 最大化 → 截图"的路径**，比通过下拉/滚动看对话内嵌内容清晰好几个量级。

#### 5.2.3 标准操作脚本（推荐 textContent 匹配，别用索引）

```bash
# 1) 滚到对话顶部加载完整工具行（虚拟列表会卸载视口外的行 → 见 §5.2.4 陷阱）
$AGENT eval "document.querySelectorAll('.overflow-auto')[1].scrollTop = 0"
$AGENT wait 800

# 2) 用 textContent 包含关键词匹配目标行 → click
$AGENT eval "(() => {
  const row = [...document.querySelectorAll('.compact-tool-row')]
    .find(r => r.textContent.includes('用数值排序键正确排序'));
  if (!row) return 'not-found';
  row.scrollIntoView({block:'center'});
  row.click();
  return 'clicked';
})()"
$AGENT wait 1500

# 3) (可选) 点最大化, 录屏视觉冲击力 +5
$AGENT eval "(() => {
  const btn = [...document.querySelectorAll('button')]
    .find(b => b.querySelector('.anticon-expand') && b.offsetParent);
  if (btn) { btn.click(); return 'maximized'; }
  return 'no-expand-btn';
})()"
$AGENT wait 1200
$AGENT screenshot ./05-detail-maximized.png

# 4) 切换查看其它步骤: 直接点新的 .compact-tool-row, 不用先关闭面板
$AGENT eval "(() => {
  const row = [...document.querySelectorAll('.compact-tool-row')]
    .find(r => r.textContent.includes('绘制2024年1月至今'));
  row?.click(); return row ? 'switched' : 'no-row';
})()"
$AGENT wait 1500
$AGENT screenshot ./06-chart-detail.png

# 5) 还原 + 关闭
$AGENT eval "(() => {
  const restore = [...document.querySelectorAll('button')]
    .find(b => b.querySelector('.anticon-compress') && b.offsetParent);
  restore?.click(); return restore ? 'restored' : 'no-restore-btn';
})()"
$AGENT wait 800
$AGENT eval "(() => {
  const close = [...document.querySelectorAll('button')]
    .filter(b => b.offsetParent && b.querySelector('.anticon-close'))
    .find(b => { const r = b.getBoundingClientRect(); return r.y < 120 && r.x > 1300; });
  close?.click(); return close ? 'closed' : 'no-close';
})()"
```

#### 5.2.4 虚拟列表陷阱：`.compact-tool-row` 索引会漂移 ⚠️

`document.querySelectorAll('.compact-tool-row')` 拿到的**只是当前 DOM 里挂载的那些行**——视口外的会被卸载。**所以按下标取（如 `rows[5]`）极易拿到错的行**：

实测踩坑：在底部点完 rows[9] 后立刻 `rows[0].scrollIntoView()` + click，预期是滚到顶并点第一个步骤"探索失业率数据集的表结构"，**实际却点到了"查询2024年1月至今的16-24岁失业率趋势数据"**——因为页面滚到底部时，前面几个工具行被虚拟列表卸载了，当时的 `rows[0]` 实际是 DOM 残存中的第 4 个语义步骤。

**两种修法**：

```js
// 修法 A: 永远先滚到顶 + 等 mount + 再 query
container.scrollTop = 0;
await new Promise(r => setTimeout(r, 800));
const rows = [...document.querySelectorAll('.compact-tool-row')];
// 此时 rows.length 才等于实际步骤数, 索引才稳定

// 修法 B (推荐, 完全不依赖索引): textContent 包含关键词
const row = [...document.querySelectorAll('.compact-tool-row')]
  .find(r => r.textContent.includes('<步骤名关键词>'));
```

**写教程 / 录屏脚本时一律用修法 B**——不会因为虚拟列表 unmount 就跑错。

#### 5.2.5 切换不需要先关闭

打开"任务查看"面板后，**点其它 `.compact-tool-row` 会原地切换面板内容**，不会另外开新窗口、也不需要先关。这对录屏极友好——一句话字幕配一个步骤的明细切换，节奏可控。

#### 5.2.6 对话区被遮住时的回滚

最大化态会把对话区完全遮住——如果脚本过程中需要回查上下文，记得先 `.anticon-compress` 还原再 `.overflow-auto[1].scrollTop` 滚动。最大化态下 `scrollTop` 改的还是被遮的对话容器，但截屏看不到。

### 5.3 "文件" tab：产物（SVG / zip）的下载机制 ⭐⭐ daemon 不直接落盘的隐藏坑

打开右侧面板后，顶部 tab 不只有"任务查看"——还有 **当前会话 / 文件 / 任务查看**（"文件"是 InfiniSynapse 帮 AI 生成的所有可下载产物列表，比如绘制好的 SVG 图、导出的 CSV 等）。

#### 5.3.1 切换到"文件" tab

三个 tab 都是**普通 div 不是 antd Tabs**，class 为 `cursor-pointer select-none`：

```js
const tab = [...document.querySelectorAll('div.cursor-pointer.select-none')]
  .find(d => {
    const direct = [...d.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
    return direct === '文件';   // 或 '当前会话' / '任务查看'
  });
tab?.click();
```

⚠️ **不要用 `.find(d => d.textContent === '文件')`** —— 该 div 的 textContent 会包含子节点（活动 tab 还会拼上 ✕ 图标），必须用 **direct text node** 精准匹配。

#### 5.3.2 文件列表行的结构

```
.flex.items-center.justify-between.group       ← row 容器, cursor:pointer
├── span.text-sm.truncate                      ← 文件名 (含扩展名 .svg .csv ...)
└── div.relative.flex.items-center
    ├── span.text-gray-400.text-xs (group-hover:opacity-0)   ← 文件大小, 默认显示
    └── button.ant-btn.ant-btn-text.ant-btn-sm
        .absolute!.right-0.opacity-0.group-hover:opacity-100  ⭐ 下载按钮
        └── .anticon-cloud-download                          ← 云朵下载图标
```

**关键**：
- 行的 `.group` class 配合按钮的 `group-hover:opacity-100` —— **默认 opacity:0 隐身，hover 整行才显出来**（CSS `:hover`，dispatchEvent 模拟无效，必须真实鼠标 / 选中行）
- "文件大小"和"下载按钮"是**同一位置互斥显示**：默认显示大小，hover 显示下载图标
- **点击文件行（选中状态）→ 下载按钮也会保持显示**（不是只有 hover 才显），便于自动化稳定 click

#### 5.3.3 两种下载入口

| 入口 | 位置 | 类型 | 产物 |
|---|---|---|---|
| **批量下载** | 搜索框右侧的 `.anticon-cloud-download`（**常驻可见**，不在 row 里、无 `group-hover` 限制） | 单击 | **zip 包**（type `application/zip`），含全部文件 |
| **单文件下载** | 每个文件行末尾的 `.anticon-cloud-download` button（hover/选中才显） | 单击 | **原文件**（如 `application/svg+xml` 或空 type 的 SVG bytes） |

#### 5.3.4 daemon 模式的下载落盘陷阱 ⭐⭐⭐ 核心坑

实测点 button 后 **`document.body.innerText`、UI、Chromium 都没任何反应**，`~/Downloads` 也不会多新文件。原因如下：

1. button click → 触发 React handler → 用 `URL.createObjectURL(blob)` 构造下载
2. 内部用某种方式（`<a download>` 或 `window.open`）触发 Chromium 下载
3. **agent-browser daemon 启动 Playwright 时没装 `page.on('download')` listener**，downloaded blob 落到 Chromium 默认临时位置（不可访问）然后被丢弃
4. 网络层也没有 `.svg` GET 请求（因为 blob 是前端构造，不走 HTTP）

**反例**（不会下载到 `~/Downloads`）：

```bash
$AGENT click "<download-button-selector>"
sleep 3
ls -lt ~/Downloads | head -3   # ❌ 没有新文件
```

#### 5.3.5 Workaround：在 `URL.createObjectURL` 拦截 blob 转 base64 ⭐ 实战可行

既然 blob 已经在前端构造完成（验证：13052 字节 = 实际 SVG 大小），**改写 `URL.createObjectURL`，把 blob → base64 暴露到 window，再从 shell 解码写盘**——等价于"完成下载"。

```bash
# 1) 安装 patch
$AGENT eval "(() => {
  if (window.__origCreateObjectURL) URL.createObjectURL = window.__origCreateObjectURL;
  window.__origCreateObjectURL = URL.createObjectURL;
  window.__capturedBlobs = [];
  URL.createObjectURL = function(blob) {
    const u = window.__origCreateObjectURL.call(URL, blob);
    const reader = new FileReader();
    reader.onloadend = () => {
      window.__capturedBlobs.push({
        url: u, size: blob.size, type: blob.type,
        b64: reader.result.split(',')[1],
      });
    };
    reader.readAsDataURL(blob);
    return u;
  };
  return 'patched';
})()"

# 2) 选中目标文件行 (让按钮 opacity:1)
$AGENT eval "(() => {
  const span = [...document.querySelectorAll('span.text-sm.truncate')]
    .find(s => s.textContent.trim().startsWith('<文件名前缀>'));
  let row = span;
  while (row && getComputedStyle(row).cursor !== 'pointer') row = row.parentElement;
  row?.click(); return 'selected';
})()"
$AGENT wait 1000

# 3) click 该行的下载按钮 (用 textContent 精确定位 row, 再取 row 内 button)
$AGENT eval "(() => {
  const span = [...document.querySelectorAll('span.text-sm.truncate')]
    .find(s => s.textContent.trim().startsWith('<文件名前缀>'));
  let row = span;
  for (let i = 0; i < 6 && row; i++) {
    if (row.querySelector('.anticon-cloud-download')) break;
    row = row.parentElement;
  }
  row.querySelector('button.ant-btn').click();
  return 'clicked';
})()"
$AGENT wait 2000

# 4) 验证 blob 已被捕获
$AGENT eval "JSON.stringify({n: window.__capturedBlobs.length, sizes: window.__capturedBlobs.map(b=>b.size)})"

# 5) 取 base64 → 解码 → 落盘
B64=$($AGENT eval "window.__capturedBlobs[0].b64" 2>&1 | tail -1 | sed 's/^\"//; s/\"\$//')
echo "\$B64" | base64 -d > ./output/<文件名>.svg

# 6) (可选) 拆掉 patch
$AGENT eval "(() => { URL.createObjectURL = window.__origCreateObjectURL; delete window.__origCreateObjectURL; delete window.__capturedBlobs; return 'unpatched'; })()"
```

**批量下载**（zip）流程一样，只是第 3 步换成点搜索框旁的常驻按钮：

```js
const topBtn = [...document.querySelectorAll('button')].find(b =>
  b.querySelector('.anticon-cloud-download') &&
  !(b.className||'').toString().includes('group-hover')   // 排除文件行内的
);
topBtn.click();
```

#### 5.3.6 实战记录（2026-05-05）

在 `app.infinisynapse.cn` task `16233de7-...` 上验证：

| 操作 | blob.size | blob.type | 验证 |
|---|---|---|---|
| 单文件下载（"绘制2024年1月至今...折线图.svg"） | 13052 | (空) | `file <out>.svg` 显示 *SVG Scalable Vector Graphics image* ✅ |
| 批量下载（搜索框旁按钮） | 4624 | `application/zip` | `unzip -l` 列出 2 个 SVG，总计 28342 字节 ✅ |

**结论**：下载按钮的前端逻辑完全可用，daemon 限制可以靠 monkeypatch workaround 100% 绕过。写教程 / 演示时如果只是"展示有下载按钮"，截图即可（截图 hover 状态见 §5.3.7）；要真正拿到文件做后续处理（比如把 SVG 转 PNG / 嵌进文章），走 5.3.5 的 workaround。

#### 5.3.7 截图小技巧：让"hover 才出现"的下载按钮显形

CSS `:hover` 不能 dispatchEvent 模拟，但**点击该文件行（让它选中）会让下载按钮的 opacity 变成 1**——这是录屏 / 截教程时让按钮显形的最稳办法：

```bash
$AGENT eval "(() => {
  const span = [...document.querySelectorAll('span.text-sm.truncate')]
    .find(s => s.textContent.trim().startsWith('<文件名前缀>'));
  let row = span;
  while (row && getComputedStyle(row).cursor !== 'pointer') row = row.parentElement;
  row?.click();
})()"
$AGENT wait 800
$AGENT screenshot ./show-download-button.png
```

或者用 `agent-browser hover "[selector]"` —— Playwright 的真实鼠标 move 会触发 :hover 伪类（截图前不要再发其它命令把鼠标移走）。

---

## 6. 记忆库（Save to memory）⭐ 本 skill 最核心一节

### 6.1 写入：把已完成的会话存进记忆库

**前提**：任务必须**已跑完**（左侧任务行有绿色 ✓ 状态图标），未完成的任务存进去内容不完整。

```bash
# 1) 确保现在停在那条任务的详情页（任务在侧边栏会被高亮 .task-item.active）
~/.auto-coder/.autocodertools/agent-browser click ".task-item.active .task-more-btn"
~/.auto-coder/.autocodertools/agent-browser wait 1000

# 2) 弹出下拉菜单后点 "Save to memory"
~/.auto-coder/.autocodertools/agent-browser click --text "Save to memory"
~/.auto-coder/.autocodertools/agent-browser wait 2000

# 3) 验证：顶部应出现 ✓ "Save successful!" toast
~/.auto-coder/.autocodertools/agent-browser screenshot ./NN-saved.png
```

### 6.2 记忆库 ≠ 聊天记录

存的不是对话原文，而是 Agent **从对话中蒸馏出的结构化"上下文卡片"**：

- **Date Range** —— 用了什么时间范围
- **Tables & Columns** —— 主表 / 关键字段
- **Metrics** —— 指标的具体口径
- **Chart Structure** —— 图表类型 / 轴 / 标题样式

下次新会话只 RAG 回这些**事实条目**，不是聊天上下文。

### 6.3 召回：在新会话里调用记忆 ⭐

记忆库**不会自动注入**新会话。只有当 prompt 里出现"找历史"的语义信号时，Agent 才会规划一个 **Phase 1 = "RAG Research"** 阶段去捞。

| 提示词写法 | 触发记忆库召回 |
|---|---|
| `"Recall the X analysis I ran earlier"` | ✅ 高概率（最稳） |
| `"Continue from yesterday's task about X"` | ✅ 高概率 |
| `"Refresh the X numbers with today's data"` | ✅ 中等 |
| `"接着昨天那份 X 分析"` / `"上次那个图刷新一下"` | ✅ 中等（中文也吃） |
| `"Show me X"` | ❌ 当全新问题处理 |
| `"What's X today?"` | ❌ 当全新问题处理 |

**判定召回成功的硬信号**：第一个阶段的 type 标签是 **"RAG Research"**，且阶段名形如 *"Recover prior analysis context..."* / *"Query memory for the earlier..."*。

进一步验证可以读 Phase 1 展开后的内容——如果出现：

```
Based on the provided documents, here is the earlier analysis...
1. Date Range: ...
2. Tables & Columns: Primary Table = `xxx`, Key Column = `created_at`
3. Metrics: ...
4. Chart Structure: ...
```

这就是结构化上下文卡片被还原回来了。

### 6.4 召回后 Agent 仍会"快速核对"

记忆库被设计成**强先验、不当圣经**。即使从记忆里恢复了表名和字段，Phase 2 通常仍是 *"Inspect relevant ... tables and identify source fields"*——它会再 `SHOW CREATE` 一次确认 schema 没变。

**这是好事不是冗余**：表 / 字段被改名 / 删除时，召回的旧上下文会被这步发现并校正。

### 6.5 记忆库在 UI 上没有显式列表 ⚠️

打开 `/rag/private`（My Data → Knowledge Base）和 `/rag/my`（Subscribed Knowledge Base）**都看不到**通过 "Save to memory" 存的条目——它们是用户**账号级的隐性记忆**，不在 RAG 列表 UI 上展示。

**怎么知道存了多少**：只能从行为反推——新会话用召回 prompt 试一下，看 Phase 1 的 RAG Research 是否找回内容。

---

## 7. 任务轮询 + 滚动陷阱

### 7.1 轮询模板（典型分析任务 60~180 秒，但**别假设上限**）

```bash
for i in 1 2 3 4 5; do
  sleep 30
  STATE=$(~/.auto-coder/.autocodertools/agent-browser eval "(() => {
    const txt = document.body.innerText;
    const completed = txt.includes('Task completed') || txt.includes('任务完成');
    const m = txt.match(/(\\d+)\\/(\\d+)\\nType a message/);
    return JSON.stringify({ completed, phase: m ? m[1]+'/'+m[2] : null });
  })()")
  echo "[$i] $STATE"
  # ⚠️ 不要直接 grep, 用 Python 解析 — 见 §7.1.1
  echo "$STATE" | grep -q '"completed":true' && break
done
```

判定完成的硬信号：**正文包含 `"Task completed"`** 或 **`"任务完成"`** （带 ✓ 绿勾）；保险起见再叠加"已经看到 `5/5` 这种 phase 进度"。

#### 7.1.0 综合信号检测 (2026-05-05 v9 实战版) ⭐⭐⭐

最稳的"任务是否在跑"判定, 综合 3 层信号 (优先级从高到低):

```js
const txt = document.body.innerText;
// 强信号 1: 页面尾部有 "任务完成" + "推荐追问" → 已完成
const tail = txt.slice(-2000);
if (tail.includes('任务完成') && tail.includes('推荐追问')) {
  return {generating: false, sig: 'done-recommend'};
}
// 强信号 2: 进度数字 N/M (M <= 15 排除日期 YYYY/M/D)
const matches = [...txt.matchAll(/(\d+)\s*\/\s*(\d+)/g)];
const filtered = matches.filter(m => {
  const cur = parseInt(m[1]);
  const tot = parseInt(m[2]);
  return tot >= 1 && tot <= 15 && cur >= 0 && cur <= tot;
});
const last = filtered.length ? filtered[filtered.length-1] : null;
if (last) {
  return {generating: parseInt(last[1]) < parseInt(last[2]), sig: 'progress'};
}
// 弱信号 (兜底): 最近 800 字符里有 "思考中" / "Thinking" / "生成中"
const thinking = /思考中|Thinking|生成中/.test(txt.slice(-800));
return {generating: thinking, sig: thinking ? 'thinking' : 'idle'};
```

**为什么这三层?**

| 层 | 何时有效 | 何时失效 |
|---|---|---|
| done-recommend (任务完成+推荐追问) | 跑完后稳定显示 | 任务还没跑 / 出错 |
| progress N/M | phase 跑动期间 | thinking 阶段没出 phase / 残留上轮的 N/N |
| thinking text | progress 还没出来时 | 历史 reasoning 残留误触发 (用 last 800 字符局限) |

**踩过的坑**:
- 日期 `2026/5/5` 被 N/M regex 误识别 → 限制 M<=15
- 历史 reasoning 残留"Thinking..." → 限制 last 800 字符
- 上轮跑完的 progress N==N 残留 → 用 done-recommend 强信号优先

#### 7.1.1 grep 解析 STATE 几乎必坑 — 用 Python ⚠️

`agent-browser eval` 返回的是 JSON 字符串字面值, shell 里 `STATE` 实际包含转义引号:

```
"{\"completed\":true,\"phase\":\"3/3\"}"
```

`grep '"completed":true'` 找的是 `"completed":true` 这 17 个字符, 但实际字符串里是 `\"completed\":true` (19 个字符), **不匹配**. 循环不会 break, 一直跑到 for 上限.

**正解**:

```bash
COMPLETED=$(python3 -c "
import json
try:
    s = json.loads('''$STATE''')         # 第一层: 解 quote
    obj = json.loads(s) if isinstance(s, str) else s   # 第二层: 解内层 JSON
    print('true' if obj.get('completed') else 'false')
except Exception:
    print('false')
")
[[ "$COMPLETED" == "true" ]] && break
```

#### 7.1.2 任务时长高度不可控, 别用"固定 N 分钟超时" ⚠️

实测同一个 prompt:
- 第一次跑: 3 分 30 秒完成
- 第二次跑: 6 分 +都没完成

原因: AI 模型负载 / 数据库响应时间 / Agent 自己的"探查路径"分支 (有时它走捷径, 有时它绕远路从多个数据源验证). **没有可靠的"任务最长不超过 X 分钟"上限**.

实战建议:
1. **轮询超时给 5-10 分钟**, 别 30 秒就放弃
2. **不要假设阶段时长**, 比如不要"sleep 90s 后切下一句字幕" — 因为 AI 可能此时还在 phase 1
3. **录屏 / 字幕场景**: 字幕用"内容检测触发", 见 §7.1.3

#### 7.1.3 录屏/字幕场景: 基于"页面内容信号"切换字幕 ⭐ (从录屏教训沉淀)

**反例 (录屏字幕错位的根本原因)**:

```bash
# ❌ 假设 AI 用 90s 完成 phase 1
$SUBCAP note "AI 在探查字段"
sleep 90
$SUBCAP note "AI 在写 SQL"
sleep 90
$SUBCAP note "AI 在画图"
# 实际: AI phase 1 跑了 4 分钟才结束, 字幕全错位
```

**正例**: 检测特征性 DOM/文字才切下一句

```bash
$SUBCAP note "AI 阶段一: 探查数据集"

# 等"出现 SQL 代码块"信号 → 说明进入 phase 2
for i in $(seq 1 60); do
  sleep 5
  HAS_SQL=$($AGENT eval "(() => JSON.stringify({
    found: !!document.querySelector('pre code') || /SELECT[\\s\\S]+FROM/i.test(document.body.innerText)
  }))()")
  python3 -c "
import json
try:
    o = json.loads(json.loads('''$HAS_SQL'''))
    exit(0 if o['found'] else 1)
except: exit(1)
" && break
done
$SUBCAP note "AI 阶段二: 写 SQL 算分组"

# 等"图表 SVG 出现"信号 → 说明进入 phase 3
for i in $(seq 1 60); do
  sleep 5
  HAS_CHART=$($AGENT eval "(() => JSON.stringify({
    found: !!document.querySelector('svg.chart, svg[class*=chart], img[src*=chart]') ||
           document.body.innerText.includes('柱状图') && document.body.innerText.includes('生成')
  }))()")
  python3 -c "
import json
try:
    o = json.loads(json.loads('''$HAS_CHART'''))
    exit(0 if o['found'] else 1)
except: exit(1)
" && break
done
$SUBCAP note "AI 阶段三: 画柱状图"

# 等"任务完成"
for i in $(seq 1 60); do
  sleep 5
  DONE=$($AGENT eval "(() => JSON.stringify({d: document.body.innerText.includes('任务完成')}))()")
  python3 -c "
import json
try:
    o = json.loads(json.loads('''$DONE'''))
    exit(0 if o['d'] else 1)
except: exit(1)
" && break
done
$SUBCAP note "✓ 任务完成, 看最终报告"
```

**信号词 / DOM 速查表** (基于 InfiniSynapse 实际页面):

| 阶段标志 | 检测信号 (按强度排序) |
|---|---|
| 进入 Phase 2 (写 SQL) | `pre code` 元素出现; 或文本含 `SELECT...FROM` |
| 进入 Phase 3 (画图) | `svg[class*=chart]` 出现; 或文本含 "生成柱状图" / "Generating chart" |
| 任务完成 | 文本含 `"任务完成"` / `"Task completed"`; 底部出现 ✓ 绿勾 |
| 出现表格输出 | `table.markdown-table` 或 `pre + table` |

每个信号都加 5 分钟超时 + 超时也要 note 一句 fallback (避免字幕断流).

### 7.2 双 `.overflow-auto` 容器 ⭐ 滚动 / 截图必踩坑

页面上有**两个** `.overflow-auto` 元素：

| 索引 | class | 作用 | scrollHeight |
|---|---|---|---|
| `[0]` | `ant-layout-content flex-1 min-h-0 overflow-auto` | 整个右半页布局容器 | 通常 `=clientHeight`，**没有真正的滚动空间** |
| `[1]` | `overflow-auto` | **对话消息列表** | 实际有滚动空间，比如 sh=2231 / ch=648 |

**所以 `window.scrollTo(0,0)` 和滚 `[0]` 都没用**——对话区根本没动。必须滚 **`[1]`**：

```bash
# 滚到对话顶部（看 Phase 1 RAG Research 的输出）
~/.auto-coder/.autocodertools/agent-browser eval "document.querySelectorAll('.overflow-auto')[1].scrollTop = 0"
~/.auto-coder/.autocodertools/agent-browser wait 600
~/.auto-coder/.autocodertools/agent-browser screenshot ./NN-top.png

# 滚到中间（看 SQL / 表格）
~/.auto-coder/.autocodertools/agent-browser eval "document.querySelectorAll('.overflow-auto')[1].scrollTop = 1300"

# 滚到底部（看最终结论）
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const c = document.querySelectorAll('.overflow-auto')[1];
  c.scrollTop = c.scrollHeight;
  return c.scrollTop;
})()"
```

**为什么不能用 `screenshot --full`**：`--full` 截的是浏览器视口的可滚动区域（即 page-level），而对话内容是**内嵌在 fixed-height 容器里的**，全页截图也只能拿到当前可见的那一段。

### 7.3 sticky 头：用户问题永远在顶

页面顶部那条用户原问题（圆角灰底）是 sticky 元素，**滚动时不会被覆盖**——所以截图永远能看到"你问的是啥"。这是好事，命名截图时不用为它单独留位。

---

## 8. 数据源 / RAG 列表的细节

### 8.1 Data Source 列（`/database/private`）

字段：`Database Name | Database Description | Associated RAG | Database Type | Is Enabled | Database Source | Creation T... | Operation`

- **`Is Enabled` 开关**：直接 click toggle，前端改完会立刻发 PATCH，刷新仍生效。
- **`Edit / Bind RAG / Delete`**：行尾 Operation 列。

### 8.2 Knowledge Base 列（`/rag/private`）

字段：`RAG Name | Description | Associated Database | Source | Is Enabled | Creation Time | Operation`

**新增 RAG**：右上 `+ New RAG` 或 `+ Add Public RAG`（用市场里的公共库）。

### 8.3 订阅生命周期：三层状态 + 取消订阅的隐藏入口 ⭐

数据市场卡片上能看到的"订阅 / 取消"按钮其实只表示**两层状态**之间切换，**第三层"彻底取消订阅"的入口在另一个页面**。容易混淆。

**三层状态**：

| 状态 | 卡片上看到的按钮 | 含义 |
|---|---|---|
| **未订阅** | `+ 订阅` + `查看` | 完全没建立关联 |
| **已订阅 + 启用** | `已启用` 标签 + `取消` + `查看` | 订阅了且 AI 会话可以引用 |
| **已订阅 + 未启用** | `启用` + `查看`（无"已启用"标签） | 订阅记录还在，但当前 disable，AI 不能用 |

**陷阱**：卡片上的 **`取消` 按钮 = 取消"启用"**（变成第三层），**不是取消订阅**。点完之后：

- 订阅记录依然在 `/database/my` 列表里
- 卡片不会回到"+ 订阅"状态，而是变成 `启用 + 查看`
- 你以为已经清干净了，其实没有

**真正取消订阅**：去 `/database/my`（`我的订阅 → 订阅数据`）页面，行尾红色 **`取消订阅`** 按钮：

```bash
$AGENT open "https://app.infinisynapse.cn/database/my"
sleep 2

# 找目标行 + 点取消订阅
$AGENT eval "(() => {
  const rows = [...document.querySelectorAll('tr')];
  const target = rows.find(r => r.textContent.includes('subscribe_unemployment') || r.textContent.includes('中国分年龄'));
  if (!target) return 'no-row';
  const btn = [...target.querySelectorAll('button, a, span')].find(b =>
    b.textContent.replace(/\s/g,'').includes('取消订阅'));
  if (btn) { btn.click(); return 'clicked'; }
  return 'no-btn';
})()"
sleep 2

# 弹的是 Popconfirm (不是 Modal!) — 见 §3.4
$AGENT eval "(() => {
  const popovers = [...document.querySelectorAll('.ant-popover, .ant-popconfirm')]
    .filter(p => p.offsetParent && p.getBoundingClientRect().height > 30);
  for (const p of popovers) {
    const btn = [...p.querySelectorAll('button')].find(b =>
      b.textContent.replace(/\s/g,'') === '确定');
    if (btn) { btn.click(); return 'confirm-clicked'; }
  }
  return 'no-confirm';
})()"
```

**完整订阅生命周期 + 选择器口径**：

```
未订阅
  ↓ 卡片上点 [订阅] (textContent==='订阅', 自定义按钮无空格)
  ↓ Modal.confirm 弹"确认订阅" → 点 [确 认] (textContent==='确 认' 带空格 → 用 JS replace(/\s/g,''))
已订阅 + 已启用 (卡片显示"已启用" + [取消] + [查看])
  ↓ 卡片上点 [取消]
  ↓ (无弹窗, 直接生效)
已订阅 + 未启用 (卡片显示 [启用] + [查看], "已启用"标签消失)
  ↓ 必须去 /database/my, 行尾点 [取消订阅] (无空格)
  ↓ Popconfirm 弹"确定要取消订阅..." → 点 [确 定] (textContent==='确 定' 带空格)
未订阅 (回到起点, 卡片重新显示 [+ 订阅] + [查看])
```

**录"完整订阅 demo"前的 hygiene 检查脚本**：

```bash
# 确认目标数据集是 "未订阅" 状态, 否则录不到 "+订阅" 那段
$AGENT eval "(() => {
  const card = [...document.querySelectorAll('div')].find(d =>
    (d.className||'').includes('rounded-2xl') && d.textContent.includes('<目标关键词>'));
  return JSON.stringify({
    has_subscribe_btn: card && card.textContent.includes('订阅') && !card.textContent.includes('已启用') && !card.textContent.includes('启用查看'),
    text: card ? card.textContent.slice(0, 80) : 'no-card'
  });
})()"
# has_subscribe_btn:true → 可以录
# 否则 → 先去 /database/my 取消订阅, 再回来录
```

---

## 9. 常用 prompt 模板

### 9.1 第一次跑分析（深做）

```
Using <database_name> database, give me <metric> for <period>, broken down by <dim>.
If a chart helps, draw one.
```

故意写正式，让 Agent 把 schema discovery / 计算 / 出图都做完——这一份就是值得 **Save to memory** 的。

### 9.2 召回旧分析（轻做）

```
Recall the <topic> analysis I ran earlier — refresh the numbers with today's data,
draw the same kind of <chart_type> chart, and give me a one-sentence trend summary.
```

关键词：**recall + earlier + refresh + same kind of**。

### 9.3 接力新指标（混合）

```
Continue from the <topic> analysis I saved before — use the same source table and metric
definition, but switch the metric to <new_metric>.
```

---

## 10. 截图编号约定（写教程时用）

| 编号 | 内容 |
|---|---|
| `01-landing.png` | 进 `/tasks` 的首屏（"What can I do for you?"） |
| `02-data-sources.png` | `/database/private` 数据源列表 |
| `03-question-typed.png` | 第一次问题打进输入框 |
| `04-task-thinking.png` | 进入"Thinking..." + 第一阶段进行中 |
| `05-task-all-phases.png` | 滚到对话顶部，看到 5 个 phase 全列 |
| `06-task-result.png` | 最终图表 + Task completed |
| `07-save-to-memory-menu.png` | 三点菜单展开（Save to memory / Move to Project / Delete） |
| `08-saved-toast.png` | "Save successful!" toast |
| `09-recall-question.png` | 新会话里输入 "Recall ..." |
| `10-rag-research.png` | Phase 1 = RAG Research，结构化上下文回填 |
| `11-final-chart.png` | 第二次任务的同款图 |
| `12-summary.png` | 数字 + 一句话总结 |

文章存放：`产品/InfiniSynapse/文章/<topic>/article.md` + `images/`。范例：`产品/InfiniSynapse/文章/infinisynapse-memory-take-a-break/article.md`。

---

## 反模式（见到就阻止自己）

1. ❌ **在 SPA 上用 `WebFetch` / `curl`** —— `app.infinisynapse.com` 是 React SPA，HTML 里没有内容。**走 agent-browser**。
2. ❌ **`click --text "Send"` 或 `find role button --name "Send"`** —— 发送按钮 label 是空字符串。**用 snapshot 给的 ref 或 §4.1.2 的 JS 选择器**。
3. ❌ **`click --text "Data Source"`（不加 `--exact`）** —— 会撞两个元素（侧边栏 + Data Marketplace 段落文案）。
4. ❌ **`window.scrollTo(0, 0)` / 滚 `.overflow-auto[0]`** —— 对话区在 `[1]`，前两种都不动。必须 `document.querySelectorAll('.overflow-auto')[1].scrollTop = X`。
5. ❌ **`screenshot --full` 期望抓到完整对话** —— 内嵌容器外的全页截图拿不到滚动内容。**滚 `[1]` 之后多张截图拼**。
6. ❌ **任务还在跑就 Save to memory** —— 存进去的是不完整快照。等 `"Task completed"` 出现再存。
7. ❌ **新会话直接说 `"今天注册多少人"` 期望它复用昨天的 schema** —— 不会触发记忆库。必须用 `Recall / Continue / Refresh` 类引子。
8. ❌ **以为 `/rag/private` 列表里能看到记忆库内容** —— Save to memory 存的是账号级隐性记忆，UI 上没有显式列表。只能从召回行为反推。
9. ❌ **跨 snapshot 复用 `@eN` ref** —— 提交问题前后 DOM 重排，e1 已经不是同一个 textbox。**当场 snapshot 当场用**。
10. ❌ **轮询 30 秒就判任务失败** —— 数据分析任务 60~180s 是常态。坚持轮到 `Task completed` 或 5 分钟超时为止。
11. ❌ **`click --text "确认" --exact` 点 antd 弹窗按钮** —— antd 中文按钮 textContent 是 `确 认`（带空格）。`--text` / `--exact` 一律不灵。**必须 JS + `replace(/\s/g,'')`**，见 §3.3。
12. ❌ **以为 antd 弹窗按钮能在 snapshot 里看到** —— `agent-browser snapshot` 不输出 modal 内的按钮。pretest 时永远跑一次 JS query 验证选择器，**别等 click 超时才发现**。
13. ❌ **混用 `.ant-modal` 和 `.ant-popover` 选择器** —— `Modal.confirm` 用前者，行内 `Popconfirm` 用后者。文案也有差（`确 认` vs `确 定`）。**两个 class 都加，文案候选都列**，见 §3.4。
14. ❌ **以为卡片上点"取消"就是取消订阅** —— 那是"取消启用"。真正取消订阅在 `/database/my`，见 §8.3。
15. ❌ **录屏前不验证目标数据集是"未订阅"状态** —— 录到一半发现卡片是"已启用"，订阅流程演示不出来。**录前必跑 §8.3 的 hygiene 检查**。
16. ❌ **演示"AI 跑了什么 SQL / 拿到了什么数据"靠对话区滚动+截图** —— 内嵌 SQL/表格在对话流里挤成小条，观众看不清。**走 §5.2 的 `.compact-tool-row` 点开 → 最大化 → 截图**，效果好一个数量级。这是用户专门强调过的能力。
17. ❌ **按下标取 `.compact-tool-row` (如 rows[5])** —— 虚拟列表会卸载视口外的行，索引会漂移。**永远用 textContent 包含关键词匹配**，见 §5.2.4。
18. ❌ **每次切换查看明细都先关旧面板再开新的** —— 完全多余。**直接点新的 `.compact-tool-row` 就原地切换**面板内容，节奏更连贯。
19. ❌ **以为 `agent-browser click` "文件" tab 的下载按钮 → 文件就到 `~/Downloads`** —— daemon 没装 `page.on('download')` listener，下载触发了但落不到磁盘。**走 §5.3.5 的 monkeypatch `URL.createObjectURL` + base64 workaround**，验证过 100% 可用。
20. ❌ **想 click 文件行末尾的下载按钮但忽略 `group-hover:opacity-100`** —— 默认 opacity:0，dispatchEvent 模拟的 hover 不能激活 CSS `:hover`。**先 click 文件行让它选中** 或者 `agent-browser hover` 真实鼠标移动，按钮才可点。
21. ❌ **用 `div.textContent === '文件'` 找 tab** —— 活动 tab 的 textContent 还包含 ✕ 等子元素文字。**必须只比较 direct text node**：`[...d.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('')`。

---

## 与其他 skill / rule 的关系

- **必依赖**：
  - `~/.cursor/rules/use-agent-browser-for-web.mdc` —— 浏览器一律走 agent-browser
  - [`web-ui-review-skill`](../web-ui-review-skill/SKILL.md) —— 8 个原子动作的来源
- **强相关**：
  - [`winclaw-infinisynapse-skill`](../winclaw-infinisynapse-skill/SKILL.md) —— 反方向：把 InfiniSynapse 接进 WinClaw，不是直接驱动控制台
  - [`screen-subtitled-recording-skill`](../screen-subtitled-recording-skill/SKILL.md) —— 录 InfiniSynapse 控制台 demo 视频。**联用时务必先读本 skill 的 §3.3 §3.4 §4.1 §5.2 §5.3 §8.3**，那几节都是真实录屏踩坑沉淀下来的（§5.2 是"展示 AI 工作过程"的最佳画面来源；§5.3 是把生成的 SVG / 数据导出做后续二次加工的核心通路）
  - [`browser-subtitled-recording-skill`](../browser-subtitled-recording-skill/SKILL.md) —— 同上，区别在录浏览器内嵌画面而非整屏
  - `.cursor/rules/infinisynapse-command-tools.mdc` —— 写文章时的口径规则
- **可选配套**：
  - [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) —— 教程完成后发到公众号草稿
  - `~/.cursor/rules/use-markdown2pdf-for-pdf.mdc` —— 出 PDF
- **范例产物**：
  - 文章版：`产品/InfiniSynapse/文章/infinisynapse-memory-take-a-break/article.md` + `article-en.md` + `images/01..12.png`
  - 录屏版：`产品/InfiniSynapse/视频/infinisynapse-unemployment-tutorial/final-with-subs.mp4` + `events.jsonl` + `record_script.sh`（2026-05-04 实操，"订阅失业率数据集 → AI 跑分析 → 看结果"端到端 2 分 03 秒）

---

## 一张图总结：典型端到端流程

```
                ┌──────────────────────────────────────┐
                │ open /tasks  (登录态预检)               │
                └──────────────────┬──────────────────┘
                                   ▼
                ┌──────────────────────────────────────┐
                │ snapshot → 拿 textbox @e1 + send @eN  │
                │ fill 问题 → click @eN → 跳 ?taskId     │
                └──────────────────┬──────────────────┘
                                   ▼
                ┌──────────────────────────────────────┐
                │ 轮询 (30s × 6) 直到 'Task completed'    │
                │ 滚 .overflow-auto[1] → 截图 5 个关键帧  │
                └──────────────────┬──────────────────┘
                                   ▼
                  (演示分支: 展示 AI 跑了什么 SQL/数据/图)
                                   ▼
                ┌──────────────────────────────────────┐
                │ 点 .compact-tool-row [textContent 匹配]│
                │ 右侧弹"任务查看"面板 (SQL+表/图)        │
                │ 点 .anticon-expand 最大化 → 截图        │
                │ 切其它步骤直接再 click, 不用先关        │
                │ 完事 .anticon-compress 还原 + close    │
                └──────────────────┬──────────────────┘
                                   ▼
                ┌──────────────────────────────────────┐
                │ click .task-item.active .task-more-btn │
                │ click "Save to memory"                │
                │ 等 "Save successful!" toast            │
                └──────────────────┬──────────────────┘
                                   ▼
                  (任意时间后, 全新会话)
                                   ▼
                ┌──────────────────────────────────────┐
                │ click "New Task"                      │
                │ fill "Recall the ... — refresh ..."   │
                │ click @send                           │
                └──────────────────┬──────────────────┘
                                   ▼
                ┌──────────────────────────────────────┐
                │ 校验 Phase 1 type = "RAG Research"     │
                │ 看 Date Range / Tables / Metrics 回填   │
                │ 等任务完成 → 看新数据 + 同款图           │
                └──────────────────────────────────────┘
```

---

## 13 条口诀就够了

1. **能 `open <url>` 直跳就别点菜单** —— URL 路由表见 §2
2. **送出按钮 label 是空字符串** —— 用 snapshot 的 `@eN` 或 §4.1.2 的 JS 选择器，别用 `--text`
3. **重名元素加 `--exact`** —— `Data Source` 是常见坑
4. **三点菜单藏在 `.task-item .task-more-btn`** —— hover 才显示但 selector 直接 click 就行
5. **对话区滚动用 `.overflow-auto[1]`，不是 `[0]` 也不是 window** —— 双容器陷阱
6. **任务跑完才存记忆** —— Task completed 出现后再点 Save to memory
7. **召回 prompt 必须含 Recall / Continue / Refresh** —— 否则不进 RAG Research
8. **判定召回成功看 Phase 1 type = "RAG Research"** —— 这是记忆库被真正命中的硬证据
9. **antd 中文弹窗按钮文案带空格** —— `取 消 / 确 认 / 确 定`，必须 JS + `textContent.replace(/\s/g,'')`
10. **snapshot 看不到 modal 内按钮** —— 跑 click 之前先 JS query 一遍 `.ant-modal` / `.ant-popover` 验证选择器
11. **取消订阅 ≠ 卡片上点取消** —— 卡片"取消"=取消启用；真正取消订阅去 `/database/my` 行尾红色按钮，弹的是 Popconfirm 不是 Modal
12. **演示 AI 工作过程默认走 `.compact-tool-row` 点开 → `.anticon-expand` 最大化 → 截图** —— 比对话区内嵌看清楚一个数量级；切换不同步骤直接再 click，不用先关；选行用 textContent 匹配不要用索引（虚拟列表会漂移）。见 §5.2
13. **"文件" tab 的下载按钮，daemon 不会落盘到 `~/Downloads`** —— 必须 monkeypatch `URL.createObjectURL` 在 blob 构造时把字节转 base64 暴露到 window，再从 shell 解码写盘。批量下载得 zip，单文件得原文件。见 §5.3

---

*本 skill 的每一条坑都是真实跑出来的（2026-04-27 在 `app.infinisynapse.com` 全英文界面跑完一个完整的"Save to memory + 召回"循环验证；2026-05-04 在 `app.infinisynapse.cn` 中文界面跑完整"订阅数据集 + 提问 + 看 AI 跑完"录屏 demo，新增 §3.3 §3.4 §4.1.1-3 §8.3 这几节都是这次实战补的；2026-05-05 在 `app.infinisynapse.cn` 实测 `.compact-tool-row` 执行明细面板的完整交互闭环——10 个工具行逐个点开，验证 SQL+表/SQL+图两种内容形态、最大化/还原/关闭三个右上角按钮、textContent 匹配优于索引匹配、虚拟列表会卸载视口外行——新增 §5.2 这一节即此次实战沉淀；同日继续实测"文件" tab 的下载机制——发现 daemon 模式下 click 下载按钮会触发 React handler 构造 blob 但落盘失败（Playwright 无 `page.on('download')` listener），用 monkeypatch `URL.createObjectURL` 拦截 blob → base64 → shell 写盘的 workaround 100% 可用，单文件 13052 字节 SVG 完整还原，批量下载 4624 字节 zip 含 2 个 SVG 解压验证通过，新增 §5.3 这一节），后续遇到新坑请直接更新此文件。*
