#!/usr/bin/env python3
"""De-duplicate shared operations boilerplate into topic-specific sections (generic).

Replaces the block from the first operations boilerplate H2 through (not incl.)
'## Frequently Asked Questions' with two topic-specific H2 sections plus one H3,
weaving the SAME links found in the block (link graph preserved). Produces 3
headings to keep the outline count stable.

Usage: python3 reduce-boilerplate-generic.py <article.md> "<Topic Label>"
"""
import re
import sys
from pathlib import Path

START_HEADS = (
    "## Operational Readiness Notes",
    "## Operational Readiness Checklist",
    "## Implementation Lessons",
    "## Stakeholder Communication Patterns",
    "## Review Cadence and Metrics",
    "## Production Debugging Notes",
    "## Field Notes from Deployments",
)


def main() -> int:
    path = Path(sys.argv[1])
    topic = sys.argv[2]
    text = path.read_text(encoding="utf-8")
    faq = text.find("## Frequently Asked Questions")
    if faq == -1:
        print(f"SKIP {path.parent.name}: no FAQ")
        return 1
    starts = [text.find(h) for h in START_HEADS if 0 <= text.find(h) < faq]
    if not starts:
        print(f"SKIP {path.parent.name}: no boilerplate")
        return 1
    block_start = min(starts)
    block = text[block_start:faq]
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", block)
    mid = (len(links) + 1) // 2
    a, b = links[:mid], links[mid:]

    def weave(ls, lead):
        if not ls:
            return ""
        parts = [f"[{t}]({u})" for t, u in ls]
        if len(parts) == 1:
            return f" {lead} {parts[0]}."
        return f" {lead} {', '.join(parts[:-1])} and {parts[-1]}."

    sec = (
        f"## Operating {topic} in Production\n\n"
        f"Treat {topic} as an operating capability, not a one-off task: confirm owners, metric definitions, "
        f"and review gates for the first workflow before widening scope, because teams that log exceptions weekly "
        f"compound accuracy faster than teams chasing new features. Capture the first reliable run as a reusable "
        f"template — assumptions, checks, and reviewer sign-off in one playbook — so quality holds when data, "
        f"schemas, or priorities change.{weave(a, 'Ground these controls in')}\n\n"
        f"### What to review on a regular cadence\n\n"
        f"Audit {topic} monthly: compare rerun consistency, validation pass rate, and time-to-first-insight against "
        f"baseline, retire stale definitions, and re-confirm access scopes so silent drift is caught before it reaches "
        f"a stakeholder report.\n\n"
        f"## Communicating Results to Stakeholders\n\n"
        f"Share a concise weekly brief with platform and business leads — what ran, what was reviewed, and which "
        f"assumptions are open — so {topic} stays aligned with governance and stakeholders can inspect intermediate "
        f"steps without waiting for a rebuild. When cycle time improves but reopen rates climb, pause net-new features "
        f"and fix definitions first, since most accuracy problems trace to stale dimensions, not weak models."
        f"{weave(b, 'Align governance and review practices with')}\n\n"
    )
    new_text = re.sub(r"\n{3,}", "\n\n", text[:block_start] + sec + text[faq:])
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.parent.name}: consolidated {len(links)} links for '{topic}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
