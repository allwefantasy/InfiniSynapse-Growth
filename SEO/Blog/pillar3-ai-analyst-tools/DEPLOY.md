# 前端部署手册 · Pillar 3（20 篇）

> 给前端 / CMS 工程师的集成说明。每篇文章是一个自包含的发布包，按 slug 一对一映射到站点路由。
>
> **内容集群**：AI Data Analyst Tools / Alternatives / vs（规划文档 024–043）

## 1. 路由映射

所有文章使用 **扁平 slug**，不带日期前缀：

| slug | 源目录 | 发布 URL |
|---|---|---|
| `best-ai-tools-for-data-analysis` | `024-best-ai-tools-for-data-analysis/` | `https://infinisynapse.cn/blog/best-ai-tools-for-data-analysis` |
| `ai-data-analysis-tools` | `025-ai-data-analysis-tools/` | `https://infinisynapse.cn/blog/ai-data-analysis-tools` |
| `sql-data-analysis-tools` | `026-sql-data-analysis-tools/` | `https://infinisynapse.cn/blog/sql-data-analysis-tools` |
| `ai-excel-data-analysis-tools` | `027-ai-excel-data-analysis-tools/` | `https://infinisynapse.cn/blog/ai-excel-data-analysis-tools` |
| `ai-data-visualization-tools` | `028-ai-data-visualization-tools/` | `https://infinisynapse.cn/blog/ai-data-visualization-tools` |
| `self-hosted-ai-data-analyst` | `029-self-hosted-ai-data-analyst/` | `https://infinisynapse.cn/blog/self-hosted-ai-data-analyst` |
| `chatgpt-data-analysis-alternatives` | `030-chatgpt-data-analysis-alternatives/` | `https://infinisynapse.cn/blog/chatgpt-data-analysis-alternatives` |
| `julius-ai-alternatives` | `031-julius-ai-alternatives/` | `https://infinisynapse.cn/blog/julius-ai-alternatives` |
| `thoughtspot-alternatives` | `032-thoughtspot-alternatives/` | `https://infinisynapse.cn/blog/thoughtspot-alternatives` |
| `databricks-genie-alternatives` | `033-databricks-genie-alternatives/` | `https://infinisynapse.cn/blog/databricks-genie-alternatives` |
| `tableau-pulse-alternatives` | `034-tableau-pulse-alternatives/` | `https://infinisynapse.cn/blog/tableau-pulse-alternatives` |
| `perplexity-data-analysis-alternatives` | `035-perplexity-data-analysis-alternatives/` | `https://infinisynapse.cn/blog/perplexity-data-analysis-alternatives` |
| `code-interpreter-alternatives` | `036-code-interpreter-alternatives/` | `https://infinisynapse.cn/blog/code-interpreter-alternatives` |
| `infinisynapse-vs-julius-ai` | `037-infinisynapse-vs-julius-ai/` | `https://infinisynapse.cn/blog/infinisynapse-vs-julius-ai` |
| `infinisynapse-vs-chatgpt` | `038-infinisynapse-vs-chatgpt/` | `https://infinisynapse.cn/blog/infinisynapse-vs-chatgpt` |
| `infinisynapse-vs-databricks-genie` | `039-infinisynapse-vs-databricks-genie/` | `https://infinisynapse.cn/blog/infinisynapse-vs-databricks-genie` |
| `julius-ai-vs-chatgpt` | `040-julius-ai-vs-chatgpt/` | `https://infinisynapse.cn/blog/julius-ai-vs-chatgpt` |
| `thoughtspot-vs-databricks-genie` | `041-thoughtspot-vs-databricks-genie/` | `https://infinisynapse.cn/blog/thoughtspot-vs-databricks-genie` |
| `infinisynapse-vs-tableau` | `042-infinisynapse-vs-tableau/` | `https://infinisynapse.cn/blog/infinisynapse-vs-tableau` |
| `infinisynapse-review` | `043-infinisynapse-review/` | `https://infinisynapse.cn/blog/infinisynapse-review` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 单页集成步骤

### Step A · 解析正文

1. 读取 `article.md`
2. 跳过文件顶部元数据注释块（Slug / Target keyword 等），或映射为 CMS 自定义字段
3. 将 Markdown 渲染为 HTML
4. **必须为所有 H2/H3 生成 `id` 属性**，与 TOC 锚点一致

### Step B · 注入 `<head>`

1. 将 `meta-tags.html` 中 HTML 注释以外的标签原样插入 `<head>`
2. 将 `schema.json` 包裹为：

```html
<script type="application/ld+json">
  <!-- paste schema.json array -->
</script>
```

### Step C · 图片

1. 正文 `![alt](images/xxx.png)` 为相对路径
2. 上传到 CDN：`/blog/assets/pillar3/<slug>/xxx.png`
3. **OG 统一路径**：`/blog/assets/pillar3/<slug>/hero.png`（各文件夹 `images/hero.png` 已生成）
4. 同步更新正文 `<img>`、`meta-tags.html` `og:image`、`schema.json` `image`

