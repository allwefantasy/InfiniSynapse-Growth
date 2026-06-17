#!/usr/bin/env python3
"""Fix citations glued to --- rules or table rows by spread-citations pass."""
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

CITATION_START = re.compile(
    r"(Regulated rollouts|Enterprise AI adoption|Operational maturity|Foundational warehouse|"
    r"LLM-backed analytics|Production rollouts|Adoption benchmarks|The move from dashboard|"
    r"Leaderboard scores|The \[BIRD)"
)


def fix_line(line: str) -> str:
    # ---. Sentence...
    m = re.match(r"^---\.\s+(.+)$", line.strip())
    if m:
        return "---\n\n" + m.group(1)

    # Table row with glued sentence: | a | b | c |. Sentence
    if line.strip().startswith("|") and "|." in line:
        idx = line.find("|.")
        row = line[: idx + 1].rstrip()
        rest = line[idx + 2 :].lstrip()
        if CITATION_START.search(rest):
            return row + "\n\n" + rest
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
