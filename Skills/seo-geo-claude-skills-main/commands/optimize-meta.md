---
name: optimize-meta
description: Optimize title tags, meta descriptions, and Open Graph tags for a page
argument-hint: "<URL or page details>"
parameters:
  - name: source
    type: string
    required: true
    description: URL or page details to optimize
  - name: keyword
    type: string
    required: false
    description: Target keyword
  - name: mode
    type: string
    required: false
    description: "Set to 'a/b-test' to generate multiple variants for testing"
---

# Optimize Meta Command

Optimize title tags, meta descriptions, and Open Graph/Twitter tags.

## Route

Use [meta-tags-optimizer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/meta-tags-optimizer/SKILL.md).

## Steps

1. Parse URL/page details, target keyword, and SERP intent.
2. Draft compliant title/meta/social variants.
3. Check length, uniqueness, CTR angle, brand fit, and claim support.
4. Provide A/B variants when requested.

## Output

Recommended tags, alternatives, rationale, implementation snippet, and test plan.
