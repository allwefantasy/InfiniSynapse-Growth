# 5 张博客图片的制作方案

> 本批次（2026-05-19 Data Agent 系列 4 篇博客）一共引用 5 张图。其中 3 张能直接复用源稿，2 张需要用 HTML 模板渲染，1 张需要真实产品截图。
>
> 所有制作流程沿用团队现有的 **HTML 模板 → Chrome headless 截图 → PNG** 工作流（参考 01 源稿 `visuals/code-agent-data-agent-cover.html`）。

## 一键执行（推荐）

```bash
cd /Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth

# 1. 复制源稿里已有的图（01 / 02 / 04 多张产品截图）
bash SEO/Blog/scripts/copy-source-images.sh

# 2. 渲染新做的 2 张 HTML → PNG（03 hero + 04 cover）
bash SEO/Blog/scripts/render-html-to-png.sh all

# 3. （仅剩一项）按下面"03 Task View 截图指南"手动捕一张
```

跑完 1+2，4 篇中的 4 张图就位，只剩 03 的 Task View 截图需要手动操作。

## 5 张图的来源对照

| # | 目标位置 | 来源 | 方式 |
|---|---|---|---|
| 01 hero | `01/images/code-agent-data-agent-cover.png` | 源稿 `01/images/code-agent-data-agent-cover.png` | `cp` |
| 02 cover | `02/images/cover.png` | 源稿 `02/cover-1080p.png`（1920×1080） | `cp` |
| 03 hero | `03/images/hero-supabase-connect.png` | `03/visuals/hero-supabase-connect.html`（新写） | Chrome headless |
| 03 Task View | `03/images/task-view-supabase-q1.png` | 真实产品 + 真实数据 | 手动截图 |
| 04 cover | `04/images/cover-roadshow.png` | `04/visuals/cover-roadshow.html`（新写） | Chrome headless |
| 04 配图（可选） | `04/images/assets/*.png`（13 张） | 源稿 `04/assets/` | `cp` |

## 三种制作方式详解

### 方式 A：直接复制（01 hero、02 cover、04 配图）

源稿里已经有了，跑 `copy-source-images.sh` 即可。这部分用了团队之前已经审过、已经发布过的视觉资产，**零额外工作**。

### 方式 B：HTML 模板 → Chrome headless 截图（03 hero、04 cover）

这就是团队之前做封面图的标准工作流（看 `01-why-code-agent-cannot-solve-enterprise-data-analysis/visuals/code-agent-data-agent-cover.html` 就是这种模板）。

**模板已经写好，在每篇 bundle 的 `visuals/` 子目录里**：

- `03/visuals/hero-supabase-connect.html` — 暗色科技风，10 个数据源 chip + 箭头 + InfiniSynapse target 卡片
- `04/visuals/cover-roadshow.html` — MPD 演讲封面，左侧标题 + 演讲者，右侧八件套 chip + 3 组硬证据数字

渲染：

```bash
# 单张
bash SEO/Blog/scripts/render-html-to-png.sh 03-hero-supabase
bash SEO/Blog/scripts/render-html-to-png.sh 04-cover-roadshow

# 全部
bash SEO/Blog/scripts/render-html-to-png.sh all
```

**实际命令是这个**（脚本里已封装）：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --hide-scrollbars \
  --disable-gpu \
  --force-device-scale-factor=2 \
  --window-size=1200,630 \
  --screenshot=output.png \
  file:///path/to/visual.html
