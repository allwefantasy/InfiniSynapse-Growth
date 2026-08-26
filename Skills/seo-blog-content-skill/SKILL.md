---
name: seo-blog-content-skill
description: >-
  SEO/GEO 博客正文与质量门禁：≥5 高 DR 外链、11 项发布审计、EEAT、反 AI 模板、
  自适应关键词密度；Pillar 16–20 Vibe 系列另含 Reddit GEO 三规则与 301 部署。
  写/改/审 SEO/Blog/pillar* article.md 时使用。
---

# SEO Blog Content Skill

> **完整硬规则**：[`infinisynapse-blog-full-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/infinisynapse-blog-full-rules.md)（外链/内链/关键词/大纲/On-Page/Sitemap）  
> **Pillar Hub 终极指南框架**（Hub = 落地页，禁止薄索引）：[`pillar-hub-ultimate-guide-framework.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/pillar-hub-ultimate-guide-framework.md)  
> **质量检验**：[`content-quality-gates.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/content-quality-gates.md)（EEAT、字数密度、反模板、修复流程）  
> **问题与修复活文档**（踩坑默认追加，无需用户要求）：[`seo-content-learnings-log.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/seo-content-learnings-log.md)  
> **Vibe 交付说明**：[`vibe-coding-series-handoff.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/vibe-coding-series-handoff.md)  
> **Reddit GEO · Vibe 系列（Pillar 16–20）**：[`reddit-geo-vibe-series-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/reddit-geo-vibe-series-rules.md)（三规则、97/97 门禁、脚本流水线、301 重定向）  
> **部署规则**（前端/CMS/On-Page 交付标准，build 脚本从此处取用为交付物模板）：
> [`FRONTEND-DEPLOY-GUIDE.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/FRONTEND-DEPLOY-GUIDE.md) ·
> [`PROGRAMMER-SEO-DEPLOY.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/PROGRAMMER-SEO-DEPLOY.md) ·
> [`QUICKCREATOR-SEO-FIX.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/QUICKCREATOR-SEO-FIX.md)  
> **配图规则**（HTML 模板 → Chrome headless 截图 → PNG 工作流）：
> [`image-generation-guide.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/image-generation-guide.md)
> ；脚本 `scripts/`：`copy-source-images.sh` · `render-html-to-png.sh` · `generate-cover-image-ai.sh` · `cover-prompt.template`  
> **正文数据图硬规则**（`chart-*.png` 必须 ≥2 数据维度；禁止单调 Before/After 两根柱）：
> [`body-data-chart-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/body-data-chart-rules.md)  
> ；脚本：`gen-data-charts-p26-30.py` · `overlay-hero-titles-p26-30.py`  

> **文件布局**（规则文档 / 脚本放哪、SEO/Blog 只放产物）：
> [`skill-file-layout.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/skill-file-layout.md)  
> **技能库完整版**：[`Skills/seo-geo-claude-skills-main/build/seo-blog-content/SKILL.md`](../seo-geo-claude-skills-main/build/seo-blog-content/SKILL.md)

## 何时使用

- 写/改/审 `SEO/Blog/pillar1` … `pillar8` 的 `article.md`
- 写/改/审 **Vibe Coding 系列** `pillar16` … `pillar20`（97 篇，含 Reddit GEO）
- 批量质检 90/97 篇集群、修复 boilerplate、跑发布门禁
- 检查 EEAT、关键词密度、外链重合度、内链覆盖

## 发布门禁（90/90）

**11 项主审计 + EEAT 快扫**，全部 Pass；外链重合度 **0 violations**。

脚本已随技能库一起存放（产物仍写回 `SEO/Blog/`）：

