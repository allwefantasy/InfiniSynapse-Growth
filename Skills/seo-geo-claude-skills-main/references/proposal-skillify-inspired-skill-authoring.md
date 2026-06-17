# Skillify-Inspired Skill Authoring Proposal

**Status**: implemented in unreleased tree
**Date**: 2026-04-28
**Source**: https://github.com/garrytan/gbrain/blob/master/skills/skillify/SKILL.md
**Scope**: skill creation, routing, validation, and controlled evolution for this SEO/GEO skill library

## Executive Summary

`skillify` is useful because it treats a skill as a complete, reachable capability, not just a `SKILL.md` file. The core lesson for this repository is to add a maintainer workflow that proves every new or heavily changed skill is discoverable by real user language, distinct from sibling skills, covered by eval cases, and synchronized with the library release surfaces.

This repository already has strong pieces: `/seo:evolve-skill`, `/seo:run-evals`, `/seo:validate-library`, `validate-skill.sh`, and `validate-slimming-guardrails.sh`. The missing layer is a front-door authoring workflow that runs before controlled evolution review: "is this skill complete, routable, and ready to enter the library?"

## Goals

1. Add a repeatable authoring checklist for new skills and major skill rewrites.
2. Make user-intent routing explicit and reviewable.
3. Add routing evals that test trigger phrases against expected skills using the existing `eval-case` contract.
4. Prevent incomplete scaffolded skills from entering release builds.
5. Preserve the repository's content-only design: no runtime dependency and no mandatory external tools for Tier 1 behavior.

## Non-Goals

- Do not copy `gbrain` implementation details such as TypeScript scripts, brain page filing, or live endpoint tests.
- Do not make Tier 1 skill behavior depend on MCP, SEO tools, or network access.
- Do not weaken existing CORE-EEAT, CITE, auditor runbook, memory, or evolution protocol gates.
- Do not replace `/seo:evolve-skill`; this proposal adds an authoring gate before evolution and release review.

## Current State

The repository already validates:

- SKILL frontmatter and shared section shape via `scripts/validate-skill.sh`.
- Release and slimming guardrails via `scripts/validate-slimming-guardrails.sh`.
- Library-wide release consistency via `/seo:validate-library`.
- Controlled evolution proposals via `/seo:evolve-skill`.
- Lightweight behavior regression cases via `/seo:run-evals` and `evals/`.

The repository does not yet have:

- A reviewer-facing skill intent index that reconciles routing language across skill metadata.
- Routing evals that assert real user phrasing maps to the intended skill.
- A formal "skill completeness" scorecard for newly added or heavily rewritten skills.
- A scaffold-stub marker that blocks release until placeholders are replaced.

## Proposed Design

### 1. Add a Skill Authoring Command

Create a maintenance command:

```text
/seo:skillify <skill-or-feature> [--new] [--category research|build|optimize|monitor|cross-cutting] [--pr-ready]
```

The command should be read-first and proposal-first. It may produce a checklist, recommended files, and draft text, but it should not edit files unless a future command variant explicitly opts into scaffolding.

Recommended command responsibilities:

- Identify whether the target should be a new skill, an extension to an existing skill, a command, or a reference update.
- Compare the target against the skill completeness checklist.
- Suggest the correct category and neighboring skills.
- Generate candidate trigger phrases using real user language.
- Recommend eval cases, including routing cases.
- Report required release-surface updates if the skill is accepted.

### 2. Add a Skill Resolver Reference

Create:

```text
references/skill-resolver.md
```

The resolver is not executable code and is not the runtime source of truth. It is a derived maintainer-facing review index that must reconcile with each skill's `description`, `when_to_use`, `metadata.triggers`, `Next Best Skill`, and handoff language.

Governance rules:

- Routine row updates that only reflect an already-approved skill change may be included in the same PR as that skill change.
- Changes that alter cross-skill routing, ownership boundaries, or handoff order are `high` risk and require `/seo:evolve-skill` with an EvolutionEvent.
- Changes that affect protocol-layer gates, hooks, auditor behavior, memory ownership, or shared contracts are `protocol` risk and require a decision record or ADR.
- The resolver must not contradict skill frontmatter. If the resolver and a skill disagree, the PR must update both or leave the resolver row advisory and marked `needs-review`.

Suggested schema:

```markdown
| User intent | Example phrases | Primary route | Route role | Adjacent skills | Sequence / handoff rule | Governance |
|-------------|-----------------|---------------|------------|-----------------|-------------------------|------------|
| Find keyword opportunities | "find keywords", "keyword ideas", "topic clusters" | keyword-research | primary | content-gap-analysis, serp-analysis | Handoff to content-gap-analysis when competitor coverage is requested. | ordinary skill update |
```

This file should make overlap visible. For example, `geo-content-optimizer`, `entity-optimizer`, and `domain-authority-auditor` can all relate to AI citations, but they should be separated by user intent:

