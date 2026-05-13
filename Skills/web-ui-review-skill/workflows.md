# Workflows — 3 种典型任务的完整命令串

> 本文件是 [SKILL.md](SKILL.md) 的配套详情，所有"基础动作编号"都对应主文件 `## 8 个通用基础动作` 一节。

---

## A. UI/UX 审查工作流

**适用场景**：用户说"这个页面有没有问题"、"UI review"、"截图看看界面"。

**产物**：结构化的 UI 体验报告（用 SKILL.md § 产物收敛模板 1）。

### 7 步闭环

```bash
# 0. 准备
mkdir -p /tmp/ui-review && cd /tmp/ui-review
URL="http://127.0.0.1:3000/zh/dashboard"

# 1. 探活 + daemon
curl -s -o /dev/null -w "HTTP %{http_code}\n" -L "$URL"
~/.auto-coder/.autocodertools/agent-browser daemon status

# 2. 打开 + 等待（networkidle 超时是常态，别慌）
~/.auto-coder/.autocodertools/agent-browser open "$URL"
~/.auto-coder/.autocodertools/agent-browser wait --load networkidle
~/.auto-coder/.autocodertools/agent-browser get url
~/.auto-coder/.autocodertools/agent-browser get title

# 2a. 若被重定向到 /login —— 截登录页 + ask 用户手动登录
# ~/.auto-coder/.autocodertools/agent-browser screenshot ./00-login.png
# → ask: "页面要求登录，请在打开的浏览器窗口里手动登录，完成后告诉我继续"

# 3. 三件套
~/.auto-coder/.autocodertools/agent-browser screenshot ./01-viewport.png
~/.auto-coder/.autocodertools/agent-browser screenshot --full ./02-fullpage.png
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c > ./snapshot-main.txt

# 4. 找溢出容器
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const h=[...document.querySelectorAll('*')].filter(n=>{
    const s=getComputedStyle(n);
    return (s.overflowX==='auto'||s.overflowX==='scroll')&&n.scrollWidth>n.clientWidth+10;
  }).slice(0,5).map(n=>({tag:n.tagName,cls:(n.className||'').toString().slice(0,120),sw:n.scrollWidth,cw:n.clientWidth,diff:n.scrollWidth-n.clientWidth}));
  return JSON.stringify(h);
})()"
# 如果有 diff > 0 的容器，强滚到底再截：
~/.auto-coder/.autocodertools/agent-browser eval "(() => { const el=document.querySelector('<那个 selector>'); el.scrollLeft=el.scrollWidth; return 'ok'; })()"
~/.auto-coder/.autocodertools/agent-browser screenshot ./03-scrolled.png

# 5. 多视口对照
~/.auto-coder/.autocodertools/agent-browser set viewport 1440 900
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser screenshot --full ./04-1440.png

~/.auto-coder/.autocodertools/agent-browser set viewport 1024 768
~/.auto-coder/.autocodertools/agent-browser wait 500
~/.auto-coder/.autocodertools/agent-browser screenshot --full ./05-1024.png

# 6. 关键交互链路验证（1~3 个核心动作）
~/.auto-coder/.autocodertools/agent-browser find text "<关键按钮名>" click
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser screenshot ./06-after-click.png
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | head -40

# 7. 读图 → 写报告（SKILL.md 模板 1）
```

### 判定口径

- **1440 视口仍横向滚动** = UI 问题，不是"屏幕不够大"
- **networkidle 不到** + 骨架屏不消失 = 骨架/loading 逻辑有 bug
- **点击后 URL 和 snapshot 都没变** = 这个入口可能是坏的
- **切 1024 后关键功能看不到** = 响应式断裂

---

## B. 功能链路体验工作流

**适用场景**：用户说"在界面上走一遍 xxx 流程"、"帮我创建一个 xxx 并跑完"、"按这个步骤操作一下"。

**产物**：链路体验总结 + 一组按步骤编号的截图（用 SKILL.md § 产物收敛模板 2）。

### 真实案例：在 auto-coder.chat 看板创建并运行一个需求

**目标**：在 `http://127.0.0.1:3000/zh/dashboard` 上完成"新建需求 → 执行 → 等完成 → 查看 review 详情 → 拖到已完成 → 刷新验证"。

### 完整 10 步

