# Pillar Hub 终极指南 · 内容框架（Hub = 落地页）

> **硬规则**：每个 Pillar 的 Hub 长文是一篇**完整、自成体系、高信息密度**的终极指南（Ultimate Guide），不是文章列表页。  
> **URL**：`/en/blog/{hub-slug}`（见 `cluster-link-registry.py` · `PRIMARY_HUB`）  
> **禁止**：仅用卡片网格替代正文；禁止 `/en/blog/pillar/*` 薄索引页。

---

## 类比：项目管理终极指南

| 模块 | PM 示例 | Hub 长文对应 |
|------|---------|--------------|
| **标题** | 《项目管理终极指南（2026版）》 | `{Topic}: The Complete 2026 Guide` / `Ultimate Guide` |
| **是什么** | 什么是项目管理、为何 2026 不同 | Key Definition + TL;DR + 背景段 |
| **核心框架** | 5 大流程组、10 大知识领域 | 主题特有的 4–6 个「支柱/阶段/方法」+ **表格或架构图** |
| **方法论对比** | 瀑布 vs 敏捷 vs OKR（内链→集群文） | 对比表 + 叙事句链到 Cluster（如 Code Agent vs Data Agent） |
| **工具/方案推荐** | 工具测评、选型矩阵（内链→测评文） | Tool landscape + buyer scorecard + 链到 listicle/review 文 |
| **实施路径** | 分阶段 rollout、检查清单 | Step-by-step workflow / implementation roadmap |
| **案例/证据** | 真实项目数字、前后对比 | Production case / pilot metrics（带可审计细节） |
| **FAQ** | 4–6 问，与 schema 一致 | `## Frequently Asked Questions` |
| **延伸阅读** | 附录资源列表 | `## Cluster guides in this pillar` **表格**（无部署序号） |

**内链原则**：对比段、工具段、实施段里**自然嵌入** Cluster 链接（每次 1 条、完整句）；表格是索引补充，不能替代正文深度。

---

## 每篇 Hub 必备结构（H2 级）

发布前自检，**全部 H2 须存在**（措辞可因主题微调）：

| # | H2 模块 | 内容要求 |
|---|---------|----------|
| 1 | `TL;DR` | 可扫读摘要 + What you'll learn |
| 2 | 定义 / 是什么 | Key Definition 引用块 + 2026 语境 |
| 3 | 核心框架 | ≥1 表格或图；4–6 个子概念 |
| 4 | 方法论 / 类别对比 | 对比表 + **≥2 条 Cluster 内链** |
| 5 | 工具 / 方案 landscape | 分 tier 叙述 + **≥2 条工具/测评 Cluster 内链** |
| 6 | 工作流 / 实施 |  numbered steps 或 phased roadmap |
| 7 | 案例或生产模式 | 具体数字、时间线、可 replay 证据 |
| 8 | 选型 / Scorecard |  buyer checklist 或 decision matrix |
| 9 | 常见失败模式 | ≥3 条 Failure + Fix |
| 10 | `Cluster guides in this pillar` | 表格索引全 Cluster（标题无 001/002 前缀） |
| 11 | `Frequently Asked Questions` | ≥4 问，与 `schema.json` FAQPage 一致 |
| 12 | `Conclusion` | 收束 + 1 条 Hub 相关 Cluster 链 |

---

## 体量与密度

| 指标 | Hub（Pillar Page） | Cluster Page |
|------|-------------------|--------------|
| 正文字数（TL;DR 起） | **2000–2800**（目标 2300+） | 1900–2800 |
| H2 + H3 + H4 | **20–30** | 20–30 |
| 关键词密度 | 1.2%–1.7% | 自适应 |
| 高 DR 外链 | ≥5，叙事嵌入 | ≥5 |
| 原创图表 | ≥1（hero + 正文图） | ≥1 |

---

## 15 个 Hub 主题框架速查

