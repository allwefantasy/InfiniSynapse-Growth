---
name: keyword-research
description: Research and analyze keywords for a topic or niche
argument-hint: "<seed keyword or topic>"
parameters:
  - name: seed
    type: string
    required: true
    description: Seed keyword or topic
  - name: audience
    type: string
    required: false
    description: Target audience
  - name: market
    type: string
    required: false
    description: City, country, language, or service area for local/international targeting
  - name: goal
    type: string
    required: false
    description: "Business goal: traffic, leads, sales, awareness"
  - name: authority
    type: string
    required: false
    description: "Site authority level: low, medium, high"
  - name: competitors
    type: string
    required: false
    description: Competitor domains (comma-separated) for keyword gap analysis
---

# Keyword Research Command

Research keywords for a seed topic, audience, and business goal.

## Route

Use [keyword-research](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/SKILL.md).

## Steps

1. Confirm market, service area, audience, business goal, and local constraints when relevant.
2. Classify intent and funnel stage.
3. Expand seed keywords and competitor gaps.
4. Estimate difficulty, opportunity, GEO potential, and business value; mark no-tool estimates as directional.
5. Cluster terms into content targets.
6. Return priorities and next skill.

## Output

Keyword table, intent, difficulty, opportunity score, cluster map, recommended content type, and handoff.