### Step D · 内链

正文内链格式 `/blog/<slug>`，保持站内相对路径，不加 `nofollow`。

## 3. HTML 页面骨架示例

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- meta-tags.html（去注释） -->
  <title>Best AI Tools for Data Analysis in 2026</title>
  <meta name="description" content="...">
  <link rel="canonical" href="https://infinisynapse.cn/blog/best-ai-tools-for-data-analysis">
  <script type="application/ld+json">[ ... ]</script>
</head>
<body>
  <article class="blog-post"><!-- article.md HTML --></article>
</body>
</html>
```

## 4. CMS 字段建议

| CMS 字段 | 来源 |
|---|---|
| `title` | `meta-tags.html` `<title>` |
| `description` | `meta[name=description]` |
| `slug` | `article.md` Slug 行 |
| `published_at` | `schema.json` `datePublished` |
| `author` | `InfiniSynapse Data Team` |
| `primary_keyword` | `article.md` Target keyword |
| `body` | `article.md` |
| `og_image` | `/blog/assets/pillar3/<slug>/hero.png` |
| `pillar` | `pillar3-ai-analyst-tools` |

## 5. 批量导入

```bash
PILLAR_DIR="SEO/Blog/pillar3-ai-analyst-tools"
for dir in "$PILLAR_DIR"/[0-9][0-9][0-9]-*/; do
  slug=$(basename "$dir" | sed 's/^[0-9]*-//')
  echo "Route: /blog/$slug"
done
```

## 6. 质量门禁（发布前）

对照 `audit.md`：

| 检查项 | 方法 |
|---|---|
| Title ≈ H1 | 比对 meta 与 `article.md` H1 |
| Canonical 无尾斜杠 | `https://infinisynapse.cn/blog/<slug>` |
| **正文字数 2000–2500** | `python3 SEO/Blog/audit-wordcount.py`（见下表） |
| **主关键词密度 1.2%–1.7%** | 关键词 = `**Target keyword**` 完整短语 |
| **高 DR 外链 ≥ 5 且叙事嵌入** | `python3 SEO/Blog/audit-high-dr-links.py` + `audit-external-links.py` |
| FAQ = schema | 页面 FAQ 与 FAQPage schema 逐条一致 |
| 图片 alt | 所有 `<img>` 非空 alt |
| 内链 200 | 抽样 Related Reading |

### 字数与关键词密度（批量门禁）

| 指标 | 要求 | 统计口径 |
|---|---|---|
| 正文字数 | **2000–2500** 词 | 从 `## TL;DR` 至文末（不含 frontmatter、TOC） |
| 主关键词密度 | **1.2%–1.7%** | 完整短语精确匹配（大小写不敏感） |
| 目标词频（约 2200 词） | 约 **26–37 次** | 出现次数 ÷ 总词数 × 100% |

```bash
python3 SEO/Blog/audit-wordcount.py
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar3-ai-analyst-tools
```

脚本：[SEO/Blog/audit-wordcount.py](../../audit-wordcount.py)。正文变更后重跑；若改 FAQ 须同步 `schema.json`。

**高 DR 权威外链**（≥5 条，叙事嵌入正文，HTTP 200）：

```bash
python3 SEO/Blog/audit-high-dr-links.py
python3 SEO/Blog/audit-external-links.py
python3 SEO/Blog/audit-eeat.py
```

规则与来源清单：`SEO/Blog/SKILL.md`、`high-dr-authority-sources.py`。EEAT 另需 byline、TL;DR、Key Definition、FAQ、内链集群。详见 Pillar 1 `DEPLOY.md` §6。

同步 `audit.md` 门禁字段：`python3 SEO/Blog/sync-audit-gates.py`

## 7. 不需要部署的文件

| 文件 | 用途 |
|---|---|
| `audit.md` | QA，不上线 |
| `README.md` | 交付说明 |
| `preview.html` / `INDEX-preview.html` | 本地预览 |
| `visuals/*.html` | 封面源文件 |
| `build-*.py` / `render-all-images.sh` | 生成脚本 |

生成预览：

```bash
python3 SEO/Blog/pillar3-ai-analyst-tools/build-preview.py
```

## 8. 插入博客列表页（Últimas novedades）

读取 [blog-index-import.json](./blog-index-import.json)，将 `posts` 合并进 `blogPosts`。

### A. 卡片字段

| 卡片元素 | 字段 |
|---|---|
| 标签 | `card_tag` |
| 日期 | `display_date` |
| 标题 | `title` |
| 摘要 | `excerpt` |
| 链接 | `url` |
| 封面 | `hero_image` |
| 筛选 | `filter_category` |

