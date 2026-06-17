---
name: audit-page
description: Run a comprehensive on-page SEO + CORE-EEAT content quality audit for a given URL or content
argument-hint: "<URL or paste content>"
allowed-tools: ["WebFetch"]
parameters:
  - name: source
    type: string
    required: true
    description: URL to audit or pasted content
  - name: keyword
    type: string
    required: false
    description: Target keyword for relevance scoring
---

# Audit Page Command

Run on-page SEO plus CORE-EEAT content quality audit for a URL or pasted content.

## Route

Use [on-page-seo-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/on-page-seo-auditor/SKILL.md), then [content-quality-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/content-quality-auditor/SKILL.md) for ranking-diagnosis, content-quality, trust, or publish-verdict work.

## Steps

1. Fetch or parse the source; if fetch is unavailable, ask for page copy, title/meta, H1-H2, URL, target keyword, and competitors.
2. If keyword is missing, infer likely targets from title/H1/body, mark confidence, and continue `DONE_WITH_CONCERNS`.
3. Audit title, meta, headings, content quality, images, links, schema, accessibility, and intent fit.
4. Run CORE-EEAT quick scan; run the full content-quality auditor when ranking/content/trust diagnosis needs it.
5. Produce score, fixes, evidence, and handoff.

## Output

URL/source, keyword, section scores, CORE-EEAT quick scan, critical issues, prioritized fixes, and next best skill.