> **布局铁律**：规则 → `references/`；脚本 → `scripts/`；**禁止**在 `SEO/Blog/` 根目录新增规则或脚本。见 [`skill-file-layout.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/skill-file-layout.md)。

```bash
# 从仓库根目录运行；脚本自动定位 SEO/Blog 内容与产物
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  python3 "$S/$s.py" || exit 1
done
```

| 维度 | 规则摘要 |
|------|----------|
| 外链 | ≥5 高 DR；叙事嵌入；重合度 ≤30%；见 [`SKILL.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/infinisynapse-blog-full-rules.md) |
| 内链 | **双向索引(图书馆模型)**：Pillar→链全部 Cluster，每篇 Cluster→链回 Pillar+≥2 兄弟；叙事单链；禁止 Related Reading；URL 用 `/en/blog/{slug}` |
| 关键词 | Target keyword 不可改；禁止 `this workflow`；title/desc 各 1 次 |
| 大纲 | 1×H1；H2+H3+H4 = 20–30 |
| 字数/密度 | **1900–2800** 词；密度下限 **≥1.2%**（新集群 21–25：1–3 词 1.2–1.8%；4–5 词 1.2–1.6%；6+ 词 1.2–1.4%）；16–20 旧文 ≥1.0% 兼容 |
| 内容质量 | 无重复句、无 AI 模板句、无 Pilot note 填充；FAQ ≥4 问 |
| EEAT | 署名 + Last updated 2026 + 一手信号（scorecard/指标/案例） |
| 正文数据图 | `chart-*.png` **≥2 数据维度**（分组柱/多系列线/堆叠等）；禁止单指标 Before/After 两根柱；见 [`body-data-chart-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/body-data-chart-rules.md) |

## On-Page / CMS 发布合规（5 项）

经 CMS（QuickCreator）/ headless 前端发布时，On-Page 检查器要求每页满足 5 项。**两层模型**：源 `article.md` 保留 **1×H1**（作者门禁依赖）；发布层 body **去 H1**（页面 H1 由标题渲染）。

| # | 要求 | 落点 |
|---|------|------|
| 1 | Canonical 必有、无尾斜杠 | `https://infinisynapse.com/en/blog/{slug}` |
| 2 | 页面仅 **1 个 H1**；发布 body 无 H1；禁止「平台标题 H1 + 正文 H1」 | 发布层 article.md |
| 3 | Meta 描述 **150–160 字符**（严格、完整句、跨篇不重复） | md `**Meta Description**` + meta-tags(desc/og/twitter) + schema + head.html |
| 4 | 社交标签齐全（og:* + twitter:*） | meta-tags.html / head.html / seo-meta.json |
| 5 | Meta `<title>` **40–60 字符**且含关键词；H1/headline 可较长（保留完整关键词） | `fix-meta-title-length.py` 改 `<title>`+og/twitter title，不动 H1/schema |

> 第 5 项与「Title 必含完整关键词」的关系：`<title>` 是 SEO 标题（40–60），H1 是展示标题（可长）。两者都须含关键词；若关键词本身 >58 字符，保留完整关键词、接受 `<title>` 超长（QC 黄色警告）。
>
> **关键认知**：canonical / description / og / twitter 即使源文件正确，**线上仍可能报错**——因为 CMS/前端没把每篇 `head.html` 注入 `<head>`（实测线上 description 会退回站点默认）。务必让部署注入每篇 `head.html` 或 `seo-meta.json` 字段。

程序员产物：每篇 `head.html`（`<head>` 片段 + JSON-LD）+ `seo-meta.json`（按 slug，供 Next.js/SSR/API 注入）。

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/fix-meta-descriptions.py"     # 描述归一化 150–160（幂等，同步五处）
python3 "$S/fix-production-urls.py"        # 域名 .com + /en/blog/ 路径（幂等）
python3 "$S/fix-meta-title-length.py"      # <title> 改 40–60 含关键词（不动 H1/schema）
python3 "$S/generate-deploy-meta.py"       # 生成 head.html + seo-meta.json
python3 "$S/generate-cms-import-csv.py" && python3 "$S/generate-blog-index-master.py"
python3 "$S/build-frontend-handoff.py"     # 交付包：body 去 H1 + 带 head.html/seo-meta.json
python3 "$S/build-frontend-package.py"     # catalog 包（程序员用）
python3 "$S/audit-quickcreator-onpage.py"  # 发布层 5 项（审计 frontend-handoff/content）
```

**禁止**：直接对源 `article.md` 删 H1（会挂 outline/keyword 门禁，去 H1 只在发布层）。详见 [`infinisynapse-blog-full-rules.md` § On-Page/CMS 发布合规](../seo-geo-claude-skills-main/build/seo-blog-content/references/infinisynapse-blog-full-rules.md)。

## Sitemap（站点地图）

新增/更新文章后须重生成 `sitemap.xml` 并交付程序员替换线上 `https://infinisynapse.com/sitemap.xml`。

| 规则 | 说明 |
|---|---|
| **完整域名 + locale** | 博客 URL 用 canonical：`https://infinisynapse.com/en/blog/{slug}`（与 head canonical 一致，无尾斜杠） |
| **保留老 URL** | 现有非博客 URL（`use-cases/*`、`guides/*`）**原样保留** lastmod/priority，禁止覆盖 |
| **lastmod** | 取自各文 `schema.json` 的 `dateModified`（脚本自动） |
| **priority** | Hub/Pillar 页 0.9，其余 0.7；老页沿用原值 |
| **changefreq** | 博客 weekly；老页沿用原值 |
| **只含已上线 200 的 URL** | 未上线/会 404 的不放（对照 `部署清单-完整URL.csv`）；**中文 `/zh/blog/` 未上线则不收录** |
| **robots.txt** | 含 `Sitemap: https://infinisynapse.com/sitemap.xml` |

```bash
python3 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/build-sitemap.py   # 合并老 URL + 100 篇新博客 → SEO/Blog/sitemap.xml（XML 自校验）
```

老 URL 清单内嵌在脚本 `EXISTING` 常量（站点结构变化时同步更新）。生成后 GSC → Sitemaps 重新提交。

## 反模板（零容忍）

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/cleanup-pilot-note-filler.py"      # Pilot/Operational note 行
python3 "$S/dedup-standalone-citations.py"     # 重复 citation 句
python3 "$S/fix-this-workflow-placeholder.py"  # this workflow → Target keyword
```

跨篇 filler H2（如 `Production Debugging Notes`）、`Within this topic cluster, explore…` 内链罗列 — **0 命中**。详见 [`content-quality-gates.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/content-quality-gates.md) §3。

