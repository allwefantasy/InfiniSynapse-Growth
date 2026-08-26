---
name: seo-blog-content
description: >-
  SEO/GEO 博客正文生产与质检规则（90 篇 pillar 集群）。当用户要求写/改/审
  SEO/Blog/pillar* 下的 article.md、检查外链引用、EEAT、关键词密度或发布门禁时使用。
---

# SEO Blog Content Skill

> 适用范围：`SEO/Blog/pillar1` … `pillar8` 下所有 `article.md`（及同批次 legacy 单篇博客若用户指定）。

## 硬规则 · 高 DR 权威引用（R02 升级版）

**每篇文章正文中必须包含 ≥5 条来自高 Domain Rating（DR ≥ 70）站点的唯一外链引用。**

### 什么叫「高 DR 站点」

以 Ahrefs DR 为参考（发布前用 `audit-external-links.py` 验证 HTTP 200）：

| 来源 ID | 锚文本示例 | URL | 约 DR |
|---------|-----------|-----|-------|
| `stanford-hai` | Stanford HAI AI Index | `https://hai.stanford.edu/ai-index` | 91 |
| `ibm-augmented` | IBM augmented analytics overview | `https://www.ibm.com/topics/augmented-analytics` | 92 |
| `nist-ai-rmf` | NIST AI Risk Management Framework | `https://www.nist.gov/itl/ai-risk-management-framework` | 88 |
| `ms-data-arch` | Microsoft data architecture guidance | `https://learn.microsoft.com/en-us/azure/architecture/data-guide/` | 96 |
| `owasp-llm` | OWASP Top 10 for LLM Applications | `https://owasp.org/www-project-top-10-for-large-language-model-applications/` | 84 |
| `google-cloud-ai` | Google Cloud AI overview | `https://cloud.google.com/discover/what-is-artificial-intelligence` | 93 |
| `aws-ml-lens` | AWS Well-Architected ML Lens | `https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/welcome.html` | 96 |
| `iso-27001` | ISO/IEC 27001 | `https://www.iso.org/isoiec-27001-information-security.html` | 90 |
| `wikipedia-dw` | Wikipedia data warehouse overview | `https://en.wikipedia.org/wiki/Data_warehouse` | 97 |
| `google-sre` | Google SRE book | `https://sre.google/sre-book/table-of-contents/` | 93 |
| `spider-bench` | Spider NL2SQL benchmark | `https://yale-lily.github.io/spider` | 75 |
| `bird-bench` | BIRD benchmark | `https://bird-bench.github.io/` | 72 |
| `databricks-genie` | Databricks Genie post | `https://www.databricks.com/blog/pushing-frontier-data-agents-genie` | 85 |
| `snowflake-cortex` | Snowflake Cortex Analyst | `https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst` | 82 |

完整清单与织入模板见 [`high-dr-authority-sources.py`](./high-dr-authority-sources.py)。

### 什么叫「合理嵌入」

**禁止：**

- `## Sources` / `## References` 独立外链列表（含文末裸 URL 列表，如 `NIST AI RMF: https://...`）
- 裸 URL 作锚文本（`[https://...](https://...)`）
- 独立一行只有链接（含 `**Product entry**:`）
- 外链仅出现在 `> **Evaluation basis**` 块、正文叙事段完全没有
- 外链集中在文末 `Production Debugging` / `Conclusion` 之后（须分布在正文前 85% 的章节里）

**必须：**

- 描述性锚文本（机构名 + 文档名）
- 链接出现在完整英文句子里（≥8 词或 blockquote 叙事段）
- 按章节主题分布：治理/安全 → NIST、OWASP、ISO；采用趋势 → Stanford、Google Cloud；架构/连接器 → Microsoft、AWS；NL2SQL → Spider、BIRD、Databricks

**示例（合格）：**

```markdown
Production rollouts should align access and review controls with the
[NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework),
especially when recurring queries touch live schemas.
```

### Pillar 推荐补充源（在基础三件套之外再选 2+）

