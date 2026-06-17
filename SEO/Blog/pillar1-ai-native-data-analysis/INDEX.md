# Pillar 1 · AI-Native Data Analysis — 13 篇发布包总览

> 基于 `SEO/100页主题集群规划-v1-替换后主关键词版.md` 中 **Pillar 1（001–013）** 生成。全流程遵循 `Skills/seo-geo-claude-skills-main/`（seo-content-writer → meta-tags-optimizer → schema-markup-generator → content-quality-auditor）。**生成日期：2026-06-08**。
>
> **交付形态**：每篇一个独立文件夹，前端可直接按 slug 部署。详见 [DEPLOY.md](./DEPLOY.md)。

## 集群定位

| 字段 | 值 |
|---|---|
| Pillar 主题 | AI-Native Data Analysis |
| 文章数 | 13 |
| 语言 | 英文 |
| 品类锚点（已有） | [/blog/ai-native-data-analysis](../native-data-analysis/) |
| 平均审计分 | 91.5 / 100（全部 SHIP） |
| 总 FAQ 数 | 78（13 × 6） |

## 13 篇文章索引

| # | 文件夹 | Slug | 主关键词 | Vol | KD | 类型 | 审计 |
|---|---|---|---|---:|---:|---|---:|
| 001 | [001-ai-for-data-analysis](./001-ai-for-data-analysis/) | `/blog/ai-for-data-analysis` | ai for data analysis | 3600 | 58 | 指南 | 92 |
| 002 | [002-data-agent-manifesto](./002-data-agent-manifesto/) | `/blog/data-agent-manifesto` | data agent | 210 | 47 | 宣言 | 93 |
| 003 | [003-what-is-a-data-agent](./003-what-is-a-data-agent/) | `/blog/what-is-a-data-agent` | what is a data agent | 20 | 29 | What-is | 94 |
| 004 | [004-ai-native-data-platform](./004-ai-native-data-platform/) | `/blog/ai-native-data-platform` | ai-native data platform | 10 | 17 | 买家指南 | 91 |
| 005 | [005-best-agentic-analytics](./005-best-agentic-analytics/) | `/blog/best-agentic-analytics` | best agentic analytics for data-driven insights | 110 | 5 | 列表评测 | 92 |
| 006 | [006-autonomous-data-agent](./006-autonomous-data-agent/) | `/blog/autonomous-data-agent` | autonomous data agent | 10 | 21 | What-is | 93 |
| 007 | [007-ai-data-analyst](./007-ai-data-analyst/) | `/blog/ai-data-analyst` | ai data analyst | 390 | 59 | 角色指南 | 91 |
| 008 | [008-ai-data-analyst-job-description](./008-ai-data-analyst-job-description/) | `/blog/ai-data-analyst-job-description` | ai data analyst job description | 20 | 22 | 招聘模板 | 94 |
| 009 | [009-data-agent-memory](./009-data-agent-memory/) | `/blog/data-agent-memory` | data agent (memory) | 210 | 47 | 深度专题 | 92 |
| 010 | [010-fabric-data-agent-vs-copilot](./010-fabric-data-agent-vs-copilot/) | `/blog/fabric-data-agent-vs-copilot` | fabric data agent vs copilot | 10 | — | 对比页 | 91 |
| 011 | [011-ai-native-vs-augmented-analytics](./011-ai-native-vs-augmented-analytics/) | `/blog/ai-native-vs-augmented-analytics` | ai-native data platform | 10 | 17 | 对比页 | 93 |
| 012 | [012-ai-data-analysis](./012-ai-data-analysis/) | `/blog/ai-data-analysis` | ai data analysis | 2900 | 56 | 头部指南 | 94 |
| 013 | [013-data-agent-glossary](./013-data-agent-glossary/) | `/blog/data-agent-glossary` | what is a data agent (glossary) | 20 | 29 | 术语表 | 90 |

## 关键词分层（不抢量）

```
头部流量（001, 012）     ai for data analysis / ai data analysis
        │
品类教育（003, 004, 006, 011, 013）  data agent / ai-native platform / glossary
        │
商业意图（005, 007, 008, 010）       agentic analytics / ai data analyst / JD / Fabric vs Copilot
        │
品牌叙事（002, 009）                 manifesto / memory distillation
        │
已有 Pillar 锚点                     /blog/ai-native-data-analysis（5 支柱定义）
```

## 内链拓扑

