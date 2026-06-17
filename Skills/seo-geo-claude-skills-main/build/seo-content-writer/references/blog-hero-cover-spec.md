# Blog Hero Cover Spec (OG / First Image)

Mandatory standard for **article hero images** in SEO blog bundles. Hero covers are **not** decorative stock art — they are the first in-article image, the `og:image` / Twitter card asset, and the visual anchor for social sharing.

**Reference implementation**: `SEO/Blog/pillar1-ai-native-data-analysis/` (InfiniSynapse Pillar 1, 13 articles, 2026-06).

---

## Two-Tier Image System

| Tier | Role | Method | Content |
|------|------|--------|---------|
| **Hero / OG** | First image in `article.md`; `og:image`; `og-cover.png` | HTML cover → headless Chrome PNG | **Article H1 title** + abstract tech geometry |
| **Body diagrams** | In-section illustrations | HTML infographic → Chrome PNG | Tables, matrices, flows with real professional content |

Do **not** merge tiers. Hero = title cover. Body = substantive diagrams.

---

## Hero Requirements (Mandatory)

### Content

| Rule | Detail |
|------|--------|
| **Title text** | Must display the **exact** `article.md` H1 (character-for-character match with `<title>` / schema `headline`) |
| **Kicker** | Short uppercase label above title (content type + year), e.g. `Guide · 2026`, `Definition`, `Comparison` |
| **Brand** | Small wordmark bottom-left, e.g. `InfiniSynapse` |
| **No extra copy** | No subtitle paragraph, no lorem ipsum, no fake UI labels on the hero |

### Visual Style

| Dimension | Spec |
|-----------|------|
| **Aspect ratio** | **16:9** |
| **Render size** | **1200 × 630 px** (OG standard; also satisfies `summary_large_image`) |
| **Mood** | Dark tech editorial — professional, readable, contemporary |
| **Background** | Deep gradient: `#070b14` → `#0f172a` → `#151030` |
| **Accent colors** | Deep blue `#1d4ed8` / `#2563eb`, violet `#6d28d9` / `#7c3aed`, cyan glow `#38bdf8` |
| **Geometry** | Abstract SVG only: nodes, arcs, pillars, rings, hex chains, hub-spoke — **one variant per article** |
| **Composition** | **Left ~54%**: title block on calm dark area. **Right ~46%**: grid overlay + glowing geometry |
| **Depth** | Radial glow behind SVG, `drop-shadow` on shapes, subtle tech grid on right panel |
| **Typography** | System sans-serif; title scales by length: 42px (≤42 chars) → 36px → 32px → 28px (long H1) |
| **Title color** | `#f1f5f9` with light text-shadow for legibility |

### Strict Negatives (Hero)

Never ship hero covers with:

- AI-generated **misspelled** or **placeholder** text (use HTML text rendering instead)
- Watermarks, stock-photo people, corporate handshake clichés
- Busy tables, dense infographic content (belongs in body tier)
- Light pastel “generic SaaS” backgrounds unless brand explicitly requires light mode
- Title that differs from H1, `<title>`, or schema `headline`

---

## File & Bundle Conventions

Per article folder:

```
{slug-folder}/
  article.md              # First image: ![alt](images/hero-*.png)
  meta-tags.html          # og:image + twitter:image → hero or og-cover.png
  schema.json             # BlogPosting.image[] → hero URL
  images/
    hero-{descriptive}.png
    og-cover.png          # Copy of hero (same bytes)
  visuals/
    hero.html             # Source for Chrome render
  prompts/
    cover.prompt          # Optional; only if using AI background layer (text still via HTML)
```

**Alt text**: Describe the article topic + visual metaphor (6–20 words). Do not repeat the full H1 verbatim if the image already shows it.

**Canonical URLs** in meta/schema should point to the deployed CDN path after upload.

---

## Generation Method (Required)

### Preferred: HTML → PNG

1. Build `visuals/hero.html` with embedded CSS + SVG (title from `article.md` H1).
2. Render with headless Chrome at `1200×630`, `device-scale-factor=2`.
3. Save to `images/hero-*.png`.
4. `cp hero-*.png images/og-cover.png`.

**Why HTML, not pure AI image gen**: Image models hallucinate typography (`HEADLINE`, `LORUM`, misspelled words). HTML guarantees exact title spelling and OG readability.

### Optional: AI background only

If using `imagen-4-fast` or similar for the right-side geometry:

- Prompt must say **pure abstract background, no text, no UI mockup**
- Still overlay title via HTML or post-compose
- Use `--negative-prompt` for: `text, letters, typography, headline, lorem ipsum, UI mockup, watermark`

---

## Meta / Schema Alignment

| Field | Must match hero |
|-------|-----------------|
| `article.md` H1 | Title on hero image |
| `<title>` | Same string as H1 (may differ in year modifier only if H1 also includes it) |
| `og:title` / `twitter:title` | Same as H1 |
| `og:image` / `twitter:image` | Hero PNG URL (1200×630) |
| `og:image:width` / `height` | `1200` / `630` |
| `og:image:alt` | Descriptive alt (not empty) |
| `schema.json` `BlogPosting.image` | Same hero URL |
| `schema.json` `headline` | Same as H1 |

---

## QA Checklist (Pre-Ship)

- [ ] Hero PNG is 1200×630 (16:9)
- [ ] Visible title text **equals** `article.md` H1 exactly
- [ ] No typos, no placeholder glyphs, no watermark
- [ ] Dark tech palette; blue/violet accents visible; geometry on right
- [ ] `og-cover.png` exists and matches hero
- [ ] `meta-tags.html` `og:image` and `twitter:image` populated
- [ ] `schema.json` `image` array includes hero URL
- [ ] First `![...](images/hero-*.png)` in `article.md` points to the same file
- [ ] Spot-check at 50% zoom — title still readable

---

## Toolchain (InfiniSynapse Pillar 1)

```bash
# 1. Update HEROES list in build-visuals.py when H1 changes
python3 SEO/Blog/pillar1-ai-native-data-analysis/build-visuals.py

# 2. Render hero + body PNGs (hero syncs og-cover.png)
bash SEO/Blog/pillar1-ai-native-data-analysis/render-all-images.sh

# 3. Regenerate local preview pages (see blog-preview-html-spec.md)
python3 SEO/Blog/pillar1-ai-native-data-analysis/build-preview.py
```

**Preview HTML**: [blog-preview-html-spec.md](blog-preview-html-spec.md) — `preview.html` per article + `INDEX-preview.html` for local review.

When creating a **new** blog bundle, copy the pattern from `SEO/Blog/scripts/cover-prompt.template` and `build-visuals.py` (`hero_cover()`, `COVER_CSS`, `SVG_VARIANTS`).

---

## Body Diagram Spec (Brief)

Hero rules do **not** apply to body images.

| Dimension | Body infographics |
|-----------|-------------------|
| Size | 1200 × 720 px typical |
| Background | Light gradient `#f8fafc` → `#eef2ff` (readability for tables) |
| Headers | Deep blue gradient `#1e3a8a` → `#1e40af`, text `#e0f2fe` |
| Content | Real tables, matrices, timelines, architecture stacks — no empty decoration |

See `_style-guide.md` in each blog pillar folder for the full body diagram inventory.

---

## When to Apply This Skill

Use this spec when:

- Writing or auditing SEO blog bundles with `article.md` + `meta-tags.html` + `schema.json`
- Generating or reviewing hero covers for pillar/cluster content
- Optimizing `og:image` for social CTR (hero title reinforces click intent)
- Running [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) or [on-page-seo-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/on-page-seo-auditor/SKILL.md) on blog pages