| Pillar | 优先补充 |
|--------|---------|
| pillar1 范式 | OWASP、Google Cloud、ISO、Wikipedia |
| pillar3 工具对比 | OWASP、Google Cloud、ISO、AWS ML Lens |
| pillar4 连接器 | OWASP、Snowflake Cortex、AWS ML Lens、ISO |
| pillar5 NL2SQL | Spider、BIRD、Databricks Genie、OWASP |
| pillar6 Excel/CSV | Wikipedia、Google Cloud、OWASP、ISO |
| pillar7 角色/行业 | ISO、OWASP、Google Cloud、AWS ML Lens |
| pillar8 模板/术语 | Wikipedia、ISO、OWASP、Google SRE |

## 硬规则 · 外链重合度 ≤30%（跨篇）

90 篇集群内，**任意两篇文章**的外部链接 URL 集合，重合度不得超过 **30%**。

### 定义

- 外链集合 = 正文中所有非 `infinisynapse` 的 `https?://` 唯一 URL（与 `audit-external-links.py` 一致）
- 重合度 = `|A ∩ B| / min(|A|, |B|)`（按规范化 URL：去尾斜杠、小写）
- 阈值：**> 0.30 即 Fail**（例如两篇各 10 条外链时，共享 URL 不得超过 3 条）

### 生产要求

- 每篇目标 **10 条**唯一高 DR 外链（由 `fix-external-link-overlap.py` 从 `high-dr-authority-sources.py` 池贪心分配）
- 禁止 90 篇共用同一组「IBM + NIST + Stanford」模板而不换 URL
- 补链须用 `weave` 叙事句嵌入正文前 85%，不得堆在 FAQ 前

### 审计与批量修复

```bash
# 两两重合度审计（90 篇 → 4005 对；目标 0 violations）
python3 SEO/Blog/audit-external-link-overlap.py

# 贪心去重合 + 替换/织入外链（跑后须再跑 placement + high-dr 审计）
python3 SEO/Blog/fix-external-link-overlap.py
```

## 硬规则 · Target keyword 全文一致（禁止 `this workflow` 代词）

每篇 `article.md` 头部有 `**Target keyword**: \`...\`` 时，**全文叙事须使用该关键词或其自然变体**，不得在后半章用无搜索量的泛化代词顶替。

### 禁止

- 用 **`this workflow`** / **`this connector workflow`** 批量替换主关键词（常见于 Operating model、FAQ、Conclusion 前填充段）
- 前半章写 `airtable data analysis`、后半章突然改叫 `this workflow` 的**关键词断层**
- `fix-content-quality.py` 的 header 降噪把正文关键词改成 `this workflow`（应改为 `this approach` 或缩短标题，**不得**污染正文）
- FAQ 标题双问号：`deploy this workflow with Airtable??`

### 必须

- Operating model、FAQ、Conclusion 与正文前段**同一主关键词**（可交替数据源名 + 关键词，如 `Airtable` + `airtable data analysis`）
- 关键词过长（>48 字符）时，可用标题中的数据源短标签 + 意图词（如 `Snowflake connector analytics`），**不能**退回 `this workflow`
- 允许 1 处以内的泛指 `workflow`（非 `this workflow`），如 *how a workflow changed*

**示例（不合格）：**

```markdown
## Operating model inside InfiniSynapse
A production operating model for **this workflow** combines three loops:
...
### How long does it take to deploy this workflow with Airtable??
```

**示例（合格）：**

```markdown
## Operating model inside InfiniSynapse
A production operating model for **airtable data analysis** combines three loops:
...
### How long does it take to roll out airtable data analysis?
```

### 自动修复与审计

```bash
# Pillar4 批量把 this workflow 改回 Target keyword（默认 pillar4，可加路径）
python3 SEO/Blog/fix-this-workflow-placeholder.py

# 全文审计（>1 处 this workflow 即 Fail）
python3 SEO/Blog/audit-keyword-placeholder.py

# FAQ 损坏修复 + schema.json 同步 + 标题关键词降噪
python3 SEO/Blog/fix-faq-and-headers.py
```

`audit-content-quality.py` 已内置同一门禁（`this workflow` >1 处且已定义 Target keyword → Fail）。`fix-faq-and-headers.py` 会从 `schema.json` 或集群模板恢复损坏的 FAQ，并同步结构化数据。

## 硬规则 · Title & Description 必须含 Target keyword

### 铁律：不得修改 Target keyword