```
                    ┌─────────────────────────────┐
                    │ 已有 Pillar（品类定义）      │
                    │ /blog/ai-native-data-analysis│
                    └──────────────┬──────────────┘
                                   │
     ┌─────────────┬───────────────┼───────────────┬─────────────┐
     ▼             ▼               ▼               ▼             ▼
  001 头部      012 头部        003 定义         013 术语表    002 宣言
  ai for       ai data         what is          glossary      manifesto
  data analysis analysis        data agent
     │             │               │               │             │
     └─────────────┴───────┬───────┴───────────────┴─────────────┘
                           ▼
              004 平台 / 005 评测 / 006 自治 / 007 角色 / 008 JD
              009 记忆 / 010 Fabric对比 / 011 Augmented对比
                           │
                           ▼
              姊妹集群（已有）
              /blog/best-ai-tools-for-data-analysis
              /blog/why-code-agents-cannot-solve-enterprise-data-analysis
              /blog/data-agent-new-civilization
```

## 每篇文件清单（统一结构）

```
NNN-<slug>/
├── article.md        ← 正文（Markdown，含 frontmatter 元数据块）
├── meta-tags.html    ← <head> 标签包（title/desc/OG/Twitter/hreflang）
├── schema.json       ← JSON-LD（BlogPosting + FAQPage + BreadcrumbList）
├── audit.md          ← CORE-EEAT 审计报告（SHIP 门禁）
├── README.md         ← 单篇交付说明
└── images/           ← 图片目录（.gitkeep，待设计 hero）
```

## 发布前 Checklist（站点层面）

### ✅ 内容层已完成

- [x] 13 × `article.md`（byline / TL;DR / TOC / FAQ / Related Reading）
- [x] 13 × `meta-tags.html`（canonical + hreflang + OG + Twitter）
- [x] 13 × `schema.json`（FAQPage 全覆盖；003 + 013 含 DefinedTermSet）
- [x] 13 × `audit.md`（全部 SHIP，无 veto）
- [x] 13 × `README.md`
- [x] 集群内互链 + 链到已有 Pillar / 姊妹文章

### ⚠️ 前端 / 设计待办

- [ ] 设计 13 组 hero 图（1200×630，见各 `article.md` 首图引用）
- [ ] CMS 注册 13 个 slug（见 [manifest.json](./manifest.json)）
- [ ] 将 `meta-tags.html` + `schema.json` 内嵌到页面 `<head>`
- [ ] Markdown → HTML 渲染（保留 heading id 以匹配 TOC 锚点）
- [ ] 上传图片到 CDN，更新 schema `image` URL 与 OG `og:image`
- [ ] 确认 `/about` 页面存在（schema `author.url` 引用）
- [ ] 首发后跑 `domain-authority-auditor`

## 建议发布节奏

| 批次 | 文章 | 理由 |
|---|---|---|
| **Wave 1** | 012, 001 | 头部词抢位（ai data analysis + ai for data analysis） |
| **Wave 2** | 003, 013, 006 | 定义层 + 术语表（GEO 引用友好） |
| **Wave 3** | 007, 008, 005 | 角色 + 招聘 + 商业评测 |
| **Wave 4** | 004, 011, 010 | 平台买家 + 对比页 |
| **Wave 5** | 002, 009 | 品牌叙事 + 记忆专题 |

## 与 100 页规划的对应

| 规划编号 | 本批次文件夹 | 备注 |
|---|---|---|
| 001 | 001-ai-for-data-analysis | 主词替换为 ai for data analysis |
| 002 | 002-data-agent-manifesto | 主词 data agent，manifesto 角度 |
| 003 | 003-what-is-a-data-agent | 精确匹配 |
| 004 | 004-ai-native-data-platform | 精确匹配 |
| 005 | 005-best-agentic-analytics | 主词替换 |
| 006 | 006-autonomous-data-agent | 精确匹配 |
| 007 | 007-ai-data-analyst | 精确匹配 |
| 008 | 008-ai-data-analyst-job-description | 精确匹配 |
| 009 | 009-data-agent-memory | data agent 记忆角度 |
| 010 | 010-fabric-data-agent-vs-copilot | 对比页 |
| 011 | 011-ai-native-vs-augmented-analytics | ai-native platform 承接 |
| 012 | 012-ai-data-analysis | 主词替换 |
| 013 | 013-data-agent-glossary | glossary 场景 |
