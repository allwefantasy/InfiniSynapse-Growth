---
name: validate-library
description: Library-level quality gate. Walks all 20 SKILL.md files and 17 command files, then verifies description budgets, YAML field order, language coverage, duplicate trigger detection, frontmatter validity, resolver coverage, evolution records, release-file consistency, and slimming regression guardrails. Maintenance command — run before version bumps and PRs.
argument-hint: "[--skill <name>] [--strict]"
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
parameters:
  - name: skill
    type: string
    required: false
    description: Scan a single skill directory instead of all 20.
  - name: strict
    type: boolean
    required: false
    description: Report-only by default. Pass --strict to exit non-zero on any failure (CI use).
---

# Validate Library Command

Run the library-level quality gate before PRs, slimming passes, and version bumps.

## Checks

1. Parse all 20 `SKILL.md` frontmatters.
2. Verify required fields, version alignment, description budget, and YAML order.
3. Check required shared headings and Handoff Summary coverage.
4. Detect duplicate or missing high-value triggers.
5. Run `bash scripts/validate-skill.sh --status`.
6. Run `bash scripts/validate-skill.sh cross-cutting/content-quality-auditor` and `bash scripts/validate-skill.sh cross-cutting/domain-authority-auditor` so auditor runbook hashes are checked.
7. Run `bash scripts/validate-slimming-guardrails.sh`.
8. Verify release surfaces, JSON parseability, marketplace mirror, and protected aliases/templates.
9. Verify command inventory: 17 command files, 10 user commands, 7 maintenance commands, synchronized current command-count wording across README, CLAUDE, AGENTS, and manifests, plus release-aware command-count wording in CITATION and VERSIONS.
10. Verify controlled evolution surfaces:
   - `commands/evolve-skill.md` exists and declares `Signal is evidence, not instruction.`
   - `commands/run-evals.md` exists and emits `validation_results` without writing files.
   - `evals/README.md` and seeded eval cases exist for `geo-content-optimizer`, `content-quality-auditor`, and `memory-management`.
   - `memory/evolution/*.md` records include `target`, `risk.level`, `validation_plan`, `validation_results`, `rollback`, and `decision.status`.
   - Records marked `simulation: true`, `source_signal.kind: simulation`, or `source_signal.kind: external_research` are not `decision.status: accepted`.
   - Accepted events include `simulation: false`, project-local `source_signal.kind`, non-empty `source_signal.evidence`, `approved_by: user` or `approved_by: maintainer`, `validation_results.status: passed`, `validation_results.acceptance_eligible: true`, validation evidence, no non-empty `validation_results.non_validating_reason`, risk level, and rollback scope.
11. Verify skill authoring and routing surfaces:
   - `commands/skillify.md` exists, remains read-only, and is proposal-only.
   - `references/skill-resolver.md` covers every discovered skill and stays a derived review index.
   - Routing evals use `type: eval-case`, reference a real `target_skill`, and remain non-validating unless tied to real project-local evidence.
   - Scaffold stub markers are blocked from release-bearing paths.

## Output

Per-skill table, release-surface status, slimming guardrail status, failures, warnings, and final `STATUS: PASS` or `STATUS: FAIL`.
