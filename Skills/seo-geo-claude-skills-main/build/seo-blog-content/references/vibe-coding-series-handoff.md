# Vibe Coding → API/Data Infra SEO Series · COMPLETE

Based on [`seo_pillar_strategy_vibe_coding_api.md`](seo_pillar_strategy_vibe_coding_api.md).

## Status: 97/97 articles written

| Deliverable | Path |
|-------------|------|
| Topic plan | `SEO/Blog/blog-vibe-coding-topics-plan.csv` |
| All articles | `SEO/Blog/pillar16` … `pillar20` / `203-*` … `299-*` |
| Blog index (97 posts) | `SEO/Blog/blog-index-import-master.json` |
| Sitemap | `SEO/Blog/sitemap.xml` |
| **Programmer zip** | **`SEO/Blog/vibe-coding-handoff-pack.zip`** (~170 MB, includes hero PNGs) |

## Pillars

| Priority | Folder | Hub slug | IDs |
|----------|--------|----------|-----|
| 1 | `pillar18-api-integration-vibe-built` | `api-integration-services` | 203–222 |
| 2 | `pillar19-tool-calling-agent-workflows` | `agentic-orchestration` | 223–242 |
| 3 | `pillar20-data-api-production-readiness` | `professional-data-api` | 243–262 |
| 4 | `pillar17-vibe-coding-stack` | `vibe-coding-tools` | 263–282 |
| 5 | `pillar16-vibe-coding-workflow` | `vibe-coding-best-practices` | 283–299 |

## Quality gates (97/97 pass)

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/audit-wordcount.py" SEO/Blog/pillar16-vibe-coding-workflow SEO/Blog/pillar17-vibe-coding-stack SEO/Blog/pillar18-api-integration-vibe-built SEO/Blog/pillar19-tool-calling-agent-workflows SEO/Blog/pillar20-data-api-production-readiness
python3 "$S/audit-outline-structure.py" SEO/Blog/pillar16-vibe-coding-workflow SEO/Blog/pillar17-vibe-coding-stack SEO/Blog/pillar18-api-integration-vibe-built SEO/Blog/pillar19-tool-calling-agent-workflows SEO/Blog/pillar20-data-api-production-readiness
python3 "$S/audit-keyword-in-title-desc.py" SEO/Blog/pillar16-vibe-coding-workflow SEO/Blog/pillar17-vibe-coding-stack SEO/Blog/pillar18-api-integration-vibe-built SEO/Blog/pillar19-tool-calling-agent-workflows SEO/Blog/pillar20-data-api-production-readiness
```

## Handoff

See `SEO/Blog/vibe-coding-handoff-pack/README.md`:
- `article.publish.md` = body without H1 (CMS paste)
- `head.html` + `schema.json` per article
- Hero PNGs still needed (`images/hero-{slug}.png`)

## Notable deep articles (hand-polished)

- **203** `api-integration-services` — Hub ultimate guide
- **206** `api-integration-tools` — InfiniSynapse Server API / vibe coding walkthrough
- **221** `api-integration-testing`
- **223** `agentic-orchestration` — Hub
- **224** `tool-calling`

## Regenerate

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/generate-vibe-coding-articles.py"   # skip existing ≥1800w
python3 "$S/tune-vibe-audit-gates.py"
python3 "$S/tune-vibe-headings.py"
python3 "$S/generate-deploy-meta.py"
python3 "$S/generate-blog-index-master.py"
python3 "$S/build-sitemap.py"
```

Reddit GEO 规则与完整流水线：[`reddit-geo-vibe-series-rules.md`](reddit-geo-vibe-series-rules.md)
