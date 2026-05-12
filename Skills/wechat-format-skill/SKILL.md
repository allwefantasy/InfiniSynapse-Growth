---
name: wechat-format-skill
description: 把任意 Markdown / 纯文本 / 粗糙笔记**排版**成微信公众号编辑器兼容的、视觉精美的 HTML。覆盖：(1) 微信编辑器兼容性硬规则（必须内联样式、ul/ol 抹样式问题、外链屏蔽、CJK 间距）；(2) AI 内容分析与结构增强（自动识别对话→气泡、连续多图→画廊、核心观点→callout、纯文本→自动加 `##` 标题/列表/加粗）；(3) **复杂排版降维**——对多列表格、对比矩阵、流程图、时间线等公众号原生排版必崩的内容，用 HTML 单独绘制再渲染成 PNG 作为配图插入（复用 `text-to-poster-skill/assets/render.sh`）；(4) 8 套精选主题（报纸/赤陶/墨韵/GitHub/中国风/暗夜/日落/极简）+ 选型决策树；(5) 与 `wechat-mp-draft-skill` 接力完成"内容→草稿"全链路。当用户说"排版这篇文章"、"公众号排版"、"格式化为公众号格式"、"把 md 转成微信格式"、"换个主题再排一版"、"这表格公众号里太丑了"、"把对比图做成图片"时使用。
---

# 微信公众号排版 Skill

把"做出公众号读者一眼就觉得专业的视觉"这件事程式化：内容分析 → 结构增强 → 主题选择 → 出 HTML → 浏览器预览 → 和 [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) 接力贴到草稿。

