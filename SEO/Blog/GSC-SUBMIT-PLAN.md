# GSC 提交计划 · 100 篇全量上线版

> **前提**：100 篇文章 **一次性全部部署上线**（同一 sitemap、Blog 列表、内链成网）。  
> **本计划只优化**：Google Search Console **手动「请求编入索引」** 的顺序与节奏。  
> **更新**：2026-06-16

---

## 1. 核心原则（不影响收录）

| 做法 | 说明 |
|------|------|
| ✅ **D0 提交完整 sitemap** | 100 个 URL **全部**写入 sitemap 并在 GSC 提交一次。这是收录主通道，与手动提交不冲突。 |
| ✅ **Blog 列表 + 内链** | 全量上线后，Hub 页、Related Reading、use-cases 索引 **链向所有新 URL**，爬虫可自然发现。 |
| ✅ **手动提交按优先级排队** | GSC 手动请求有配额（约 **8–12 条/天/属性**），只用来 **加速高价值页**，不是唯一收录途径。 |
| ❌ **不要** noindex 未手动提交的页 | 未手动提交的页面仍应 `index, follow`，靠 sitemap + 内链抓取。 |
| ❌ **不要** 分批开放 robots | 100 页同时可抓取，仅 **手动提交顺序** 分波次。 |

**结论**：全量上线 **不会** 伤害收录；手动提交是 **加速器**，不是 **开关**。

---

## 2. 节奏总览（90 天 · 13 周）

| 阶段 | 周次 | 手动提交篇数 | 重点 |
|------|------|-------------|------|
| **Wave 1 · BOFU 拦截** | W1–W2 | 16 | 竞品对比、替代品、连接器、品牌评测 |
| **Wave 2 · BOFU 补全** | W3–W4 | 16 | 剩余 P0 对比/连接/榜单 |
| **Wave 3 · MOFU 建权威** | W5–W8 | 32 | 科普 Hub、BI 对比、工具榜、ChatGPT 局限 |
| **Wave 4 · 长尾/场景** | W9–W10 | 16 | NL2SQL、Excel、场景、评测 |
| **Wave 5 · 余量** | W11–W13 | 20 | P1/P2 长尾；低优先页可 **仅 sitemap 抓取** |

- **每周手动提交**：**8 篇**（工作日每天 1–2 条 URL 检查 → 请求编入索引）  
- **执行清单**：[`gsc-submit-order-100.csv`](./gsc-submit-order-100.csv)（按 `gsc_submit_order` 列操作）

---

## 3. D0 上线日 Checklist（全量部署当天）

- [ ] 100 篇 URL 全部 200 可访问  
- [ ] **sitemap.xml 含 100 URL** → GSC → Sitemaps → 提交/刷新  
- [ ] Blog 列表页展示全部卡片（含新 filter 标签）  
- [ ] 6 个 Hub 页 + use-cases 索引 **内链** 指向高优先对比/连接文  
- [ ] 不批量 noindex、不删 canonical  
- [ ] （可选）GSC 手动提交 **W1 前 8 篇**（见 CSV `gsc_week=W1`）

---

## 4. 每周操作 SOP（运营 · 约 15 分钟/周）

1. 打开 [`gsc-submit-order-100.csv`](./gsc-submit-order-100.csv)，筛选本周 `gsc_week`  
2. 对 `submit_method=manual_inspection` 的 URL：  
   - GSC → URL 检查 → 输入完整 URL → **请求编入索引**  
   - 在 CSV 填 `gsc_submitted=日期`  
3. 对 `submit_method=sitemap_crawl_primary` 的 URL：**不强制手动**，仅在收录慢时补提交  
4. 每周五：GSC → 页面 → 看「已发现 - 尚未编入索引」数量；Wave 1–2 页优先处理  

---

## 5. W1–W4 手动提交 URL（优先预览）

### W1（8 篇 · 最高优先）

| # | URL | 目标关键词 |
|---|-----|-----------|
| 1 | `/blog/infinisynapse-vs-julius-ai` | infinisynapse vs julius ai |
| 2 | `/blog/julius-ai-alternatives` | julius ai alternatives |
| 3 | `/blog/infinisynapse-vs-chatgpt` | infinisynapse vs chatgpt data analysis |
| 4 | `/blog/connect-supabase-to-ai-data-analyst` | connect supabase…（Hub 重抓） |
| 5 | `/blog/chatgpt-data-analysis-alternatives` | chatgpt for data analysis alternatives |
| 6 | `/blog/infinisynapse-review` | infinisynapse review |
| 7 | `/blog/connect-postgres-to-ai-data-analyst` | connect postgres to ai data analyst |
| 8 | `/blog/connect-snowflake-to-ai-analyst` | connect snowflake to ai analyst |

### W2（8 篇）

| # | URL |
|---|-----|
| 9–16 | bigquery · best-ai-tools Hub · google sheets · genie vs · thoughtspot alt · code-agent Hub · chatgpt limitations · ai-data-analysis-tools |

> W3–W13 完整列表见 CSV。

---

## 6. 与 90 天增长目标对齐

| 原 90 天阶段 | 调整后含义（全量上线版） |
|-------------|-------------------------|
| Phase 1 W1–4 | **GSC 手动提交 Wave 1–2**（32 篇 BOFU）+ 监控 Wave 1 收录 |
| Phase 2 W5–8 | **GSC Wave 3**（32 篇 MOFU）+ 排名表更新 |
| Phase 3 W9–12 | **GSC Wave 4–5**（余量 36 篇）+ 90 天收录复盘 |

**内容发布节奏** → 改为 **「全量上线 + GSC 分波加速」**；SEO 质检、内链、Reddit 分发节奏仍按原 90 天手册。

---

## 7. 文件索引

| 文件 | 用途 |
|------|------|
| [`gsc-submit-order-100.csv`](./gsc-submit-order-100.csv) | 100 篇 GSC 提交顺序台账 |
| [`frontend-package/gsc-submit-order-100.csv`](./frontend-package/gsc-submit-order-100.csv) | 同上（交付包内） |
| [`blog-content-catalog.csv`](./frontend-package/blog-content-catalog.csv) | 部署路径对照 |
| [`SEO-90天可执行操作手册.md`](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/SEO-90天可执行操作手册.md) | 整体 SEO 节奏 |

---

## 8. 验收 KPI（90 天）

| 指标 | 目标 |
|------|------|
| Sitemap 已提交 URL | 100/100 |
| 手动提交完成 | Wave 1–4 ≥ 80 篇 |
| GSC 已编入索引（至少已抓取） | ≥ 70 篇（W12） |
| P0 BOFU 页（前 32 篇）已索引 | ≥ 28 篇（W8） |
| 来自 Google 的 Demo/着陆页可统计 | W12 复盘 |
