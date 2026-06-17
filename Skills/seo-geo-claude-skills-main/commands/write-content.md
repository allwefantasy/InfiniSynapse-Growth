---
name: write-content
description: Write SEO and GEO optimized content from a topic and target keyword
argument-hint: "<topic> keyword=\"<target keyword>\" type=\"<content type>\" [engine/audience/entity]"
parameters:
  - name: topic
    type: string
    required: true
    description: Content topic
  - name: keyword
    type: string
    required: true
    description: Primary SEO target keyword
  - name: type
    type: string
    required: false
    description: "Content type (default: blog post). Options: blog post, how-to guide, comparison, listicle, landing page, ultimate guide"
  - name: engine
    type: string
    required: false
    description: Target AI/search surface, such as ChatGPT, Perplexity, AI Overviews, Gemini, or Google
---

# Write Content Command

Write SEO and GEO optimized content from topic and target keyword.

## Route

Use [seo-content-writer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/seo-content-writer/SKILL.md), then [geo-content-optimizer](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/build/geo-content-optimizer/SKILL.md).

## Steps

1. If the request combines research and writing, run keyword-research first and select the priority keyword.
2. Confirm topic, keyword, content type, audience, intent, CTA, entity/brand context, AI engine, and constraints.
3. Build outline, title, meta description, and section plan.
4. Draft content with keyword placement, snippets, links, FAQ, and evidence.
5. Add GEO citability blocks and final self-check.

## Output

Final content, title/meta, outline, SEO notes, GEO notes, unresolved assumptions, and quality handoff.
