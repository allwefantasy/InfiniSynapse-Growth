---
name: audit-domain
description: Run a full CITE domain authority audit with 40-item scoring, veto checks, and prioritized action plan
argument-hint: "<domain>"
parameters:
  - name: domain
    type: string
    required: true
    description: Domain to audit (e.g., example.com)
  - name: type
    type: string
    required: false
    description: "Domain type: Content Publisher, Product & Service, E-commerce, Community & UGC, Tool & Utility, Authority & Institutional"
  - name: competitors
    type: string
    required: false
    description: Competitor domains for comparison (space-separated)
---

# Audit Domain Command

Run a CITE domain authority audit for a domain.

## Route

Use [domain-authority-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/domain-authority-auditor/SKILL.md) with [references/cite-domain-rating.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/cite-domain-rating.md).

## Steps

1. Normalize the domain and optional competitors/type.
2. Collect evidence for identity, citation, trust, impact, and expertise signals.
3. Score all 40 CITE items; apply veto and cap rules from the auditor runbook.
4. Compare competitors when provided.
5. Return verdict, score, critical fixes, evidence, and next best skill.

## Output

Domain, type, raw score, final score, verdict, vetoes, priority fixes, competitor gaps, evidence table, and handoff summary.