```bash
# 0. 准备
mkdir -p /tmp/kanban-flow && cd /tmp/kanban-flow
URL="http://127.0.0.1:3000/zh/dashboard"

# 1. 探活 + daemon + 打开 + 等待（同工作流 A 的 1~2）
curl -s -o /dev/null -w "HTTP %{http_code}\n" -L "$URL"
~/.auto-coder/.autocodertools/agent-browser daemon status
~/.auto-coder/.autocodertools/agent-browser set viewport 1440 900
~/.auto-coder/.autocodertools/agent-browser open "$URL"
~/.auto-coder/.autocodertools/agent-browser wait 2500
~/.auto-coder/.autocodertools/agent-browser get url
~/.auto-coder/.autocodertools/agent-browser screenshot ./01-dashboard.png

# 2. 确认默认实例（是给谁干活的）
~/.auto-coder/.autocodertools/agent-browser eval "document.body.innerText.match(/默认实例[:：]?\\s*[^\\n]{0,80}/)?.[0] || ''"
# → "默认实例: jiaoyang.local · auto-coder"
# 根据这个决定要提什么需求

# 3. 打开新建表单
~/.auto-coder/.autocodertools/agent-browser find text "新建需求" click
~/.auto-coder/.autocodertools/agent-browser wait 1200
~/.auto-coder/.autocodertools/agent-browser screenshot ./02-new-issue-modal.png
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | head -80
# → 记下标题/描述/验收标准/标签/创建按钮的 @eN ref

# 4. 填表单（注意多行用真换行）
~/.auto-coder/.autocodertools/agent-browser fill @e41 "更新 README 的 Latest News 时间线"
~/.auto-coder/.autocodertools/agent-browser fill @e43 "README.md 中 Latest News 小节最新条目是 2025/01，已过时。请在列表最上方新增一行 2026/04 占位条目。只改 README.md 一个文件。"
~/.auto-coder/.autocodertools/agent-browser fill @e45 "- Latest News 列表最上方新增了 [2026/04] Update roadmap for 2026 条目
- 未修改 README.md 以外的任何文件
- README.md 整体结构保持不变"
~/.auto-coder/.autocodertools/agent-browser fill @e60 "docs, readme, demo"
~/.auto-coder/.autocodertools/agent-browser screenshot ./03-form-filled.png

# 5. 提交
~/.auto-coder/.autocodertools/agent-browser is enabled @e62        # 先确认按钮能点了
~/.auto-coder/.autocodertools/agent-browser click @e62
~/.auto-coder/.autocodertools/agent-browser wait 3000               # 等模态关闭 + 卡片出现
~/.auto-coder/.autocodertools/agent-browser screenshot ./04-card-created.png
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | head -50
# → 确认左侧"待规划"列 +1、新卡片带编号（如 #6）

# 6. 点击新卡片的执行按钮
# 从上一步 snapshot 取新卡片"执行"按钮的 ref（通常是 [nth=1] 的那一组）
~/.auto-coder/.autocodertools/agent-browser click @e31
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser screenshot ./05-running.png
# 验证：左侧"正在运行"从 0 变成 1，卡片自动从"待规划"移到"进行中"

# 7. 进入任务会话看实时输出
~/.auto-coder/.autocodertools/agent-browser snapshot -i -c | grep -i "正在运行\|执行中"
# 找到左侧栏那条任务条目的 ref
~/.auto-coder/.autocodertools/agent-browser click @e18     # 点任务名
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser get url
~/.auto-coder/.autocodertools/agent-browser screenshot ./06-task-chat.png

# 8. 轮询等任务完成
for i in 1 2 3 4 5 6; do
  ~/.auto-coder/.autocodertools/agent-browser wait 15000
  status=$(~/.auto-coder/.autocodertools/agent-browser eval "document.body.innerText.match(/(已完成|已取消|运行中|失败)/)?.[0] || ''")
  echo "Poll $i: $status"
  [[ "$status" == *"已完成"* || "$status" == *"已取消"* || "$status" == *"失败"* ]] && break
done
~/.auto-coder/.autocodertools/agent-browser screenshot ./07-task-done.png
# → 读图，拿 agent 的交付总结

# 9. 回看板看卡片去向（带验收标准的需求会去"待审查"而非直接"已完成"）
~/.auto-coder/.autocodertools/agent-browser open "$URL"
~/.auto-coder/.autocodertools/agent-browser wait 2500
~/.auto-coder/.autocodertools/agent-browser eval "(() => { const el = document.querySelector('.flex.gap-3.overflow-x-auto'); if (el) el.scrollLeft = el.scrollWidth; return 'ok'; })()"
~/.auto-coder/.autocodertools/agent-browser screenshot ./08-review-column.png

# 10a. 点卡片看验收详情
~/.auto-coder/.autocodertools/agent-browser click --text "更新 README 的 Latest News 时间线"
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser screenshot ./09-card-detail.png
~/.auto-coder/.autocodertools/agent-browser press Escape

# 10b. 拖动卡片到"已完成"—— 看板用 HTML5 DnD，必须 dispatchEvent
~/.auto-coder/.autocodertools/agent-browser eval "(() => {
  const src = [...document.querySelectorAll('[draggable=\"true\"]')].find(n => n.innerText.includes('更新 README'));
  const cols = [...document.querySelectorAll('.flex.flex-col.w-\\\\[280px\\\\]')];
  const dst = cols[cols.length - 1];   // 最后一列 = 已完成
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
~/.auto-coder/.autocodertools/agent-browser wait 1500
~/.auto-coder/.autocodertools/agent-browser eval "(() => { const el = document.querySelector('.flex.gap-3.overflow-x-auto'); if (el) el.scrollLeft = el.scrollWidth; return 'ok'; })()"
~/.auto-coder/.autocodertools/agent-browser screenshot ./10-after-drag.png

# 10c. 刷新验证后端持久化
~/.auto-coder/.autocodertools/agent-browser reload
~/.auto-coder/.autocodertools/agent-browser wait 5000      # 两次 wait 避开"加载瞬间全是 0"的中间态
~/.auto-coder/.autocodertools/agent-browser eval "(() => { const el = document.querySelector('.flex.gap-3.overflow-x-auto'); if (el) el.scrollLeft = el.scrollWidth; return 'ok'; })()"
~/.auto-coder/.autocodertools/agent-browser screenshot ./11-done-persisted.png

# 11. 文件层面验证（如果是代码类需求）
cd ~/projects/auto-coder && git diff <可能被改的文件>
# 对着验收标准逐条核对
```