```

`--force-device-scale-factor=2` 让输出变 2400×1260（Retina @2x），上 CMS 后自动 downscale 看着锐。

**想改设计**？直接编辑 `visuals/*.html` 里的 CSS，重新跑脚本即可，无需设计师。

### 方式 C：真实产品截图（03 Task View）

这一张是**唯一需要真实数据 + 真实产品**的图。流程：

1. 登录 [app.infinisynapse.cn](https://app.infinisynapse.cn)
2. **准备一个 Supabase Demo 项目**（不要用客户真实数据）：
   - 用 Supabase 官方提供的电商示例（`orders` / `customers` / `products` 三表）
   - 或自建一个有 ~50 行数据的 demo 项目
3. 在 InfiniSynapse 里新建 task，运行 article.md 中"A Working Business-Question Example"那段提示词：
   > *"Which product categories grew fastest in Q1 2026, controlling for promotion windows, and which 3 customers contributed most to that growth?"*
4. 等 task 跑完，**Task View 展开到完整的 4-tool-call SQL 轨迹 + 中间表**（`q1_orders` → `q1_orders_tagged` → `category_growth` → `top_contributors`）
5. 截图工具：
   - **macOS 系统截图**：`Cmd + Shift + 4` 选区截
   - **更高级**：用 [Cleanshot X](https://cleanshot.com) 或 [Shottr](https://shottr.cc/)，自动加阴影 + 圆角
   - **如果整个 Task View 太长**：用 Chrome DevTools → ⌘+Shift+P → "Capture full size screenshot"
6. 输出：1200×750–900 都可（比 hero 高没关系，是内嵌图不是 OG 图），存到 `03/images/task-view-supabase-q1.png`

**敏感数据脱敏**：截图前在 Supabase 里把 `customers.email` 改成 `user1@example.com` / `user2@example.com` 等示例邮箱。

> **如果暂时没条件做真实截图**：article.md 里有这张图的 markdown 引用，可以先注释掉，文章 SHIP 不受影响（audit 是 SHIP 状态）。后期补图就行。

## 如果想用 AI 生成图（替代/互补方案）

> **何时用 AI 出图**：HTML 模板做不了的写实/插画风、A/B 多版备选、还没写 HTML 模板时的快速 prototype。文字精确、可版本化的封面，**首选 HTML 模板**。

### 方式 D · OpenOctopus CLI 自动出图（推荐用本仓库脚本）

前置：CLI 已装好并登录（`ooct auth status` 显示 Authenticated）。

> **强制规则（脚本会 lint，违规直接拒跑）**
>
> 1. **prompt 正文必须英文**——不允许 CJK 字符、中文标点、全角符号。中文笔记 / TODO 写在 `# ` 注释行里会被自动剥离。
> 2. **正文里必须写 `no text, no lettering, no logos, no watermarks`**。图像模型连英文都常拼错，中文文字叠加一律走 HTML 模板（方式 B），AI 只产纯视觉。
>
> 设计本意：把"写漂亮文字"和"出抽象视觉"两件事拆开。HTML 模板擅长前者（可版本化、可改字、可校对），AI 擅长后者（写实、隐喻、构图）。把两件事混在一张 AI 图里，是最容易翻车的姿势。

```bash
# 1) 给目标 bundle 写一份 prompt
mkdir -p SEO/Blog/<slug>/prompts
cp SEO/Blog/scripts/cover-prompt.template SEO/Blog/<slug>/prompts/cover.prompt
# ↑ 用编辑器改成本篇博客适用的描述

# 2) 出图（默认 imagen-4 / 16:9 / 2k，约 $0.038/张，输出到 images/cover-ai.png）
bash SEO/Blog/scripts/generate-cover-image-ai.sh <slug>

# 3) 跑全部已写 prompt 的博客
bash SEO/Blog/scripts/generate-cover-image-ai.sh all

# 4) 看计划但不真跑（不花钱）
bash SEO/Blog/scripts/generate-cover-image-ai.sh all --dry-run
```

常用 flags：

```bash
--model openoctopus/nano-banana-pro    # 切高质量（$0.14/张 1k|2k；$0.24/张 4k）
--resolution 2k                        # 默认 2k；nano-banana-pro 支持 4k
--aspect-ratio 16:9                    # 也支持 1:1 / 4:3 / 9:16 / 3:4
--output-name hero-ai.png              # 默认 cover-ai.png（避免覆盖 HTML 渲染产物）
--prompt "..."                         # 内联 prompt，不读文件
--prompt-file path/to.prompt           # 外部 prompt 文件
--force                                # 允许覆盖已有同名图
```

脚本会先打印计划 + 估价，跑批 ≥2 张或单价 ≥ $0.20 时要求 y 确认；模型与单价从 `ooct models inspect` 抓的，更新单价时改脚本里的 `price_for()`。

### 方式 E · 手动 prompt 丢给 ChatGPT / Midjourney / Firefly（备份）

下面的 prompt 也可以直接丢给 ChatGPT / Midjourney / Adobe Firefly：

**03 hero 备用 prompt**：

> A modern dark-themed banner image, 1200×630 pixels, for a tech blog. Left side shows 10 database/service logos arranged in a 2×5 grid: Supabase (highlighted with green glow), PostgreSQL, MySQL, ClickHouse, MongoDB, Snowflake, SQL Server, Apache Doris, Excel, REST API. An arrow flows from the grid to a single highlighted card on the right labeled "InfiniSynapse Data Agent — One Task, Ten Sources". Color palette: deep navy (#0c1117), Supabase green accent (#3ba874), neutral text (#e8edf3). Minimalist, technical, editorial style — no people, no clip art.

**04 cover 备用 prompt**：

> A dark editorial conference-talk cover, 1200×630 pixels. Left half: bold Chinese title "构建 Data Agent 的完整 Harness", subtitle "不是一个功能解决一个问题，而是一条由八件套组成的闭环一起收敛", speaker name "祝海林 · InfiniSynapse 创始人", event "MPD AI 驱动创新峰会 2026-05-29 上海". Right half: 8 small rectangular chips labeled InfiniAgent / 数据源对象化 / 跨源执行 / InfiniSQL / InfiniRAG / Runtime RAG / Task View / 资产沉淀, plus 3 statistic blocks below: "1400+ 张表", "92s 端到端", "AUC 0.7712". Color palette: dark teal (#071111), bright teal accent (#00bfa6). Tech-conference style.

但**强烈推荐用 HTML 模板**，原因：
- AI 生成的英文/中文文字常出错
- 改字、改色不用重新生成
- 与团队之前的视觉风格统一
- 完全可控、可版本化（HTML 进 git）

## 验收（生成后跑一遍）

```bash
# 检查 5 张图都到位
for d in 2026-05-19-why-code-agents-cannot-solve-enterprise-data-analysis \
         2026-05-19-data-agent-new-civilization \
         2026-05-19-ai-analyst-real-data-supabase \
         2026-05-19-data-agent-harness-roadshow; do
  echo "── $d ──"
  ls -la SEO/Blog/"$d"/images/ 2>/dev/null
done

# 检查尺寸
for png in SEO/Blog/2026-05-19-*/images/*.png; do
  echo "$png"
  sips -g pixelWidth -g pixelHeight "$png" 2>/dev/null | grep pixel
done
```

## 文件结构

```
SEO/Blog/
├── scripts/
│   ├── README.md                          ← 本文件
│   ├── copy-source-images.sh              ← 一键复制源稿已有图
│   ├── render-html-to-png.sh              ← 一键 HTML → PNG（首选）
│   ├── generate-cover-image-ai.sh         ← 一键 AI 出图（OpenOctopus CLI）
│   └── cover-prompt.template              ← prompt 模板（复制到 <bundle>/prompts/cover.prompt）
├── 2026-05-19-ai-analyst-real-data-supabase/
│   ├── visuals/
│   │   └── hero-supabase-connect.html     ← 03 hero 模板（新）
│   └── images/
│       └── hero-supabase-connect.png      ← 渲染输出
└── 2026-05-19-data-agent-harness-roadshow/
    ├── visuals/
    │   └── cover-roadshow.html            ← 04 cover 模板（新）
    └── images/
        └── cover-roadshow.png             ← 渲染输出
```
