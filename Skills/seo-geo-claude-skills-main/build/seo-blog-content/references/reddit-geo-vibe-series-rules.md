# Reddit GEO · Vibe Coding 系列规则（Pillar 16–20）

> **适用范围**：`SEO/Blog/pillar16-vibe-coding-workflow` … `pillar20-data-api-production-readiness`（97 篇，ID 203–299）。  
> **基础门禁**：仍遵守 [`content-quality-gates.md`](content-quality-gates.md) 与 [`infinisynapse-blog-full-rules.md`](infinisynapse-blog-full-rules.md)；本文只补充 Reddit GEO 增量规则与脚本流水线。

---

## 三条 Reddit GEO 规则

### Rule 1 · 关键词与 URL 含 Reddit

| 字段 | 要求 |
|------|------|
| **Target keyword** | 在规划表关键词末尾追加 ` reddit`（小写、空格分隔） |
| **H1** | 含完整 Reddit 关键词；格式 `{Title Case Keyword}: {副标题}` |
| **Meta Description** | 以 Title Case 关键词开头；仍须含完整 Target keyword 一次 |
| **Slug** | `/blog/{原 slug}-reddit`（仅追加一次 `-reddit`，禁止 `-reddit-reddit`） |
| **Canonical** | `https://infinisynapse.com/en/blog/{slug}-reddit` |

**示例**

- Keyword: `vibe coding checklist reddit`
- H1: `# Vibe Coding Checklist Reddit: Best Practices Before You Add Integrations`
- Slug: `/blog/vibe-coding-checklist-reddit`

**例外（仅应用 Rule 2 + 3，不改 keyword/slug）**

字面 `reddit` 在 URL/标题中 SEO 价值低的长尾技术词：

| ID | 原 keyword |
|----|------------|
| 250 | `database application programming interface` |
| 252 | `webhook relay service api data model` |
| 262 | `prod system` |

### Rule 2 · LLM 友好结构（倒金字塔）

在 `## TL;DR` 标题后、正文展开前插入 **Direct answer** 块：

```markdown
## TL;DR

> **Direct answer:** {一句话直接回答，含完整 **target keyword reddit**}

{第一人称 Reddit 研究 hook} here is what held up in production—not the hype comments.

{原有 TL;DR 要点…}
```

要求：

- **Direct answer** 放在 TL;DR 最前（文章前 30% 内给出可引用结论）
- 答案须可独立被 LLM/摘要抓取，避免「见下文」式拖延
- 保留原有 TL;DR bullet 列表，Direct answer 是增量而非替换

### Rule 3 · Reddit 口吻开场

| 元素 | 规则 |
|------|------|
| **Byline 副句** | `*We build InfiniSynapse and write these notes like a builder posting after a Reddit thread—not a brochure for…*` |
| **Research hook** | 第一人称 + 具体数字 + 子版块（如 r/Cursor、r/webdev、r/LocalLLaMA） |
| **语气** | _builder 复盘帖_，非企业白皮书；少用「leverage」「synergy」类套话 |

Hook 模板（轮换使用，避免全系列同句）：

- `I read {n} threads on r/Cursor, r/vibecoding, and r/SideProject while shipping InfiniSynapse—`
- `After skimming {n}+ Reddit posts that actually shipped (not just demo gifs), `
- `I pulled {n} Reddit discussions from r/webdev and r/LocalLLaMA while we hardening production APIs—`
- `From {n} Reddit build logs I archived this quarter, `

---

## 发布门禁（97/97）

Vibe 系列沿用 Pillar 1–8 同一套审计脚本，Pass 标准为 **97/97**：

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  python3 "$S/$s.py" || exit 1
done
```

| 维度 | 规则 |
|------|------|
| 字数 | **1900–2800** 词（自 `## TL;DR` 起算） |
| 密度 | **正文以规划表核心词计**（`blog-vibe-coding-topics-plan.csv`）；H1/meta/slug 仍用完整 `{core} reddit`。**下限 ≥1.0%**（必须超过 1% 以下区间）：1–3 词 1.0–1.8%；4–5 词 1.0–1.5%；6+ 词 1.0–1.2% |
| 高 DR 外链 | ≥5；叙事嵌入；分布正文前 85% |
| 外链重合度 | ≤30%（pairwise） |
| EEAT | 署名 + Last updated + FAQ ≥4 问（`### …?` 格式） |
| keyword-in-title-desc | H1 + Meta Description 各含完整 Target keyword |

---

## 脚本流水线（`Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/`）

### 一次性 Reddit GEO 升级

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/upgrade-vibe-reddit-geo.py"
```

作用：Rule 1–3 批量应用；更新 `articles_registry.json`；全局替换内链 slug。

> **禁止重复运行** `upgrade-vibe-reddit-geo.py`（slug 逻辑虽幂等，但全局 replace 有污染风险）。

### 内容修改后的安全顺序

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/fix-vibe-citation-integrity.py"   # 锚文本↔URL 对齐（overlap 后必跑）
python3 "$S/fix-vibe-semantic-citations.py"   # 重复 URL / 语境错配
python3 "$S/boost-vibe-core-keyword-density.py"   # 正文改 weave 核心词（0.6–1.0% 带）
python3 "$S/tune-vibe-reddit-density.py"        # 字数 + 密度校准
python3 "$S/fix-vibe-all-audits.py"             # 高 DR / EEAT / FAQ / H1 / meta 同步
# 若 title/desc/slug 变更，upgrade 脚本内的 sync_meta 逻辑或手动同步 meta-tags.html / schema.json
python3 "$S/build-vibe-handoff-pack.py"         # 重建交付 zip
```

