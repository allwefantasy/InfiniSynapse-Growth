# Audit and Fix Commands

Run from repository root (`InfiniSynapse-Growth/`).

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
```

## Publish gates (target 90/90 each)

**Primary 11 gates** (all required):

```bash
python3 "$S/audit-keyword-placeholder.py"
python3 "$S/audit-keyword-in-title-desc.py"
python3 "$S/audit-keyword-meta-stuffing.py"
python3 "$S/audit-outline-structure.py"
python3 "$S/audit-internal-links.py"
python3 "$S/audit-link-placement.py"
python3 "$S/audit-high-dr-links.py"
python3 "$S/audit-external-link-overlap.py"   # 0 violations / 4005 pairs
python3 "$S/audit-external-links.py"
python3 "$S/audit-content-quality.py"
python3 "$S/audit-wordcount.py"
```

**EEAT quick scan** (also 90/90):

```bash
python3 "$S/audit-eeat.py"
```

One-liner:

```bash
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  python3 "$S/$s.py" || exit 1
done
```

Optional:

```bash
python3 "$S/audit-inline-external-links.py"
```

Content quality rules: [content-quality-gates.md](content-quality-gates.md)

## Batch fixers (run matching audit after each)

Active fixers in `scripts/`:

```bash
python3 "$S/fix-this-workflow-placeholder.py"
python3 "$S/fix-meta-descriptions.py"
python3 "$S/fix-meta-title-length.py"
python3 "$S/fix-production-urls.py"
python3 "$S/cleanup-pilot-note-filler.py"
python3 "$S/dedup-standalone-citations.py"
```

Historical one-off fixers (Pillar 1–15 migrations) live in `scripts/_archive/` — e.g. `fix-internal-links.py`, `patch-high-dr-citations.py`, `weave-brand-keyword.py`. Run only with migration context.

**Vibe series (Pillar 16–20)**: see [reddit-geo-vibe-series-rules.md](reddit-geo-vibe-series-rules.md) §脚本流水线.

## Pillar 21–25 (Data Analysis cluster · 88 articles)

Scripts live in `scripts/` (`*-p21-25.py` / `*-p21-25.sh`). Metadata via `article-meta.json` + [`article_keyword_meta.py`](../scripts/article_keyword_meta.py).

```bash
# Visuals: HTML hero (H1 title) + body data tables
python3 "$S/build-visuals-p21-25.py" all
bash "$S/render-visuals-p21-25.sh" all          # heroes + tables → PNG
bash "$S/render-visuals-p21-25.sh" heroes       # force hero re-render

# Meta / schema
python3 "$S/gen-meta-schema-p21-25.py"

# Internal links (Library Model)
python3 "$S/fix-internal-links-p21-25.py"
python3 "$S/audit-internal-links-p21-25.py"

# Content cleanup
python3 "$S/fix-cleanup-p21-25.py"
python3 "$S/fix-header-stuffing-p21-25.py"
python3 "$S/strip-authoring-meta-p21-25.py"

# Keyword density advisor (P21–25)
python3 "$S/density-advisor.py" pillar21-data-analysis-fundamentals
```

# Pillar 21–25 (Data Analysis cluster · 88 articles)

```bash
# head.html + seo-meta.json (all pillars)
python3 "$S/generate-deploy-meta.py"

# sitemap = live base + pillar 16–20 + pillar 21–25
python3 "$S/build-sitemap.py"

# programmer zip (88 articles + sitemap.xml)
python3 "$S/build-p21-25-handoff-pack.py"
# → SEO/Blog/p21-25-handoff-pack.zip
```

## Preview regeneration

```bash
python3 SEO/Blog/pillarN-.../build-preview.py
```

Run for every pillar touched after body or meta edits.

## Pass standard

All **11 primary audits + `audit-eeat.py`** at **90/90 Pass**; external overlap at **0 violations**.
