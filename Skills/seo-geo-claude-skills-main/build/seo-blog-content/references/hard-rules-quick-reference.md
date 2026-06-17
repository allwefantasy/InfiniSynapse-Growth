# Hard Rules Quick Reference

Canonical live copy: [`SEO/Blog/SKILL.md`](../../../../SEO/Blog/SKILL.md). Update both when rules change.

## Checklist (14 items)

1. **External count** — each `article.md` has ≥ **5** unique high-DR external URLs (`high-dr-authority-sources.py`).
2. **External embed** — descriptive anchor + full English sentence; no `## Sources`, bare URL lists, or bare URL anchors.
3. **External placement** — links in the first **85%** of body; not clustered in Evaluation basis blocks only.
4. **External overlap** — `|A∩B|/min(|A|,|B|)` ≤ **30%** across all 90 articles (`audit-external-link-overlap.py` → 0 violations); fix with `fix-external-link-overlap.py`.
5. **Target keyword** — use `**Target keyword**` naturally in body; ban `this workflow` / `this connector workflow` (>1 → Fail).
6. **Title & Description** — full Target keyword phrase in H1, `<title>`, `**Meta Description**:`, and `meta-tags.html` description (sync `schema.json`). **Never change** the planning-table keyword. One keyword occurrence per title and per description; no stuffing templates.
7. **Outline** — **1×H1**; **H2+H3+H4 = 20–30**; H3 under H2, H4 under H3; no filler duplicate sections.
8. **Internal links · ban** — no `## Related Reading`, template bullets, or `Within this topic cluster, explore [A], [B], [C]…` list paragraphs.
9. **Internal links · embed** — one `/blog/` link per narrative sentence; max 2 internal links per paragraph.
10. **Internal links · Pillar Page** — link all other Pillar Pages in the cluster; single-hub pillars also link every Cluster Page.
11. **Internal links · Cluster Page** — link primary hub + ≥2 cluster siblings.
12. **Preview** — rerun `build-preview.py` after `article.md` changes.
13. **Audit gates** — **11 scripts + `audit-eeat.py`** at 90/90; see [audit-and-fix-commands.md](audit-and-fix-commands.md) and [content-quality-gates.md](content-quality-gates.md).
14. **Fix scripts** — `fix-outline-structure.py`, `fix-keyword-in-title-desc.py`, `fix-keyword-meta-natural.py`, `patch-high-dr-citations.py`, `fix-external-link-overlap.py`, `fix-internal-links.py`, `fix-this-workflow-placeholder.py` (human read-through after batch fixes).

Cursor rule: `.cursor/rules/seo-blog-high-dr-citations.mdc`
