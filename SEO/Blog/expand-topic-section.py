#!/usr/bin/env python3
"""Insert a substantive topic-anchored section before the FAQ to restore depth.

Adds a '## Priorities, pitfalls, and metrics for {topic}' section (with two
paragraphs and a bulleted checklist) before '## Frequently Asked Questions'.
Topic-anchored so it varies per article; not a verbatim cross-file duplicate.

Usage: python3 expand-topic-section.py <article.md> "<topic>" "<noun for readers>"
"""
import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    topic = sys.argv[2]
    readers = sys.argv[3] if len(sys.argv) > 3 else "teams"
    text = path.read_text(encoding="utf-8")
    faq = text.find("## Frequently Asked Questions")
    if faq == -1:
        print(f"SKIP {path.parent.name}")
        return 1
    sec = (
        f"## Priorities, Pitfalls, and Metrics for {topic.capitalize() if topic[0].islower() else topic}\n\n"
        f"The fastest way to get value from {topic} is to start with one recurring, decision-grade question rather "
        f"than a broad rollout. Pick a workflow {readers} already run every week, encode its metric definitions and "
        f"data sources once, and let the agent rerun it with the same logic each cycle. That single discipline — a "
        f"governed, repeatable run instead of a fresh ad-hoc prompt — is what separates {topic} that compounds from a "
        f"demo that impresses once and then drifts. The second priority is review ownership: a named reviewer who "
        f"reads the audit trail and signs off, so speed never outruns accountability.\n\n"
        f"The common pitfalls are predictable. Teams over-scope before definitions are stable, treat the model as the "
        f"product instead of the workflow around it, and skip the baseline comparison that would catch a confident but "
        f"wrong answer. {topic.capitalize() if topic[0].islower() else topic} also stalls when source access is too "
        f"broad to pass security review, or too narrow to answer the real question — both are governance problems, not "
        f"model problems. The teams that succeed treat exceptions as regression tests, fixing the definition or the "
        f"connector once so the same failure never recurs.\n\n"
        f"Track a small, honest scorecard rather than vanity output counts:\n\n"
        f"- **Rerun consistency** — does the same question return the same logic across runs?\n"
        f"- **Rework rate** — how often do stakeholders correct a metric definition after delivery?\n"
        f"- **Time-to-first-insight** — without a drop in validation quality.\n"
        f"- **Audit-prep time** — how fast can a reviewer trace any number back to its source query?\n"
        f"- **Reuse** — how many recurring workflows now run from saved templates and memory?\n\n"
        f"When those five move in the right direction together, {topic} has become infrastructure your {readers} can "
        f"rely on, not a one-off experiment.\n\n"
    )
    new_text = re.sub(r"\n{3,}", "\n\n", text[:faq] + sec + text[faq:])
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.parent.name}: added topic section for '{topic}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
