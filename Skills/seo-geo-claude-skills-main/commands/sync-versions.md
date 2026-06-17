---
name: sync-versions
description: Propagate the canonical version from .claude-plugin/plugin.json to all cross-agent manifest files so Gemini, Qwen, CodeBuddy, and the skills.sh marketplace stay in lockstep with the Claude Code manifest. Reads and writes JSON files directly, then runs the Bash release guardrail.
argument-hint: "[--dry-run]"
allowed-tools: ["Read", "Edit", "Bash"]
parameters:
  - name: dry-run
    type: boolean
    required: false
    description: Report what would change without writing. Default is apply.
---

# Sync Versions Command

Propagate the canonical version from `.claude-plugin/plugin.json` to release surfaces.

## Files

`.claude-plugin/plugin.json`, `marketplace.json`, `.claude-plugin/marketplace.json`, `gemini-extension.json`, `qwen-extension.json`, `.codebuddy-plugin/marketplace.json`, `CITATION.cff`, `README.md`, `docs/README.zh.md`, `CLAUDE.md`, and `VERSIONS.md`.

## Steps

1. Read canonical plugin version.
2. Compare every release surface.
3. In dry-run mode, report drift only.
4. In apply mode, update version fields and badges, then keep both marketplace files byte-identical.
5. Run `bash scripts/validate-slimming-guardrails.sh` afterward.

## Output

Changed files, unchanged files, unresolved manual checks, and validation command.
