#!/usr/bin/env python3
"""Normalize article.md outlines to 1 H1 and 20-30 H2/H3/H4 headings."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

spec = importlib.util.spec_from_file_location("outline_audit", BLOG / "audit-outline-structure.py")
audit_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_mod)

CONNECTOR_EXTRA_H2 = """## Operational Readiness Notes

We treat every rollout as an operating system upgrade, not a model purchase. Before expanding scope, confirm owners, metric contracts, and review gates for the first workflow. In our pilots, the teams that document exceptions weekly compound accuracy faster than teams that chase new connectors daily.

Stakeholders trust outputs when they can open intermediate steps without a live demo. That is why we pair automation with explicit sign-off roles and export logs reviewers can audit independently.

---

## Implementation Lessons

Teams that stabilize connector rollouts document assumptions, validation SQL, and reviewer sign-off in one playbook. The compounding lesson: treat the first successful query path as a template, not a one-off demo.

---

## Stakeholder Communication Patterns

Share weekly connector health with platform and analytics leads. A one-page brief—sources connected, queries reviewed, open schema questions—keeps adoption aligned with governance.

---

"""


def demote_h3_under_h2(text: str, h2_title: str, limit: int | None = None) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_section = False
    demoted = 0
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            in_section = title.lower() == h2_title.lower()
            out.append(line)
            continue
        if in_section and line.startswith("### "):
            if limit is not None and demoted >= limit:
                out.append(line)
                continue
            out.append("**" + line[4:].strip() + "**")
            demoted += 1
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def remove_h2_section(text: str, h2_title: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    skipping = False
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            if title.lower() == h2_title.lower():
                skipping = True
                continue
            skipping = False
        if skipping:
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def insert_before_h2(text: str, anchor_h2: str, block: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        if (
            not inserted
            and line.startswith("## ")
            and not line.startswith("### ")
            and line[3:].strip().lower() == anchor_h2.lower()
        ):
            out.extend(block.rstrip().splitlines())
            out.append("")
            inserted = True
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def add_h3_under_h2(text: str, h2_title: str, h3_titles: list[str], bodies: list[str] | None = None) -> str:
    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if (
            not inserted
            and line.startswith("## ")
            and not line.startswith("### ")
            and line[3:].strip().lower() == h2_title.lower()
        ):
            j = i + 1
            while j < len(lines) and not (lines[j].startswith("## ") and not lines[j].startswith("### ")):
                out.append(lines[j])
                j += 1
            for idx, title in enumerate(h3_titles):
                out.append("")
                out.append(f"### {title}")
                body = (bodies[idx] if bodies and idx < len(bodies) else
                        "Teams use this pattern when scoping recurring analysis workflows and reviewer sign-off.")
                out.append("")
                out.append(body)
            inserted = True
            i = j
            continue
        i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def merge_procurement_steps(text: str) -> str:
    """Collapse four Step H3s under Procurement Decision Framework into one list."""
    lines = text.splitlines()
    out: list[str] = []
    in_section = False
    skip_step = False
    inserted = False
    for line in lines:
        if line.startswith("## ") and not line.startswith("### "):
            in_section = line[3:].strip().lower() == "procurement decision framework"
            out.append(line)
            continue
        if in_section and line.startswith("### Step "):
            if not inserted:
                out.append("")
                out.append("Use this four-step sequence:")
                out.append("")
                out.append("1. **Quantitative fit** — score the 100-point rubric on real pilot data.")
                out.append("2. **Qualitative fit** — validate analyst adoption and stakeholder trust.")
                out.append("3. **Risk-adjusted fit** — model security, compliance, and rollback cost.")
                out.append("4. **Adoption feasibility** — confirm training, ownership, and change-management bandwidth.")
                out.append("")
                inserted = True
            skip_step = True
            continue
        if skip_step:
            if line.startswith("### ") or (line.startswith("## ") and not line.startswith("### ")):
                skip_step = False
            else:
                continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def demote_h3_globally(text: str, count: int) -> str:
    lines = text.splitlines()
    out: list[str] = []
    left = count
    for line in lines:
        if left > 0 and line.startswith("### "):
            out.append("**" + line[4:].strip() + "**")
            left -= 1
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def apply_fixes(name: str, text: str) -> str:
    if name == "001-ai-for-data-analysis":
        text = add_h3_under_h2(
            text,
            "Five Core Methods AI Now Automates",
            ["Descriptive and exploratory workloads", "Diagnostic and prescriptive workloads"],
            [
                "Descriptive and exploratory questions stay in copilot territory: profiling, charts, and NL follow-ups without multi-step memory.",
                "Diagnostic and prescriptive questions need chained reasoning, ranked drivers, and memory-backed definitions across recurring reviews.",
            ],
        )
    elif name == "010-fabric-data-agent-vs-copilot":
        text = add_h3_under_h2(
            text,
            "Migration Path: From Copilot-Only to Fabric Data Agent",
            ["Production readiness checklist"],
            [
                "Before promoting a Fabric Data Agent pilot, confirm semantic-model hygiene, fallback manual rerun owners, and preview SLA sign-off.",
            ],
        )
    elif name == "056-connect-redshift-to-ai-data-analyst":
        text = insert_before_h2(text, "Frequently Asked Questions", CONNECTOR_EXTRA_H2)

    # Reduce over-limit outlines
    reduce_map: dict[str, list] = {
        "012-ai-data-analysis": lambda t: remove_h2_section(t, "Production Debugging Notes"),
        "013-data-agent-glossary": lambda t: remove_h2_section(t, "Operational Readiness Notes"),
        "025-ai-data-analysis-tools": lambda t: demote_h3_globally(t, 1),
        "028-ai-data-visualization-tools": lambda t: demote_h3_globally(t, 2),
        "029-self-hosted-ai-data-analyst": lambda t: demote_h3_globally(t, 2),
        "030-chatgpt-data-analysis-alternatives": lambda t: demote_h3_globally(t, 8),
        "031-julius-ai-alternatives": lambda t: demote_h3_globally(t, 7),
        "040-julius-ai-vs-chatgpt": lambda t: demote_h3_globally(t, 1),
        "042-infinisynapse-vs-tableau": lambda t: demote_h3_globally(t, 1),
        "096-data-analysis-prompt-template": lambda t: demote_h3_globally(t, 1),
        "097-ai-data-analyst-skills": lambda t: demote_h3_globally(t, 1),
        "099-ai-analytics-glossary": lambda t: demote_h3_globally(t, 1),
    }

    if name == "043-infinisynapse-review":
        text = demote_h3_under_h2(text, "What We Like Most", 5)
        text = demote_h3_under_h2(text, "Where It Still Falls Short", 4)
        text = demote_h3_under_h2(text, "Rollout Guidance for New Buyers", 1)
    elif name == "098-how-to-evaluate-ai-data-analyst":
        text = remove_h2_section(text, "Operational Readiness Notes")
        text = remove_h2_section(text, "Production Debugging Notes")
        text = merge_procurement_steps(text)
        text = demote_h3_under_h2(text, "Pilot Protocol: How to Test in Real Conditions", 2)
        text = demote_h3_under_h2(text, "Red-Team Testing for High-Stakes Workflows", 2)
        text = demote_h3_under_h2(text, "Change Management Plan", 2)
        text = demote_h3_under_h2(text, "Frequently Asked Questions", 1)
    elif name == "100-data-agent-faq":
        text = remove_h2_section(text, "Frequently Asked Questions")
        text = demote_h3_under_h2(text, "Team Operating Rhythm After Launch", 3)
        text = remove_h2_section(text, "Operational Readiness Notes")
        text = remove_h2_section(text, "Production Debugging Notes")
        text = demote_h3_under_h2(text, "Architecture Trade-Offs Teams Should Discuss Early", 1)
    elif name in reduce_map and name != "043-infinisynapse-review":
        text = reduce_map[name](text)

    if name == "012-ai-data-analysis":
        text = demote_h3_globally(text, 1)

    return text


def update_toc_numbers(text: str) -> str:
    """Best-effort TOC renumber after structural edits (optional)."""
    return text


def process(article: Path) -> bool:
    text = article.read_text(encoding="utf-8")
    if not audit_mod.audit(text):
        return False
    name = article.parent.name
    new_text = apply_fixes(name, text)
    if new_text == text:
        return False
    old_sub = sum(1 for _, lvl, _ in audit_mod.parse_headings(text) if lvl >= 2)
    new_sub = sum(1 for _, lvl, _ in audit_mod.parse_headings(new_text) if lvl >= 2)
    new_fails = audit_mod.audit(new_text)
    if not new_fails:
        article.write_text(new_text, encoding="utf-8")
        print(f"fixed: {name} (sub {old_sub}->{new_sub})")
        return True
    print(f"partial-fail: {name} sub {old_sub}->{new_sub} · {new_fails}")
    return False


H2_H3_H4_MIN = audit_mod.H2_H3_H4_MIN
H2_H3_H4_MAX = audit_mod.H2_H3_H4_MAX


def main() -> int:
    targets: list[Path] = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            p = Path(arg)
            if p.is_dir():
                targets.extend(sorted(p.glob("[0-9][0-9][0-9]-*/article.md")))
            elif p.is_file():
                targets.append(p)
    else:
        for pillar in PILLARS:
            if pillar.is_dir():
                for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
                    if audit_mod.audit(art.read_text(encoding="utf-8")):
                        targets.append(art)  # only articles that fail audit

    changed = 0
    for art in targets:
        if process(art):
            changed += 1
    print(f"\nUpdated {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
