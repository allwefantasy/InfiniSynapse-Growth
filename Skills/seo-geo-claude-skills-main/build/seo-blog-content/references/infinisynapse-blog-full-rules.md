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
- **描述**：首句或前缀须含完整关键词；总长建议 ≤165 字符，但**不得以截断破坏关键词完整性**
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
- H1 建议 ≤90 字符；Meta Description ≤165 字符，且不得以截断破坏关键词完整短语

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

## 硬规则 · 主题集群内链（Pillar / Cluster）

每篇 `article.md` 须先确定**页面性质**（见 [`cluster-link-registry.py`](./cluster-link-registry.py)），再按角色织入内链。内链与外链一样：**写在正文叙事句里**，不得堆在文末。

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
