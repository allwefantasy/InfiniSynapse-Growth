#!/usr/bin/env python3
"""Remove URL clusters from Evaluation basis blockquote; keep prose EEAT signal."""
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

REPLACEMENT = (
    "> **Evaluation basis**: We build and evaluate InfiniSynapse on production customer workflows. "
    "Governance, adoption, and security context is cited inline throughout this guide—not in a "
    "standalone reference list."
)

PATTERN = re.compile(
    r"> \*\*Evaluation basis\*\*:[^\n]*\[(?:[^\]]+)\]\([^)]+\)[^\n]*\n",
    re.M,
)


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not PATTERN.search(text):
        return False
    new_text = PATTERN.sub(REPLACEMENT + "\n", text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if process(art):
                n += 1
                print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {n} articles")


if __name__ == "__main__":
    main()
