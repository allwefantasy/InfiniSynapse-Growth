#!/usr/bin/env python3
"""De-duplicate the shared pillar4 operations boilerplate into source-specific sections.

For each target article, replaces the block from the first operations boilerplate
H2 through (but not including) '## Frequently Asked Questions' with two
source-specific sections that weave the SAME links found in the original block,
so the external/internal link graph is preserved while the prose stops being an
exact cross-file duplicate.

Usage: python3 reduce-pillar4-boilerplate.py <article.md> "<Source Label>"
"""
import re
import sys
from pathlib import Path

START_HEADS = (
    "## Operational Readiness Notes",
    "## Implementation Lessons",
    "## Stakeholder Communication Patterns",
    "## Review Cadence and Metrics",
)


def main() -> int:
    path = Path(sys.argv[1])
    src = sys.argv[2]
    text = path.read_text(encoding="utf-8")

    faq = text.find("## Frequently Asked Questions")
    if faq == -1:
        print(f"SKIP {path.parent.name}: no FAQ")
        return 1
    # find earliest boilerplate heading before FAQ
    starts = [text.find(h) for h in START_HEADS if 0 <= text.find(h) < faq]
    if not starts:
        print(f"SKIP {path.parent.name}: no boilerplate block")
        return 1
    block_start = min(starts)
    block = text[block_start:faq]

    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", block)
    # split links across the two sections
    mid = (len(links) + 1) // 2
    a, b = links[:mid], links[mid:]

    def weave(ls):
        if not ls:
            return ""
        parts = [f"[{t}]({u})" for t, u in ls]
        if len(parts) == 1:
            return f" Ground connector and review decisions in {parts[0]}."
        head = ", ".join(parts[:-1])
        return f" Ground connector and review decisions in {head} and {parts[-1]}."

    sec = (
        f"## Operating {src} Analysis at Scale\n\n"
        f"Treat a {src} rollout as an operating capability, not a one-time setup: confirm owners, "
        f"metric contracts, and review gates for the first workflow before widening scope, because teams "
        f"that log exceptions weekly compound accuracy faster than teams chasing new connectors. Capture the "
        f"first successful query path as a template — assumptions, validation SQL, and reviewer sign-off in one "
        f"playbook — and track connection uptime, validation pass rate, and time-to-first-insight against a "
        f"monthly baseline, adjusting memory cards when definitions drift.{weave(a)}\n\n"
        f"## Communicating {src} Connector Health\n\n"
        f"Share weekly {src} connector health with platform and analytics leads in a one-page brief — sources "
        f"connected, queries reviewed, and open schema questions — so adoption stays aligned with governance and "
        f"stakeholders can open intermediate steps without waiting for a rebuild. When cycle time improves but "
        f"reopen rates climb, pause net-new features and fix definitions first, since most accuracy problems trace "
        f"to stale dimensions, not weak models.{weave(b)}\n\n"
    )

    new_text = text[:block_start] + sec + text[faq:]
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.parent.name}: consolidated {len(links)} links into 2 sections for '{src}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