- 以集群规划表（如 `SEO/100页主题集群规划-v1-替换后主关键词版.md`）及每篇 `article.md` 头部 `**Target keyword**` 为准
- **禁止**为标题可读性、slug 原词或页面主题，替换 / 缩短 / 改写 Target keyword（含「改回更自然的连接词」）
- 标题、描述、正文只能在**不改关键词**的前提下，把该**完整短语**自然织入

每篇 `article.md` 头部 `**Target keyword**: \`...\`` 的**完整短语**（大小写不敏感、连续子串匹配）必须同时出现在 **标题** 与 **描述** 四处元数据里：

| 字段 | 位置 |
|------|------|
| **Title** | `article.md` H1（`# …`） |
| **Title** | `meta-tags.html` 的 `<title>`（并同步 `og:title`、`twitter:title`） |
| **Description** | `article.md` 的 `**Meta Description**:` |
| **Description** | `meta-tags.html` 的 `<meta name="description">`（并同步 `og:description`、`twitter:description`） |

`schema.json` 中 `BlogPosting.headline` / `description` 须与上述 H1、Meta Description **保持一致**。

### 匹配规则

- **完整短语**：`Target keyword` 作为**连续子串**出现（`best agentic analytics for data-driven insights` 不能拆成散落词）
- **大小写不敏感**：`SQL for Data Analysis` 可满足 `sql for data analysis`
- **禁止**为塞关键词而截断标题/描述导致短语被切断（修复脚本不得对含关键词的字符串做尾部硬截断）

### 标题/描述织入原则

- **标题**：优先将关键词置于 H1 前部（`{Keyword}: {原意标题}` 或词序重排，如 `Airtable Data Analysis: …`）
- **描述**：首句或前缀须含完整关键词；**总长须 150–160 字符**（On-Page 严格区间，见下「On-Page 发布合规」），且**不得以截断破坏关键词完整性**
- 对比/替代类长关键词（如 `agentic data plane hosted vs self-hosted comparison`）允许较长 H1，**关键词完整性优先于字数**

### 禁止

- H1 / `<title>` 仅有同义词或品牌词，**不含** Target keyword 完整短语
- Meta Description 仅写产品名或泛化文案（如只写 *Compare tools in 2026*）
- `article.md` 与 `meta-tags.html` / `schema.json` 三处标题或描述不一致

**示例（不合格）：**

```markdown
# How to Connect Supabase to an AI Data Analyst in 2026
**Target keyword**: `sql for data analysis`
**Meta Description**: Connect Supabase with governance checklist and FAQ.
```

（H1 与描述均未含 `sql for data analysis` 完整短语。）

**示例（合格）：**

```markdown
# SQL for Data Analysis: Connect Supabase to an AI Data Analyst (2026)
**Target keyword**: `sql for data analysis`
**Meta Description**: SQL for data analysis guide with setup checklist, security controls, example SQL, and FAQ for 2026 teams.
```

### 禁止堆砌（Title / Description）

- 关键词在 H1 与 Meta Description 中**各出现 1 次即可**（全文叙事另计）
- **禁止**描述模板：`Connect {源} to InfiniSynapse for {keyword} with setup checklist…`
- **禁止**描述模板：`Practical guide to {keyword} with pain points…`
- **禁止** H1 与 Meta Description **重复同一冒号前缀**（如 H1 与 desc 均以 `What Is a Data Agent:` 开头）
- 关键词过长（>48 字符）时：H1 可仅用 `{Keyword} (2026)`，副标题信息写入描述，**不得**在标题末尾硬截断关键词
- H1 建议 ≤90 字符；**Meta Description 须 150–160 字符**（见「On-Page 发布合规」），且不得以截断破坏关键词完整短语

### 自动修复与审计

```bash
# 批量织入 H1 / Meta Description，并同步 meta-tags.html + schema.json
python3 SEO/Blog/fix-keyword-in-title-desc.py

# 去堆砌：自然化标题/描述（不改 Target keyword）
python3 SEO/Blog/fix-keyword-meta-natural.py

# 发布门禁：90/90 Pass
python3 SEO/Blog/audit-keyword-in-title-desc.py
python3 SEO/Blog/audit-keyword-meta-stuffing.py
```

正文变更后须重跑 `build-preview.py`，避免 `preview.html` 残留旧 title/description。

