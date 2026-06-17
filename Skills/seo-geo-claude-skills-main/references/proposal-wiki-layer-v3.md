# Archive Note — Wiki Knowledge Layer v3

**Status**: archived design summary
**Original proposal date**: 2026-04-05
**Reason for slimming**: the full proposal was a 700+ line design artifact. Runtime behavior now lives in the implementation-facing docs listed below, so this file keeps only the durable decisions and navigation links.

## Current Source of Truth

Use these files for active maintenance:

- [references/state-model.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) — current memory and wiki data model
- [cross-cutting/memory-management/SKILL.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/SKILL.md) — execution behavior and ownership rules
- [hooks/hooks.json](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/hooks/hooks.json) — SessionStart, PostToolUse, and Stop automation behavior
- [commands/wiki-lint.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/commands/wiki-lint.md) — lint and health-check workflow

Treat this file as design history, not executable spec.

## What Survived From v3

The proposal introduced a derived `memory/wiki/` layer that compiles WARM records into a navigation-friendly index without mutating the source files. The implemented system keeps these ideas:

- `memory/wiki/` is a compiled view, not the canonical store
- `memory-management` is the semantic owner of wiki writes
- hooks may perform narrowly scoped delegated refreshes
- project-specific indexes live under `memory/wiki/<project>/`
- deleting `memory/wiki/` is the supported rollback path
- summaries are best-effort; structured fields are preferred when available

## Durable Decisions

### 1. Keep WARM immutable

Wiki output is a derivative view. Source files in `memory/` remain the durable records and should not be rewritten by wiki maintenance flows.

### 2. Separate low-risk and high-risk writes

Two classes of write still matter:

- low-risk: index refreshes and append-only logs
- higher-risk: compiled entity or keyword pages with synthesized judgments

This distinction explains why hooks can safely refresh indexes while compiled pages still belong to `memory-management`.

### 3. Support project isolation

The active project may scope wiki reads and writes to `memory/wiki/<project>/index.md`. If no project is declared, the global index remains the fallback.

### 4. Preserve zero-cost rollback

Any future redesign must retain the ability to remove `memory/wiki/` and return to HOT/WARM/COLD behavior without migration of source memory files.

## What Was Intentionally Removed

The archived long-form proposal included:

- reviewer notes and acceptance feedback
- phased rollout plans
- verbose examples and UI phrasing experiments
- test matrices and rollout checklists
- migration discussion that is now reflected in live docs

Those details remain in git history if needed, but they no longer need to live in the runtime-facing reference set.

## Migration Guidance For Maintainers

If you touch wiki behavior today:

1. Update the live implementation docs first.
2. Keep terminology aligned across `state-model`, `memory-management`, and `hooks`.
3. Only update this archive when a design decision changes, not for routine wording or implementation edits.

## Compatibility Notes

- Existing links to `references/proposal-wiki-layer-v3.md` continue to work.
- Existing wiki rollback guidance is unchanged: delete `memory/wiki/`.
- Existing ownership model is unchanged: `memory-management` remains the semantic sole writer.

## Retrieval Hint

If you need the full historical rationale, use git history for this path. The working repository keeps only this compressed archive note to reduce maintenance and activation overhead.
