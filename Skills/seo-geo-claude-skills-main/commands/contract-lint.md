---
name: contract-lint
description: Validate auditor Runbook inline copies, handoff schema compliance, controlled-evolution guardrails, and jargon leaks across all SKILL.md files. Produces drift report.
argument-hint: "[--skill <name>] [--strict]"
allowed-tools: ["Read", "Grep", "Bash"]
parameters:
  - name: skill
    type: string
    required: false
    description: Limit the scan to a single skill directory. If omitted, scans all skills in the library.
  - name: strict
    type: boolean
    required: false
    description: Exit with non-zero status if ANY drift is found (for CI use). Default is report-only.
---

# Contract Lint

Validate auditor Runbook drift, handoff schema compliance, and user-facing jargon leaks.

## Source of Truth

[references/auditor-runbook.md §6 Lint Coverage Manifest](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/auditor-runbook.md) wins if this command and the runbook disagree.

## Checks

1. Locate auditor skills by `class: auditor` and `runbook-sync` markers.
2. Verify exactly one ordered start/end marker per auditor.
3. Compare `source_sha256` with `references/auditor-runbook.md`.
4. Compare `block_sha256` with the inline block and source §1-5.
5. Verify Handoff Summary schema, cap fields, Artifact Gate, and User-Facing Translation rules.
6. Scan controlled evolution surfaces for contract breakage:
   - `/seo:evolve-skill` keeps signal isolation wording.
   - `skill_inferred` is never described as user approval.
   - EvolutionEvents cannot bypass `memory/decisions.md` provenance rules.
   - Accepted EvolutionEvents require `simulation: false`, project-local `source_signal.kind`, user or maintainer approval, `validation_results.status: passed`, `validation_results.acceptance_eligible: true`, and validation evidence.
   - Simulated and external-research-only EvolutionEvents cannot be accepted.
   - Auditor-related proposals default to protocol risk and cannot lower veto, cap, BLOCKED, or artifact-gate standards.
   - `/seo:evolve-skill` remains proposal-only and cannot edit workflow, memory, hook, manifest, version, or release surfaces.
7. Scan outputs/docs for forbidden internal jargon leakage.

## Output

PASS/FAIL summary, per-file drift, expected vs found hashes, schema gaps, evolution guardrail gaps, jargon leaks, and strict-mode exit recommendation.