## 硬规则 · On-Page / CMS 发布合规（5 项）

文章经 CMS（如 **QuickCreator**）或 headless 前端发布时，On-Page SEO 检查器对每页有 5 项硬要求。内容本身没问题，关键在「发布层」要把元数据接对、并保证页面**只有 1 个 H1**。

### 两层模型（务必区分，否则会把作者门禁搞挂）

| 层 | 位置 | H1 | 谁负责 |
|----|------|----|--------|
| **作者层（源）** | `SEO/Blog/pillar*/article.md` | **有且仅 1 个 H1** | outline / keyword-in-title 门禁依赖它，**不要删** |
| **发布层（交付）** | `frontend-handoff/content/**/article.md`（body-only）+ `head.html` + `seo-meta.json` | **body 无 H1**，页面 `<h1>` 由标题渲染 | 由 `build-frontend-handoff.py` 复制时自动去 H1 |

### 5 项要求

| # | 要求 | 落点 |
|---|------|------|
| 1 | **Canonical** 必有、无尾斜杠 | `https://infinisynapse.com/en/blog/{slug}`（英文）；`https://infinisynapse.com/zh/blog/{slug}`（hreflang zh-CN） |
| 2 | 页面**有且仅 1 个 H1**；H1 由标题（meta `<title>` / `seo-meta.json` title）渲染，发布 body **无 H1**；**禁止**「平台标题 H1 + 正文 H1」双 H1 | 发布层 `article.md` |
| 3 | **Meta 描述 150–160 字符**（严格）；扩写须**完整句、不得截断成残句、跨篇不得重复** | `article.md` `**Meta Description**` + `meta-tags.html`(description/og/twitter) + `schema.json` + `head.html` 五处同步 |
| 4 | **社交标签齐全**：`og:type/url/title/description/image(+width/height/alt)/site_name` + `twitter:card/title/description/image` | `meta-tags.html` / `head.html` / `seo-meta.json` |
| 5 | **Meta `<title>` 40–60 字符**且含完整关键词 | `fix-meta-title-length.py` 改 `<title>` + `og:title` + `twitter:title`；H1 与 `schema.headline` 保持完整（可较长） |

### 标题长度（第 5 项）细则

- `<title>`（SEO 标题）与 H1（展示标题）**可不同**：`<title>` 40–60，H1 可保留完整关键词与副标题。
- `<title>` 仍须含**完整关键词**（满足 `audit-keyword-in-title-desc.py`）。
- **例外**：关键词本身 >58 字符（如 `data integration platforms supporting snowflake bigquery redshift`）时，保留完整关键词、接受 `<title>` >60（QC 为黄色警告，非红色错误；关键词完整性优先）。
- 修复脚本按 `content_type` 选副标题（versus→Comparison、listicle→Top Tools、how-to→Setup Guide、glossary→Key Terms…），**禁止**在虚词（for/and/the…）处截断。

### ⚠️ 部署注入是合规前提（实测教训）

源文件正确 ≠ 线上合规。实测线上页面**只注入了 `<title>` + `ld+json`**，缺失 `canonical` / `og:*` / `twitter:*`，且 `description` 退回**站点默认**。

- canonical / description / og / twitter 必须由部署代码**逐页注入** `head.html`（或 `seo-meta.json` 字段）。
- 验证用 `curl` 抓线上原始 HTML（不是渲染文本）确认 `<head>` 是否含这些标签。

### 程序员直接可用的产物

- **`<article>/head.html`**：去注释的 `<head>` 片段 + JSON-LD，直接注入页面 `<head>`
- **`seo-meta.json`**：按 slug 的全部 SEO 字段，程序化注入（Next.js `generateMetadata` / SSR / CMS API）
- 装配规则：**页面 `<h1>` 用标题渲染（1 个）→ head.html 注入 `<head>` → body 渲染 article.md（无 H1）**

### 脚本

