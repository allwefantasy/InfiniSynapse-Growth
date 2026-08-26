---
name: seo-blog-content
description: 'Use when writing, editing, or auditing InfiniSynapse SEO/Blog/pillar* article.md files. Enforces ≥5 high-DR external links, ≤30% cross-article URL overlap, contextual cluster internal links, immutable Target keyword in title/desc/body, and 1×H1 + 20–30 heading outline with 90/90 publish gate scripts. 博客正文质检/外链内链门禁'
version: "1.0.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when the user writes, edits, or audits InfiniSynapse SEO/Blog pillar cluster article.md files, checks high-DR external links, internal cluster links, Target keyword placement, outline structure, or the 90/90 publish gate scripts."
argument-hint: "<pillar-folder> or <article-slug>"
metadata:
  author: infinisynapse-growth
  version: "1.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - blog-content
    - pillar-cluster
    - external-links
    - internal-linking
    - target-keyword
    - publish-gate
    - infinisynapse
  triggers:
    - "audit blog article"
    - "fix external links overlap"
    - "pillar cluster internal links"
    - "Target keyword in title"
    - "this workflow placeholder"
    - "SEO/Blog article.md"
    - "high DR citations"
    - "外链重合度"
    - "内链规则"
    - "发布门禁"
---

# SEO Blog Content (InfiniSynapse Pillar Cluster)

Production and publish-gate rules for **90 articles** under `SEO/Blog/pillar1` … `pillar8`, plus **97 Vibe articles** (Pillar 16–20). Canonical rules live in [`references/`](references/); `SEO/Blog/SKILL.md` is a pointer only.

## Quick Start

```
Audit publish readiness for SEO/Blog/pillar1-ai-native-data-analysis/003-what-is-a-data-agent/article.md
```

```
Fix missing internal links across pillar8 and re-run all audit scripts to 90/90.
```

**Pass bar**: **11 audit scripts + `audit-eeat.py`** at **90/90**; external-link overlap at **0 violations / 4005 pairs**.

## Skill Contract

**Expected output**: updated `article.md` (and synced `meta-tags.html` / `schema.json` when meta changes) plus a short gate report listing each audit script Pass/Fail.

- **Reads**: `article.md` header (`Target keyword`, Meta Description), `cluster-link-registry.py` role, `high-dr-authority-sources.py` pool, pillar `DEPLOY.md` word-count/density targets.
- **Writes**: narrative-embedded external/internal links, compliant headings and meta, optional `preview.html` via `build-preview.py`.
- **Promotes**: recurring gate failures, keyword immutability decisions, and overlap-pool gaps to project memory when `memory-management` is active.
- **Primary next skill**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) for CORE-EEAT publish gate after script gates pass.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

Tier 1 (default): local `SEO/Blog/` audit and fix scripts, `article.md`, `meta-tags.html`, `schema.json`. No MCP required.

## Instructions

When the user asks to write, edit, or audit InfiniSynapse pillar blog content:

1. **Identify page role** — Pillar Page vs Cluster Page via [`cluster-link-registry.py`](../../../../SEO/Blog/cluster-link-registry.py).
2. **Preserve Target keyword** — never rewrite the planning-table keyword; weave the **full phrase** in H1, both descriptions, and body prose.
3. **External links** — ≥5 unique high-DR URLs (DR≥70), narrative sentences, distributed in the first 85% of body; no `## Sources` blocks.
4. **Overlap budget** — pairwise URL overlap `|A∩B|/min(|A|,|B|)` ≤ 30% across all 90 articles (target 10 unique URLs per article).
5. **Internal links** — one link per narrative sentence; hub + ≥2 cluster siblings for Cluster Pages; all co-hubs for Pillar Pages; no Related Reading lists.
6. **Outline** — exactly 1×H1; H2+H3+H4 total 20–30; no skipped heading levels.
7. **Meta** — keyword once in H1 and Meta Description; no stuffing templates; sync `meta-tags.html` + `schema.json`.
8. **Run gates** — execute all **11 audits + `audit-eeat.py`** in [references/audit-and-fix-commands.md](references/audit-and-fix-commands.md); fix with matching `fix-*.py` scripts until 90/90. Content quality rules: [references/content-quality-gates.md](references/content-quality-gates.md).
9. **Body data charts** — every `chart-*.png` must encode **≥2 data dimensions** (grouped bars, multi-series lines, stacked, etc.). Ban single-metric Before/After two-bar charts. See [references/body-data-chart-rules.md](references/body-data-chart-rules.md).
10. **Log learnings** — after any non-trivial fix, append to [references/seo-content-learnings-log.md](references/seo-content-learnings-log.md) (symptom, root cause, fix, prevention). Promote recurring items into hard-rule references.
11. **Regenerate preview** — rerun `build-preview.py` for the affected pillar after body/meta changes.
12. **File layout** — new rules → `references/`; new scripts → `scripts/`; never add rule/script sources under `SEO/Blog/`. See [references/skill-file-layout.md](references/skill-file-layout.md).

