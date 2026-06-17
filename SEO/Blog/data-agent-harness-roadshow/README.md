# 构建 Data Agent 的完整 Harness — Deliverable Bundle

> 一篇 Talk Recap + Architecture Deep-Dive 复合文章的完整发布包。由 `seo-geo-claude-skills` 工具链全流程产出。
>
> **Verdict: SHIP** — **93 / 100**（v1，Excellent）。本批次中**专业度最高、最适合企业决策人画像**的一篇 —— 含八件套 + 3 组硬证据 + 4 条私有化边界，完整买家旅程素材。

## 关键词

| 类型 | 关键词 |
|---|---|
| Primary | `Data Agent Harness 架构` |
| Secondary | `企业级 Data Agent 实践`、`InfiniSynapse 架构`、`Agentic Analytics 落地` |

## 文件清单

| 文件 | 内容 | 状态 |
|---|---|---|
| `article.md` | 文章正文（中文版，~3,400 字，基于 reveal.js 22 张幻灯片整理）| ✅ 完成（93 / 100）|
| `schema.json` | JSON-LD（BlogPosting + **Event** + **FAQPage** + BreadcrumbList，含 `isBasedOn` 指向原演讲）| ✅ 完成 |
| `meta-tags.html` | Meta 标签包（title ×3 / desc ×3 / OG / Twitter / hreflang）| ✅ 完成 |
| `audit.md` | CORE-EEAT 审计（93 / 100，Talk Recap + Architecture Deep-Dive 复合权重）| ✅ 完成 |
| `images/` | 文章图片目录 | ⚠️ 待设计 1 张封面（其他图建议直接 link 源稿 assets/）|

## Skill 流程

```
源稿：外部合作/.../04-data-agent-harness-roadshow/index.html（reveal.js 22 张幻灯片）
           ↓
seo-content-writer        ─→ 将 22 张幻灯片转为长文叙事：TL;DR / 三挑战 / 八解法 / 硬证据 / 私有化 / Takeaway
           ↓
geo-content-optimizer     ─→ 加 25-75 字 harness 定义块 + 8 段"演讲原话"blockquote + entity mentions
           ↓
schema-markup-generator   ─→ BlogPosting + **Event**（MPD 演讲）+ **isBasedOn**（指向原演讲）+ FAQPage 6 项
           ↓
meta-tags-optimizer       ─→ A/B/C × title/desc + 中英 hreflang
           ↓
content-quality-auditor   ─→ 93 / 100 SHIP（Talk Recap + Architecture Deep-Dive 复合权重）
```

## 发布前 Checklist

### ✅ 已完成

- [x] **保留全部 22 张幻灯片信息**：三挑战 + 八解法 + 硬证据 + Private 部署 + Takeaway，每节都对应原幻灯片
- [x] **三组硬证据**：1400+ 张表 / 92 秒 / AUC 0.7712（vs 0.7611 XGBoost 基线）
- [x] **8 段"演讲原话"blockquote**（GEO 友好，AI 引擎可直接 lift）
- [x] **ASCII 八件套架构图** + **ASCII Private 部署图**（文字化重建幻灯片，无需图片即可理解架构）
- [x] **真实 InfiniSQL 4-tool-call 代码块**（`region_revenue` → `abnormal_region` → `campaign_bridge` → `scorecard_model`）
- [x] **完整 byline**：演讲者（祝海林·创始人）+ 整理者（InfiniSynapse Team）+ 时间地点（MPD 峰会 2026-05-29 上海）
- [x] **Event + isBasedOn dual schema**：让 AI 引擎识别"这是峰会演讲整理"
- [x] **6 项 FAQ ↔ schema 1:1**：覆盖八件套是否必须全用 / InfiniSQL 学习成本 / 硬证据复现 / 央国企模型替换 / 与 Databricks Genie 关系 / 幻灯片下载

### ⚠️ 发布前还需做

- [ ] **设计 1 张封面图**：`images/cover-roadshow.png`（1200×630，基于源稿 `assets/logo-full.png` + `live-home.png`）
- [ ] **同步发布幻灯片资源页**：`/talks/data-agent-harness-roadshow`（HTML + PDF 同步上线，否则结尾"下载完整幻灯片"section 形同虚设）
- [ ] **schema.json / meta-tags.html 内嵌到 HTML `<head>`**
- [ ] **确认 4 条内链已发布**：3 篇姊妹文 + Databricks 外链
- [ ] **创始人作者页**：`/about/zhuhailin`（fix Ept02）
- [ ] **Q3 NDA 声明**：经销售 / 法务 review，避免承诺过度
- [ ] **演讲录像链接更新**：2026-06-15 后释出时回填

### 🎯 可选优化（v2，把分数推到 96+）