## 硬规则速查（15 条）

1. 外链 ≥5 高 DR · 2. 叙事嵌入 · 3. 分布正文前 85% · 4. 重合度 ≤30%
5. 禁止 `this workflow` · 6. Title/Desc 含完整 Target keyword · 7. 大纲 1×H1 + 20–30 标题
8–11. 内链规则（禁止 Related Reading / 叙事嵌入 / Pillar / Cluster）
12. 改文后 `build-preview.py` · 13. 跑 11 项门禁 · 14. fix 脚本跑后再人工通读
15. **正文数据图 ≥2 维度**（禁止单调 Before/After 两根柱）

完整清单：[`hard-rules-quick-reference.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/hard-rules-quick-reference.md) · 数据图细则：[`body-data-chart-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/body-data-chart-rules.md)

## 修复顺序

1. FAQ/标题 → 2. 关键词占位 → 3. boilerplate 清理 → 4. 内外链 → 5. 扩写/降密度 → 6. 同步 meta/schema/preview → 7. 全套门禁 → **8. 问题入库**（见下）

## 问题与修复 · 默认入库

修复审计/部署/脚本类问题后，**同一会话内**追加到 [`seo-content-learnings-log.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/seo-content-learnings-log.md)，无需用户再次要求。

| 步骤 | 动作 |
|------|------|
| 1 | 按模板写：场景 / 症状 / 根因 / 修复 / 防复发 |
| 2 | 重复 ≥2 次或影响门禁 → 提升到 `content-quality-gates.md` 等硬规则，log 标 `promoted` |
| 3 | 更新 log 底部索引表 |

Cursor 规则：`.cursor/rules/seo-content-learnings-capture.mdc` · `.cursor/rules/seo-blog-high-dr-citations.mdc`

## Vibe Coding 系列 · Reddit GEO（Pillar 16–20）

完整规则：[`reddit-geo-vibe-series-rules.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/reddit-geo-vibe-series-rules.md)

| 规则 | 摘要 |
|------|------|
| **Rule 1** | Target keyword + ` reddit`；H1/title/desc/slug 同步；slug 后缀 `-reddit` |
| **Rule 2** | TL;DR 内 `> **Direct answer:**` 倒金字塔；前 30% 可独立引用 |
| **Rule 3** | 第一人称 Reddit research hook；byline _builder 帖_ 语气 |
| **正文密度** | 以规划表**核心词**计（非 `{core} reddit`）；H1/meta/Direct answer 保留完整 Target keyword |

**Pass bar**：97/97（同一套 11+EEAT 审计）。Vibe 脚本在技能库 `scripts/`（`upgrade-vibe-reddit-geo.py`、`tune-vibe-reddit-density.py`、`fix-vibe-all-audits.py`、`generate-vibe-reddit-301-redirects.py`）。

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
# 内容修改后（勿重复跑 upgrade）
python3 "$S/boost-vibe-core-keyword-density.py"   # 正文 weave 核心词
python3 "$S/tune-vibe-reddit-density.py"
python3 "$S/fix-vibe-all-audits.py"
python3 "$S/build-vibe-handoff-pack.py"
python3 "$S/generate-vibe-reddit-301-redirects.py"   # slug 变更部署前
```

**手改轻触**：203 · 204 · 206 · 218 · 221 · 223 · 224。**无 Reddit slug 例外**：250 · 252 · 262。