- Improve content for AI citation: `geo-content-optimizer`.
- Strengthen entity recognition: `entity-optimizer`.
- Audit domain trust and citation-worthiness: `domain-authority-auditor`.

### 3. Add Routing Evals

Do not create `evals/routing/cases.md` in the first implementation. Current eval tooling expects `evals/<skill-name>/cases.md`, `type: eval-case`, `target_skill`, and `expected_behavior`. Routing evals should therefore be attached to the target skill's existing eval file until a protocol-level routing eval mode is explicitly added to `evals/README.md`, `commands/run-evals.md`, and the guardrail parser.

```text
evals/<target-skill>/cases.md
```

Example compatible routing case for `evals/geo-content-optimizer/cases.md`:

```yaml
id: routing-sim-geo-001
type: eval-case
status: simulated
target_skill: geo-content-optimizer
scenario: "User asks why AI search is not citing a product page."
input_summary: "AI search is not citing our product page. Help me fix it."
expected_behavior:
  - "Route `geo-content-optimizer` as the primary page-level citation-readiness skill."
  - "Recommend `entity-optimizer` only when canonical identity or sameAs evidence is missing."
  - "Recommend `domain-authority-auditor` only when domain trust or citation-worthiness evidence is the limiting factor."
  - "Return NEEDS_INPUT when no page content, URL, entity details, or citation evidence is available."
failure_modes:
  - "Routes directly to generic content writing without citation-readiness analysis."
  - "Uses domain-authority-auditor before checking page-level GEO readiness."
  - "Treats all AI citation problems as entity problems."
evolution_use: "Use when changing GEO routing, AI citation handoffs, or Next Best Skill language."
```

Routing evals should remain simulated until tied to real project-local evidence, using the same evidence boundary already defined in `evals/README.md` and `references/evolution-protocol.md`.

Future protocol-level routing evals are allowed only after the eval contract is extended. That future mode should encode route sequence explicitly: primary skill, required gate, downstream handoff, stop-and-present-options, or `NEEDS_INPUT` / `BLOCKED`.

### 4. Add a Skill Completeness Checklist

Adapt `skillify`'s 10-part checklist to this content-only repository:

| # | Check | Requirement |
|---|-------|-------------|
| 1 | SKILL file | `SKILL.md` exists with valid required frontmatter. |
| 2 | Description | Description includes use case, trigger phrases, function, and scope boundaries. |
| 3 | User triggers | `when_to_use` and `metadata.triggers` use natural user language. |
| 4 | Resolver index row | `references/skill-resolver.md` maps key intents to the skill and reconciles with frontmatter. |
| 5 | MECE boundary | Adjacent skills and handoff rules are explicit. |
| 6 | Tier 1 viability | Skill can produce useful output with user-provided data and no tools. |
| 7 | Handoff | Handoff Summary includes objective, evidence, open loops, score fields, priority items, and URL where relevant. |
| 8 | Eval coverage | At least normal, edge, and adversarial cases exist or are proposed. |
| 9 | Routing eval | At least one compatible `eval-case` asserts primary route, sequencing, acceptable handoffs, and ambiguity handling. |
| 10 | Release surfaces | README, CLAUDE, VERSIONS, manifests, marketplace mirrors, and localized docs are identified when a release change is required. |

### 5. Add Stub Sentinels for Scaffolds

If a future workflow creates scaffold files, include a blocking marker:

```text
SEO_GEO_SKILL_STUB
```

`/seo:validate-library --strict` and `scripts/validate-slimming-guardrails.sh` should fail when this marker appears in release-bearing surfaces: `research/`, `build/`, `optimize/`, `monitor/`, `cross-cutting/`, `commands/`, root manifests, marketplace files, README files, `CLAUDE.md`, `AGENTS.md`, `CITATION.cff`, or `VERSIONS.md`.

Allowed mentions must be path-based, not inferred from prose. Proposal and authoring-reference files may mention the marker only when they are explicitly allowlisted by path. This avoids a fragile "example block" parser and keeps the bash guard mechanically checkable.

## Implementation Plan

### Phase 1: Documentation-Only

1. Add this proposal document.
2. Record unresolved design choices in this proposal without changing command inventory, manifests, or release wording.

### Phase 2: Resolver and Compatible Eval Seeds

1. Add `references/skill-resolver.md` as a derived review index with an initial table for all 20 skills.
2. Add a small simulated routing seed set to existing skill eval files using `type: eval-case` and `target_skill`.
3. Update `evals/README.md` to explain routing cases inside the existing eval schema.
4. Update `commands/validate-library.md` to mention routing coverage as advisory only.
5. Do not change command counts, plugin manifests, marketplace files, or release wording in this phase.

### Phase 3: Command Surface and Release Inventory Sync

