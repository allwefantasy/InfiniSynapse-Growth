#!/usr/bin/env python3
"""Audit article.md outline: exactly 1 H1; H2+H3+H4 between 20 and 30; valid hierarchy."""
from __future__ import annotations

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

H2_H3_H4_MIN = 20
H2_H3_H4_MAX = 30


def parse_headings(text: str) -> list[tuple[int, int, str]]:
    headings: list[tuple[int, int, str]] = []
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    return headings


def audit(text: str) -> list[str]:
    heads = parse_headings(text)
    fails: list[str] = []
    h1 = sum(1 for _, lvl, _ in heads if lvl == 1)
    h2 = sum(1 for _, lvl, _ in heads if lvl == 2)
    h3 = sum(1 for _, lvl, _ in heads if lvl == 3)
    h4 = sum(1 for _, lvl, _ in heads if lvl == 4)
    sub = h2 + h3 + h4

    if h1 != 1:
        fails.append(f"H1 count {h1} (must be exactly 1)")
    if sub < H2_H3_H4_MIN:
        fails.append(f"H2+H3+H4={sub} (need {H2_H3_H4_MIN}-{H2_H3_H4_MAX})")
    if sub > H2_H3_H4_MAX:
        fails.append(f"H2+H3+H4={sub} (need {H2_H3_H4_MIN}-{H2_H3_H4_MAX})")

    prev = 0
    for line_no, lvl, title in heads:
        if lvl == 3 and prev < 2:
            fails.append(f"H3 without parent H2 at line {line_no}: {title[:40]}")
        if lvl == 4 and prev < 3:
            fails.append(f"H4 without parent H3 at line {line_no}: {title[:40]}")
        if lvl == 1 and prev not in (0, 1):
            fails.append(f"H1 not at document top (line {line_no})")
        prev = lvl

    # Body text before first H2 (excluding meta block) should be minimal
    lines = text.splitlines()
    first_h2 = next((i for i, l in enumerate(lines) if l.startswith("## ") and not l.startswith("## Table")), None)
    if first_h2 is not None:
        between = "\n".join(lines[:first_h2])
        if re.search(r"^#{3,4}\s", between, re.M):
            fails.append("H3/H4 appears before first H2")

    return fails


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = fail_n = 0
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            fails = audit(art.read_text(encoding="utf-8"))
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
