# `infinisynapse.com/use-cases/` SEO & GEO 优化执行手册

| 字段 | 值 |
|---|---|
| 审计目标 URL | https://infinisynapse.com/use-cases/index.html |
| 审计日期 | 2026-05-13 |
| 审计框架 | CORE-EEAT 80 项 + CITE 40 项（seo-geo-claude-skills v9.9.5） |
| 使用 Skill | `on-page-seo-auditor` / `meta-tags-optimizer` / `schema-markup-generator` / `geo-content-optimizer` / `technical-seo-checker` |
| 当前综合分 | **5.0 / 10（C 级）** |
| 目标综合分 | **≥ 8.0 / 10（B+ 级）** |
| 预计总工时 | **3.5 ~ 5 小时**（不含文章页内链补全） |

---

## 0. 修复前状态快照（Baseline）

| 维度 | 现状 | 分数 |
|---|---|---|
| Title | 74 字符（>60），未含主词 `data analysis` | 6/10 |
| Meta Description | 139 字符，无 CTA，无年份 | 6.5/10 |
| H1 | `InfiniSynapse Resources`，零关键词 | 4/10 |
| H2 × 5 | **全部是 slug** （`sql-data-analysis-with-ai` 等） | 2/10 |
| 卡片摘要 | 5 张全部以 `...` 截断 | 3/10 |
| 结构化数据 | **无任何 JSON-LD** | 0/10 |
| OG / Twitter Card | **完全缺失** | 0/10 |
| Canonical / Favicon / robots | 全部缺失 | 2/10 |
| 数据自洽性 | "5 Guides / 5 Topics" 不一致 → 触发 R10 veto | Warn |
| 内链 | 仅 hub→article 单向，无面包屑、无回链 | 4/10 |
| E-E-A-T 信号 | 无作者、无更新日期、无 About | 3/10 |

---

## 1. 执行总览

| 阶段 | Skill | 工时 | 优先级 |
|---|---|---|---|
| Step 1 | `meta-tags-optimizer` — 改 title/description/OG/Twitter | 30 min | **P0** |
| Step 2 | `on-page-seo-auditor` — 重写 H1 / 合并 H2 / 修数据 | 60 min | **P0** |
| Step 3 | `schema-markup-generator` — 加 3 段 JSON-LD | 30 min | **P1** |
| Step 4 | `geo-content-optimizer` — Hero 定义段 + 簇导语 + FAQ | 90 min | **P1** |
| Step 5 | `technical-seo-checker` — canonical / robots / preconnect / 301 | 30 min | **P1** |
| Step 6 | `internal-linking-optimizer` — 文章互链 + 面包屑 | 60 min | **P2** |
| Step 7 | 验收 & 提交 | 30 min | — |

---

## 2. Step 1 — Meta & Head（P0｜30 min）

### 2.1 修改 `<title>`

**改前**

```html
<title>InfiniSynapse Resources — AI Data Analyst Guides for Enterprise Teams</title>
```

**改后（任选其一，均 ≤66 字符）**

```html
<title>Data Analysis Guides for 2026 — SQL, Excel, AI Tools | InfiniSynapse</title>
```

> 备选：`AI Data Analyst Guides: SQL, Excel & BI Tutorials | InfiniSynapse`

验收：长度 ≤ 60 ~ 65 字符，包含主词 `data analysis` + 年份 `2026` + 品牌 `InfiniSynapse`。

### 2.2 修改 `<meta name="description">`

**改后**

```html
<meta name="description" content="Practitioner guides on SQL, NL2SQL, Excel, BI software, and AI data analysts for enterprise teams — updated for 2026. By InfiniSynapse.">
```

验收：≤ 160 字符 / 含 CTA / 含年份。

### 2.3 新增 OG + Twitter Card + canonical + robots + favicon

在 `<head>` 中追加：

```html
<link rel="canonical" href="https://infinisynapse.com/use-cases/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="author" content="InfiniSynapse">

<meta property="og:type" content="website">
<meta property="og:site_name" content="InfiniSynapse">
<meta property="og:title" content="Data Analysis Guides for 2026 — InfiniSynapse Resources">
<meta property="og:description" content="SQL, Excel, and AI tools for enterprise data analysis. Updated 2026.">
<meta property="og:url" content="https://infinisynapse.com/use-cases/">
<meta property="og:image" content="https://infinisynapse.com/og/use-cases.png">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Data Analysis Guides for 2026">
<meta name="twitter:description" content="SQL, Excel, and AI tools for enterprise data analysis.">
<meta name="twitter:image" content="https://infinisynapse.com/og/use-cases.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="alternate" hreflang="en" href="https://infinisynapse.com/use-cases/">
<link rel="alternate" hreflang="x-default" href="https://infinisynapse.com/use-cases/">
```