- [ ] 若拿到客户授权，把 Q3 中"某金融科技客户"替换为真实品牌名 —— 显著 lift A06 + 显著提升整体 GEO 引用率
- [ ] 加 2–3 张产品实拍截图（Task View / Data Source Management / RAG Research）—— 直接复用源稿 `assets/` 目录的截图即可
- [ ] 同步发英文版镜像（`/blog/data-agent-harness-roadshow-recap`）—— hreflang 已挂位

## 部署位置建议

```
https://infinisynapse.cn/zh/blog/data-agent-harness-roadshow-recap   (中文版，主战场)
https://infinisynapse.cn/blog/data-agent-harness-roadshow-recap      (英文版，建议补)
https://infinisynapse.cn/talks/data-agent-harness-roadshow           (HTML 幻灯片)
https://infinisynapse.cn/talks/data-agent-harness-roadshow.pdf       (PDF 幻灯片)
```

## 分发建议

| 渠道 | 用途 | 备注 |
|---|---|---|
| **官网博客 + 公众号** | 主分发 | 配合幻灯片资源页同步首发 |
| **MPD 峰会官方渠道** | 演讲后官方回顾文章 | 提前与 MPD 协调 cross-post 或反链 |
| **知乎专栏** | 长文友好平台 | 标题用 C 变体"从规划到证据链的可信答案生产线" |
| **LinkedIn 创始人个人账号** | 企业决策人触达 | 配合 Private 部署 ASCII 图 + 硬证据 3 数字 |
| **企业客户邮件 newsletter** | 已有客户教育 | 此文最适合做 enterprise lead 培育素材 |
| **销售支撑材料** | 配合销售拜访 | PDF 版本 + 关键章节摘录 |

## 发布后

| Skill | 用途 |
|---|---|
| `rank-tracker` | 监控 `Data Agent Harness 架构` / `企业级 Data Agent` / `InfiniSynapse 架构` |
| `geo-drift-check` | 1 个月后查 AI 引擎是否在"什么是 Data Agent harness"、"企业级 Data Agent 架构怎么搭"类查询中引用本文 |
| `backlink-analyzer` | 追踪 MPD 官方、行业 KOL 是否引用本文与原演讲 |
| `content-refresher` | 6 个月后用第二批客户案例 + 演讲录像更新 |

## 关键决策记录

- **Talk Recap 文体最佳实践**：每节给一段"演讲原话"blockquote + 一段文字化解释 + 一张表。这一结构兼顾"现场感"（GEO 友好）+ "可读性"（SEO 友好）。
- **ASCII 图替代图片**：源稿是 reveal.js 视觉重的幻灯片，但博客读者很多是手机 + 慢加载场景。把核心架构改写成 ASCII 图，让文字版独立成立。后续可选择性补真图作为增强。
- **dual schema（Event + isBasedOn）**：这是本文 GEO 分高于其他三篇的关键 —— AI 引擎会识别"这是某场真实演讲的整理"，提升内容权威信号。
- **不堆砌、不夸大**：硬证据三个数字 + 客户脱敏 + "愿 NDA 重现"开放姿态 = 比"行业领先"等空话有效得多。Trust 维度的真正护城河。
- **互链结构闭环**：本文（产品深度）+ 01（论证）+ 02（观点）+ 03（产品入口）形成内链回路。enterprise lead 从本文 → 03 接入产品 → 01/02 加深认同，路径清晰。

---

## 姊妹批次与 7 篇主题集群

> 本文属于 **2026-05-19 发布的 7 篇主题集群**（"AI-Native Data Analysis × Data Agent"），分两个互链批次：
>
> - **本批次（Data Agent 4 篇）**：[INDEX.md](../INDEX.md)
> - **姊妹批次（AI-Native 3 篇）**：[INDEX-ai-native-analysis.md](../INDEX-ai-native-analysis.md)

**本文角色**：**中文架构深度篇** —— 集群里最厚重的工程证据。姊妹批次 Pillar 提的 5 支柱、架构原理在本文里有"八件套"的硬实现描述。是企业决策人采购转化的关键节点。

**强联动文章**（已在 article.md 延伸阅读 区做互链）：

| 关系 | 文章 | Canonical URL |
|---|---|---|
| 同批次（论证）| 为什么 Code Agent 无法解决企业数据分析 | `/blog/why-code-agents-cannot-solve-enterprise-data-analysis` |
| 同批次（观点）| Data Agent 是驶向新文明的第一艘飞船 | `/zh/blog/data-agent-new-civilization` |
| 同批次（产品入口）| Connect Supabase to an AI Data Analyst | `/blog/connect-supabase-to-ai-data-agent` |
| 姊妹批次 Pillar | AI-Native Data Analysis: What It Means in 2026 | `/blog/ai-native-data-analysis` |
| 姊妹批次 Companion | Best AI Tools for Data Analysis in 2026 | `/blog/best-ai-tools-for-data-analysis` |
| 姊妹批次 Use-Case | How to Clean Excel Data with AI in 2026 | `/blog/ai-excel-data-cleaning` |