```bash
cd SEO/Blog
# 修复
python3 fix-production-urls.py           # 域名 .com + /en/blog/ 路径（幂等）
python3 fix-meta-descriptions.py          # 描述归一化到 150–160（幂等；同步 md/meta/schema）
python3 generate-deploy-meta.py           # 每篇 head.html + 合并 seo-meta.json
python3 build-frontend-handoff.py         # 交付包：复制时 body 去 H1 + 带 head.html/seo-meta.json
python3 strip-leading-h1.py [deploy_dir]  # 只对交付副本去 H1（默认 frontend-handoff/content）

# 审计
python3 fix-meta-title-length.py          # <title> 改 40–60 含关键词（不动 H1/schema）
python3 build-sitemap.py                   # 合并老 URL + 100 篇新博客 → sitemap.xml

# 审计
python3 audit-quickcreator-onpage.py      # 发布层 5 项（默认审计 frontend-handoff/content；H1 须 0）
python3 audit-outline-structure.py        # 作者层：源 article.md H1 须 1
```

### 禁止

- **直接对源 `article.md` 删 H1**（会让 `audit-outline-structure.py` / `audit-keyword-in-title-desc.py` 全挂）→ 去 H1 只在发布层做
- Meta 描述 <150 或 >160；用残句（如 `It adds.` / `a real example,.`）或跨篇重复句凑长度
- 把 `meta-tags.html` 顶部注释块、`preview.html` 当正文上线
- 改 `canonical` / `og:url` 的域名或路径

### 验收（抽 5 篇）

- 页面 `document.querySelectorAll('h1').length === 1`
- `<head>` 有 `canonical`（无尾斜杠）、`description` 150–160、`og:*` + `twitter:*`、`<script type="application/ld+json">`（含 FAQPage）
- `<title>` 40–60 字符（长关键词例外见上）

## 硬规则 · Sitemap（站点地图）

新增/更新文章后，须重生成完整 `sitemap.xml` 交付程序员，**整体替换**线上 `https://infinisynapse.com/sitemap.xml`（不是只给新博客的子地图）。

### 规则

| 规则 | 说明 |
|---|---|
| **URL = canonical** | 博客用 `https://infinisynapse.com/en/blog/{slug}`，与 head `canonical` 完全一致（完整域名、含 `/en/`、无尾斜杠） |
| **保留存量 URL** | 现有非博客 URL（`use-cases/*`、`guides/*` 等）**原样保留** `lastmod`/`changefreq`/`priority`，禁止丢失或改写 |
| **lastmod** | 博客取自各文 `schema.json` `dateModified`；老页沿用原值 |
| **priority** | Hub/Pillar 0.9，普通博客 0.7；老页沿用原值 |
| **changefreq** | 博客 `weekly`；老页沿用原值 |
| **仅收录 200 页** | 只放已上线、可 200 访问的 URL（对照 `部署清单-完整URL.csv`）；**`/zh/blog/` 中文页未上线则不收录**，避免 GSC「已提交未找到」 |
| **robots.txt** | 含 `Sitemap: https://infinisynapse.com/sitemap.xml` |
| **协议** | sitemaps.org 0.9；生成后 XML 须可解析（脚本自带 `xml.dom.minidom` 校验） |

### 脚本

```bash
python3 SEO/Blog/build-sitemap.py   # 老 URL(EXISTING 常量) + /en/blog 列表页 + 100 篇博客 → sitemap.xml
```

- 存量 URL 内嵌在脚本 `EXISTING` 常量；站点新增非博客栏目时同步维护该常量。
- 数据源 `seo-meta.json`（canonical + schema 日期），保证与 head 一致。
- 生成后：GSC → Sitemaps → 重新提交 `sitemap.xml`。

### 禁止

- 用相对路径或 `.cn` 旧域名做 `<loc>`（必须完整 `https://infinisynapse.com/...`）
- 漏掉存量 `use-cases/*`、`guides/*`（会导致老页从地图消失、收录回退）
- 收录尚未上线/会 404 的 URL（含未发布的中文页）

## 硬规则 · 大纲结构（Outline / Heading Hierarchy）

每篇 `article.md` 正文须满足以下**标题层级门禁**（审计脚本统计 H1–H4，跳过代码块内 `#`）：

### 数量

| 层级 | 要求 |
|------|------|
| **H1** | **有且仅有 1 个**（文章标题；不得在中途再出现 H1） |
| **H2 + H3 + H4** | **合计 20–30 个**（不含 H1；即全文标题总数为 **21–31**） |
| **H4** | 可选；若使用，必须挂在 H3 下 |