### B. 分类计数（在 Pillar 1 导入后基础上 +20）

| filter_category | 西班牙语 | Pillar1 后 | +Pillar3 后 |
|---|---|---:|---:|
| `all` | Todos | 37 | **57** |
| `comparisons` | Comparativas y alternativas | 14 | **26** |
| `tools_reviews` | Herramientas y reseñas | 3 | **10** |
| `deep_dive` | Análisis técnico a fondo | 6 | **7** |
| `knowledge` | Base de conocimiento | 13 | 13 |
| `tutorials` | Tutoriales | 1 | 1 |

20 篇分类映射：

| slug | filter_category | card_tag |
|---|---|---|
| best-ai-tools-for-data-analysis | `tools_reviews` | Tools & Reviews |
| ai-data-analysis-tools | `tools_reviews` | Tools & Reviews |
| sql-data-analysis-tools | `tools_reviews` | Tools & Reviews |
| ai-excel-data-analysis-tools | `tools_reviews` | Tools & Reviews |
| ai-data-visualization-tools | `tools_reviews` | Tools & Reviews |
| self-hosted-ai-data-analyst | `deep_dive` | Deep Dive |
| chatgpt-data-analysis-alternatives | `comparisons` | Comparisons |
| julius-ai-alternatives | `comparisons` | Comparisons |
| thoughtspot-alternatives | `comparisons` | Comparisons |
| databricks-genie-alternatives | `comparisons` | Comparisons |
| tableau-pulse-alternatives | `comparisons` | Comparisons |
| perplexity-data-analysis-alternatives | `comparisons` | Comparisons |
| code-interpreter-alternatives | `comparisons` | Comparisons |
| infinisynapse-vs-julius-ai | `comparisons` | Comparisons |
| infinisynapse-vs-chatgpt | `comparisons` | Comparisons |
| infinisynapse-vs-databricks-genie | `comparisons` | Comparisons |
| julius-ai-vs-chatgpt | `comparisons` | Comparisons |
| thoughtspot-vs-databricks-genie | `comparisons` | Comparisons |
| infinisynapse-vs-tableau | `comparisons` | Comparisons |
| infinisynapse-review | `tools_reviews` | Tools & Reviews |

### C. 详情页数据源

```
posts[i].source_folder → SEO/Blog/pillar3-ai-analyst-tools/{folder}/
```

### D. 排序

`sort_priority` 120→101，新文排在 Pillar 1 之前。Featured：`024`、`025`、`039`、`043`。

### E. 多语言

UI 西班牙语，**文章标题保持英文**（与现有 37 篇一致）。`hreflang` 已在 meta-tags 预留。

## 9. 与 Pillar 1 的关系

- Pillar 3 内链大量指向 Pillar 1（`ai-for-data-analysis`、`what-is-a-data-agent` 等）
- **024** 与旧独立包 `SEO/Blog/best-ai-tools-for-data-analysis/` 主题重叠——**以本集群 slug `best-ai-tools-for-data-analysis` 为准**，旧包勿重复上线
- 姊妹文章：`/blog/natural-language-to-sql`、`/blog/ai-excel-data-cleaning` 等

## 10. 正文插图（5 篇对比/评测）

以下文章除 Hero 外各有 **1 张正文信息图**，PNG 已生成（`build-visuals.py` + `render-all-images.sh`）：

| slug | 文件名 | CDN 路径 |
|---|---|---|
| `infinisynapse-vs-databricks-genie` | `lakehouse-decision-infinisynapse-vs-genie.png` | `/blog/assets/pillar3/infinisynapse-vs-databricks-genie/` |
| `julius-ai-vs-chatgpt` | `decision-flow-julius-vs-chatgpt.png` | `/blog/assets/pillar3/julius-ai-vs-chatgpt/` |
| `thoughtspot-vs-databricks-genie` | `decision-chart-thoughtspot-vs-genie.png` | `/blog/assets/pillar3/thoughtspot-vs-databricks-genie/` |
| `infinisynapse-vs-tableau` | `matrix-infinisynapse-vs-tableau.png` | `/blog/assets/pillar3/infinisynapse-vs-tableau/` |
| `infinisynapse-review` | `five-pillars-radar-infinisynapse.png` | `/blog/assets/pillar3/infinisynapse-review/` |

Hero + OG + 正文图：**25/25 PNG 就绪**（20 hero + 5 body）。

同步 `audit.md` 门禁字段：

```bash
python3 SEO/Blog/sync-audit-gates.py
```

## 11. 联系与变更

- 内容源：`SEO/Blog/pillar3-ai-analyst-tools/`
- 规划对照：`SEO/100页主题集群规划-v1-替换后主关键词版.md` § Pillar 3
- SEO 技能链：`Skills/seo-geo-claude-skills-main/`
- 改正文后同步 `schema.json` FAQ 与 `meta-tags.html`
