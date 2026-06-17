# 前端部署手册 · Pillar 1（13 篇）

> 给前端 / CMS 工程师的集成说明。每篇文章是一个自包含的发布包，按 slug 一对一映射到站点路由。

## 1. 路由映射

所有文章使用 **扁平 slug**，不带日期前缀：

| slug | 源目录 | 发布 URL |
|---|---|---|
| `ai-for-data-analysis` | `001-ai-for-data-analysis/` | `https://infinisynapse.cn/blog/ai-for-data-analysis` |
| `data-agent-manifesto` | `002-data-agent-manifesto/` | `https://infinisynapse.cn/blog/data-agent-manifesto` |
| `what-is-a-data-agent` | `003-what-is-a-data-agent/` | `https://infinisynapse.cn/blog/what-is-a-data-agent` |
| `ai-native-data-platform` | `004-ai-native-data-platform/` | `https://infinisynapse.cn/blog/ai-native-data-platform` |
| `best-agentic-analytics` | `005-best-agentic-analytics/` | `https://infinisynapse.cn/blog/best-agentic-analytics` |
| `autonomous-data-agent` | `006-autonomous-data-agent/` | `https://infinisynapse.cn/blog/autonomous-data-agent` |
| `ai-data-analyst` | `007-ai-data-analyst/` | `https://infinisynapse.cn/blog/ai-data-analyst` |
| `ai-data-analyst-job-description` | `008-ai-data-analyst-job-description/` | `https://infinisynapse.cn/blog/ai-data-analyst-job-description` |
| `data-agent-memory` | `009-data-agent-memory/` | `https://infinisynapse.cn/blog/data-agent-memory` |
| `fabric-data-agent-vs-copilot` | `010-fabric-data-agent-vs-copilot/` | `https://infinisynapse.cn/blog/fabric-data-agent-vs-copilot` |
| `ai-native-vs-augmented-analytics` | `011-ai-native-vs-augmented-analytics/` | `https://infinisynapse.cn/blog/ai-native-vs-augmented-analytics` |
| `ai-data-analysis` | `012-ai-data-analysis/` | `https://infinisynapse.cn/blog/ai-data-analysis` |
| `data-agent-glossary` | `013-data-agent-glossary/` | `https://infinisynapse.cn/blog/data-agent-glossary` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 单页集成步骤

对每一篇文章，按以下顺序集成：

### Step A · 解析正文

1. 读取 `article.md`
2. 跳过文件顶部到第一个 `---` 分隔线之后的 **元数据注释块**（Slug / Target keyword 等行），或保留为 CMS 自定义字段
3. 将 Markdown 渲染为 HTML
4. **必须为所有 H2/H3 生成 `id` 属性**，与 TOC 锚点一致（如 `#tldr`、`#frequently-asked-questions`）

### Step B · 注入 `<head>`

1. 将 `meta-tags.html` 中 **HTML 注释以外的 `<meta>` / `<title>` / `<link>` 标签** 原样插入页面 `<head>`
2. 将 `schema.json` 内容包裹为：

```html
<script type="application/ld+json">
  <!-- paste schema.json array contents here -->
</script>
```

3. `schema.json` 是 **JSON 数组**（2–4 个 schema 对象），作为一个 `<script>` 块输出，或拆成多个 `<script>` 块均可

### Step C · 图片

1. 各 `article.md` 中 `![alt](images/xxx.png)` 引用的是 **相对路径**
2. 部署时上传到 CDN，建议路径：`/blog/assets/pillar1/<slug>/xxx.png`
3. 同步更新：
   - 正文 `<img src>`
   - `meta-tags.html` 中 `og:image`
   - `schema.json` 中 `image` 数组

### Step D · 内链

正文中的内链格式为 Markdown 链接：`/blog/<slug>`。渲染后应保持为站内相对路径，**不要**加 `nofollow`。

## 3. HTML 页面骨架示例

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- 从 meta-tags.html 粘贴（去掉注释块） -->
  <title>AI for Data Analysis: The Complete 2026 Guide</title>
  <meta name="description" content="...">
  <link rel="canonical" href="https://infinisynapse.cn/blog/ai-for-data-analysis">
  <!-- ... OG / Twitter / hreflang ... -->

  <script type="application/ld+json">
  [
    { "@context": "https://schema.org", "@type": "BlogPosting", ... },
    { "@context": "https://schema.org", "@type": "FAQPage", ... },
    { "@context": "https://schema.org", "@type": "BreadcrumbList", ... }
  ]
  </script>
</head>
<body>
  <article class="blog-post">
    <!-- article.md 渲染后的 HTML -->
  </article>