### 关键经验（每一条都是踩过的坑）

1. **提交后要多等一会儿**：有些系统从"保存中"到模态关闭需要 2~3 秒，`wait 3000` 比 `wait 1000` 稳。
2. **点击后 ref 会失效**：每次大动作后重新 snapshot，别用旧 ref。
3. **模糊匹配 `find text` 的坑**：`"任务总览"` 可能误匹配到左侧栏的某条历史任务名。确切有歧义时：
   - 加 `--exact`：`click --text "任务总览" --exact`
   - 或先 snapshot 拿到准确 ref 再点
4. **拖拽先真后假**：先试 `mouse down/move/up`——如果卡片没动 = HTML5 DnD，改用 dispatchEvent（见 SKILL.md § 基础动作 8）。
5. **刷新后有加载态瞬间**：`reload` 之后会有 1~3 秒所有列显示 0 条，这是 UI 小瑕疵不是数据丢了——再 `wait 3000` 就恢复。
6. **选"小而美"示例数据**：链路体验默认**会真改数据库/代码**，优先选能 `git reset` 或 soft-delete 的对象。改 README 一行、创建一个带 `[TEST]` 前缀的卡片都是好选择。

### 选"示例需求"的清单

如果用户让你"提一个需求"，优先选：

- ✅ 只改 **1 个文件**的文档类小改（README 加一行、doc 改错别字）
- ✅ 只动 **1 个函数**的小重构（加一个边界检查）
- ✅ 创建**一个新文件**但不引入依赖
- ❌ 新加依赖、改构建配置、改数据库 schema
- ❌ 需要触发 CI 才能验证的改动

---

## C. 体验 → 写教程工作流

**适用场景**：用户说"体验完顺便写份教程"、"把这次操作整理成文档"、"教用户怎么 xxx"。

**产物**：完整教程目录（SKILL.md § 产物收敛模板 3）。

### 流程

```
1. 先跑一次工作流 B（真实完成整条链路，攒截图）
      ↓
2. 把 /tmp/<task>/ 的截图复制到教程 images/ 目录，按步骤重命名
      ↓
3. 按"模板结构"写 README.md
      ↓
4. （可选）markdown2pdf 转 PDF 分发
```

### 命令串

