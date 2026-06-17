# SEO & GEO Skills Library - Versions

Current versions for the plugin and all 21 skills. Agents can fetch this file from `https://raw.githubusercontent.com/aaron-he-zhu/seo-geo-claude-skills/main/VERSIONS.md` once per session.

**Current release**: `9.9.5` (2026-04-28). Skill `version`, `metadata.version`, plugin manifests, marketplace files, badges, and `CITATION.cff` are aligned to the same public version.

## Skills

| Skill | Category | Version | Last Updated |
|-------|----------|---------|--------------|
| keyword-research | research | 9.9.5 | 2026-04-28 |
| competitor-analysis | research | 9.9.5 | 2026-04-28 |
| serp-analysis | research | 9.9.5 | 2026-04-28 |
| content-gap-analysis | research | 9.9.5 | 2026-04-28 |
| seo-content-writer | build | 9.9.5 | 2026-04-28 |
| seo-blog-content | build | 1.0.0 | 2026-06-08 |
| geo-content-optimizer | build | 9.9.5 | 2026-04-28 |
| meta-tags-optimizer | build | 9.9.5 | 2026-04-28 |
| schema-markup-generator | build | 9.9.5 | 2026-04-28 |
| on-page-seo-auditor | optimize | 9.9.5 | 2026-04-28 |
| technical-seo-checker | optimize | 9.9.5 | 2026-04-28 |
| internal-linking-optimizer | optimize | 9.9.5 | 2026-04-28 |
| content-refresher | optimize | 9.9.5 | 2026-04-28 |
| rank-tracker | monitor | 9.9.5 | 2026-04-28 |
| backlink-analyzer | monitor | 9.9.5 | 2026-04-28 |
| performance-reporter | monitor | 9.9.5 | 2026-04-28 |
| alert-manager | monitor | 9.9.5 | 2026-04-28 |
| content-quality-auditor | cross-cutting | 9.9.5 | 2026-04-28 |
| domain-authority-auditor | cross-cutting | 9.9.5 | 2026-04-28 |
| entity-optimizer | cross-cutting | 9.9.5 | 2026-04-28 |
| memory-management | cross-cutting | 9.9.5 | 2026-04-28 |

## Changelog

### Unreleased

**Added**: `build/seo-blog-content` — InfiniSynapse 90-article pillar cluster publish gates (high-DR external links, ≤30% URL overlap, internal cluster links, Target keyword, outline structure). Registered in plugin and marketplace manifests.

### Unreleased (prior)

No other unreleased changes.

### v9.9.5 - Skill authoring and routing resolver (2026-04-28)

Adds a read-only skill authoring workflow and explicit routing review surfaces while preserving the content-only operating model.

**Added**: `/seo:skillify` as a read-only skill authoring audit; `references/skill-resolver.md` as a derived routing review index; compatible routing eval seed cases inside target skill eval files; routing coverage documentation in `/seo:validate-library`; and strict guardrails for resolver coverage, routing eval target validity, command inventory, and scaffold stub leakage.

**Changed**: synchronized the command inventory from 16 to 17 commands across README, CLAUDE, AGENTS, CITATION, plugin manifests, marketplace mirrors, Gemini/Qwen/CodeBuddy manifests, and guardrails. Skill `version` and `metadata.version` fields are aligned to 9.9.5.

**Protected**: all 20 skills and 17 commands remain. Routing evals stay inside existing `eval-case` files and simulated cases remain non-validating until tied to project-local evidence.

### v9.9.0 - Simulation-complete controlled evolution candidate (2026-04-27)

Simulation-complete release candidate for controlled skill evolution. This version makes self-improvement reviewable and parser-guarded while keeping simulated evidence explicitly non-validating.