</body>
</html>
```

## 4. CMS 字段建议

| CMS 字段 | 来源 | 说明 |
|---|---|---|
| `title` | `meta-tags.html` `<title>` | 推荐用 Option A |
| `description` | `meta-tags.html` `meta[name=description]` | |
| `slug` | `article.md` **Slug** 行 | 如 `/blog/ai-for-data-analysis` → slug = `ai-for-data-analysis` |
| `published_at` | `schema.json` `datePublished` | `2026-06-08T10:00:00+08:00` |
| `author` | `InfiniSynapse Data Team` | Organization 类型 |
| `primary_keyword` | `article.md` **Target keyword** | SEO 追踪用 |
| `body` | `article.md` 正文 | Markdown 源 |
| `og_image` | 待设计 hero PNG | 1200×630 |
| `audit_score` | `audit.md` Overview 表 | 运营追踪用，不上线 |
| `pillar` | `pillar1-ai-native-data-analysis` | 集群标签 |

## 5. 批量导入脚本思路

若使用静态站点生成器（Next.js / Hugo / Astro），可用以下逻辑批量注册：

```bash
PILLAR_DIR="SEO/Blog/pillar1-ai-native-data-analysis"
for dir in "$PILLAR_DIR"/[0-9][0-9][0-9]-*/; do
  slug=$(basename "$dir" | sed 's/^[0-9]*-//')
  echo "Route: /blog/$slug"
  echo "  article:  $dir/article.md"
  echo "  meta:     $dir/meta-tags.html"
  echo "  schema:   $dir/schema.json"
done
```

## 6. 质量门禁（发布前必查）

每篇发布前对照 `audit.md` 确认：

| 检查项 | 方法 |
|---|---|
| Title = H1 主旨一致 | 比对 `<title>` 与 `article.md` H1 |
| Canonical 无尾斜杠 | `https://infinisynapse.cn/blog/<slug>`（无 `/` 结尾） |
| **正文字数 2000–2500** | 见下方「字数与关键词密度」；跑 `python3 SEO/Blog/audit-wordcount.py` |
| **主关键词密度 1.2%–1.7%** | 同上；关键词 = `article.md` 中 `**Target keyword**` 完整短语 |
| **高 DR 外链 ≥ 5 且叙事嵌入** | `python3 SEO/Blog/audit-high-dr-links.py` + `audit-external-links.py`；见 [`SEO/Blog/SKILL.md`](../../SKILL.md) |
| FAQ 可见文本 = schema | 页面 FAQ 段落与 `schema.json` FAQPage 逐条一致 |
| 图片 alt 存在 | 所有 `<img>` 有非空 alt |
| hreflang 200 | `/blog/<slug>` 和 `/zh/blog/<slug>` 均可用或暂时移除中文 alternate |
| 内链 200 | 抽样点击 Related Reading 中 3 条链接 |

### 字数与关键词密度（批量门禁）

| 指标 | 要求 | 统计口径 |
|---|---|---|
| 正文字数 | **2000–2500** 词 | 从 `## TL;DR` 至文末（不含 frontmatter、TOC） |
| 主关键词密度 | **1.2%–1.7%** | `Target keyword` 完整短语，大小写不敏感精确匹配 |
| 目标词频（约 2200 词） | 约 **26–37 次** | 密度 = 关键词出现次数 ÷ 总词数 × 100% |

```bash
# Pillar 1 + Pillar 3 一次性复查（33 篇）
python3 SEO/Blog/audit-wordcount.py

# 仅本集群
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar1-ai-native-data-analysis
```

脚本路径：[SEO/Blog/audit-wordcount.py](../../audit-wordcount.py)。扩写或删改正文后须重跑，并同步检查 FAQ ↔ `schema.json` 是否仍一致。

**高 DR 权威外链**：每篇 `article.md` 至少 **5 个**来自 DR≥70 站点的唯一外链，**织入正文叙事句**（禁止 `## Sources` 列表、裸 URL 锚文本）。发布前须 HTTP 200：

```bash
python3 SEO/Blog/audit-high-dr-links.py
python3 SEO/Blog/audit-external-links.py
```

批准来源清单：`SEO/Blog/high-dr-authority-sources.py`。规则全文：`SEO/Blog/SKILL.md`。

### CORE-EEAT 快速门禁（12 项）

```bash
python3 SEO/Blog/audit-eeat.py
```

| 维度 | 检查项 |
|---|---|
| **Trust (T)** | T04 品牌披露 byline（`We build InfiniSynapse`） |
| **Expertise (Ept)** | 作者团队 + `schema.json` BlogPosting.author |
| **Experience (Exp)** | 一手评估语料（`We evaluate` / `Evaluation basis` / hands-on） |
| **Referenceability (R)** | R02 外链密度、R06 更新日期、R08 内链集群 |
| **Context (C)** | TL;DR、Key Definition、FAQ ≥4 |
| **Organization (O)** | TOC、schema.json |

Veto 代理项：无品牌披露、FAQ 与 schema 不一致、数据自相矛盾 — 发布前人工复核 `audit.md`。

同步 `audit.md` 字数 / 密度 / EEAT / 外链门禁表：

```bash
python3 SEO/Blog/sync-audit-gates.py
```

## 7. 不需要部署的文件

