#!/usr/bin/env python3
"""Fix awkward ': Citation sentence' joins from automated weave pass."""
from __future__ import annotations

import re
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

CITATION_STARTS = (
    "Production rollouts should align",
    "Adoption benchmarks in the",
    "The move from dashboard-first BI",
    "Multi-source connector design should follow",
)


def fix_line(line: str) -> str:
    for start in CITATION_STARTS:
        idx = line.find(f": {start}")
        if idx == -1:
            continue
        before = line[:idx].rstrip()
        after = line[idx + 2 :]  # drop ": "
        if before.endswith(":"):
            before = before[:-1].rstrip()
        if before.endswith((".", "!", "?")):
            return f"{before} {after}"
        return f"{before}. {after}"
    return line


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = [fix_line(ln) for ln in original.splitlines()]
    text = "\n".join(lines)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if process(art):
                n += 1
                print(f"fixed: {art.parent.name}")
    print(f"\nFixed {n} articles")


if __name__ == "__main__":
    main()
