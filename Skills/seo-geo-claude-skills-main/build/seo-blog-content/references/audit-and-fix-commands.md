# Audit and Fix Commands

Run from repository root (`InfiniSynapse-Growth/`).

## Publish gates (target 90/90 each)

**Primary 11 gates** (all required):

```bash
python3 SEO/Blog/audit-keyword-placeholder.py
python3 SEO/Blog/audit-keyword-in-title-desc.py
python3 SEO/Blog/audit-keyword-meta-stuffing.py
python3 SEO/Blog/audit-outline-structure.py
python3 SEO/Blog/audit-internal-links.py
python3 SEO/Blog/audit-link-placement.py
python3 SEO/Blog/audit-high-dr-links.py
python3 SEO/Blog/audit-external-link-overlap.py   # 0 violations / 4005 pairs
python3 SEO/Blog/audit-external-links.py
python3 SEO/Blog/audit-content-quality.py
python3 SEO/Blog/audit-wordcount.py
```

**EEAT quick scan** (also 90/90):

```bash
python3 SEO/Blog/audit-eeat.py
```

One-liner:

```bash
cd SEO/Blog && for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  python3 $s.py || exit 1; done
```

Optional:

```bash
python3 SEO/Blog/audit-inline-external-links.py
```

Content quality rules: [content-quality-gates.md](content-quality-gates.md)

## Batch fixers (run matching audit after each)

```bash
python3 SEO/Blog/fix-this-workflow-placeholder.py
python3 SEO/Blog/fix-keyword-in-title-desc.py
python3 SEO/Blog/fix-keyword-meta-natural.py
python3 SEO/Blog/fix-outline-structure.py
python3 SEO/Blog/fix-internal-links.py
python3 SEO/Blog/fix-external-link-overlap.py
python3 SEO/Blog/patch-high-dr-citations.py
python3 SEO/Blog/fix-faq-and-headers.py
python3 SEO/Blog/cleanup-pilot-note-filler.py
python3 SEO/Blog/dedup-standalone-citations.py
python3 SEO/Blog/reduce-keyword-density.py
python3 SEO/Blog/weave-brand-keyword.py
python3 SEO/Blog/expand-topic-section.py
python3 SEO/Blog/expand-topic-section2.py
```

## Preview regeneration

```bash
python3 SEO/Blog/pillarN-.../build-preview.py
```

Run for every pillar touched after body or meta edits.

## Pass standard

All **11 primary audits + `audit-eeat.py`** at **90/90 Pass**; external overlap at **0 violations**.
