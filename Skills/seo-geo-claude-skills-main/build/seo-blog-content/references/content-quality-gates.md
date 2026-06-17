# Content Quality Gates (InfiniSynapse Blog)

Canonical live copy: [`SEO/Blog/content-quality-gates.md`](../../../../SEO/Blog/content-quality-gates.md). Update both when rules change.

## Pass bar

- **11 audit scripts** at **90/90 Pass** each
- **`audit-eeat.py`**: 90/90 (12/12 quick scan)
- **`audit-external-link-overlap.py`**: **0 violations / 4005 pairs**

## Gate list

| Script | Checks |
|--------|--------|
| `audit-keyword-placeholder.py` | No `this workflow` replacing Target keyword |
| `audit-keyword-in-title-desc.py` | Full keyword in H1 + both descriptions |
| `audit-keyword-meta-stuffing.py` | One keyword per title/desc; no templates |
| `audit-outline-structure.py` | 1×H1; 20–30×(H2/H3/H4) |
| `audit-internal-links.py` | Contextual cluster links; no Related Reading |
| `audit-link-placement.py` | Narrative embed; first 85% of body |
| `audit-high-dr-links.py` | ≥5 unique DR≥70 URLs |
| `audit-external-link-overlap.py` | Pairwise overlap ≤30% |
| `audit-external-links.py` | HTTP 200; count ≥5 |
| `audit-content-quality.py` | EEAT signals; no duplicate sentences; no AI template phrases |
| `audit-wordcount.py` | 1900–2800 words; adaptive density by keyword length |

## Word count & density

| Keyword words | Density band |
|---------------|--------------|
| 1–3 | 0.6% – 1.8% |
| 4–5 | 0.35% – 1.5% |
| 6+ | 0.2% – 1.0% |

## Anti-boilerplate (zero tolerance)

- Delete: `Pilot note N:`, `Operational note:`, `Field note:`, `Practitioner note:` (no links) → `cleanup-pilot-note-filler.py`
- No cross-article filler H2s (`Production Debugging Notes`, etc.)
- No duplicate sentences (>40 chars, ≥2×) → `dedup-standalone-citations.py`
- No AI template phrases (see full doc)

## Fix workflow order

1. `fix-faq-and-headers.py` → meta/outline fixes
2. `fix-this-workflow-placeholder.py` → density weavers
3. `cleanup-pilot-note-filler.py` → manual boilerplate rewrite
4. Link fixers → full 11-gate re-run

See [audit-and-fix-commands.md](audit-and-fix-commands.md) for all commands.
