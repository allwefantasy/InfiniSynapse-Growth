# InfiniSynapse · SEO 90 天可执行操作手册

> **对应增长方案**：[`index.html#seo-weekly`](./index.html#seo-weekly) · [`增长方案.md` §4.3](./增长方案.md) · [`§1.2 渠道 1 SEO`](./增长方案.md)  
> **编制日期**：2026-06-15 · **更新**：2026-06-16（**100 篇全量上线 + GSC 分波提交** 版）  
> **目标**：**D0 一次性部署 100 篇**（8 支柱全覆盖）→ 90 天内按 [`gsc-submit-order-100.csv`](./gsc-submit-order-100.csv) **分 13 周手动提交 GSC**（每周 8 篇），完成 **4 轮质检**、**主题集群内链成网**，并能统计 Google 带来的 Demo。

---

## 0. 策略一句话 + 权威依据

| 结论 | 权威出处 |
|------|----------|
| 客户采购前会在 Google 搜「**X 替代品 / vs / 怎么连数据库**」— 我们几乎不占位 | 增长方案 [`index.html#seo`](./index.html#seo) · Julius 约 **30%** 流量来自 Google |
| **学 Julius**：对比文 + 连接教程 + FAQ；**学 ThoughtSpot**：定义/科普 Hub 吃长尾 | [`competitors/julius-ai.html`](./competitors/julius-ai.html) · [`competitors/thoughtspot.html`](./competitors/thoughtspot.html) |
| **100 篇英文稿已在仓库 `SEO/Blog/`**，**40 篇 P0 已把策略关键词写入 H1/meta/schema/正文，全仓 11 项门禁 100/100 Pass、外链重合 0 violations** | [`P0-八支柱执行映射.md`](../../SEO/100页关键词验证/P0-八支柱执行映射.md) · [`blog-cms-import-100.csv`](../../SEO/Blog/blog-cms-import-100.csv) |
| **100 篇 D0 全量上线**，90 天重点是 **GSC 分波加速 + 质检 + 互链 + 排名监控**，不是分批发布 | [`GSC-SUBMIT-PLAN.md`](./GSC-SUBMIT-PLAN.md) · [`FRONTEND-DEPLOY-GUIDE.md`](../../SEO/Blog/FRONTEND-DEPLOY-GUIDE.md) |
| 差异化叙事 | **多库联邦 · 私有化 · 操作留痕** | 增长方案 [`index.html#product`](./index.html#product) |

### 三阶段过关线（全量上线版 · 8 支柱全覆盖）

| 阶段 | 周次 | GSC 手动提交 | 过关标志 |
|------|------|-------------|----------|
| **Phase 0** | **D0** | sitemap 提交 **100 URL** | 100 篇可访问 · Blog 列表 + Hub 内链 · sitemap 刷新 |
| **Phase 1** | W1–4 | **Wave 1–2 · 32 篇**（P3/P4 BOFU 优先） | 前 32 篇 ≥28 已索引 · P0 对比/连接词进排名表 |
| **Phase 2** | W5–8 | **Wave 3 · 32 篇**（P1/P2/P3 MOFU 建权威） | 累计手动提交 64 篇 · Hub 集群互链 · 排名表 ≥20 词 |
| **Phase 3** | W9–13 | **Wave 4–5 · 36 篇**（P5–P8 长尾 + 余量） | 手动提交完成 · ≥70 篇已索引 · 案例页 + 90 天复盘 |

> **GSC 操作细则**：见 [`GSC-SUBMIT-PLAN.md`](./GSC-SUBMIT-PLAN.md) · 执行清单 [`gsc-submit-order-100.csv`](./gsc-submit-order-100.csv)

---

## 0.5 全量上线 + GSC 分波提交（2026-06 策略调整）

> **变更**：由「每周发 2–3 篇」改为 **100 篇 D0 一次性部署**，GSC **手动请求编入索引** 按优先级排队（**不影响**未手动提交页的收录）。

| 动作 | 时机 | 说明 |
|------|------|------|
| **部署 100 篇** | D0 | 前端按 [`frontend-package/`](../../SEO/Blog/frontend-package/) 全量上线 |
| **sitemap 含 100 URL** | D0 | GSC → Sitemaps 提交/刷新（**主收录通道**） |
| **手动 GSC 提交** | W1 起 · 每周 8 篇 | 按 CSV `gsc_submit_order` 1→100 操作 |
| **未轮到手动的页** | D0 起 | 靠 sitemap + 内链自然抓取 · **禁止 noindex** |

**每周 15 分钟 SOP**：筛选 CSV 本周 `gsc_week` → URL 检查 → 请求编入索引 → 填 `gsc_submitted` 列。

---

## 0.6 八支柱 × 90 天编排总览（本次新增核心）

> 全量 P0 见 [`P0-八支柱执行映射.md`](../../SEO/100页关键词验证/P0-八支柱执行映射.md)。下表 = 每支柱在 90 天的「先发哪几篇 + 排在第几周 + 余量进 Q2」。

| Pillar | 主题 | Hub 页 | 90 天先发（周次） | 进 Q2 队列 |
|--------|------|--------|-------------------|-----------|
| **P1** AI-Native | 数据智能体定义/平台 | `001` / `004` / `007` | `005`(W5) · `003`(W5) · `007`(W6) | `002` · `004` · `010` |
| **P2** vs Alternatives | 与 Code Agent/BI/Chatbot 对比 | `014`（已发） | `016`(W6) · `018`(W7) · `014`改版(W2) | `015` · `017` · `021` |
| **P3** AI Analyst Tools | 工具榜/对比/替代品/评测 | `024`（已发） | `037`·`031`(W1) · `039`(W2) · `038`·`030`(W3) · `032`(W4) · `025`(W7) · `043`·`033`(W8) | `026` · `027` |
| **P4** Connectors | 连接 X 到 AI 分析师 | `044`（已发） | `045`(W2) · `047`(W3) · `048`·`051`(W4) | `046` · `052` |
| **P5** NL2SQL | Text-to-SQL/基准 | `059`（已发） | `060`·`061`(W10) | `062` |
| **P6** Excel/CSV | 表格/透视/公式 AI | `069`（已发） | `073`·`070`(W11) | `071` · `072` |
| **P7** Use Cases | 角色/行业场景 | `081` | `081`(W12) | `082`·`083`·`084`·`089`·`090` |
| **P8** Skills/Templates | Prompt/评测/FAQ Hub | `100` | `098`(W9) · `100`(W12) | `095` · `096` · `097` · `099` |

**说明**：Hub 页（已发）作为各支柱内链中枢；90 天先发优先 BOFU（P3/P4）→ 建权威（P1/P2）→ 补全长尾支柱（P5/P6/P7/P8）。Q2 队列见 §附录 E（按支柱列全）。

---

## 1. 优先级矩阵（按 Pillar 分组 · 关键词以仓库现状为准）

> 关键词已与 [`keywords-100-master.csv`](../../SEO/100页关键词验证/keywords-100-master.csv) 的 P0 列对齐，并写入各篇 `article.md` / `meta-tags.html` / `schema.json`。

### 1.1 P3 · 对比 / 替代品 / 评测（学 Julius）

| 优先级 | Slug | Target keyword（已对齐） | 仓库 |
|--------|------|--------------------------|------|
| P0 | `infinisynapse-vs-julius-ai` | `infinisynapse vs julius ai` | pillar3/037 |
| P0 | `julius-ai-alternatives` | `julius ai alternatives` | pillar3/031 |
| P0 | `infinisynapse-vs-chatgpt` | `infinisynapse vs chatgpt data analysis` | pillar3/038 |
| P0 | `chatgpt-data-analysis-alternatives` | `chatgpt for data analysis alternatives` | pillar3/030 |
| P0 | `ai-data-analysis-tools` | `best ai data analyst tools 2026` | pillar3/025 |
| P0 | `infinisynapse-review` | `infinisynapse review` | pillar3/043 |
| P1 | `infinisynapse-vs-databricks-genie` | `databricks genie` | pillar3/039 |
| P1 | `thoughtspot-alternatives` | `best ai data visualization tools` | pillar3/032 |
| P1 | `databricks-genie-alternatives` | `databricks assistant vs genie` | pillar3/033 |

### 1.2 P4 · 连接教程（学 Julius 集成页）

| Slug | Target keyword（已对齐） | 仓库 |
|------|--------------------------|------|
| `connect-postgres-to-ai-data-analyst` | `connect postgres to ai data analyst` | pillar4/045 |
| `connect-snowflake-to-ai-analyst` | `connect snowflake to ai analyst` | pillar4/047 |
| `connect-bigquery-to-ai-data-analyst` | `connect bigquery to ai data analyst` | pillar4/048 |
| `ai-data-analysis-google-sheets` | `ai data analysis for google sheets` | pillar4/051 |
| `connect-mysql-to-ai-data-analyst` | `connect mysql to ai data analyst` | pillar4/046（Q2） |
| `ai-data-analysis-csv-files` | `ai data analysis for csv files` | pillar4/052（Q2） |

### 1.3 P1 · 科普 / 定义 Hub（学 ThoughtSpot）

| Slug | Target keyword（已对齐） | 仓库 |
|------|--------------------------|------|
| `best-agentic-analytics` | `agentic analytics` | pillar1/005 |
| `what-is-a-data-agent` | `what is a data agent` | pillar1/003 |
| `ai-data-analyst` | `ai data analyst` | pillar1/007 |
| `data-agent-manifesto` | `data agent manifesto` | pillar1/002（Q2） |
| `ai-native-data-platform` | `ai-native data platform` | pillar1/004（Q2） |
| `fabric-data-agent-vs-copilot` | `data agent vs ai copilot` | pillar1/010（Q2） |

### 1.4 P2 · 思想领导 / 对比（建权威）

| Slug | Target keyword（已对齐） | 仓库 |
|------|--------------------------|------|
| `ai-data-analyst-vs-bi-tools` | `ai data analyst vs bi tools` | pillar2/016 |
| `chatgpt-data-analysis-limitations` | `chatgpt for data analysis limitations` | pillar2/018 |
| `code-agent-vs-data-agent` | `code agent vs data agent`（已发 · W2 改版） | pillar2/014 |
| `data-agent-architecture` | `data agent architecture` | pillar2/015（Q2） |
| `data-agent-vs-llm-chatbot` | `data agent vs llm chatbot` | pillar2/017（Q2） |
| `ai-data-analyst-vs-human-analyst` | `ai data analyst vs human analyst` | pillar2/021（Q2） |

### 1.5 P5 / P6 / P7 / P8 · 技术信任 + 长尾场景 + 模板

| Slug | Target keyword（已对齐） | 仓库 | 周次 |
|------|--------------------------|------|------|
| `text-to-sql-llm` | `text to sql llm` | pillar5/060 | W10 |
| `nl2sql-benchmark-spider-bird` | `nl2sql benchmark spider bird` | pillar5/061 | W10（GEO 高引用） |
| `analyze-csv-with-ai` | `analyze csv with ai` | pillar6/073 | W11 |
| `ai-alternative-to-pivot-table` | `ai alternative to pivot table` | pillar6/070 | W11 |
| `ai-tools-for-data-analysts` | `ai tools for data analysts` | pillar7/081 | W12 |
| `how-to-evaluate-ai-data-analyst` | `how to evaluate ai data analyst` | pillar8/098 | W9 |
| `data-agent-faq` | `what is a data agent` | pillar8/100 | W12（FAQ Hub） |

### 1.6 已发待改版

| Slug | 动作 | 参考 |
|------|------|------|
| `code-agent-vs-data-agent` | W2 补：开头 40 字产品定义 + 5 条 FAQ + 链买家指南 | [`014`](../../SEO/Blog/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/article.md) |

### 1.7 第 9 周 · 案例（学 Julius 案例研究）

| 类型 | 说明 | 权威参考 |
|------|------|----------|
| **新案例页** | 1 个垂直场景 + 量化结果（如「2 天 → 20 分钟」）+ 场景录屏 | Julius「AthenaHQ 1 天→1 小时」· [`julius-ai.html`](./competitors/julius-ai.html) |
| **可复用素材** | Supabase 连接教程已有 Task View 截图流程 | [`ai-analyst-real-data-supabase`](../../SEO/Blog/ai-analyst-real-data-supabase/) |
| **必链** | 案例页 ↔ 对比文 ↔ [产品页 / 预约演示](https://app.infinisynapse.cn) |

---

## 2. 发布前总规则（每次必查）

### 2.1 四步流水线（增长方案 §4.3）

| 步骤 | 做什么 | 权威文档 |
|------|--------|----------|
| **1. 取稿** | 从 `SEO/Blog/.../article.md` 取正文 · **不改 Target keyword** | [`SKILL.md`](../../SEO/Blog/SKILL.md) |
| **2. 质检** | 跑 11+1 项 audit · 目标 **90/90 Pass** | [`content-quality-gates.md`](../../SEO/Blog/content-quality-gates.md) |
| **3. 上线** | 按发布包部署 · 更新 sitemap · GSC「请求编入索引」 | [`FRONTEND-DEPLOY-GUIDE.md`](../../SEO/Blog/FRONTEND-DEPLOY-GUIDE.md) |
| **4. 互链** | 链入 ≥3 篇旧文 · 链出 ≥2 篇新文 · 链产品页或预约演示 | [`cluster-link-registry.py`](../../SEO/Blog/cluster-link-registry.py) |

### 2.2 质检一键命令

```bash
cd SEO/Blog
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  echo "=== $s ==="; python3 $s.py || exit 1
done
```

**硬门禁摘要**（详见 SKILL）：

| 项 | 标准 |
|----|------|
| 字数 | 1900–2800 词 |
| 高 DR 外链 | ≥5 条 · DR≥70 · 叙事嵌入正文前 85% |
| 内链 | 禁 Related Reading 块 · Cluster 页须链 hub + ≥2 同集群文 |
| 标题/描述 | 含 Target keyword **完整短语** |
| FAQ | ≥4 问 · `schema.json` FAQPage |

> **现状**：100 篇全仓上述门禁 **100/100 Pass**，外链重合度 **0 violations**（2026-06-16 复核）。上线前对单篇再跑一次即可。

### 2.3 每篇必含的「产品定义块」（GEO + SEO 双用）

```markdown
InfiniSynapse is a governed data-agent platform for multi-source analytics—
natural-language questions over SQL warehouses, spreadsheets, and documents,
with audit trails and optional self-hosted deployment.
```

**出处**：增长方案 SEO 线 · Reddit 手册 · 各篇开头 40 字定义

---

## 3. 第 1–12 周逐条执行（每篇：动作 · 路径 · 互链 · 验收）

---

### 第 1 周 · P3 对比双发（BOFU）

| 动作 | Slug | 仓库 | Target keyword | 必链 |
|------|------|------|----------------|------|
| 1-A | `infinisynapse-vs-julius-ai` | pillar3/037 | `infinisynapse vs julius ai` | `julius-ai-alternatives` · `best-ai-tools-for-data-analysis` · `sql-data-analysis-tools` · [web app](https://app.infinisynapse.cn) |
| 1-B | `julius-ai-alternatives` | pillar3/031 | `julius ai alternatives` | ↔ 1-A · `best-ai-tools-for-data-analysis` · `ai-data-visualization-tools` |

**验收**：2 URL 可访问 · 各 ≥3 内链 · audit 通过 · GSC 提交 · 记入附录 C 台账

---

### 第 2 周 · P3 Genie 对比 + P4 Postgres + 改版 #014

| 动作 | Slug | 仓库 | Target keyword | 要点 |
|------|------|------|----------------|------|
| 2-A | `infinisynapse-vs-databricks-genie` | pillar3/039 | `databricks genie` | 差异化：**多库联邦 · 私有化** · [`databricks-genie.html`](./competitors/databricks-genie.html) |
| 2-B | `connect-postgres-to-ai-data-analyst` | pillar4/045 | `connect postgres to ai data analyst` | 分步截图 · HowTo Schema · 对标 Supabase #044 |
| 2-C | `code-agent-vs-data-agent`（改版） | pillar2/014 | — | ① 开头 40 字定义 ② 补 5 FAQ ③ 链产品页 ④ 跑 audit |

**验收**：Genie 页 + Postgres 教程上线 · #014 更新 · W1–2 共 5 页 keyword audit Pass

---

### 第 3 周 · P3 ChatGPT 对比 + P4 Snowflake

| 动作 | Slug | 仓库 | Target keyword | 互链 |
|------|------|------|----------------|------|
| 3-A | `infinisynapse-vs-chatgpt` | pillar3/038 | `infinisynapse vs chatgpt data analysis` | W1 Julius 对比 · alternatives |
| 3-B | `chatgpt-data-analysis-alternatives` | pillar3/030 | `chatgpt for data analysis alternatives` | 3-A · `chatgpt-data-analysis-limitations`(W7 预告) |
| 3-C | `connect-snowflake-to-ai-analyst` | pillar4/047 | `connect snowflake to ai analyst` | postgres · supabase |

**验收**：累计 **7 篇** · 新文各加 3 链指向前两周 · 跑 `audit-content-quality.py`

---

### 第 4 周 · Phase 1 收官（10 篇齐）

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 4-A | `thoughtspot-alternatives` | pillar3/032 | `best ai data visualization tools` |
| 4-B | `connect-bigquery-to-ai-data-analyst` | pillar4/048 | `connect bigquery to ai data analyst` |
| 4-C | `ai-data-analysis-google-sheets` | pillar4/051 | `ai data analysis for google sheets` |

- **4-D · FAQ Schema**：10 篇全部确认 `schema.json` 含 FAQPage · [富媒体测试](https://search.google.com/test/rich-results)抽 3 页截图。
- **4-E · Sitemap**：更新 sitemap · GSC 重新提交 · 记录收录日期。

**✅ Phase 1 验收**：**10 篇**在线（P3×6 + P4×3 + 改版×1）· FAQ 格式统一 · 富媒体测试无报错

---

### 第 5 周 · P1 科普 Hub（建权威起点）

| 动作 | Slug | 仓库 | Target keyword | 结构 |
|------|------|------|----------------|------|
| 5-A | `best-agentic-analytics` | pillar1/005 | `agentic analytics` | ThoughtSpot Hub 式：定义 → 大表 → 8 FAQ → 轻提产品 |
| 5-B | `what-is-a-data-agent` | pillar1/003 | `what is a data agent` | 定义页 + FAQ → ChatGPT 易引 |

**要求**：各 8+ FAQ · 开头 40 字定义 · 内链 ≥3 篇 W1–4 对比文

---

### 第 6 周 · P1 角色 Hub + P2 BI 对比

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 6-A | `ai-data-analyst` | pillar1/007 | `ai data analyst` |
| 6-B | `ai-data-analyst-vs-bi-tools` | pillar2/016 | `ai data analyst vs bi tools` |

**要求**：互链 W5 科普文 · 链 `best-ai-tools-for-data-analysis` · P2 文锚定 Tableau/Power BI/Looker

---

### 第 7 周 · P3 工具榜 + P2 ChatGPT 局限

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 7-A | `ai-data-analysis-tools` | pillar3/025 | `best ai data analyst tools 2026` |
| 7-B | `chatgpt-data-analysis-limitations` | pillar2/018 | `chatgpt for data analysis limitations` |

**要求**：7-A 榜单链 W1–4 对比文；7-B 链 W3 ChatGPT 对比/替代品 · 记录关键词排名表第 1 版（≥20 词，模板见附录 B）

---

### 第 8 周 · Phase 2 收官（评测 + Genie 集群）

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 8-A | `databricks-genie-alternatives` | pillar3/033 | `databricks assistant vs genie` |
| 8-B | `infinisynapse-review` | pillar3/043 | `infinisynapse review` |

- **8-C · Genie 集群内链**：`infinisynapse-vs-databricks-genie` · `databricks-genie-alternatives` · `databricks-genie-vs-data-agent`(pillar2/020) 必须互相可点。

```bash
python3 SEO/Blog/fix-internal-links.py && python3 SEO/Blog/audit-internal-links.py
```

- **8-D · 全站 title/meta 复查**：`audit-keyword-in-title-desc.py` + `audit-keyword-meta-stuffing.py`

**✅ Phase 2 验收**：累计 **18 篇** · 科普 Hub 3 篇 · Genie 集群互链 Pass · 评测文可转发

---

### 第 9 周 · P8 采购评测 + 案例研究

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 9-A | `how-to-evaluate-ai-data-analyst` | pillar8/098 | `how to evaluate ai data analyst` |
| 9-B | **案例研究**（新 slug 或 use-cases 子页） | — | 场景 → 前后数字 → 录屏 → 3 FAQ → 链买家指南 |

**要求**：9-A 写清采购评测维度（治理/多源/留痕/私有化），不用未验证自测分数；9-B 学 Julius 量化 ROI · 旧对比文「案例」段落改链到新 URL · 跑 `audit-internal-links.py` 查断链

---

### 第 10 周 · P5 NL2SQL 技术信任（GEO 高引用）

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 10-A | `text-to-sql-llm` | pillar5/060 | `text to sql llm` |
| 10-B | `nl2sql-benchmark-spider-bird` | pillar5/061 | `nl2sql benchmark spider bird` |

**要求**：技术深度文，内链 `data-agent-architecture`(Q2 预告) 与 `best-ai-tools-for-data-analysis`；Spider/BIRD 基准是 GEO 被引高地，FAQ 写清「基准 ≠ 生产可靠性」

---

### 第 11 周 · P6 Excel/CSV 长尾

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 11-A | `analyze-csv-with-ai` | pillar6/073 | `analyze csv with ai` |
| 11-B | `ai-alternative-to-pivot-table` | pillar6/070 | `ai alternative to pivot table` |

**要求**：链 P6 Hub `clean-excel-data-with-ai`(#069) + `ai-data-analysis-csv-files`(P4)；面向「Excel 起步、后续升级」人群

---

### 第 12 周 · P7 场景入口 + P8 FAQ Hub + 复盘

| 动作 | Slug | 仓库 | Target keyword |
|------|------|------|----------------|
| 12-A | `ai-tools-for-data-analysts` | pillar7/081 | `ai tools for data analysts`（P7 Hub） |
| 12-B | `data-agent-faq` | pillar8/100 | `what is a data agent`（20+ 问 FAQ Hub，每答链专题文） |

- **12-C · 复盘**：GA4/GSC Organic 会话 · Demo 点击 · 着陆页 Top 10 · 更新附录 B 排名表 · 写 90 天复盘（发了啥/收录啥/下季度优先）· 修剩余死链。

**✅ Phase 3 验收**：累计 **24 篇** · **8 支柱各有上线** · 案例 + FAQ Hub 上线 · 能回答「Demo 从 Google 哪几篇来」

---

## 4. 90 天发文顺序总表（复制到台账）

| 周 | # | Slug | Pillar | P 级 | 类型 | Target keyword |
|----|---|------|--------|------|------|----------------|
| 1 | 1 | infinisynapse-vs-julius-ai | 3 | P0 | vs | infinisynapse vs julius ai |
| 1 | 2 | julius-ai-alternatives | 3 | P0 | alternatives | julius ai alternatives |
| 2 | 3 | infinisynapse-vs-databricks-genie | 3 | P1 | vs | databricks genie |
| 2 | 4 | connect-postgres-to-ai-data-analyst | 4 | P0 | how-to | connect postgres to ai data analyst |
| 2 | — | code-agent-vs-data-agent（改版） | 2 | — | refresh | code agent vs data agent |
| 3 | 5 | infinisynapse-vs-chatgpt | 3 | P0 | vs | infinisynapse vs chatgpt data analysis |
| 3 | 6 | chatgpt-data-analysis-alternatives | 3 | P0 | alternatives | chatgpt for data analysis alternatives |
| 3 | 7 | connect-snowflake-to-ai-analyst | 4 | P0 | how-to | connect snowflake to ai analyst |
| 4 | 8 | thoughtspot-alternatives | 3 | P1 | alternatives | best ai data visualization tools |
| 4 | 9 | connect-bigquery-to-ai-data-analyst | 4 | P0 | how-to | connect bigquery to ai data analyst |
| 4 | 10 | ai-data-analysis-google-sheets | 4 | P0 | how-to | ai data analysis for google sheets |
| 5 | 11 | best-agentic-analytics | 1 | P0 | hub | agentic analytics |
| 5 | 12 | what-is-a-data-agent | 1 | P0 | definition | what is a data agent |
| 6 | 13 | ai-data-analyst | 1 | P0 | role hub | ai data analyst |
| 6 | 14 | ai-data-analyst-vs-bi-tools | 2 | P0 | comparison | ai data analyst vs bi tools |
| 7 | 15 | ai-data-analysis-tools | 3 | P0 | listicle | best ai data analyst tools 2026 |
| 7 | 16 | chatgpt-data-analysis-limitations | 2 | P0 | thought-leadership | chatgpt for data analysis limitations |
| 8 | 17 | databricks-genie-alternatives | 3 | P1 | alternatives | databricks assistant vs genie |
| 8 | 18 | infinisynapse-review | 3 | P0 | review | infinisynapse review |
| 9 | 19 | how-to-evaluate-ai-data-analyst | 8 | P0 | guide | how to evaluate ai data analyst |
| 9 | 20 | *case-study*（新） | — | — | case | — |
| 10 | 21 | text-to-sql-llm | 5 | P0 | tech | text to sql llm |
| 10 | 22 | nl2sql-benchmark-spider-bird | 5 | P0 | tech/GEO | nl2sql benchmark spider bird |
| 11 | 23 | analyze-csv-with-ai | 6 | P0 | how-to | analyze csv with ai |
| 11 | 24 | ai-alternative-to-pivot-table | 6 | P0 | how-to | ai alternative to pivot table |
| 12 | 25 | ai-tools-for-data-analysts | 7 | P0 | use-case hub | ai tools for data analysts |
| 12 | 26 | data-agent-faq | 8 | P2 | faq hub | what is a data agent |

> **已上线不计入**：`connect-supabase-to-ai-data-analyst`(P4 Hub) · `best-ai-tools-for-data-analysis`(P3 Hub · W10 更新) · `code-agent-vs-data-agent`(P2 Hub · W2 改版) · `natural-language-to-sql`(P5 Hub) · `clean-excel-data-with-ai`(P6 Hub)。

---

## 5. 质检日历（4 轮）

| 轮次 | 周次 | 范围 |
|------|------|------|
| **R1** | W3 末 | W1–3 新上线 7 篇 · 单项 audit |
| **R2** | W4 末 | Phase 1 全部 10 篇 · FAQ Schema · 富媒体测试 |
| **R3** | W8 末 | 全站 18 篇 · 内链集群 · Genie 三角 |
| **R4** | W11 | 全站 11 项 + overlap · 8 支柱抽检 · 仅修 Fail |

---

## 附录 A · 发布包文件清单（每篇相同）

```
SEO/Blog/pillarN-.../NNN-slug/
├── article.md       ✅ 部署
├── meta-tags.html   ✅ 复制进 <head>
├── schema.json      ✅ JSON-LD
├── images/          ✅ hero + 正文图
├── preview.html     ❌ 仅本地
└── audit.md         ❌ 运营 QA
```

部署细则：[`FRONTEND-DEPLOY-GUIDE.md`](../../SEO/Blog/FRONTEND-DEPLOY-GUIDE.md) · 前端交付包：[`frontend-handoff/`](../../SEO/Blog/frontend-handoff/)（100 篇 + 100 预览 + 310 图，已 2026-06-16 重建）  
CMS 批量索引：[`blog-cms-import-100.csv`](../../SEO/Blog/blog-cms-import-100.csv) · [`blog-index-import-master.json`](../../SEO/Blog/blog-index-import-master.json)

---

## 附录 B · 重点关键词跟踪表（≥20 词 · 已对齐）

| Keyword | 目标 URL | Pillar | P 级 | 90 天目标排名 | W4 | W8 | W12 |
|---------|----------|--------|------|---------------|----|----|-----|
| infinisynapse vs julius ai | /blog/infinisynapse-vs-julius-ai | 3 | P0 | Top 20 | | | |
| julius ai alternatives | /blog/julius-ai-alternatives | 3 | P0 | Top 20 | | | |
| infinisynapse vs chatgpt data analysis | /blog/infinisynapse-vs-chatgpt | 3 | P0 | Top 30 | | | |
| chatgpt for data analysis alternatives | /blog/chatgpt-data-analysis-alternatives | 3 | P0 | Top 30 | | | |
| best ai data analyst tools 2026 | /blog/ai-data-analysis-tools | 3 | P0 | Top 20 | | | |
| infinisynapse review | /blog/infinisynapse-review | 3 | P0 | Top 10（品牌词） | | | |
| databricks genie | /blog/infinisynapse-vs-databricks-genie | 3 | P1 | Top 30 | | | |
| connect postgres to ai data analyst | /blog/connect-postgres-to-ai-data-analyst | 4 | P0 | Top 30 | | | |
| connect snowflake to ai analyst | /blog/connect-snowflake-to-ai-analyst | 4 | P0 | Top 30 | | | |
| connect bigquery to ai data analyst | /blog/connect-bigquery-to-ai-data-analyst | 4 | P0 | Top 30 | | | |
| ai data analysis for google sheets | /blog/ai-data-analysis-google-sheets | 4 | P0 | Top 30 | | | |
| agentic analytics | /blog/best-agentic-analytics | 1 | P0 | Top 10 | | | |
| what is a data agent | /blog/what-is-a-data-agent | 1 | P0 | Top 20 | | | |
| ai data analyst | /blog/ai-data-analyst | 1 | P0 | Top 30 | | | |
| ai data analyst vs bi tools | /blog/ai-data-analyst-vs-bi-tools | 2 | P0 | Top 30 | | | |
| chatgpt for data analysis limitations | /blog/chatgpt-data-analysis-limitations | 2 | P0 | Top 30 | | | |
| how to evaluate ai data analyst | /blog/how-to-evaluate-ai-data-analyst | 8 | P0 | Top 30 | | | |
| text to sql llm | /blog/text-to-sql-llm | 5 | P0 | Top 30 | | | |
| nl2sql benchmark spider bird | /blog/nl2sql-benchmark-spider-bird | 5 | P0 | Top 20（GEO） | | | |
| analyze csv with ai | /blog/analyze-csv-with-ai | 6 | P0 | Top 30 | | | |
| ai alternative to pivot table | /blog/ai-alternative-to-pivot-table | 6 | P0 | Top 30 | | | |
| ai tools for data analysts | /blog/ai-tools-for-data-analysts | 7 | P0 | Top 30 | | | |

数据来源：GSC · SEMrush（[`SEMrush-验证SOP`](../../SEO/100页关键词验证/SEMrush-验证SOP.md)）

---

## 附录 C · 上线台账

| 周 | Slug | 上线日期 | GSC 提交 | Audit | 内链≥3 | FAQ Schema | 备注 |
|----|------|----------|----------|-------|--------|------------|------|
| 1 | infinisynapse-vs-julius-ai | | ☐ | ☐ | ☐ | ☐ | |
| 1 | julius-ai-alternatives | | ☐ | ☐ | ☐ | ☐ | |
| … | | | | | | | |

---

## 附录 D · 权威文档索引

| 文档 | 路径 | 用途 |
|------|------|------|
| **P0 八支柱映射** | [`P0-八支柱执行映射.md`](../../SEO/100页关键词验证/P0-八支柱执行映射.md) | 40 P0 × 8 支柱落地 |
| 增长方案 SEO 周历 | [`index.html#seo-weekly`](./index.html#seo-weekly) | 90 天节奏 |
| 增长方案 Markdown | [`增长方案.md` §1.2 · §4.3](./增长方案.md) | 策略与 KPI |
| Julius 搜索标杆 | [`competitors/julius-ai.html`](./competitors/julius-ai.html) | 对比文/教程结构 |
| ThoughtSpot Hub 标杆 | [`competitors/thoughtspot.html`](./competitors/thoughtspot.html) | 科普/FAQ 集群 |
| Genie 对比拦截 | [`competitors/databricks-genie.html`](./competitors/databricks-genie.html) | Genie 差异化 |
| 100 页规划 | [`100页主题集群规划-v1-替换后主关键词版.md`](../../SEO/100页主题集群规划-v1-替换后主关键词版.md) | 全量主题 |
| 关键词主表 | [`keywords-100-master.csv`](../../SEO/100页关键词验证/keywords-100-master.csv) | P0/P1 优先级 |
| 写作/质检 SKILL | [`SEO/Blog/SKILL.md`](../../SEO/Blog/SKILL.md) | 硬规则 |
| 质量门禁 | [`content-quality-gates.md`](../../SEO/Blog/content-quality-gates.md) | 11 项 audit |
| 前端部署 | [`FRONTEND-DEPLOY-GUIDE.md`](../../SEO/Blog/FRONTEND-DEPLOY-GUIDE.md) | 上线步骤 |
| 产品入口 | [InfiniSynapse web app](https://app.infinisynapse.cn) | 文章 CTA |
| Reddit 互链分发 | [`Reddit-90天可执行操作手册.md`](./Reddit-90天可执行操作手册.md) | 发文后论坛回复链同一 URL |

---

## 附录 E · Q2 候选队列（按支柱列全 · W11 勾选）

> 90 天未上线的 P0/P1/P2 余量，按支柱分组，确保 8 支柱后续均有续航。

| Pillar | Slug | 仓库 | Target keyword | P 级 |
|--------|------|------|----------------|------|
| P1 | data-agent-manifesto | 002 | data agent manifesto | P0 |
| P1 | ai-native-data-platform | 004 | ai-native data platform | P0 |
| P1 | fabric-data-agent-vs-copilot | 010 | data agent vs ai copilot | P0 |
| P2 | data-agent-architecture | 015 | data agent architecture | P0 |
| P2 | data-agent-vs-llm-chatbot | 017 | data agent vs llm chatbot | P0 |
| P2 | ai-data-analyst-vs-human-analyst | 021 | ai data analyst vs human analyst | P0 |
| P2 | databricks-genie-vs-data-agent | 020 | databricks assistant vs genie | P1 |
| P3 | sql-data-analysis-tools | 026 | best ai tools for sql data analysis | P0 |
| P3 | ai-excel-data-analysis-tools | 027 | best ai tools for excel data analysis | P0 |
| P4 | connect-mysql-to-ai-data-analyst | 046 | connect mysql to ai data analyst | P0 |
| P4 | ai-data-analysis-csv-files | 052 | ai data analysis for csv files | P0 |
| P5 | ai-sql-generator | 062 | ai sql generator | P0 |
| P6 | ai-vlookup-replacement | 071 | ai vlookup replacement | P0 |
| P6 | ai-excel-formula-generator | 072 | ai excel formula generator | P0 |
| P7 | ai-data-analysis-product-managers | 082 | ai data analysis for product managers | P0 |
| P7 | ai-data-analysis-finance-teams | 083 | ai data analysis for finance teams | P0 |
| P7 | ai-data-analysis-marketing | 084 | ai data analysis for marketing | P0 |
| P7 | ai-data-analysis-ecommerce | 089 | ai data analysis for ecommerce | P0 |
| P7 | ai-data-analysis-saas | 090 | ai data analysis for saas | P0 |
| P8 | ai-data-analysis-prompts | 095 | ai data analysis prompts | P0 |

完整列表：`blog-cms-import-100.csv` 中 `target_keyword` 列 + [`100页主题集群规划`](../../SEO/100页主题集群规划-v1-替换后主关键词版.md)

---

*本手册随 GSC 收录与排名数据更新；若某 slug audit 未过，**不得上线**，顺延到当周 backlog 而非跳过质检。8 支柱编排见 §0.6，全量 P0 落地见 [`P0-八支柱执行映射.md`](../../SEO/100页关键词验证/P0-八支柱执行映射.md)。*