| Pillar | Hub slug | 指南标题方向 | 核心框架（H2 主题） | 对比段内链示例 | 工具段内链示例 |
|--------|----------|--------------|---------------------|----------------|----------------|
| P1 | `ai-for-data-analysis` | AI for Data Analysis Complete Guide | 5 分析方法、Enabled vs Native | AI-native vs Augmented | Best agentic analytics |
| P2 | `code-agent-vs-data-agent` | Code Agent vs Data Agent Guide | 架构差异、治理、5 non-negotiables | vs LLM chatbot, vs BI | Genie vs Data Agent |
| P3 | `best-ai-tools-for-data-analysis` | Best AI Tools Ultimate Guide | 评估维度、工具 tier、场景矩阵 | vs ChatGPT, vs Julius | Tool listicle  siblings |
| P4 | `connect-supabase-to-ai-data-analyst` | SQL / Connector Hub Guide | 连接生命周期、安全、验证 SQL | Postgres/MySQL/Snowflake  siblings | Connector runbooks |
| P5 | `natural-language-to-sql` | NL2SQL Complete Guide | NL→SQL 架构、失败模式、语义层 | SQL agent vs text-to-SQL | AI SQL generator |
| P6 | `clean-excel-data-with-ai` | AI for Excel & CSV Guide | 清洗阶段、公式/透视替代、自动化 | Pivot vs AI, VLOOKUP 替代 | Wrangling tools |
| P7 | `ai-tools-for-data-analysts` | AI Tools by Role Guide | 角色场景、行业切片、工作流 | Role/industry siblings | Analyst tool comparisons |
| P8 | `data-agent-faq` | Data Agent FAQ Hub | 概念环、实施检查、术语 | What is a Data Agent | Glossary, prompts |
| P9 | `semantic-layer` | Semantic Layer Ultimate Guide | 定义、dbt、架构要求 | dbt semantic layer alt | Requirements guide |
| P10 | `mcp-for-data-analysis` | MCP for Data Analysis Guide | MCP 架构、安全边界、server 设计 | MCP vs direct API | MCP tooling |
| P11 | `agentic-analytics` | Agentic Analytics Guide | 定义、编排、vs augmented | vs traditional BI | Buyer guide siblings |
| P12 | `what-are-data-trends` | Data Trends 2026 Guide | 趋势分类、评分卡、路线图 | Integration/privacy  siblings | Warehouse trends |
| P13 | `data-security-compliance` | Data Security & Compliance Guide | 框架、控制项、合规路径 | Privacy trends | Security controls |
| P14 | `enterprise-data-security-solutions` | Enterprise Data Security Guide | 5 层安全、scorecard、零信任 | Governance, platform | Security platform buyer |
| P15 | `public-data` | Public Data for AI Analysis Guide | 数据源类型、可靠性、discovery | Open data siblings | Search/discovery |

详细逐篇大纲：`SEO/Blog/pillar-hub-section-checklist.csv`（由 `generate-pillar-hub-checklist.py` 生成）。

---

## 程序员部署（Hub = 落地页）

1. **渲染整篇 `article.md`**（2000+ 词）— 这是 Pillar 落地页正文，不是可选。
2. 卡片网格（若有）放在正文**之后**，或仅作 UI 增强；**不得**只部署卡片。
3. `<head>` 注入 Hub 的 `head.html`（BlogPosting + FAQPage schema）。
4. 列表页 / 分类「查看全部」→ Hub URL（`hub-landing-pages-master.json`）。

验收：

```bash
# 正文词数（TL;DR 起）应 ≥ 2000
# 页面 HTML 中 H2 数量应 ≥ 8（不含 TOC）
curl -s "https://infinisynapse.com/en/blog/{hub-slug}" | grep -c '<h2'
```

---

## 与 Cluster 的分工

| | Hub 终极指南 | Cluster 深度文 |
|---|-------------|----------------|
| 角色 | 全景地图 + 选型框架 | 单点打透 |
| 内链 | 链到**全部** Cluster | 链回 Hub + ≥2 兄弟 |
| 表格 | Cluster guides 总表 | 专题对比表 |
| 重复 | 可以概述 | 不可与 Hub 大段重复 |

---

*维护：内容团队扩写 Hub 时遵循本文；发布门禁见 `infinisynapse-blog-full-rules.md` · Pillar Page 字数/密度。*
