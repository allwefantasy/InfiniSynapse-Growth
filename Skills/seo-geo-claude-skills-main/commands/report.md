---
name: report
description: Generate a comprehensive SEO and GEO performance report for a single domain, a named project, or across all projects in memory.
argument-hint: "<domain|project=slug|project=all> <time period>"
parameters:
  - name: domain
    type: string
    required: false
    description: "Single domain to report on (e.g., example.com). Exactly one of domain or project is required."
  - name: project
    type: string
    required: false
    description: "Project slug (e.g., acme-q2) to load from memory/wiki/<slug>/index.md. Use `all` to aggregate every project. Exactly one of domain or project is required."
  - name: period
    type: string
    required: true
    description: "Time period: last-month, last-quarter, Q[N]-[YYYY], [YYYY-MM-DD] to [YYYY-MM-DD], last-30-days, last-90-days"
  - name: comparison
    type: string
    required: false
    description: "Comparison period: vs previous-quarter, vs last-year, vs previous-period"
  - name: format
    type: string
    required: false
    description: "Output format: detailed (default) or executive (condensed for stakeholders)"
---

# Report Command

Generate SEO/GEO performance report for a domain or memory project.

## Route

Use [performance-reporter](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/SKILL.md).

## Steps

1. Require exactly one scope: domain or project. If absent, ask for scope before reporting.
2. Gather traffic, rankings, conversions, authority, backlink, technical, and AI-citation evidence.
3. Require source/date for every metric.
4. Summarize wins, losses, risks, and next actions.

## Output

Executive summary, KPI table, trend analysis, AI visibility, authority status, source/date freshness, missing metrics, recommendations, and handoff.
