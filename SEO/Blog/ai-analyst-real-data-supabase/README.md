# Connect Supabase to an AI Data Analyst — Deliverable Bundle

> 一篇 Product Update + How-to 复合文章的完整发布包。由 `seo-geo-claude-skills` 工具链全流程产出。
>
> **Verdict: SHIP** — **92 / 100**（v1，Excellent）。本批次中最容易跑出 SEO 流量的一篇 —— 关键词长尾纯净、HowTo schema 适合抢富片段、6 项 FAQ 适合 AI Overview 引用。

## 关键词

| 类型 | 关键词 |
|---|---|
| Primary | `connect supabase to ai data analyst` |
| Secondary | `supabase ai analytics`、`query supabase with ai`、`ai analyst real data` |

## 文件清单

| 文件 | 内容 | 状态 |
|---|---|---|
| `article.md` | 文章正文（英文版，~2,700 字，扩展自源稿 ~150 字小红书 post）| ✅ 完成（92 / 100）|
| `schema.json` | JSON-LD（BlogPosting + **HowTo** + FAQPage + BreadcrumbList，含 9 个数据源 SoftwareApplication 实体）| ✅ 完成 |
| `meta-tags.html` | Meta 标签包（title ×3 / desc ×3 / OG / Twitter / hreflang）| ✅ 完成 |
| `audit.md` | CORE-EEAT 审计（92 / 100，Product Update + How-to 复合权重）| ✅ 完成 |
| `images/` | 文章图片目录 | ⚠️ 待设计 1 张 hero + 1 张 Task View 截图 |

## Skill 流程

```
源稿：外部合作/.../03-ai-analyst-real-data-supabase/post.txt（~150 字小红书）
           ↓
seo-content-writer        ─→ 扩展为 Product Update + How-to 复合文：
                              TL;DR / 完整连接器表 / 3 分钟接入 / Q1 端到端例子 / Security / FAQ
           ↓
geo-content-optimizer     ─→ 加 50-字定义块 + Code Agent 对比表 + 3 处 quotable + entity mentions
           ↓
schema-markup-generator   ─→ BlogPosting + **HowTo（PT3M）** + FAQPage（6 项）+ BreadcrumbList
           ↓
meta-tags-optimizer       ─→ A/B/C × title/desc + 中英 hreflang + Twitter Card
           ↓
content-quality-auditor   ─→ 92 / 100 SHIP（Product+HowTo 复合权重）
```

## 发布前 Checklist

### ✅ 已完成

- [x] **保留源稿全部产品信息**：10 个数据源全列出，"返回 SQL、源表、过滤条件、指标、文档、决策依据"原话扩展为"What InfiniSynapse returns instead"专节 + 表格
- [x] **3 分钟接入实操**：每步含 Supabase Studio 真实路径 + Postgres `create role` SQL + InfiniSynapse 操作路径
- [x] **端到端例子**：Q1 2026 类目增长 + Top 3 客户的 4-tool-call 完整 InfiniSQL 链路（命名中间表 `q1_orders` → `q1_orders_tagged` → `category_growth` → `top_contributors`）
- [x] **HowTo schema**：4 步骤，totalTime PT3M，可被 Google 富片段抽取
- [x] **Code Agent vs Data Agent 对比表**：互链到姊妹篇 01
- [x] **6 项 FAQ**：与 schema.json FAQPage 1:1 对齐（覆盖 Edge Functions / 数据出境 / 跨源 / RLS / vs Supabase Studio 自带 AI / 最快上手路径）
- [x] **Security & 数据驻留专节**：read-only role、pushdown、Self-hosted Private VPC

### ⚠️ 发布前还需做

- [ ] **设计 1 张 hero 图**：`images/hero-supabase-connect.png`（1200×630，展示 Supabase + 9 个数据源 logo 汇入 InfiniSynapse 的连接器示意图）
- [ ] **补 1 张 Task View 实拍截图**：展示上面 Q1 类目增长例子的完整 SQL 轨迹 + 中间表（强烈建议 — Exp 维度从 92 → 95+）
- [ ] **schema.json / meta-tags.html 内嵌到 HTML `<head>`**
- [ ] **确认内链已发布**：`/blog/why-code-agents-cannot-solve-enterprise-data-analysis` / `/blog/data-agent-new-civilization` / `/blog/data-agent-harness-roadshow` / `/blog/best-ai-tools-for-data-analysis` / `/docs/command-tools` / `/enterprise`

### 🎯 可选优化（v2，把分数推到 95+）

- [ ] 加 1 条 Supabase 用户引用 / Supabase team 转发（lift A06）
- [ ] 发中文版镜像（`/zh/blog/connect-supabase-to-ai-data-agent`，对国内 Supabase 用户友好）

