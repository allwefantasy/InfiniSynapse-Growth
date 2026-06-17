---
name: check-technical
description: Run a quick technical SEO health check for a given URL or domain
argument-hint: "<URL or domain>"
allowed-tools: ["WebFetch"]
parameters:
  - name: target
    type: string
    required: true
    description: URL or domain to check
  - name: performance_report
    type: string
    required: false
    description: Optional PageSpeed, CrUX, Lighthouse, or Core Web Vitals data
---

# Check Technical Command

Run a technical SEO health check for a URL or domain.

## Route

Use [technical-seo-checker](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/optimize/technical-seo-checker/SKILL.md).

## Steps

1. Normalize target and gather crawlability, indexability, rendering, performance, HTTPS/security, schema, and architecture evidence.
2. Keep robots.txt, sitemap, canonical, lastmod, HSTS, INP, and structured-data opportunities explicit.
3. If PageSpeed/CrUX/Lighthouse data is missing, mark CWV metrics `N/A` and request reports instead of guessing LCP/INP/CLS.
4. Prioritize issues by severity and effort.
5. Return fixes and next best skill.

## Output

Target, health score, critical blockers, robots/sitemap status, Core Web Vitals, security findings, fix queue, and handoff.