**不要**在 dedupe 后单独跑 `tune-vibe-audit-gates.py` 而不接 `fix-vibe-all-audits.py`（会丢失高 DR / EEAT 修复）。

### 专项修复脚本

| 脚本 | 用途 |
|------|------|
| `tune-vibe-reddit-density.py` | Reddit 关键词加长后的密度/字数校准；修复 `reddit reddit` 重复 |
| `fix-vibe-all-audits.py` | 高 DR、FAQ 标题、TOC、H1 特例、meta 同步、去 tune filler |
| `fix-vibe-overlap.py` | 外链 URL 轮换降重合度（**慎用**：过度轮换可能破坏 high-DR 门禁） |
| `repair-reddit-slug-corruption.py` | 修复 `-reddit-reddit` / 错误 slug 段 |
| `fix-vibe-citation-integrity.py` | **锚文本↔URL 对齐**（overlap 轮换后必跑） |
| `fix-vibe-semantic-citations.py` | 同一 URL 重复使用、语境错配 |
| `restore-vibe-pillar-folders.py` | 从 handoff pack 恢复 `SEO/Blog/pillar16–20/` |
| `fix-vibe-hand-polished-links.py` | 手改文章（203/204/206/218/221/223/224）内链 |
| `generate-vibe-reddit-301-redirects.py` | 生成旧 slug → `-reddit` 的 301 映射 |

### 手改文章（轻触）

以下 7 篇经人工润色，批量脚本应跳过或最小 diff：

`203-api-integration-services` · `204-integration-software` · `206-api-integration-tools` · `218-manage-multiple-api-integrations` · `221-api-integration-testing` · `223-agentic-orchestration` · `224-tool-calling`

`fix-vibe-all-audits.py` 内 `H1_FIXES` 对 284/294/232/252 有固定 H1；改 H1 时同步更新该映射。

---

## 301 重定向（slug 变更部署）

94 篇 slug 追加 `-reddit` 后须部署 301（3 篇例外无 redirect）：

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/generate-vibe-reddit-301-redirects.py"
```

产物：

| 文件 | 内容 |
|------|------|
| `SEO/Blog/vibe-reddit-301-redirects.csv` | id、old/new slug、en/zh URL、canonical |
| `SEO/Blog/vibe-reddit-301-redirects.nginx.conf` | nginx `rewrite … permanent`（en + zh） |

**部署顺序**

1. 发布新 slug 文章与更新后的 `head.html` / `meta-tags.html` / `schema.json`
2. 上线 301（nginx / Vercel / Cloudflare 按 CSV 配置）
3. 重生成 `blog-index-import-master.json`、`sitemap.xml`、`seo-meta.json`
4. GSC 重新提交 sitemap；观察旧 URL 抓取与索引迁移

---

## 常见故障与修复

| 症状 | 原因 | 修复 |
|------|------|------|
| slug 出现 `-reddit-reddit-reddit` | 全局 replace 匹配 slug 前缀 | `repair-reddit-slug-corruption.py` |
| 正文 `reddit reddit` | bulk keyword 同步重复 | `tune-vibe-reddit-density.py` |
| keyword-in-title 失败 | `meta-tags.html` 未同步 | `upgrade-vibe-reddit-geo.sync_meta` 或 `fix-vibe-all-audits.py` |
| 密度超标（+` reddit` 后） | 关键词变长、出现次数不变 | `tune-vibe-reddit-density.py` |
| high-DR 失败 | `fix-vibe-overlap.py` 轮换全部 URL | 回滚后用 `fix-vibe-all-audits.py` 恢复 |
| 字数跌破 1900 | 激进 dedupe / 删 filler | 禁止全文段 dedupe；仅 dedupe tune filler 与 weave 模板 |

---

## 交付物

| 产物 | 路径 |
|------|------|
| Handoff 包 | `SEO/Blog/vibe-coding-handoff-pack.zip`（`build-vibe-handoff-pack.py`，脚本在 Skills `scripts/`） |
| 301 映射 | `SEO/Blog/vibe-reddit-301-redirects.csv` |
| Pillar registry | 各 pillar 下 `articles_registry.json` |

---

## 与通用 SEO 规则的关系

- **Target keyword 不可擅自改写**——Reddit 升级是在规划词末尾追加 ` reddit`，不是换词。
- **内链**仍用 `/en/blog/{slug}`；slug 变更后须全局更新（upgrade 脚本已处理源目录，handoff 须重建）。
- **On-Page 5 项**、Sitemap、CMS head 注入规则不变，见 [`FRONTEND-DEPLOY-GUIDE.md`](FRONTEND-DEPLOY-GUIDE.md)。
