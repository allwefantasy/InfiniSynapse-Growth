#!/usr/bin/env python3
"""Repair section/FAQ merges: inline ## headers, glued --- rules, merged FAQ ### lines."""
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

WEAVE_DUPES = [
    "Enterprise AI adoption guidance in ",
    "Adoption benchmarks in the ",
    "The move from dashboard-first BI to augmented workflows",
]


def repair(text: str) -> str:
    # Glued horizontal rules at paragraph ends
    text = re.sub(r" ---\s*\n", "\n\n---\n\n", text)
    text = re.sub(r" ---(?=\s*$)", "", text, flags=re.M)

    # Inline H2/H3 not at line start (preserve markdown links)
    text = re.sub(r"(?<!\n)(?<![#\[]) ## ", "\n\n## ", text)
    text = re.sub(r"(?<!\n)(?<![#\[]) ### ", "\n\n### ", text)

    # Merged FAQ questions on one line
    text = re.sub(r"\?\s+### ", "?\n\n### ", text)
    text = re.sub(r"\.\s+### (?=[A-Z])", ".\n\n### ", text)

    # Merged numbered lists: "1. ... 2. ..." on one line
    text = re.sub(r"(\.\s+)(\d+\.\s+\*\*)", r".\n\n\2", text)

    # Duplicate weave template sentences (keep first per paragraph)
    for prefix in WEAVE_DUPES:
        pat = re.compile(
            rf"({re.escape(prefix)}[^.]+\.)"
            rf"(?:\s+{re.escape(prefix)}[^.]+\.)+",
            re.I,
        )
        text = pat.sub(r"\1", text)

    # FAQ: question and answer must be on separate lines (EEAT C09)
    text = re.sub(
        r"^(### [^\n]+\?)\s+(.+)$",
        r"\1\n\n\2",
        text,
        flags=re.M,
    )

    # Collapse excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def needs_repair(text: str) -> bool:
    if " ---" in text:
        return True
    if re.search(r"[^\n#] ## ", text):
        return True
    if re.search(r"^### .+\? .+### ", text, re.M):
        return True
    if re.search(r"\?\s+### ", text):
        return True
    for p in WEAVE_DUPES:
        if text.lower().count(p.lower()) > 3:
            return True
    return False


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
            targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    changed = 0
    for art in targets:
        text = art.read_text(encoding="utf-8")
        if not needs_repair(text):
            continue
        new = repair(text)
        if new != text:
            art.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  {art.parent.name}")
    print(f"\nRepaired {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