附属任务：设计一张 `1200×630` 的 OG 图，命名 `og/use-cases.png`。

---

## 3. Step 2 — 结构与文案（P0｜60 min）

### 3.1 改 H1（加主关键词）

**改前**

```html
<h1>InfiniSynapse <em>Resources</em></h1>
```

**改后**

```html
<h1>Data Analysis Guides <em>for Enterprise Teams</em></h1>
<p class="subtitle">InfiniSynapse Resources · Updated May 2026</p>
```

### 3.2 把 5 个 slug-H2 合并为 3 个话题簇

**改前**：5 个 H2 全是 slug，每簇只有 1 篇文章。

**改后**：3 个有 SEO 含义的话题簇

| 新 H2 | 包含文章 |
|---|---|
| **SQL & Natural Language Data Analysis** | `sql-data-analysis-with-ai` |
| **Spreadsheet & Methodology** | `how-to-add-data-analysis-in-excel` · `data-analysis-techniques` |
| **Tools & Software Buyer Guides (2026)** | `best-data-analysis-software` · `best-ai-tools-for-data-analysis` |

每个簇下加 1 句导语（30~50 词），举例：

```html
<section class="idx-section">
  <h2>SQL &amp; Natural Language Data Analysis</h2>
  <p class="cluster-lede">
    How modern NL2SQL agents translate plain-English questions into validated
    SQL across warehouses — covering schema linking, query review, and audit
    trails for enterprise analytics teams.
  </p>
  <div class="card-grid"> ... </div>
</section>
```

### 3.3 修复"5 Guides / 5 Topics"数据不一致（CORE-EEAT R10 veto）

**改前**

```html
<div><div class="stat-num">5</div><div class="stat-label">Topics</div></div>
```

**改后**

```html
<div><div class="stat-num">5</div><div class="stat-label">Guides</div></div>
<div><div class="stat-num">3</div><div class="stat-label">Topics</div></div>
<div><div class="stat-num">40+</div><div class="stat-label">Connectors</div></div>
```

### 3.4 卡片摘要不再用 `...`，写完整 25–50 词

**改前**

```html
<div class="page-card-meta">A practical guide to modern data analysis using SQL, the AI agents that now generate, validate, and run queries on your ...</div>
```

**改后（5 张卡片全部重写为可被 AI 引用的"独立句"）**

| 文章 | 新卡片描述（≤ 50 词） |
|---|---|
| SQL Data Analysis with AI | "Explains how NL2SQL agents translate plain-English questions into validated SQL across warehouses, run them safely, and return chart-ready answers in under 10 seconds — with schema linking, query review, and audit logs." |
| How to Add Data Analysis in Excel | "Step-by-step tutorial on enabling the Analysis ToolPak in Excel 2026, plus an honest comparison of when to graduate from Excel to a multi-source AI data analyst." |
| Data Analysis Techniques | "A complete reference of descriptive, diagnostic, predictive, and prescriptive methods — with worked examples and the modern AI-assisted workflow that replaces each." |
| Best Data Analysis Software | "Eight leading platforms ranked across data analysis and reporting, AI features, multi-source connectivity, governance, and scale — refreshed for 2026 enterprise buyers." |
| Best AI Tools for Data Analysis | "Practitioner's guide to AI agents, NL2SQL utilities, and full AI data analysts — with a decision framework matched to your data stack, team size, and security needs." |

### 3.5 删除卡片里的 slug 文字 `page-card-cat`

`<div class="page-card-cat">sql-data-analysis-with-ai</div>` → 删除整行。slug 重复展示对 SEO 与 UX 都是噪声。

### 3.6 删除 H2 旁边的 `1` 计数 badge

`<span class="cat-count">1</span>` 在簇合并后会改为 1/2/2，要么显示真实值，要么直接删除。建议直接删除（信息量低）。

---

## 4. Step 3 — JSON-LD 结构化数据（P1｜30 min）

在 `</body>` 前追加 3 段 JSON-LD：