> 说明：旧口径「总标题 15–20」已废止；以 **1×H1 + 20–30×(H2/H3/H4)** 为准，保证每篇有足够章节深度又不堆砌碎片化小标题。

### 层级与段落

- **每个逻辑章节必须有 H2**：正文不得出现「无 H2 归属」的长段落块（TL;DR、Key Definition、FAQ、Conclusion 等均为独立 H2 章节）
- **H3 只能出现在某个 H2 之下**；**H4 只能出现在某个 H3 之下**（禁止跳级）
- **H3 用于拆分**：步骤、FAQ 单问、评分维度等；不必每个 H2 都有 H3，但有的 H3 必须归属明确的父 H2
- **禁止**为凑数重复 filler H2（如成对的 `Operational Readiness Notes` / `Production Debugging Notes`）
- **禁止**在同一 H2 下用大量并列 `###` 充当列表（应改为 `**小标题**` + 正文或表格）

### 推荐骨架（Cluster Page 参考）

```
# H1 标题（唯一）
## Table of Contents
## TL;DR
## Key Definition / 背景
## 核心章节 × N（每节 ##）
### 可选子节（步骤 / FAQ 问项）
## Frequently Asked Questions
## Conclusion
```

### 自动审计与修复

```bash
# 发布门禁：90/90 Pass
python3 SEO/Blog/audit-outline-structure.py

# 批量补齐/压缩 H2–H4（跑后检查 TOC 与 preview 锚点）
python3 SEO/Blog/fix-outline-structure.py
```

正文结构变更后须重跑 `build-preview.py`（预览页须为 H2/H3 生成与 TOC 一致的 `id`）。

## 硬规则 · 正文数据图 ≥2 维度

`images/chart-*.png`（及同类 matplotlib / 数据插图）**必须编码至少 2 个数据维度**。

- **禁止**：仅 Before/After 两根柱、单指标一维对比；单系列折线无对照。
- **要求**：分组柱（类别 × 阶段）、多系列折线（时间 × 系列）、堆叠构成、散点 XY 等。
- **标注**：标题/alt 含 illustrative；alt 写明图表类型与两个维度。
- **插入**：优先紧跟 `**Practical example:**`；与 scorecard 表格分工，勿用装饰性空表 PNG。

完整细则与 Hero 分层：[`body-data-chart-rules.md`](./body-data-chart-rules.md)。脚本：`scripts/gen-data-charts-p26-30.py`。

## 硬规则 · 主题集群内链（Pillar / Cluster）

每篇 `article.md` 须先确定**页面性质**（见 [`cluster-link-registry.py`](./cluster-link-registry.py)），再按角色织入内链。内链与外链一样：**写在正文叙事句里**，不得堆在文末。

### 双向索引（图书馆模型 · 必须满足）

把一个主题集群当成图书馆：**Pillar = 总目录，Cluster = 分章节的书，两者之间必须有明确的双向索引。** 缺任一方向都视为集群断链。

> **单一支柱优先（默认规则）**：每个 Pillar **应只有 1 篇支柱文章（单 Hub）**，由它内链该集群全部 Cluster。除非集群极大且主题确需拆分，否则不要设多 Hub——多 Hub 会让"哪篇索引全部 Cluster"含糊、覆盖被摊薄（Pillar 1 曾用 4 Hub，结果无单篇全覆盖，已收敛为单 Hub 001）。`cluster-link-registry.py` 的 `PILLAR_PAGE_FOLDERS` 每个 pillar 只列 1 个文件夹。