**Added**: controlled evolution workflow surfaces with `/seo:evolve-skill` and `/seo:run-evals`; 16 simulated eval cases across `geo-content-optimizer`, `content-quality-auditor`, `memory-management`, and failure-probe scenarios; accepted, rejected, and superseded EvolutionEvent samples; PR-grade mock evidence in `references/evolution-pr-grade-mock.md`; failure probes in `references/evolution-failure-probes.md`; PR-template evolution metadata; `references/evolution-protocol.md`; `references/evolution-optimization-plan.md`; `references/evolution-evidence-review.md`; and `memory/evolution/` for controlled skill improvement records.

**Changed**: retired the temporary `/seo:p2-review` command and replaced its maintenance slot with the eval execution entrypoint. All public manifests and skill versions are aligned to 9.9.0.

**Guarded**: `/seo:evolve-skill` is proposal-only with no edit permission; simulated and external-research-only evidence cannot be accepted; accepted events require approval, `validation_results.status: passed`, `validation_results.acceptance_eligible: true`, validation evidence, project-local provenance, risk, and rollback; validation and contract-lint command docs include controlled evolution checks; parser-grade slimming guardrails protect command inventory, EvolutionEvent schema, PR-grade mock evidence, failure probes, retired command references, and evolution surfaces.

**Protected**: all 20 skills and 16 commands remain. The 9.9.0 evolution layer is simulation-complete but still requires project-local evidence and human approval before an event can become accepted.

### v9.5.0 - Consolidated post-v9.0.0 release (2026-04-26)

Single public release consolidating all work after v9.0.0.

**Changed**: fixed `/seo:geo-drift-check` prompt-injection false positive; replaced the Windows-incompatible marketplace symlink with a real mirror; added `allowed-tools` to `/seo:contract-lint` from PR #10; compressed regular skill shells, commands, root docs, and high-volume reference packs; added `scripts/validate-slimming-guardrails.sh`; strengthened `validate-skill.sh` for shared-section checks and auditor runbook hash validation; updated release workflow checks; aligned cross-agent manifests, marketplace files, badges, `CITATION.cff`, and all skill versions; replaced interactive Stop hooks with an allow-only JSON Stop guard.

**Protected**: all 20 skills and 15 commands remain. Discovery aliases, CORE-EEAT, CITE, auditor runbook semantics, memory/entity contracts, schema placeholders, technical audit fields, reporting benchmarks, freshness rules, CTA logic, intent mapping, anchor thresholds, KPI formulas, WCAG checks, rich-result policy checks, and backlink disavow safeguards are preserved.

**Credit**: PR #10 from @xiaolai identified the missing `/seo:contract-lint` `allowed-tools` declaration.

### v9.0.0 - Quality pass + multi-agent compatibility (2026-04-17)

Combined a 6-agent quality review, legal/compliance hardening, directly executable playbooks, and native install support for Gemini CLI, Qwen Code, Amp, Kimi Code CLI, and CodeBuddy. No breaking changes to skill I/O contracts.

Highlights:

- Added `SECURITY.md`, FTC disclosure checks, GDPR retention/deletion flow, EU AI Act TDM notes, WCAG 2.2 AA alt-text ordering, schema truth warnings, and trademark annotations.
- Added playbooks for AI Overview recovery, bulk audits, ecommerce platform issues, LLM crawler handling, migrations, entity/GEO handoff, and GEO score feedback loops.
- Added `/seo:geo-drift-check`.
- Trimmed 11 large `SKILL.md` files and moved execution detail to compact `references/instructions-detail.md` files.
- Added Handoff Summary coverage for all skills.
- Expanded memory scaffolding and terminology.
- Hardened auditor cap arithmetic, runbook hash alignment, Next Best Skill termination, wiki ownership, and HOT cache identity.
- Split commands into 10 user commands and 5 maintenance commands.
- Removed all Python scripts; maintenance utilities are markdown slash commands plus the retained Bash validator.

### Earlier releases

Earlier versions are documented in [GitHub Releases](https://github.com/aaron-he-zhu/seo-geo-claude-skills/releases).
