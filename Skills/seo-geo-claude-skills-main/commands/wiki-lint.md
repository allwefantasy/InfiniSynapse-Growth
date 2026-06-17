---
name: wiki-lint
description: Run wiki health check — detect contradictions, orphan pages, stale claims, missing pages, and source hash mismatches across wiki and WARM files
argument-hint: "[--fix] [--project <name>] [--retire-preview]"
parameters:
  - name: fix
    type: boolean
    required: false
    description: Auto-resolve contradictions where confidence is HIGH (time-series data). MEDIUM/LOW contradictions still require user confirmation.
  - name: project
    type: string
    required: false
    description: Limit lint to a specific project. If omitted, lints the active project from hot-cache or all projects.
  - name: retire-preview
    type: boolean
    required: false
    description: "Phase 3: List WARM files fully covered by wiki compiled pages as retirement candidates. Does not execute any archival — requires explicit user confirmation."
---

# Wiki Lint Command

Check project wiki and WARM memory health.

## Route

Use [memory-management](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/SKILL.md) and [state-model.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md).

## Steps

1. Load active project or all `memory/wiki/*/index.md` files.
2. Detect contradictions, orphan pages, stale claims, missing pages, and source hash mismatches.
3. With `--retire-preview`, list WARM files fully covered by compiled wiki pages.
4. Apply only HIGH-confidence fixes when `--fix` is set; otherwise report.

## Output

Health score, contradictions, stale items, orphan pages, fixable items, retire-preview list, and save target.