> **Hub 即 Pillar 落地页（部署硬规则）**：Pillar 的**落地页 URL = Hub 长文** `https://infinisynapse.com/en/blog/{hub-slug}`（见 `hub-landing-pages-master.json`）。**禁止**另建 `/en/blog/pillar/{slug}` 索引页；若已上线须 **301** 到 Hub（见 `hub-landing-handoff-pack/redirect-deprecated-pillar-routes.csv`）。博客列表/分类「查看全部」须链到 Hub URL，而非 /pillar/*。

> **Hub 正文 = 终极指南（Ultimate Guide）**：每篇 Hub 须是一篇**完整、自成体系、高信息密度**的长文（类比《项目管理终极指南》）——含定义、核心框架、方法论对比（内链→Cluster）、工具/方案 landscape、实施路径、案例、Scorecard、失败模式、FAQ 与 Cluster 索引表。**禁止**仅用 `cluster-articles.json` 卡片网格替代正文。框架见 [`pillar-hub-ultimate-guide-framework.md`](./pillar-hub-ultimate-guide-framework.md)；自检表 `SEO/Blog/pillar-hub-section-checklist.csv`（`generate-pillar-hub-checklist.py`）。

1. **Pillar → 链到所有 Cluster**（向下索引）
   - 单 Hub 集群（P3–P10）的 Pillar Page **必须**链到该集群**每一篇** Cluster Page。
   - 在 Pillar 正文里**提到对应细分话题的那一段**，自然地把该话题词作锚文本链到对应 Cluster 文章（不是文末罗列）。
   - **加入新 Cluster 文章时**：必须回到 Pillar 文章，在相关段落补 1 句指向新文的链接（这是加新文唯一强制要改的老文）。

2. **每篇 Cluster → 链回 Pillar**（向上索引）
   - 每篇 Cluster Page **必须**在正文合适处（定义段 / 背景段 / 实施段）引导读者回到 Pillar Page 看概览，用描述性锚文本叙事嵌入。
   - 同时链 **≥2 篇同集群兄弟 Cluster**（横向索引）。

3. **URL 格式**：内链统一用 `/en/blog/{slug}`（与 canonical 一致）。审计 `audit-internal-links.py` 已识别 `/blog/`、`/en/blog/`、`/zh/blog/` 前缀；写链接时用 `/en/blog/`。

4. **Cluster guides 表格与锚文本（禁止部署序号）**
   - Pillar Hub 上的 `## Cluster guides in this pillar` 表格：**Focus** 列与 **Guide** 列链接锚文本均使用文章标题，**不得**前缀部署序号（`001`、`002` …）。
   - 正文内链锚文本同理：禁止 `[002 Data Agent Manifesto](/en/blog/...)`；应使用 `blog-index-import-master.json` 中的正式标题或语境合适的短标题，但**不含**三位数字前缀。
   - 序号仅用于文件夹命名（`002-data-agent-manifesto`）与 CMS 导入排序，**不出现在**读者可见文案、表格或链接锚文本。
   - 修复脚本：`python3 SEO/Blog/fix-cluster-guide-ids.py`（同步 Hub 表格 + 清除 `[NNN …]` 锚文本）。

> 审计口径见 `audit-internal-links.py`：Pillar Page 校验「链满全部 Cluster + 其它 Pillar Page」；Cluster Page 校验「链回 primary hub + ≥2 兄弟」。两者皆过才算集群闭环。

### 禁止（负例）

- `## Related Reading` / `## Conclusion + Related Reading` 独立章节
- 文末重复模板 bullet：`For related workflow depth, see [Title](/blog/...).`（每条相同开头）
- **集群内链罗列段**：`Within this topic cluster, explore [A], [B], [C], and [D] when you extend this workflow across the cluster.`（一句多链、固定开头）
- `**Pillar N cluster — read next**:` 列表块
- `## Internal Link Recommendations` 表格
- **同一段落内 3+ 条 `/blog/` 内链**（视为列表，非叙事嵌入）

### 页面性质与最低内链要求

| 性质 | 判定 | 必须内链 |
|------|------|----------|
| **Pillar Page** | 集群 hub，见下表 | 同集群内**所有其他 Pillar Page**；单 hub 集群（P3–P8）的 hub 还须覆盖该集群**全部 Cluster Page** |
| **Cluster Page** | 同文件夹下非 hub 的 `00x-*/article.md` | **Primary hub（Pillar Page）** + **≥2 篇**同集群 Cluster Page（从集群内链集合中按上下文合理选取） |

**各集群 Pillar Page（hub）文件夹：**

| 集群 | Pillar Page |
|------|-------------|
| pillar1 | `001-ai-for-data-analysis`, `004-ai-native-data-platform`, `007-ai-data-analyst`, `012-ai-data-analysis` |
| pillar3 | `024-best-ai-tools-for-data-analysis` |
| pillar4 | `044-connect-supabase-to-ai-data-analyst` |
| pillar5 | `059-natural-language-to-sql` |
| pillar6 | `069-clean-excel-data-with-ai` |
| pillar7 | `081-ai-tools-for-data-analysts` |
| pillar8 | `100-data-agent-faq` |

### 什么叫「合理嵌入」

- **每次只嵌 1 条内链**，写进与当前段落主题相关的完整英文句（定义段、实施步骤、治理段、FAQ 答案等**正文中段**）
- 描述性锚文本；链接须服务该段论述，而非「顺带点名」同集群其他文章
- 同一 slug 可出现多次，但质检以 slug 是否出现在正文为准
- 跨集群互链允许作补充，**不能替代**上述集群内最低要求

**示例（合格）：**

```markdown
As organizations add warehouse and lakehouse systems, connector scope should stay explicit;
analysts wiring Snowflake into the same review gates can follow
[How to Connect Snowflake to an AI Data Analyst in 2026](/blog/connect-snowflake-to-ai-analyst)
for credential templates and validation SQL.
```

**示例（不合格 · 列表段）：**

```markdown
Within this topic cluster, explore [PostgreSQL guide](/blog/connect-postgres-to-ai-data-analyst),
[MySQL guide](/blog/connect-mysql-to-ai-data-analyst), and [Snowflake guide](/blog/connect-snowflake-to-ai-analyst)
when you extend this workflow across the cluster.
```

**示例（不合格 · Related Reading）：**

```markdown
## Related Reading