```bash
# 1. 选教程存放位置（已有约定：william-docs/产品/<产品>/文章/<topic>-tutorial/）
TUTORIAL_DIR=~/projects/william-docs/产品/Auto-Coder/文章/<topic>-tutorial
mkdir -p "$TUTORIAL_DIR/images"

# 2. 把截图挑重要的、按步骤命名后复制过去
cp /tmp/<task>/01-dashboard.png        "$TUTORIAL_DIR/images/01-dashboard.png"
cp /tmp/<task>/02-new-issue-modal.png  "$TUTORIAL_DIR/images/02-new-issue-modal.png"
# ... 按教程章节顺序 01 → NN

# 3. 写 README.md（用下面的"教程结构模板"）
# 4. （可选）导出 PDF
~/.auto-coder/.autocodertools/markdown2pdf convert "$TUTORIAL_DIR/README.md"
```

### 教程结构模板（中文产品类）

```markdown
# 手把手：<产品名> 做 <任务>

> 本文是一份**操作手册**：<一句话说明这篇教学覆盖什么>。全程以一个真实跑通的小例子贯穿——<具体例子>。

## 0. 前置条件

- 装了什么
- 本地 URL / 账号
- 需要的配置

## 1. 打开 XX 界面

![主界面](images/01-xxx.png)

说明这个界面的**结构**（列/区块/Tab）、哪些控件你将经常用。**加一条"小坑提醒"**让读者提前有心理准备（比如宽度、加载态）。

## 2. 点击"XX"打开表单

![表单](images/02-xxx.png)

**逐字段说明**，用表格：

| 字段 | 必填 | 建议写法 |
|---|---|---|
| 标题 | ✅ | ... |

再加一小节"**写好 XX 的 3 个技巧**"。

## 3. 填写并提交

![填好](images/03-xxx.png)

提交后的**验证点**：左栏计数变没变、按钮状态变化、模态是否关闭。

## 4~7. <后续每一步>

每一步都套这个模式：**截图 → 发生了什么 → 验证点 → 小提醒**。

## 8. 点卡片/详情看结果

![详情](images/09-xxx.png)

**重点讲"执行状态"区块怎么读**——往往这里藏着 agent 的交付总结，一眼就能判断是否达标。

## 9. 关键操作（拖动/确认/删除）

**操作细节 + 失败场景表**：

| 现象 | 原因 | 处理 |
|---|---|---|

## 10. 刷新验证持久化

强调**前端成功 ≠ 后端成功**，F5 再看一次是标准动作。

## 11. 文件/数据层面验证

```bash
git diff ...
```

对着**验收标准逐条打勾**。

## 常见问题速查

<FAQ 表格>

## 一张图总结整条流程

<ASCII 流程图>

记住 N 个口诀就够了：

1. ...

---

*撰写时所用工具：`agent-browser` CLI 全程自动化操作。截图时间：YYYY-MM-DD。*
```

### 写教程的 5 条规矩

1. **章节编号和截图编号对齐**：第 N 节对应 `images/NN-xxx.png`，读者阅读和目录跳转一致。
2. **每节三件套**：截图 → 发生了什么 → 验证点（至少有一条"可观察信号"）。
3. **把失败也写进去**：FAQ 表格、"失败怎么办" 小节比正文更有价值。
4. **用表格替代长段文字**：字段说明、状态转换、FAQ 都用表格。
5. **结尾加 ASCII 流程图 + 口诀**：帮读者把整篇文章压缩成一张图。

### 真实案例

本 skill 沉淀自以下真实任务，可作为对照：

- 教程产物：`~/projects/william-docs/产品/Auto-Coder/文章/kanban-requirement-tutorial/README.md`（339 行，11 张按步骤截图）
- 覆盖链路：新建需求 → 执行 → 运行中 → 待审查 → Review 详情 → 拖到已完成 → 刷新持久化验证

---

## 三类工作流选择速查

| 用户说法 | 选哪个 |
|---|---|
| "看看 UI 有问题吗" | A |
| "截图分析界面" | A |
| "体验一下这个页面" | A（侧重审查）或 B（侧重走流程） |
| "帮我创建一个 xxx" | B |
| "在界面上把 xxx 跑完" | B |
| "操作完给我截图证据" | B |
| "写份教程" / "教用户怎么用" | C（前置跑一遍 B） |
| "把这次操作整理成文档" | C |

混合需求（既要找问题又要写教程）：先 B 后 A 再 C，一次跑通。
