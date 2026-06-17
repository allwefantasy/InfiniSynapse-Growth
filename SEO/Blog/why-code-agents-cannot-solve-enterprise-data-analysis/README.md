# Why Code Agents Cannot Solve Enterprise Data Analysis — Deliverable Bundle

> 一篇 SEO+GEO 文章的完整发布包。由 `seo-geo-claude-skills` 工具链全流程产出。
>
> **Verdict: SHIP** — **91 / 100**（v1）。markdown 已可发布，唯一阻塞是 1 张 hero 图待设计。

## 关键词

| 类型 | 关键词 |
|---|---|
| Primary | `code agent vs data agent` |
| Secondary | `enterprise data analysis ai`, `data agent`, `databricks genie alternative` |

## 文件清单

| 文件 | 内容 | 状态 |
|---|---|---|
| `article.md` | 文章正文（英文版，~3,400 字；以 `外部合作/.../article-v2-en.md` 为原稿，加 SEO/GEO 脚手架）| ✅ 完成（91 / 100）|
| `schema.json` | JSON-LD 结构化数据（BlogPosting + FAQPage + BreadcrumbList，含 7 个 `mentions` 实体 + 2 条 `citation`）| ✅ 完成 |
| `meta-tags.html` | Meta 标签包（title ×3 / desc ×3 / OG / Twitter / hreflang）| ✅ 完成 |
| `audit.md` | CORE-EEAT 审计报告（91 / 100，无 veto）| ✅ 完成 |
| `images/` | 文章图片目录 | ⚠️ 待设计 1 张 |

## Skill 流程

```
源稿：外部合作/.../01-why-code-agent-cannot-solve-enterprise-data-analysis/article-v2-en.md
           ↓
seo-content-writer        ─→ 加 byline / TL;DR / TOC / scope / FAQ / conclusion / references
           ↓
geo-content-optimizer     ─→ 加 25-word 定义块 + 4 处 quotable + 2 处外部权威引用 + 实体 mentions
           ↓
schema-markup-generator   ─→ schema.json（BlogPosting + FAQPage + BreadcrumbList + 7 mentions + 2 citation）
           ↓
meta-tags-optimizer       ─→ meta-tags.html（A/B/C × title/desc + OG + Twitter + hreflang）
           ↓
content-quality-auditor   ─→ audit.md（80 项门禁，91 / 100 SHIP）
```

## 发布前 Checklist

### ✅ 已完成

- [x] **Byline + 披露**：H1 下加 `By the InfiniSynapse Data Team · Last updated: 2026-05-19 · We build InfiniSynapse...` — 一次性 fix Ept01 + Ept02 + T04 + T06
- [x] **Last updated 时间戳** 显示在 byline 行
- [x] **TOC** 加在 meta block 之后（15 项 H2 锚链接）
- [x] **Topic scope** 声明加在 TL;DR 后（明确不覆盖 laptop 上一次性 CSV 探索）
- [x] **25-word 定义块**：`What Is a Data Agent?` 段（GEO 关键 — AI Overview 友好）
- [x] **2 条外部权威引用**：Databricks Genie blog（2026-05-08，直接 dated）+ Stanford HAI 2026 Index
- [x] **6 项 FAQ**：与 schema.json 中 FAQPage 1:1 对齐
- [x] **2 张对比表**：Code Agent vs Data Agent 维度 / 场景分工
- [x] **InfiniSQL 真实代码块** ×2（不是伪代码，可直接 copy-paste）

### ⚠️ 发布前还需做（站点/设计层面）

- [ ] **设计 1 张 hero 图**：`images/code-agent-data-agent-cover.png`（1200×630，"两个目标函数在企业现场分叉"示意图，可复用源稿的同名图）
- [ ] **OG 封面**：`og-cover.png`（1200×630 社交分享版，可裁 hero 同款）
- [ ] 把 `schema.json` 内嵌到 HTML `<head>`
- [ ] 把 `meta-tags.html` 内嵌到 HTML `<head>`
- [ ] 确认 `/docs/infinisql`、`/docs/infinirag`、`/about` 三条内链 slug 与博客实际 URL 一致