- For related workflow depth, see [What Is a Data Agent?](/blog/what-is-a-data-agent).
```

### 自动修复与审计

```bash
# 删除 Related Reading 块，将缺失内链织入正文
python3 SEO/Blog/fix-internal-links.py

# 按 Pillar / Cluster 规则审计（90/90 为发布门禁）
python3 SEO/Blog/audit-internal-links.py
```

## 质检命令（发布前必跑）

```bash
# 主关键词：禁止 this workflow 代词顶替 Target keyword
python3 SEO/Blog/audit-keyword-placeholder.py

# Title & Description：Target keyword 完整短语须出现在 H1 + meta title + 两处 description
python3 SEO/Blog/audit-keyword-in-title-desc.py
python3 SEO/Blog/audit-keyword-meta-stuffing.py

# 大纲：1×H1；H2+H3+H4 合计 20–30；层级不跳级
python3 SEO/Blog/audit-outline-structure.py

# 内链：禁止 Related Reading；Pillar/Cluster 最低覆盖
python3 SEO/Blog/audit-internal-links.py

# 外链位置：禁止文末 Sources 块、须分布在正文章节
python3 SEO/Blog/audit-link-placement.py

# 高 DR 引用 ≥5 + 叙事嵌入
python3 SEO/Blog/audit-high-dr-links.py

# 跨篇外链重合度 ≤30%
python3 SEO/Blog/audit-external-link-overlap.py

# 外链 HTTP 200 + 数量 ≥5
python3 SEO/Blog/audit-external-links.py

# EEAT / 关键词 / 字数
python3 SEO/Blog/audit-content-quality.py
python3 SEO/Blog/audit-wordcount.py
python3 SEO/Blog/audit-eeat.py

# 批量补齐缺失引用（慎用，跑后需人工读一遍流畅度）
python3 SEO/Blog/patch-high-dr-citations.py
```

**正文变更后须重生成预览**（避免 `preview.html` 残留旧版 `## Related Reading` / `## Sources`）：

```bash
python3 SEO/Blog/pillarN-.../build-preview.py
```

**通过标准：** `audit-keyword-placeholder.py`、`audit-keyword-in-title-desc.py`、`audit-keyword-meta-stuffing.py`、`audit-outline-structure.py`、`audit-internal-links.py`、`audit-link-placement.py`、`audit-high-dr-links.py`、`audit-external-link-overlap.py`、`audit-external-links.py` 均为 90/90 Pass（外链重合度为 **0 violations / 4005 pairs**）。

## 与其他规则的关系

- Pillar Page 另需 2000–2500 词 + 1.2%–1.7% 关键词密度（Cluster Page 见各 pillar `DEPLOY.md`）
- 产品入口写 `[InfiniSynapse web app](https://app.infinisynapse.cn)`，禁止裸域名锚文本
