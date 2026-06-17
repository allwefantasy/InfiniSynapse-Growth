---
name: geo-drift-check
description: Check whether audited content is being cited by AI engines (Claude, ChatGPT, Gemini, Perplexity, Google AI Overviews) and record drift between predicted GEO Score and actual citation rate. Uses only already-connected MCP tools; no API keys bundled.
argument-hint: "<URL or leave empty to re-check all records due>"
allowed-tools: ["WebFetch", "Read", "Write", "Edit"]
parameters:
  - name: url
    type: string
    required: false
    description: URL to check. If omitted, re-checks all URLs in memory/geo-feedback/ whose next T+14 / T+45 / T+90 measurement is due.
---

# GEO Drift Check Command

Compare predicted GEO Score with actual AI-engine citation behavior at T+14, T+45, and T+90.

## Route

Use [references/geo-score-feedback-loop.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/geo-score-feedback-loop.md) and connected AI/search MCP tools when available. No bundled API keys or scheduled runner.

## Steps

1. Load URL record or due records from `memory/geo-feedback/`.
2. Query/paste AI answers for target prompts across available engines.
3. Record citation presence, quote accuracy, source/date evidence, and competitor displacement.
4. Compare actual citation rate with predicted GEO Score.
5. Update drift status and next measurement date when writing is allowed.

## Output

URL, prompts, engines, predicted score, actual citation rate, drift band, evidence, corrective action, and next check date.
