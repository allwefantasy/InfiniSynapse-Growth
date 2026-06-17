---
name: skillify
description: Audit whether a proposed or changed SEO/GEO skill is complete, routable, eval-covered, and release-ready. Use when maintainers ask to "skillify" a feature, add a skill, check skill completeness, or prepare a skill authoring PR. Proposal-only; does not edit files.
argument-hint: "<skill-or-feature> [--new] [--category research|build|optimize|monitor|cross-cutting] [--pr-ready]"
allowed-tools: ["Read", "Glob", "Grep"]
parameters:
  - name: target
    type: string
    required: true
    description: Skill slug, category path, command name, or raw feature description to assess.
  - name: new
    type: boolean
    required: false
    description: Treat the target as a proposed new skill instead of an existing surface.
  - name: category
    type: string
    required: false
    description: "Candidate category for new skills: research, build, optimize, monitor, or cross-cutting."
  - name: pr-ready
    type: boolean
    required: false
    description: Include a PR-ready checklist with validation commands and release-surface updates.
---

# Skillify Command

Audit a proposed or changed skill for completeness before it enters release review. This command is read-only: do not edit files, write memory, commit, publish, bump versions, or mark an EvolutionEvent accepted.

## Route

Use:

- [references/skill-resolver.md](../references/skill-resolver.md)
- [references/skill-contract.md](../references/skill-contract.md)
- [references/evolution-protocol.md](../references/evolution-protocol.md)
- the target `SKILL.md`, command file, eval cases, and nearby references when they exist

If the target changes auditor standards, protocol-layer routing, hooks, memory ownership, shared contracts, scoring, vetoes, cap arithmetic, or artifact gates, classify the work as `protocol` risk and require an ADR or decision record.

## Checklist

Score each item as `present`, `partial`, `missing`, or `not_applicable`:

| # | Check | Requirement |
|---|-------|-------------|
| 1 | SKILL file | `SKILL.md` exists or the proposal explains why the surface is not a skill. |
| 2 | Frontmatter | Required fields are valid; `name` matches directory; version fields align when applicable. |
| 3 | Description | Description includes user trigger language, function, and scope boundary. |
| 4 | User triggers | `when_to_use` / `metadata.triggers` use phrases users actually type. |
| 5 | Resolver row | `references/skill-resolver.md` maps the intent and reconciles with skill metadata. |
| 6 | MECE boundary | Adjacent skills and handoff rules are explicit. |
| 7 | Tier 1 viability | The skill can produce useful output with user-provided data and no tools. |
| 8 | Handoff | Handoff Summary includes objective, evidence, open loops, scores, priority items, and URL where relevant. |
| 9 | Eval coverage | Normal, edge, adversarial, and routing cases exist or are proposed. |
| 10 | Release surfaces | README, CLAUDE, VERSIONS, manifests, marketplace mirrors, localized docs, and guardrails are identified when required. |

## Steps

1. Resolve whether the target is an existing skill, proposed skill, command, reference, or protocol surface.
2. Read the target files and the relevant resolver rows.
3. Compare the target against the checklist.
4. Identify routing overlaps and ambiguous trigger phrases.
5. Recommend compatible eval cases using `type: eval-case`, `target_skill`, `expected_behavior`, and `failure_modes`.
6. Classify risk: low, medium, high, or protocol.
7. List validation commands and release-surface updates.
8. If evidence implies a behavior change, recommend `/seo:evolve-skill`; do not accept the change here.

## Output

Return:

1. **Status**: DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_INPUT
2. **Target**: skill, command, reference, or proposed feature
3. **Completeness Score**: N/10 plus item table
4. **Routing Assessment**: primary route, adjacent skills, overlap risks, and handoff sequence
5. **Eval Plan**: existing cases, missing cases, and compatible routing case drafts
6. **Risk**: level and blast radius
7. **Validation Plan**: exact commands and manual review gates
8. **Release Impact**: files that must change before merge
9. **Recommended Next Step**: implement, evolve, defer, or reject

## PR-Ready Checklist

When `--pr-ready` is present, append:

```markdown
- [ ] Target skill or command has valid frontmatter
- [ ] Resolver row exists and reconciles with skill metadata
- [ ] Routing eval cases use the existing eval-case schema
- [ ] Adjacent skills and handoff order are explicit
- [ ] Tier 1 behavior does not require tools
- [ ] Changed skills pass validate-skill.sh
- [ ] validate-slimming-guardrails.sh passes
- [ ] Command inventory and manifests are synchronized when command count changes
- [ ] EvolutionEvent or ADR is included for high/protocol routing changes
```