### 4.1 CollectionPage + hasPart

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "InfiniSynapse Resources",
  "url": "https://infinisynapse.com/use-cases/",
  "description": "Practitioner guides on SQL, Excel, BI software, and AI data analysts for enterprise teams.",
  "isPartOf": { "@type": "WebSite", "name": "InfiniSynapse", "url": "https://infinisynapse.com" },
  "about": ["data analysis","AI data analyst","NL2SQL","business intelligence","enterprise AI"],
  "dateModified": "2026-05-13",
  "hasPart": [
    {"@type":"Article","headline":"SQL Data Analysis with AI","url":"https://infinisynapse.com/use-cases/sql-data-analysis-with-ai/"},
    {"@type":"Article","headline":"How to Add Data Analysis in Excel","url":"https://infinisynapse.com/use-cases/how-to-add-data-analysis-in-excel/"},
    {"@type":"Article","headline":"Data Analysis Techniques","url":"https://infinisynapse.com/use-cases/data-analysis-techniques/"},
    {"@type":"Article","headline":"Best Data Analysis Software 2026","url":"https://infinisynapse.com/use-cases/best-data-analysis-software/"},
    {"@type":"Article","headline":"Best AI Tools for Data Analysis 2026","url":"https://infinisynapse.com/use-cases/best-ai-tools-for-data-analysis/"}
  ]
}
</script>
```

### 4.2 BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"BreadcrumbList",
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://infinisynapse.com/"},
    {"@type":"ListItem","position":2,"name":"Resources","item":"https://infinisynapse.com/use-cases/"}
  ]
}
</script>
```

### 4.3 Organization

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Organization",
  "name":"InfiniSynapse",
  "url":"https://infinisynapse.com",
  "logo":"https://infinisynapse.com/logo.png",
  "sameAs":[
    "https://x.com/infinisynapse",
    "https://www.linkedin.com/company/infinisynapse"
  ]
}
</script>
```

**验收**：把改后页面贴进 https://search.google.com/test/rich-results 三段全部解析通过。

---

## 5. Step 4 — GEO 内容优化（P1｜90 min）

> 目标：让 ChatGPT / Perplexity / Google AI Overview 拿到「可整段引用」的句子。

### 5.1 Hero 下方新增"独立定义段"（25~50 词，self-contained）

```html
<p class="lede">
  <strong>InfiniSynapse Resources</strong> is a curated library of guides on
  natural-language data analysis, NL2SQL, multi-source federation, and AI data
  analyst deployment — written for analytics, data, and BI teams at enterprises
  evaluating AI-native data tools in 2026.
</p>
```

CORE-EEAT 命中项：C02（清晰定义）、O03（可引用句）、O05（结构清晰）、E01（实体一致）。

### 5.2 页面底部新增 FAQ Section（同步 FAQPage schema）

```html
<section class="faq">
  <h2>FAQ</h2>
  <details>
    <summary>What is an AI data analyst?</summary>
    <p>An AI data analyst is an agent that connects to your databases, files, and BI tools, then translates natural-language questions into validated SQL or Python — running them, returning chart-ready answers, and citing the source rows used.</p>
  </details>
  <details>
    <summary>Is NL2SQL accurate enough for production analytics?</summary>
    <p>Modern NL2SQL with schema linking and query review reaches 90%+ executable accuracy on enterprise schemas. Production-grade systems add row-level permissions, audit logs, and human-in-the-loop validation for high-risk queries.</p>
  </details>
  <details>
    <summary>Can InfiniSynapse run on-prem?</summary>
    <p>Yes. InfiniSynapse supports on-prem and VPC deployment with 40+ data connectors, so data never leaves the customer environment.</p>
  </details>
</section>
```

```html
<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[
    {"@type":"Question","name":"What is an AI data analyst?","acceptedAnswer":{"@type":"Answer","text":"An AI data analyst is an agent that connects to databases, files, and BI tools, then translates natural-language questions into validated SQL or Python."}},
    {"@type":"Question","name":"Is NL2SQL accurate enough for production analytics?","acceptedAnswer":{"@type":"Answer","text":"Modern NL2SQL with schema linking and query review reaches 90%+ executable accuracy on enterprise schemas."}},
    {"@type":"Question","name":"Can InfiniSynapse run on-prem?","acceptedAnswer":{"@type":"Answer","text":"Yes. InfiniSynapse supports on-prem and VPC deployment with 40+ data connectors."}}
  ]
}
</script>
```

> **重要**：FAQPage schema 内容必须与 DOM 中文字 **逐字一致**（CORE-EEAT R10）。

### 5.3 Footer 增加 About + 更新日期（E-E-A-T）

```html
<footer>
  <div class="container">
    <p class="about"><strong>About InfiniSynapse:</strong> InfiniSynapse builds the AI data analyst platform for enterprise teams — natural-language querying across 40+ data sources, with on-prem and multi-modal support.</p>
    <p>Last updated: <time datetime="2026-05-13">May 13, 2026</time></p>
    <p>&copy; 2026 <a href="https://infinisynapse.com">InfiniSynapse</a>. All rights reserved.</p>
  </div>