> 提炼自社区两个评测最高的同类 skill：
> - [`xiaohuailabs/xiaohu-wechat-format`](https://github.com/xiaohuailabs/xiaohu-wechat-format)（282★）—— 30 套主题 + AI 内容增强 + 兼容性细节，**方法论主体**
> - [`geekjourneyx/md2wechat-skill`](https://github.com/geekjourneyx/md2wechat-skill)（**1293★**）—— 整合性最强（多主题 + AI 写作 + AI 去痕 + 草稿推送），命令行思路参考

---

## 范围划分（重要）

本项目里有两个公众号相关 skill，**职责完全分开**：

| Skill | 关注层 | 主要工具 | 产物 |
|---|---|---|---|
| [`wechat-format-skill`](SKILL.md)（本 skill） | **内容侧 / 视觉** | Python + 主题模板 | 微信兼容的样式化 HTML |
| [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) | **操作侧 / 自动化** | agent-browser CLI | 公众号草稿（含 mmbiz CDN 图片） |

**典型接力**：

```
用户：「把这篇 article.md 排版成报纸风发到公众号草稿，里面那张对比表太宽，做成图」

Step 1. 本 skill 处理：
        article.md
          ├─ AI 增强（对话气泡 / 图集 / callout）
          ├─ 复杂排版降维（对比表 → HTML → PNG，放到 images/）
          ├─ newspaper 主题渲染
          └─ article.html

Step 2. wechat-mp-draft-skill 接力：
        article.html → 上传 images/*.png 到 mmbiz CDN → 粘贴到 ProseMirror → 保存草稿
```

**禁忌**：本 skill **不做**草稿提交（永远不动 `mp.weixin.qq.com`）；`wechat-mp-draft-skill` **不做**视觉排版（默认走基础 md2html，要美化必须先经过本 skill）。

---

## 决策树：进来先问自己 5 件事

```
Q1. 输入是什么？
    ├─ 标准 Markdown（有 ## 标题、加粗、列表）─▶ 跳过结构化预处理
    ├─ 纯文本 / 粗糙笔记 ────────────────────▶ 先做结构化（加 ## / 列表 / 加粗）
    └─ 已经的微信 HTML ──────────────────────▶ 进入「换主题」流程

Q2. 内容类型是什么？
    ├─ 深度长文 / 行业分析 ─▶ 推荐 newspaper / magazine / ink
    ├─ 科技产品 / AI 工具  ─▶ 推荐 github / sspai
    ├─ 访谈 / 对话体       ─▶ 推荐 terracotta / coffee-house
    ├─ 教程 / 操作指南     ─▶ 推荐 github / sspai
    ├─ 文艺 / 随笔 / 观点  ─▶ 推荐 sunset-amber / lavender-dream / terracotta
    ├─ 中国风 / 文化主题   ─▶ 推荐 chinese
    └─ 创意 / 反差         ─▶ 推荐 midnight / bauhaus

Q3. 是否要 AI 内容增强？
    ├─ 文章里有连续对话 / 访谈 ─▶ 自动套 :::dialogue 气泡
    ├─ 文章里有 3 张以上连续图 ─▶ 自动套 :::gallery 横滚
    ├─ 文章里有金句 / 核心观点 ─▶ 自动套 [!important] / [!tip] 块
    └─ 都没有 ─▶ 跳过增强

Q4. 用户给了主题偏好吗？
    ├─ 给了（比如"报纸风"）─▶ 直接用对应主题
    └─ 没给 ─▶ 推荐 3 个让用户挑（结合 Q2 的内容类型）

Q5. 文章里有公众号排版必崩的"重型视觉块"吗？
    ├─ ≤3 列的简单表                ─▶ 走主题内置 <table>（md2wechat.py 自动处理）
    ├─ 4 列以上 / 单元格含长文本的表 ─▶ 图片化（Step 2.5）
    ├─ 对比矩阵、双栏 PK、打分卡    ─▶ 图片化
    ├─ 流程图、时间线、架构图、脑图 ─▶ 图片化
    └─ 以上都没有                   ─▶ 跳过 Step 2.5
```

---

## 工具前提

```bash
pip3 install markdown beautifulsoup4 pygments    # 渲染 + DOM 修复 + 代码高亮
pip3 install Pillow                              # Step 2.5 图片化后自动裁边（和 text-to-poster-skill 共用）

# 本 skill 自带脚本
SKILL_DIR="$HOME/projects/william-docs/skills/global/wechat-format-skill"
python3 "$SKILL_DIR/bin/md2wechat.py" --help

# Step 2.5 复用的截图工具（text-to-poster-skill）
RENDER_SH="$HOME/projects/william-docs/skills/global/text-to-poster-skill/assets/render.sh"
# 依赖 macOS 自带的 Google Chrome（headless 模式）
```

**配套规则**：[`compatibility-rules.md`](compatibility-rules.md)（必读，微信编辑器兼容性硬规则）+ [`themes-gallery.md`](themes-gallery.md)（8 套主题样式片段）。

---

## 完整工作流（6 步）

### Step 1：内容评估 + 结构化预处理（仅在需要时）

读完 markdown 后，**先扫一遍格式标记的密度**：

```bash
ARTICLE="article.md"

heading_count=$(grep -c '^## ' "$ARTICLE")
list_count=$(grep -cE '^[-*0-9]+\. ' "$ARTICLE")
bold_count=$(grep -cE '\*\*[^*]+\*\*' "$ARTICLE")
total_lines=$(wc -l < "$ARTICLE")

echo "## 标题: $heading_count, 列表: $list_count, 加粗: $bold_count, 总行数: $total_lines"
```

**判断规则**：

- 有 `##` 标题 + 至少一项标记（列表/加粗/引用）→ **跳过结构化**
- 缺 `##` 标题，或几乎没格式标记（纯文本笔记）→ **执行结构化**

**结构化的底线：只加结构标记，不改措辞**。

| 操作 | 做 | 不做 |
|---|---|---|
| 加 `##` 标题 | 在主题转换处插标题，从内容里提炼 | 编造没有的标题 |
| 加列表标记 | 识别并列/枚举内容，加 `- ` 或 `1. ` | 把段落拆成无意义短句 |
| 加 `**加粗**` | 关键词、产品名、核心概念 | 整段加粗 |
| 加 `> 引用` | 别人的话、原文摘抄 | 把作者自己的话当引用 |
| 清理 | 多余空行、缩进、统一标点 | 调整语序、润色文字 |
| **不动** | 措辞、删减、增补 | — |

**保存与告知**：

- 结构化后保存为 `<原路径>-structured.md`（同目录，加 `-structured` 后缀）
- 显式告诉用户："检测到原文缺少 Markdown 结构标记，已自动补充 N 个 `##` 标题、M 处加粗，保存在 `xxx-structured.md`，可检查后再排版"
- 后续步骤基于 `-structured.md`

### Step 2：AI 内容增强（识别可视化容器）

读取（结构化后的）markdown，**在 markdown 层面**插入 4 类容器标记：

#### 2.1 对话/访谈 → `:::dialogue`

**触发条件**：检测到 `**名字：**` 或 `名字：` 交替出现（中英文冒号都算）。

```markdown
:::dialogue[嘉宾对谈]
张三: 你怎么看这件事？
李四: 我觉得...（多行也可以）
:::
```

- 同一场景的连续对话**一个块**，换场景换一个新块
- 独白、叙述段落**保持原样**（不是所有"X：xxx"都要套）
- 一篇文章里 1-2 个 `:::dialogue` 是合理的，超过就停手

#### 2.2 连续多图 → `:::gallery`

**触发条件**：3 张以上连续图片（中间没有大段文字）。

```markdown
:::gallery[产品截图]
![](images/01-home.png)
![](images/02-detail.png)
![](images/03-config.png)
:::
```

适合：产品截图集、对比图、系列图。横向滚动浏览。

#### 2.3 核心观点 → callout

**触发条件**：识别"金句""核心结论""关键提醒"。

```markdown
> [!important] 标题（可选）
> 这是核心观点。

> [!tip] 实战技巧
> 小提示。

> [!warning] 注意
> 风险提醒。

> [!callout]
> 普通强调（用主题色高亮）。
```

**节制**：一篇文章 1-3 处，超过会失效。

#### 2.4 图说 → 斜体

图片后紧跟的说明用斜体段落：

```markdown
![](images/01-dashboard.png)
*图 1: 看板首页，左侧泳道为状态分组*
```

脚本会自动把斜体段渲染成居中灰色小字。

**保存**：增强后的 markdown 存为 `<路径>-enhanced.md`。

### Step 2.5：复杂排版降维 —— HTML 绘图 → PNG → 作为配图

**为什么要这一步**：微信公众号编辑器对复杂排版的支持**极差**，硬塞下面这些内容一定翻车：

- 多列表格（4 列以上必然溢出版心，移动端窄屏更是糊成一团）
- 对比矩阵 / 双栏 PK / 评分卡（`<table>` 不支持合并单元格、背景色等常用视觉）
- 流程图 / 时间线 / 架构图 / 脑图（原生 HTML 根本表达不了）
- 信息密度高的"要点卡片组"（想用 flex 布局，移动端一窄就错位）

**降维思路**：把这类内容**单独画一张 HTML**（可用 Tailwind / inline 样式 / 配色随意，不受微信编辑器 sanitizer 约束）→ 用 headless Chrome 截成 PNG → 在原 markdown 里用 `![](images/xxx.png)` 引用。这样：

- 微信只看到一张图，永远不会排版错乱
- HTML 里可以用任何现代 CSS（grid / gradient / shadow / transform / svg）
- 电脑/手机/平板、任何微信版本显示效果都完全一致
- 和 [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) 无缝接力：PNG 放进 `images/` 目录，后者会自动上传到 mmbiz CDN 并替换占位符
- **源 HTML 永远保留在 `visuals/` 目录**：后续改图只改 HTML，再重新截图导出 PNG；不要只改 PNG，也不要用 Pillow 重新手绘同一张图

#### 工作流（四步）

```
① 识别要图片化的片段 → ② 单独写 HTML → ③ Chrome headless / render.sh 截图 → ④ 原位替换 markdown
```

**① 识别**：扫一遍 markdown，遇到满足 Q5 条件的块，把它们单独抠出来。一般一篇文章 1–3 张图片化块是合理密度。

**② 写 HTML**：在文章目录同级建个 `visuals/` 子目录，每块一个 HTML：

```
article-dir/
├── article-enhanced.md
├── images/              ← 这里放给 wechat-mp-draft-skill 上传的图
└── visuals/             ← 这里放源 HTML，方便后续改
    ├── table-comparison.html
    └── flow-pipeline.html
```

HTML 可以**自由使用**（不受微信兼容性约束）：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    /* 1080px 宽是微信公众号图片的标准宽度——所有平台都按这个宽度算清晰度 */
    body { width: 1080px; margin: 0; padding: 48px; font-family: -apple-system, "PingFang SC", sans-serif; background: #fff; }
  </style>
</head>
<body>
  <!-- 表格、对比卡、流程图……任意 HTML + CSS -->
</body>
</html>
```

**硬约束**：`body` 宽度**必须 1080px**（公众号配图的事实标准，和 `text-to-poster-skill` 对齐）。高度随内容自适应，`render.sh` 会自动裁掉底部空白。

**配色建议**：和所选主题（Step 3）的主色调协调，避免图片突兀。比如选 `newspaper` 主题就用黑白灰 + 深蓝点缀；选 `terracotta` 就用暖橙系。

**③ 截图**：优先用 Chrome headless 从 HTML 源文件直接导出 PNG。对于文章内的固定尺寸流程图、架构图、说明图，推荐用这种方式，所见即所得，方便以后继续改 HTML：

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

"$CHROME" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --window-size=1080,900 \
  --screenshot="$(pwd)/images/flow-pipeline.png" \
  "file://$(pwd)/visuals/flow-pipeline.html"
```

如果底部被截断，就只调大窗口高度，例如：

```bash
"$CHROME" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --window-size=1080,980 \
  --screenshot="$(pwd)/images/flow-pipeline.png" \
  "file://$(pwd)/visuals/flow-pipeline.html"
```

**注意**：这一步是“HTML → 浏览器渲染 → PNG 截图”，不是“Python/Pillow 重绘”。Pillow 只适合裁边或做简单后处理，不要用它复刻复杂卡片、流程图、排版图，否则后续维护成本很高。

也可以复用 `text-to-poster-skill` 的 `render.sh`（已经做好 headless Chrome + Pillow 自动裁边），适合长图或高度不确定的图：

```bash
RENDER_SH="$HOME/projects/william-docs/skills/global/text-to-poster-skill/assets/render.sh"

# 参数：<input.html> [output.png] [bg_r,bg_g,bg_b]
# 第三个参数是背景色 RGB（用于识别底部空白裁剪），默认是 237,232,222（海报主题色）
# 白底 HTML 一定要传 255,255,255
"$RENDER_SH" ./visuals/table-comparison.html ./images/table-comparison.png 255,255,255
```

产出 `images/table-comparison.png`（1080px 宽、高度随内容自适应）。

**④ 原位替换 markdown**：在 `article-enhanced.md` 里把原来的表格 / Mermaid / 要图片化的段落，替换成：

```markdown
![各方案能力对比](images/table-comparison.png)
*图 2：主流 AI 编辑器能力对比（行列过多，图片版更清晰）*
```

后续 Step 4 的 `md2wechat.py` 会把它正常渲染成居中大图 + 灰色小字图说。

#### 什么时候**不要**图片化

- **单列或 2 列的简单表**：微信原生 `<table>` 完全够用，强行图片化反而增加读者的缩放成本
- **正文小段对照**（两三行那种）：用加粗 + 分隔符表达就行
- **需要选中复制的内容**（比如代码、命令、URL）：图片里读者复制不了，**坚决不能图片化**
- **移动端需要放大看细节**的图（比如详细数据表）：图片化后手机上模糊，考虑拆成多张、或接受原生表格

#### 快速起手模板（3 类最常见场景）

以下片段可直接拷到 HTML 文件里（`<body>` 内），按需改文案：

**① 多列对比表**（比原生 `<table>` 好看 10 倍）：

```html
<div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200">
  <div class="grid grid-cols-5 bg-slate-800 text-white text-sm font-semibold">
    <div class="p-4">维度</div>
    <div class="p-4 text-center">方案 A</div>
    <div class="p-4 text-center">方案 B</div>
    <div class="p-4 text-center">方案 C</div>
    <div class="p-4 text-center bg-orange-500">推荐</div>
  </div>
  <div class="grid grid-cols-5 text-sm border-b border-gray-100">
    <div class="p-4 font-medium bg-gray-50">上手难度</div>
    <div class="p-4 text-center">高</div>
    <div class="p-4 text-center">中</div>
    <div class="p-4 text-center">低</div>
    <div class="p-4 text-center bg-orange-50 font-semibold">方案 C</div>
  </div>
  <!-- 更多行…… -->
</div>
```

**② 流程图/时间线**（横向步骤）：

```html
<div class="flex items-center justify-between gap-4">
  <div class="flex-1 bg-blue-50 border-2 border-blue-400 rounded-xl p-6 text-center">
    <div class="text-4xl mb-2">①</div>
    <div class="font-bold text-lg">采集</div>
    <div class="text-sm text-gray-600 mt-2">多源接入</div>
  </div>
  <div class="text-3xl text-gray-400">→</div>
  <div class="flex-1 bg-emerald-50 border-2 border-emerald-400 rounded-xl p-6 text-center">
    <div class="text-4xl mb-2">②</div>
    <div class="font-bold text-lg">清洗</div>
    <div class="text-sm text-gray-600 mt-2">规则 + LLM</div>
  </div>
  <div class="text-3xl text-gray-400">→</div>
  <div class="flex-1 bg-orange-50 border-2 border-orange-400 rounded-xl p-6 text-center">
    <div class="text-4xl mb-2">③</div>
    <div class="font-bold text-lg">发布</div>
    <div class="text-sm text-gray-600 mt-2">定时触发</div>
  </div>
</div>
```

**③ Bento 信息卡组**（把 4–6 个要点可视化）：

```html
<div class="grid grid-cols-3 gap-4">
  <div class="col-span-2 bg-slate-900 text-white rounded-2xl p-8">
    <div class="text-xs uppercase tracking-widest opacity-60 mb-2">核心观点</div>
    <div class="text-3xl font-bold leading-snug">一句话总结，字号最大最醒目。</div>
  </div>
  <div class="bg-orange-500 text-white rounded-2xl p-6">
    <div class="text-5xl font-bold">87%</div>
    <div class="text-sm mt-2 opacity-90">关键数据</div>
  </div>
  <div class="bg-emerald-100 rounded-2xl p-6">
    <div class="font-bold text-emerald-900 mb-2">优势 1</div>
    <div class="text-sm text-emerald-800">一行描述。</div>
  </div>
  <div class="bg-blue-100 rounded-2xl p-6">
    <div class="font-bold text-blue-900 mb-2">优势 2</div>
    <div class="text-sm text-blue-800">一行描述。</div>
  </div>
  <div class="bg-amber-100 rounded-2xl p-6">
    <div class="font-bold text-amber-900 mb-2">优势 3</div>
    <div class="text-sm text-amber-800">一行描述。</div>
  </div>
</div>
```

> **姊妹 skill 提示**：如果**整篇文章**都要变成一张图（朋友圈 / 小红书封面），用 [`text-to-poster-skill`](../text-to-poster-skill/SKILL.md)；本 Step 2.5 只负责**正文里的局部片段**。

### Step 3：选主题（推荐 3 个 + 用户确认）

按 Q2 的内容类型给 3 个推荐，让用户挑。8 个核心主题速记表：

| 主题 ID | 视觉特征 | 适合 |
|---|---|---|
| `newspaper` | 纽约时报衬线、双线标题、严肃克制 | 深度长文、行业分析、评论 |
| `terracotta` | 暖橙赤陶、圆角满底标题、左渐变边 | 访谈对话、文艺随笔 |
| `ink` | 纯黑水墨、极简留白、无装饰 | 哲学思辨、文学性强的文 |
| `github` | 浅色代码块、衬线 + 等宽 | 技术教程、开源项目介绍 |
| `chinese` | 朱砂红、古典装饰元素 | 中国文化、传统主题 |
| `midnight` | 深底霓虹、赛博朋克 | 创意反差、活动预告 |
| `sunset-amber` | 琥珀暖调、温柔渐变 | 个人随笔、感性内容 |
| `magazine` | 超大字号留白、奢侈感 | 品质长文、人物特稿 |

各主题完整样式片段见 [`themes-gallery.md`](themes-gallery.md)。

### Step 4：跑脚本生成 HTML

```bash
SKILL_DIR="$HOME/projects/william-docs/skills/global/wechat-format-skill"

# 标准用法
python3 "$SKILL_DIR/bin/md2wechat.py" \
  --input  ./article-enhanced.md \
  --theme  newspaper \
  --output ./article.html

# 同时打开浏览器预览
python3 "$SKILL_DIR/bin/md2wechat.py" \
  --input  ./article-enhanced.md \
  --theme  newspaper \
  --output ./article.html \
  --open

# 列出所有主题
python3 "$SKILL_DIR/bin/md2wechat.py" --list-themes
```

脚本输出：

- `article.html`：可直接复制粘贴到公众号编辑器的样式化 HTML
- `article.preview.html`：带浏览器壳的预览版（标题、正文宽度模拟微信宽度）

### Step 5：浏览器预览 + 接力

⚠️ **不要用 `open` / `xdg-open` / 双击文件等"系统打开"方式**。`open` 会调用 macOS 的"默认应用"（可能是某个 HTML 编辑器、IDE 预览器、或者一个完全不可控的浏览器），不同人的环境结果千差万别，并且**复制出来的内容在公众号编辑器里经常丢样式**。

**正确姿势：复制 file:// 绝对路径，在浏览器地址栏粘贴打开。**

打印路径供用户复制：

```bash
PREVIEW_PATH=$(realpath ./article.preview.html)
echo ""
echo "📋 复制下面这一行，粘贴到浏览器地址栏（Chrome / Edge / Safari 任意都行）："
echo ""
echo "   file://${PREVIEW_PATH}"
echo ""
```

**用户操作**：

1. 复制上面的 `file://...` 路径
2. 切到浏览器，**直接粘贴到地址栏 → 回车**
3. 看到预览效果

**为什么必须走浏览器地址栏**：

- 浏览器是唯一稳定能渲染 inline-style HTML 的环境
- 浏览器里 Cmd+A 全选 → Cmd+C 复制 → 公众号编辑器 Cmd+V 粘贴，**样式不会丢**（这是公众号支持富文本粘贴的设计前提）
- 系统默认应用打开（例如 macOS 的"快速查看"、某些 IDE 预览器）出来的复制内容是 plain text 或带错误 MIME 的 fragment，粘到公众号会变成裸文本

预览没问题之后两条路：

1. **手动粘贴**：浏览器里全选预览内容 → Cmd+C → 公众号后台编辑器 Cmd+V
2. **自动化接力**（推荐）：转到 [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md)，把 `article.html` 作为输入

---

## 微信编辑器兼容性硬规则（速记）

完整版见 [`compatibility-rules.md`](compatibility-rules.md)。最容易翻车的 5 条：

1. **必须纯内联样式**——`<style>` 标签会被吃掉，CSS class 无效。所有样式写在每个标签的 `style="..."` 上。
2. **`<ul>` / `<ol>` 的 padding/margin 会被微信编辑器抹平**——必须改用 `<section>` + `display:flex` 模拟列表。
3. **外部链接 `<a href>` 会被微信屏蔽展示**——必须把所有外链转成"文中 [1] 角标 + 文末脚注列表"。
4. **代码块需要包一层 `overflow-x:auto`**——长行才能横向滚动而不是溢出版心。
5. **CJK 间距和加粗标点是低级错误的重灾区**：
   - 中英文/中数字之间必须有空格（`Chrome 浏览器` 而不是 `Chrome浏览器`）
   - `**文字，**` 中文标点必须移到加粗外：`**文字**，`

脚本 `md2wechat.py` 自动处理这 5 条。手写时这是必查清单。

---

## 反模式（看到就阻止自己）

1. ❌ 给 `<style>` 块或加 CSS class（微信会删掉，全失效）
2. ❌ 默认主题 = `newspaper`（要根据内容类型选，别一刀切）
3. ❌ 一篇文章里 5 个以上 `:::dialogue` 或 `[!important]`（密度过高，失去强调作用）
4. ❌ 把"作者自己的话"包成 `> 引用`（引用块语义错乱）
5. ❌ 跳过结构化直接排版纯文本笔记（出来全是大段无标题正文）
6. ❌ 没浏览器预览就直接交付（CSS 内联后预览才能看到真实效果）
7. ❌ 把外部链接保留在正文（微信会去掉跳转能力，留 URL 字符串显得脏）
8. ❌ 让 LLM 一次性手写 1000 行 inline-style HTML（必有错位）—— 走 `md2wechat.py` 脚本
9. ❌ 在公众号正文 H1（编辑器顶部已有"标题"输入框，正文 H1 重复）——本 skill 自动去掉首个 H1
10. ❌ 排好版直接粘贴到微信、不在浏览器先 Cmd+C 一次（直接从 HTML 文件复制会丢样式，必须把 `file://` 绝对路径粘到浏览器地址栏打开后再 Cmd+A → Cmd+C）
11. ❌ 用 `open file.html` / 双击 / "在快速查看里打开" 来预览（会用 macOS 默认应用打开，不同环境结果不一致；快速查看复制出来还是 plain text）—— **必须复制 `file://` 路径粘到浏览器地址栏**
12. ❌ 把 4+ 列的宽表 / 复杂对比 / 流程图**硬塞 `<table>`**（移动端必溢出版心，单元格挤到字糊）—— 走 Step 2.5 的"HTML → PNG"降维
13. ❌ 把**代码块、命令、URL、需要选中复制的内容**图片化（读者复制不了；代码块保留文本形态、用主题的代码样式）
14. ❌ 渲染 HTML 截图时**忘记传背景色**（默认裁剪色是 `237,232,222`，白底 HTML 会裁不干净）—— 白底一定要传 `255,255,255`
15. ❌ 图片化 HTML 里用**非 1080px 宽度**（公众号配图清晰度按 1080px 算，其他宽度会被放大糊掉或缩小留白）

---

## 与本项目其他 skill 的关系

- **接力 skill** [`wechat-mp-draft-skill`](../wechat-mp-draft-skill/SKILL.md) —— 本 skill 出 HTML，那个 skill 把 HTML 贴进公众号草稿（图片自动上传到 mmbiz CDN，Step 2.5 产出的 PNG 放在 `images/` 目录即可被自动拾取）
- **前置规则** `~/.cursor/rules/use-agent-browser-for-web.mdc` —— 浏览器操作（如预览自动开起）走 agent-browser
- **工具复用** [`text-to-poster-skill`](../text-to-poster-skill/SKILL.md) —— 它的 `assets/render.sh` 是本 skill Step 2.5 的截图引擎（直接复用，不要另造轮子）；整篇文章变一张图用那个 skill，局部片段图片化用本 skill 的 Step 2.5
- **姊妹 skill** [`html-ppt-skill`](../html-ppt-skill/SKILL.md) —— 同样是 markdown → HTML，但产物是放映稿；不要混用主题 / 兼容性规则（reveal.js 不需要内联样式，公众号必须）

---

## 配套文件

| 文件 | 内容 |
|---|---|
| [`compatibility-rules.md`](compatibility-rules.md) | 微信编辑器兼容性所有硬规则、抹样式案例、修复方案 |
| [`themes-gallery.md`](themes-gallery.md) | 8 套主题的颜色/字体/标题样式速查 + 选型决策表 |
| [`bin/md2wechat.py`](bin/md2wechat.py) | Markdown → 微信兼容 HTML 的渲染脚本（自动处理上述兼容性问题） |

---

*本 skill 的方法论、AI 内容增强规则、主题分类直接整理自 xiaohuailabs/xiaohu-wechat-format；命令行工具思路参考 geekjourneyx/md2wechat-skill。后续遇到新坑请直接更新此文件。*