## 部署位置建议

```
https://infinisynapse.cn/blog/connect-supabase-to-ai-data-agent      (英文版，主战场)
https://infinisynapse.cn/zh/blog/connect-supabase-to-ai-data-agent   (中文版，建议补)
```

## 分发建议（这一篇 distribution upside 最大）

| 渠道 | 用途 | 备注 |
|---|---|---|
| **Hacker News** | "Show HN: Connect Supabase to an AI Data Agent (joins with your warehouse + Excel in one task)" | 周二/周三 UTC 13:00 投放 |
| **Reddit r/Supabase** | 直接发文，强调 RLS / pooler URI 支持 | Supabase 社区对"非 Supabase 团队做的工具"普遍友好 |
| **Supabase Discord** #showcase | 简短帖 + 文章链接 | Supabase DevRel 可能转发 |
| **Twitter / X** | "We now read your Supabase + your warehouse + your Excel in one task." 配 hero 图 | @ Supabase 官方 + @kiwicopple |
| **微信公众号** | 中文版镜像首发 | 国内 Supabase 用户群体（独立开发者 + AI 初创）匹配度高 |
| **掘金 / 即刻** | 中文版镜像 | 关键词：Supabase 国内、AI 数据分析、Postgres |

## 发布后

| Skill | 用途 |
|---|---|
| `rank-tracker` | 监控 `connect supabase to ai data analyst` / `supabase ai analytics` / `query supabase with ai` |
| `geo-drift-check` | 1 个月后查 ChatGPT / Perplexity / Claude 是否在"如何用 AI 连接 Supabase"、"Supabase + AI Analytics"类查询中引用本文 |
| `content-refresher` | Edge Functions / Storage 上线时刷新 |
| `backlink-analyzer` | 发布后 2 周追踪 Supabase 生态内的反链（Discord / 用户博客 / Newsletter） |

## 关键决策记录

- **从小红书 post 重构为 SEO/GEO 主战场**：源稿是中文小红书短文，但 Supabase 用户主体在英文世界 + 国内独立开发者。决策是**英文优先 + 中文镜像**，主战场放英文版抢 Google + AI 引擎引用。
- **HowTo schema 是关键武器**：本文最稳的流量入口是 `connect supabase to ai data analyst` 这种 how-to 长尾。HowTo schema 直接帮抢 Google Featured Snippet，比 BlogPosting 主标签收益高得多。
- **完整 4-tool-call SQL 链是 Exp 维度的核心证据**：不写"伪代码"，写真能跑的 InfiniSQL，命名中间表链路一致。这也是和"Code Agent 写 pandas"对比时最有说服力的差异点。
- **Security & 数据驻留单独成节**：Supabase 用户对 RLS、pooler URI、数据出境敏感。专节回答这些 + 提到 InfiniSynapse Private 自部署选项，是企业线索转化的关键铺垫。
- **互链到 4 篇姊妹文**：本文是产品入口，其他 3 篇是叙事/思考；用户从产品页跳叙事页，转化率更高。

---

## 姊妹批次与 7 篇主题集群

> 本文属于 **2026-05-19 发布的 7 篇主题集群**（"AI-Native Data Analysis × Data Agent"），分两个互链批次：
>
> - **本批次（Data Agent 4 篇）**：[INDEX.md](../INDEX.md)
> - **姊妹批次（AI-Native 3 篇）**：[INDEX-ai-native-analysis.md](../INDEX-ai-native-analysis.md)

**本文角色**：**英文产品入口** —— 集群里转化率预期最高的页面。Supabase + AI 是窄垂直长尾词，与姊妹批次 Use-Case（Excel）共同形成"数据源覆盖矩阵"（Postgres + Excel）。

**强联动文章**（已在 article.md Related Reading 区做互链）：

| 关系 | 文章 | Canonical URL |
|---|---|---|
| 同批次（论证）| Why Code Agents Cannot Solve Enterprise Data Analysis | `/blog/why-code-agents-cannot-solve-enterprise-data-analysis` |
| 同批次（观点）| Data Agent 是驶向新文明的第一艘飞船 | `/zh/blog/data-agent-new-civilization` |
| 同批次（架构深度）| 构建 Data Agent 的完整 Harness | `/zh/blog/data-agent-harness-roadshow-recap` |
| 姊妹批次 Use-Case（Excel 对偶）| How to Clean Excel Data with AI in 2026 | `/blog/ai-excel-data-cleaning` |
| 姊妹批次 Companion | Best AI Tools for Data Analysis in 2026 | `/blog/best-ai-tools-for-data-analysis` |
| 姊妹批次 Pillar | AI-Native Data Analysis: What It Means in 2026 | `/blog/ai-native-data-analysis` |