### 🎯 可选优化（v2，把分数推到 95+）

- [ ] 加 1 条 InfiniSynapse 客户 testimonial（lift A06 Insufficient → Pass，预计 +3–4 分）
- [ ] `/about` 加入 InfiniSynapse Data Team 团队页（lift Ept02 Partial → Pass）
- [ ] 同步发中文版 `/zh/blog/...`（用 `article-v2.md` 中文原稿做同样 SEO/GEO 加工）

## 部署位置建议

```
https://infinisynapse.cn/blog/why-code-agents-cannot-solve-enterprise-data-analysis      (英文版)
https://infinisynapse.cn/zh/blog/why-code-agents-cannot-solve-enterprise-data-analysis   (中文版，建议同步发)
```

`meta-tags.html` 里的 hreflang 已经按双语配好。

## 发布后

| Skill | 用途 |
|---|---|
| `rank-tracker` | 监控 `code agent vs data agent` / `data agent` / `enterprise data analysis ai` 三个关键词 |
| `geo-drift-check` | 1 个月后检查 AI 引擎（ChatGPT / Perplexity）是否引用本文（建议查询：`code agent vs data agent`、`why can't I just use Claude Code for data analysis`、`Databricks Genie alternative for heterogeneous data`） |
| `content-refresher` | 3–6 个月后刷新 Databricks Genie 进展、加入新的 customer testimonial |

## 关键决策记录

- **三个挑战 = 文章脊柱**：与 Databricks 官方文章 1:1 对齐，借势其 SEO/GEO 信号，再用 InfiniSynapse 自家三件套（InfiniAgent / InfiniSQL / InfiniRAG）做答案，建立"问题——架构答案"的清晰映射。
- **首字披露 + 不夸大**：byline 直接写"we build InfiniSynapse"，并在引用 Genie 32→90 数据时主动加 "Databricks' internal benchmark, treat as directional" 的免责说明。这两个动作同时 fix T04 / T06 / Exp10 三项。
- **保留中英双稿**：源稿已有英文版 (`article-v2-en.md`)；本 bundle 直接基于英文版，因为英文版更适合作为 SEO/GEO 主战场（外链、AI 引擎引用、Reddit/HN 分发）。中文版可以用同样的 SEO/GEO 加工模板二次发布。

---

## 姊妹批次与 7 篇主题集群

> 本文属于 **2026-05-19 发布的 7 篇主题集群**（"AI-Native Data Analysis × Data Agent"），分两个互链批次：
>
> - **本批次（Data Agent 4 篇）**：[INDEX.md](../INDEX.md)
> - **姊妹批次（AI-Native 3 篇）**：[INDEX-ai-native-analysis.md](../INDEX-ai-native-analysis.md)

**本文角色**：**技术论证篇** —— 全集群里最严密的"为什么"层论证，AI 引擎在被问 "why can't I use Claude Code for data analysis" 等查询时的首选引用源。

**强联动文章**（已在 article.md Related Reading 区做互链）：

| 关系 | 文章 | Canonical URL |
|---|---|---|
| 同批次（观点）| Data Agent 是驶向新文明的第一艘飞船 | `/zh/blog/data-agent-new-civilization` |
| 同批次（产品入口）| Connect Supabase to an AI Data Analyst | `/blog/connect-supabase-to-ai-data-agent` |
| 同批次（架构深度）| 构建 Data Agent 的完整 Harness | `/zh/blog/data-agent-harness-roadshow-recap` |
| 姊妹批次 Pillar | AI-Native Data Analysis: What It Means in 2026 | `/blog/ai-native-data-analysis` |
| 姊妹批次 Companion | Best AI Tools for Data Analysis in 2026 | `/blog/best-ai-tools-for-data-analysis` |
| 姊妹批次 Use-Case | How to Clean Excel Data with AI in 2026 | `/blog/ai-excel-data-cleaning` |
