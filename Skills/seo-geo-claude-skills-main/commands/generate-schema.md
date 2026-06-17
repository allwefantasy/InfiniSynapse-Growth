---
name: generate-schema
description: Generate Schema.org JSON-LD structured data markup for a page
argument-hint: "<schema type> for <content description>"
allowed-tools: ["WebFetch"]
parameters:
  - name: schema_type
    type: string
    required: true
    description: "Schema type: FAQ, HowTo, Article, Product, LocalBusiness, Organization, Breadcrumb, Review, Event, Video"
  - name: source
    type: string
    required: true
    description: URL, pasted visible content, Q&A list, or product/business facts used as evidence
---

# Generate Schema Command

Generate Schema.org JSON-LD for visible page content.

## Route

Use [schema-markup-generator](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/schema-markup-generator/SKILL.md).

## Steps

1. Identify content type and eligible schema.
2. Require visible evidence for every property.
3. For publish-ready JSON-LD, omit missing or unverifiable dates, prices, durations, ratings, and review counts; list needed facts outside the JSON-LD instead.
4. Use placeholders only in clearly labeled draft templates, then validate rich-result policy constraints before output.

## Output

Schema type, eligibility notes, JSON-LD block, validation checklist, implementation location, and monitoring notes.