</footer>
```

---

## 6. Step 5 — 技术 SEO（P1｜30 min）

### 6.1 URL 规范化

服务端配置：`/use-cases/index.html` → 301 → `/use-cases/`
（或确保 canonical 已经指向无 `index.html` 版本，见 Step 1）

### 6.2 面包屑（DOM）

`<nav>` 下方追加：

```html
<nav aria-label="Breadcrumb" class="crumb">
  <a href="https://infinisynapse.com/">Home</a>
  <span aria-hidden="true">›</span>
  <span aria-current="page">Resources</span>
</nav>
```

### 6.3 性能

- 字体改 `font-display: swap`；或自托管 Inter 子集，去掉 Google Fonts 外链。
- 已加 `preconnect`（Step 1）。
- 验证 Lighthouse Performance ≥ 90。

### 6.4 sitemap & robots

- `/sitemap.xml` 必须包含 `/use-cases/` 及全部 5 篇子文章。
- `/robots.txt` 引用 sitemap：`Sitemap: https://infinisynapse.com/sitemap.xml`

---

## 7. Step 6 — 内链与互引（P2｜60 min）

| 任务 | 位置 | 说明 |
|---|---|---|
| 文章面包屑 | 每篇文章顶部 | `Home › Resources › <文章标题>` |
| 同簇互链 | 每篇文章底部 | "Related guides in this cluster" 列出同簇其余 1–2 篇 |
| 跨簇关联 | 文章正文 | 每篇至少 2 条出站到 Hub 内其他文章 |
| Hub → 产品页 | Hero CTA | `Get Started` 已存在，建议再加一条 `See pricing` |

---

## 8. 验收清单（Step 7｜30 min）

| 检查项 | 工具 | 通过标准 |
|---|---|---|
| Title 长度 | view-source 手测 | ≤ 65 字符 |
| Meta description | view-source | ≤ 160 字符，含 CTA |
| H1 含主词 | view-source | 含 `data analysis` |
| H2 全部为话题（非 slug） | view-source | 0 个 slug-H2 |
| JSON-LD 全部通过 | https://search.google.com/test/rich-results | 3 段全绿 |
| OG 预览 | https://www.opengraph.xyz/ | 标题/描述/图像正常 |
| canonical 正确 | view-source | 指向 `/use-cases/` 无 `index.html` |
| 移动端可用 | Chrome DevTools | 无横向滚动，CLS < 0.1 |
| Lighthouse | DevTools | Performance ≥ 90, SEO = 100 |
| FAQ schema vs DOM 一致 | 手测 | 逐字一致 |
| 数据自洽 | 手测 | Guides 数字 = 实际卡片数 |
| AI 引用测试 | ChatGPT / Perplexity 提问 "What is InfiniSynapse?" | 7 天后 ≥ 1 次被引用 |

---

## 9. 修复后预期分数

| 维度 | 现状 | 修后 | 提升 |
|---|---|---|---|
| Title | 6/10 | 9/10 | +3 |
| Meta | 6.5/10 | 9/10 | +2.5 |
| H1/H2 | 4/10 | 9/10 | +5 |
| Content | 4/10 | 8/10 | +4 |
| Keywords | 5/10 | 8/10 | +3 |
| Internal Links | 5/10 | 7/10 | +2 |
| Technical | 4/10 | 9/10 | +5 |
| **总分** | **5.0** | **≈ 8.4** | **+3.4** |

GEO 引用条件：Step 1 + 3 + 4 完成后，页面首次具备被 ChatGPT / Perplexity / Google AIO 引用的全部结构条件（定义段、FAQ、JSON-LD、E-E-A-T 信号、可解析 H 结构）。

---

## 10. 责任分工建议（最小化协作开销）

| Step | 负责人角色 | 输入物 | 产出物 |
|---|---|---|---|
| Step 1–2 | 前端 / 内容运营 | 本文档 | 改后 `index.html` 草案 |
| Step 3 | 前端 | 产品事实清单（slogan/连接器数） | 3 段 JSON-LD |
| Step 4 | 内容运营 | 产品 FAQ / About 段 | Lede 段 + FAQ 段 |
| Step 5 | 运维 / DevOps | 域名管理后台 | 301 规则 + sitemap.xml |
| Step 6 | 内容运营 | 5 篇文章原稿 | 每篇底部互链区 |
| Step 7 | 项目负责人 | 上述全部 | 验收清单 ✅ |

---

> 文档版本 v1.0 · 基于 seo-geo-claude-skills v9.9.5 · 审计人：Cursor Agent