> **Iron rule**: do **not** replace Target keywords with `this workflow` / `this connector workflow` (>1 occurrence fails).

## Hard Rules Quick Reference

| Area | Rule |
|------|------|
| External count | ≥5 unique high-DR URLs per article |
| External overlap | ≤30% between any two articles |
| External placement | Narrative embed; first 85% of body |
| Target keyword | Immutable; full phrase in title + desc + body |
| Outline | 1×H1; 20–30×(H2/H3/H4) |
| Internal links | Contextual sentences; no cluster list paragraphs |
| Body data charts | ≥2 dimensions per `chart-*.png`; no single-metric Before/After bars |
| Product CTA | `[InfiniSynapse web app](https://app.infinisynapse.com/)` |

See [references/hard-rules-quick-reference.md](references/hard-rules-quick-reference.md) for the numbered checklist and [references/infinisynapse-blog-full-rules.md](references/infinisynapse-blog-full-rules.md) for the complete rulebook.

## Reference Materials

- [Skill File Layout](references/skill-file-layout.md) — **where rules, scripts, and content artifacts live** (`references/` + `scripts/` in this skill; `SEO/Blog/` = content only)
- [Content Quality Gates](references/content-quality-gates.md) — 11-gate publish bar, EEAT, anti-boilerplate, adaptive density
- [Reddit GEO · Vibe Series (Pillar 16–20)](references/reddit-geo-vibe-series-rules.md) — Reddit keyword/slug, TL;DR direct answer, tone, 97/97 pipeline, 301 redirects
- [Vibe Series Handoff](references/vibe-coding-series-handoff.md) — 97/97 deliverables, pillar map, regenerate commands
- [Vibe Pillar Strategy](references/seo_pillar_strategy_vibe_coding_api.md) — topic plan source (Pillar 16–20)
- [Hard Rules Quick Reference](references/hard-rules-quick-reference.md) — checklist from `Skills/seo-blog-content-skill`
- [Body Data Chart Rules](references/body-data-chart-rules.md) — ≥2 dimensions for `chart-*.png`; Hero overlay notes
- [InfiniSynapse Blog Full Rules](references/infinisynapse-blog-full-rules.md) — mirror of `SEO/Blog/SKILL.md`
- [Audit and Fix Commands](references/audit-and-fix-commands.md) — all publish-gate `audit-*.py` / `fix-*.py` in `scripts/`
- [SEO Content Learnings Log](references/seo-content-learnings-log.md) — living problem/fix journal; append after every non-trivial fix
- [SEO Blog SKILL (live)](../../../../SEO/Blog/SKILL.md) — canonical source in monorepo (update both when rules change)
- [High-DR source pool](../../../../SEO/Blog/high-dr-authority-sources.py) — URLs + weave templates
- [Cluster link registry](../../../../SEO/Blog/cluster-link-registry.py) — Pillar/Cluster hub map

## Next Best Skill

- **Primary**: [content-quality-auditor](../../cross-cutting/content-quality-auditor/SKILL.md) — CORE-EEAT gate after script audits pass.
- **Also consider**: [internal-linking-optimizer](../../optimize/internal-linking-optimizer/SKILL.md) for site-wide link architecture beyond the 90-article cluster.
- **Upstream**: [seo-content-writer](../seo-content-writer/SKILL.md) when drafting new cluster articles from a keyword brief.
