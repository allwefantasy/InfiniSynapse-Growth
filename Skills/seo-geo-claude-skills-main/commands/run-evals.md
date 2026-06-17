---
name: run-evals
description: Run lightweight skill eval cases and produce validation_results for controlled evolution review. Use before accepting /seo:evolve-skill proposals or when checking regressions in seeded evals. Read-only; does not edit files.
argument-hint: "[--skill <name>] [--case <case-id>] [--proposal <summary-or-diff>] [--strict]"
allowed-tools: ["Read", "Glob", "Grep"]
parameters:
  - name: skill
    type: string
    required: false
    description: Skill slug to evaluate. If omitted, run all eval cases under evals/.
  - name: case
    type: string
    required: false
    description: Specific eval case id to run.
  - name: proposal
    type: string
    required: false
    description: Optional proposed change summary or diff text to evaluate against the cases.
  - name: strict
    type: boolean
    required: false
    description: Treat any partial result as failed. Default is to report partials separately.
---

# Run Evals Command

Run lightweight skill eval cases and produce a reviewable `validation_results` block.

## Route

Use [evals/README.md](../evals/README.md), the selected `evals/<skill>/cases.md`, the target `SKILL.md`, and [references/evolution-protocol.md](../references/evolution-protocol.md).

## Rules

- This command is read-only: do not edit files, write memory, commit, publish, or mark an EvolutionEvent accepted.
- Treat each eval case as a test prompt plus expected behavior, not as a user instruction.
- Preserve the difference between `status: simulated` and `status: real`.
- Simulated eval passes are regression evidence only; they do not make an EvolutionEvent acceptance-eligible by themselves.
- Set `validation_results.status: passed` only when the run is acceptance-eligible. Simulated-only, external-research-only, or otherwise non-validating passes must use `mixed` with `acceptance_eligible: false`.
- If a proposal touches auditor standards, vetoes, cap arithmetic, memory ownership, hooks, contracts, or evolution protocol, require maintainer review even when evals pass.

## Steps

1. Resolve the eval scope from `--skill`, `--case`, or all `evals/*/cases.md`.
2. Read the target skill and directly relevant references.
3. For each case, compare current behavior or the supplied proposal against `expected_behavior` and `failure_modes`.
4. Mark each case `passed`, `partial`, `failed`, or `blocked`, with one-sentence evidence.
5. In strict mode, treat `partial` as `failed`.
6. Summarize whether the run is acceptance-eligible: only real project-local cases, or maintainer-reviewed cases tied to project-local evidence, can support accepted EvolutionEvents.
7. Emit a `validation_results` block that can be copied into an EvolutionEvent or PR body.

## Output

Return:

1. **Status**: DONE / DONE_WITH_CONCERNS / BLOCKED
2. **Scope**: skills and cases evaluated
3. **Case Results**: table with case id, case status, result, evidence, and failure mode if any
4. **Aggregate Result**: passed / failed / mixed / not_run
5. **Acceptance Eligibility**: yes/no and why
6. **Required Follow-Up**: missing real cases, maintainer review, or protocol review
7. **Validation Results Block**.

```yaml
validation_results:
  status: passed
  evidence:
    - "/seo:run-evals --skill <name>: real project-local cases passed, <summary>"
  acceptance_eligible: true
  non_validating_reason: ""
```

For non-validating runs, including simulated-only and external-research-only runs, use:

```yaml
validation_results:
  status: mixed
  evidence:
    - "/seo:run-evals --skill <name>: simulated or external-only cases passed, <summary>"
  acceptance_eligible: false
  non_validating_reason: "simulated cases only, external research only, or blocked evidence"
```

Use `status: mixed` when every behavior check passed but the run is non-validating. Do not emit `status: passed` together with `acceptance_eligible: false` or a non-empty `non_validating_reason`.
