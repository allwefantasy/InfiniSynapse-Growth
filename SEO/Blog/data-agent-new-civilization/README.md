# Data Agent 是驶向新文明的第一艘飞船 — Deliverable Bundle

> 一篇创始人观点文章的完整发布包。由 `seo-geo-claude-skills` 工具链全流程产出。
>
> **Verdict: SHIP** — **88 / 100**（v1，Good+）。源稿是 18 行 250 字的宣言，扩展为 2,300 中文字的发布版本，同时保留原稿"造船技术 / 飞船 / 启航"叙事内核。

## 关键词

| 类型 | 关键词 |
|---|---|
| Primary | `Data Agent 新文明` / `data agent civilization` |
| Secondary | `code agent vs data agent`、`AI 数据驱动决策`、`Agentic Analytics` |

## 文件清单

| 文件 | 内容 | 状态 |
|---|---|---|
| `article.md` | 文章正文（中文版，~2,300 字，扩展自源稿 250 字宣言）| ✅ 完成（88 / 100）|
| `schema.json` | JSON-LD（BlogPosting + FAQPage + BreadcrumbList，含 Person 作者实体）| ✅ 完成 |
| `meta-tags.html` | Meta 标签包（title ×3 / desc ×3 / OG / Twitter / hreflang）| ✅ 完成 |
| `audit.md` | CORE-EEAT 审计（88 / 100，观点类修正权重）| ✅ 完成 |
| `images/` | 文章图片目录 | ⚠️ 待 copy（封面已在源稿目录就位）|

## Skill 流程

```
源稿：外部合作/.../02-data-agent-new-civilization/article.md（18 行 / ~250 字宣言）
           ↓
seo-content-writer        ─→ 扩展为长文：TL;DR / TOC / 6 节正文 / FAQ / 结语 / 延伸阅读
           ↓
geo-content-optimizer     ─→ 加 25–75 字定义块 + 3 处 quotable + 1 条 dated 外部引用 + entity mentions
           ↓
schema-markup-generator   ─→ BlogPosting（作者 = Person 祝海林）+ FAQPage（5 项）+ BreadcrumbList
           ↓
meta-tags-optimizer       ─→ A/B/C × title/desc + 中英 hreflang + WeChat-friendly OG
           ↓
content-quality-auditor   ─→ 88 / 100 SHIP（观点类修正权重）
```

## 发布前 Checklist

### ✅ 已完成

- [x] **保留原稿叙事内核**：造船技术 → 飞船 → 启航 → 两阶段使命
- [x] **Byline 强披露**：祝海林 · InfiniSynapse 创始人（一次性 fix Ept01 + T04 + T06）
- [x] **25-字定义块**：`关键定义：本文所说的 Data Agent 是一个自治软件系统...`
- [x] **2 张对比表**：旧拓扑 vs 新拓扑 / 三件套部件职责
- [x] **5 项 FAQ**：与 schema.json 中 FAQPage 1:1 对齐
- [x] **内部互链**：姊妹篇（01 Code Agent / 04 Roadshow）
- [x] **外部权威引用**：Databricks Genie blog（dated 2026-05-08）
- [x] **中英 hreflang**：x-default 指向中文版（源稿中文）

### ⚠️ 发布前还需做

- [ ] **复制封面图**到 `images/`：`cp 外部合作/.../02-data-agent-new-civilization/cover-1080p.png images/cover.png`
- [ ] **创建作者页**：`/about/zhuhailin`（fix Ept02 Partial → Pass）
- [ ] **schema.json 内嵌到 HTML `<head>`**
- [ ] **meta-tags.html 内嵌到 HTML `<head>`**
- [ ] **确认两条内链**（`/blog/why-code-agents-cannot-solve-enterprise-data-analysis`、`/blog/data-agent-harness-roadshow`）已上线

### 🎯 可选优化（v2，把分数推到 90+）

- [ ] 加 1 段客户使用 InfiniSynapse 做决策的真实小故事（lift Exp + A06）
- [ ] 发布 1–2 周后补英文版 founder essay（hreflang `en` 已挂位）

## 部署位置建议

```
https://infinisynapse.cn/zh/blog/data-agent-new-civilization    (中文版，主战场)
https://infinisynapse.cn/blog/data-agent-new-civilization        (英文版，规划中)
```

## 分发建议

| 渠道 | 标题变体 | 用途 |
|---|---|---|
| 公众号 / 官网博客 | A — Data Agent 是驶向新文明的第一艘飞船 | 主分发，建立叙事 |
| 知乎 / 即刻 | B — 为什么第一艘 AI 飞船一定是 Data Agent | 疑问式钩子，吸引讨论 |
| LinkedIn / X 创始人个人账号 | C — Code Agent 之后，下一艘 AI 飞船是 Data Agent | 借 Code Agent 已有的关注度做长尾 |
| 视频脚本 | 直接采用 TL;DR 段 + 两阶段使命表 | 1–2 分钟短视频 / 演讲 cold open |

## 发布后

| Skill | 用途 |
|---|---|
| `rank-tracker` | 监控 `data agent 新文明` / `code agent vs data agent` / `AI 数据驱动决策` |
| `geo-drift-check` | 1 个月后查 AI 引擎（ChatGPT / Perplexity / 通义千问）是否在"什么是 Data Agent"、"Code Agent 之后是什么"类查询中引用本文 |
| `content-refresher` | 6 个月后基于第二阶段（AI 自主决策）的真实案例做更新 |

## 关键决策记录

- **扩展但不稀释**：源稿是高密度宣言，扩展时严守"每一段都要为原观点服务"的纪律，避免变成科普文。
- **作者身份直接亮出**：观点性文章的可信度首先来自"谁在说"。byline 直接写"创始人"，比"InfiniSynapse Team"更有力。
- **不打数据牌**：观点文不堆 benchmark 数字，全程只用一条 Databricks 引用 + 一条"我宁可早讲对"的态度表达。审计权重也按观点类内容修正（弱化 A06 testimonial 要求）。
- **互链而非自吹**：让本文聚焦观点叙事，把"产品怎么做"的硬证据留给姊妹篇 04 Roadshow Recap，把"为什么不行"的论证留给姊妹篇 01 Why Code Agents Cannot。

---

## 姊妹批次与 7 篇主题集群

> 本文属于 **2026-05-19 发布的 7 篇主题集群**（"AI-Native Data Analysis × Data Agent"），分两个互链批次：
>
> - **本批次（Data Agent 4 篇）**：[INDEX.md](../INDEX.md)
> - **姊妹批次（AI-Native 3 篇）**：[INDEX-ai-native-analysis.md](../INDEX-ai-native-analysis.md)

**本文角色**：**中文观点篇** —— 把"AI-native"的判断用中文文化语境（飞船叙事）讲一遍。与姊妹批次 Pillar（英文品类入口）形成中英双语镜像。

**强联动文章**（已在 article.md 延伸阅读 区做互链）：

| 关系 | 文章 | Canonical URL |
|---|---|---|
| 同批次（论证）| 为什么 Code Agent 无法解决企业数据分析 | `/blog/why-code-agents-cannot-solve-enterprise-data-analysis` |
| 同批次（产品入口）| Connect Supabase to an AI Data Analyst | `/blog/connect-supabase-to-ai-data-agent` |
| 同批次（架构深度）| 构建 Data Agent 的完整 Harness | `/zh/blog/data-agent-harness-roadshow-recap` |
| 姊妹批次 Pillar（英文化版本）| AI-Native Data Analysis: What It Means in 2026 | `/blog/ai-native-data-analysis` |