1. Add `commands/skillify.md` as a maintenance command.
2. Keep `allowed-tools` read-only at first: `Read`, `Glob`, `Grep`.
3. Output a scorecard, missing items, recommended eval cases, and release-surface impact.
4. Do not permit the command to edit files, publish, commit, or accept evolution events.
5. In the same PR, update all command inventory surfaces from 16 commands to 17 commands:
   - `README.md`
   - `docs/README.zh.md`
   - `CLAUDE.md`
   - `AGENTS.md`
   - `CITATION.cff`
   - `VERSIONS.md`
   - `.claude-plugin/plugin.json`
   - `marketplace.json`
   - `.claude-plugin/marketplace.json`
   - `.codebuddy-plugin/marketplace.json`
   - `gemini-extension.json`
   - `qwen-extension.json`
   - `scripts/validate-slimming-guardrails.sh`
   - `commands/validate-library.md`

### Phase 4: Strict Validation Gate

1. Extend `validate-slimming-guardrails.sh` to fail on `SEO_GEO_SKILL_STUB` in release-bearing surfaces with path-based allowlists.
2. Add checks that every discovered `SKILL.md` appears in `references/skill-resolver.md`.
3. Add checks that every routing eval references an existing skill via `target_skill`.
4. Add duplicate-trigger detection only after normalization rules and false-positive handling are documented.
5. Keep command counts synchronized across release surfaces.

## Acceptance Criteria

### Advisory Criteria

- Maintainers agree that `references/skill-resolver.md` is the right home for routing intent.
- The initial resolver table covers all 20 skills.
- At least 10 compatible routing evals exist inside target skill eval files, including ambiguous SEO/GEO cases.
- Resolver rows identify primary route, route role, adjacent skills, sequence, handoff rule, and governance level.

### Implementation-Blocking Criteria

- Routing cases use the existing `type: eval-case` schema unless protocol-level eval support has already been added.
- Any routing case can be run by `/seo:run-evals --skill <target-skill>` or `/seo:run-evals --case <case-id>`.
- Resolver changes that alter cross-skill behavior include `/seo:evolve-skill` output and an EvolutionEvent draft.
- `/seo:skillify` has a read-only command spec and cannot mutate files before it is added to the command inventory.

### Release-Blocking Criteria

- Every changed skill passes `bash scripts/validate-skill.sh <category>/<skill-name>`.
- `bash scripts/validate-skill.sh --status` passes.
- `bash scripts/validate-slimming-guardrails.sh` passes.
- `/seo:validate-library --strict` reports routing coverage and release-surface consistency.
- If `commands/skillify.md` is added, command inventory is synchronized across every release-bearing surface in Phase 3.
- Routing eval runs return non-validating simulated evidence unless real project-local cases have been approved.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Resolver becomes another stale document | Routing quality degrades over time | Treat it as a derived index and validate that every skill appears in the resolver, every resolver target exists, and rows reconcile with frontmatter. |
| Resolver becomes a parallel routing authority | Maintainers bypass skill metadata and evolution governance | Require `/seo:evolve-skill` and an EvolutionEvent for cross-skill routing changes; require ADRs for protocol-layer routing changes. |
| Routing eval schema drifts from current runner | `/seo:run-evals` cannot execute the proposed cases | Keep first-generation routing cases inside existing target skill eval files with `type: eval-case` and `target_skill`. |
| Routing model is too flat | Evals miss protocol gates, sequencing, ambiguity, or blocked states | Encode primary route, required gate, downstream handoff, stop-and-present-options, and `NEEDS_INPUT` / `BLOCKED` behavior in `expected_behavior`. |
| Trigger overlap creates false activation | Agents choose the wrong skill | Add MECE notes and routing evals for ambiguous phrases; make duplicate-trigger checks advisory until normalization and thresholds are documented. |
| Command inventory drifts when `/seo:skillify` is added | Release surfaces or guardrails become inconsistent | Add `commands/skillify.md` only in the same PR as the 16-to-17 command inventory update across docs, manifests, and guardrails. |
| `/seo:skillify` duplicates `/seo:evolve-skill` | Maintainers do not know which command to use | Define `/seo:skillify` for creation/completeness, `/seo:evolve-skill` for evidence-backed changes to existing surfaces. |
| Simulated evals are mistaken for approval | Weak evidence enters release decisions | Reuse existing non-validating evidence language from `evals/README.md`. |
| Scaffold markers leak into release | Half-finished skills ship | Make `SEO_GEO_SKILL_STUB` a strict validation failure only in release-bearing paths, with explicit path allowlists for proposal or authoring-reference mentions. |

## Implementation Status

Implemented in the unreleased tree: the derived resolver reference, compatible routing eval seed cases, `/seo:skillify`, 17-command release-surface sync, and strict guardrails for resolver coverage, routing eval target validity, and scaffold stub leakage.
