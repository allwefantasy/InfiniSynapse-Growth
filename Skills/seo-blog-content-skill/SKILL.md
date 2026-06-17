---
name: seo-blog-content-skill
description: >-
  SEO/GEO 博客正文与质量门禁：≥5 高 DR 外链、11 项发布审计、EEAT、反 AI 模板、
  自适应关键词密度。写/改/审 SEO/Blog/pillar* article.md 时使用。
---

# SEO Blog Content Skill

> **活文档**：[`SEO/Blog/SKILL.md`](../../SEO/Blog/SKILL.md)（外链/内链/关键词/大纲）  
> **质量检验**：[`SEO/Blog/content-quality-gates.md`](../../SEO/Blog/content-quality-gates.md)（EEAT、字数密度、反模板、修复流程）  
> **技能库完整版**：[`Skills/seo-geo-claude-skills-main/build/seo-blog-content/SKILL.md`](../seo-geo-claude-skills-main/build/seo-blog-content/SKILL.md)

## 何时使用

- 写/改/审 `SEO/Blog/pillar1` … `pillar8` 的 `article.md`
- 批量质检 90 篇集群、修复 boilerplate、跑发布门禁
- 检查 EEAT、关键词密度、外链重合度、内链覆盖

## 发布门禁（90/90）

**11 项主审计 + EEAT 快扫**，全部 Pass；外链重合度 **0 violations**。

```bash
cd SEO/Blog
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  python3 $s.py || exit 1
done
```

| 维度 | 规则摘要 |
|------|----------|
| 外链 | ≥5 高 DR；叙事嵌入；重合度 ≤30%；见 [`SKILL.md`](../../SEO/Blog/SKILL.md) |
| 内链 | 叙事单链；Pillar/Cluster 最低覆盖；禁止 Related Reading |
| 关键词 | Target keyword 不可改；禁止 `this workflow`；title/desc 各 1 次 |
| 大纲 | 1×H1；H2+H3+H4 = 20–30 |
| 字数/密度 | **1900–2800** 词；密度按词数自适应（1–3 词 0.6–1.8%；4–5 词 0.35–1.5%；6+ 词 0.2–1.0%） |
| 内容质量 | 无重复句、无 AI 模板句、无 Pilot note 填充；FAQ ≥4 问 |
| EEAT | 署名 + Last updated 2026 + 一手信号（scorecard/指标/案例） |

## 反模板（零容忍）

```bash
python3 SEO/Blog/cleanup-pilot-note-filler.py      # Pilot/Operational note 行
python3 SEO/Blog/dedup-standalone-citations.py   # 重复 citation 句
python3 SEO/Blog/fix-this-workflow-placeholder.py  # this workflow → Target keyword
```

跨篇 filler H2（如 `Production Debugging Notes`）、`Within this topic cluster, explore…` 内链罗列 — **0 命中**。详见 [`content-quality-gates.md`](../../SEO/Blog/content-quality-gates.md) §3。

## 硬规则速查（14 条）

1. 外链 ≥5 高 DR · 2. 叙事嵌入 · 3. 分布正文前 85% · 4. 重合度 ≤30%
5. 禁止 `this workflow` · 6. Title/Desc 含完整 Target keyword · 7. 大纲 1×H1 + 20–30 标题
8–11. 内链规则（禁止 Related Reading / 叙事嵌入 / Pillar / Cluster）
12. 改文后 `build-preview.py` · 13. 跑 11 项门禁 · 14. fix 脚本跑后再人工通读

完整清单：[`hard-rules-quick-reference.md`](../seo-geo-claude-skills-main/build/seo-blog-content/references/hard-rules-quick-reference.md)

## 修复顺序

1. FAQ/标题 → 2. 关键词占位 → 3. boilerplate 清理 → 4. 内外链 → 5. 扩写/降密度 → 6. 同步 meta/schema/preview → 7. 全套门禁

Cursor 规则：`.cursor/rules/seo-blog-high-dr-citations.mdc`