| 文件 | 用途 |
|---|---|
| `audit.md` | 编辑/运营 QA 记录，不上线 |
| `README.md` | 交付说明，不上线 |
| `preview.html` | 本地预览页（每篇），不上线 |
| `INDEX-preview.html` | 预览索引（pillar 根目录），不上线 |
| `visuals/*.html` | 插图 HTML 源文件，不上线 |
| `images/.gitkeep` | 占位，上线前替换为实际 PNG |

### 生成预览 HTML

```bash
python3 SEO/Blog/pillar1-ai-native-data-analysis/build-preview.py
open SEO/Blog/pillar1-ai-native-data-analysis/INDEX-preview.html
```

规范见 Skills：`build/seo-content-writer/references/blog-preview-html-spec.md`

## 8. 插入现有博客列表页（Últimas novedades）

你截图中的列表页是 **卡片网格 + 顶部分类筛选**。13 篇需要同时做两件事：

### A. 列表页卡片（索引数据）

读取 [blog-index-import.json](./blog-index-import.json)，把 `posts` 数组合并进现有 `blogPosts` 数据源。

每张卡片需要的字段（与现有 UI 对齐）：

| 卡片元素 | 数据源字段 | 示例 |
|---|---|---|
| 左上角小标签 | `card_tag` | `Guides` / `Comparisons` / `Deep Dive` |
| 日期 | `display_date` | `08 JUN 2026` |
| 标题 | `title` | 来自 `meta-tags.html` `<title>` |
| 摘要 | `excerpt` | 来自 `meta description`（120–160 字符） |
| 链接 | `url` | `/blog/ai-for-data-analysis` |
| 筛选归属 | `filter_category` | 见下表 |

### B. 分类筛选计数更新

导入后顶部分类数字应从 **24 → 37**：

| filter_category | 西班牙语标签 | 现有 | +13 篇后 |
|---|---|---:|---:|
| `all` | Todos | 24 | **37** |
| `knowledge` | Base de conocimiento y explicaciones | 5 | **13** |
| `comparisons` | Comparativas y alternativas | 12 | **14** |
| `deep_dive` | Análisis técnico a fondo | 4 | **6** |
| `tools_reviews` | Herramientas y reseñas | 2 | **3** |
| `tutorials` | Tutoriales y buenas prácticas | 1 | 1 |

13 篇分类映射：

| slug | filter_category | card_tag |
|---|---|---|
| ai-for-data-analysis, ai-data-analysis, what-is-a-data-agent, data-agent-glossary, ai-data-analyst, ai-native-data-platform, autonomous-data-agent, ai-data-analyst-job-description | `knowledge` | Guides |
| best-agentic-analytics | `tools_reviews` | Tools & Reviews |
| fabric-data-agent-vs-copilot, ai-native-vs-augmented-analytics | `comparisons` | Comparisons |
| data-agent-manifesto, data-agent-memory | `deep_dive` | Deep Dive |

### C. 详情页（点击「Leer artículo」后）

列表卡片只负责导航；正文仍从各文件夹加载：

```
posts[i].source_folder → SEO/Blog/pillar1-ai-native-data-analysis/{folder}/
  article.md      → 渲染为详情页 body
  meta-tags.html  → 注入 <head>
  schema.json     → JSON-LD
```

### D. 排序建议

`blog-index-import.json` 里 `sort_priority` 已按发布波次排好：**新文章排在最前**（100 → 88），不会把 5 月旧文全部顶掉，但 Wave 1 头部词（001、012）会出现在第一屏。

若列表默认按 `published_at` 降序，直接导入即可；若前端写死了排序，把 `sort_priority` 接入排序逻辑。

### E. 多语言

截图 UI 是西班牙语（「Leer artículo」），但现有卡片标题也是英文——**13 篇保持英文标题即可**，与现有 24 篇一致。只需：

- 分类标签继续用西班牙语（`category_labels`）
- 按钮文案继续走 i18n（`Leer artículo` / `Read article`）
- 文章 `hreflang` 已在 `meta-tags.html` 预留 `en` + `zh-CN`

### F. 前端伪代码

```ts
import pillar1 from './blog-index-import.json';
import existingPosts from './existing-blog-posts';

const allPosts = [...pillar1.posts, ...existingPosts]
  .sort((a, b) => b.sort_priority - a.sort_priority || Date.parse(b.published_at) - Date.parse(a.published_at));

const filtered = activeCategory === 'all'
  ? allPosts
  : allPosts.filter(p => p.filter_category === activeCategory);
```

## 9. 联系与变更

- 内容源：`SEO/Blog/pillar1-ai-native-data-analysis/`
- 规划对照：`SEO/100页主题集群规划-v1-替换后主关键词版.md` § Pillar 1
- SEO 技能链：`Skills/seo-geo-claude-skills-main/`
- 若需修改正文：改 `article.md` 后同步更新 `schema.json` FAQ 和 `meta-tags.html`（防 R10 数据不一致 veto）
