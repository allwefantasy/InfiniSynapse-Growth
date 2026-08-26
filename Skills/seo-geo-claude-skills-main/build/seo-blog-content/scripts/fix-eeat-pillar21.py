#!/usr/bin/env python3
"""Mechanical EEAT fixes for Pillar 21: broken links, FAQ placeholders, InfiniSynapse trim."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar21-data-analysis-fundamentals"

LINK_MAP: dict[str, str] = {
    "what AI-native data analysis means": "ai-native-data-analysis",
    "data analysis complete guide": "data-analysis-complete-guide",
    "what data analysis is": "what-is-data-analysis",
    "data analysis definition": "data-analysis-definition",
    "data analysis process": "data-analysis-process",
    "data analysis methods": "data-analysis-methods",
    "data analysis techniques": "data-analysis-techniques",
    "types of data analysis": "types-of-data-analysis",
    "exploratory data analysis": "exploratory-data-analysis",
    "data analysis tools guide": "data-analysis-tools-guide",
    "python data analysis guide": "python-data-analysis-guide",
}

MULTI_FIXES: list[tuple[str, str]] = [
    ("in what AI-native data analysis means)", "in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore the paradigm in what AI-native data analysis means)", "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore the paradigm in depth in what AI-native data analysis means)", "We explore the paradigm in depth in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
]

FAQ_FIXES: dict[str, list[tuple[str, str]]] = {
    "300-data-analysis-complete-guide": [
        (r"### What are the \\1options\\2\?", "### What are the main types of data analysis?"),
        (r"### What tools are used \?", "### What tools are used for data analysis?"),
        (r"### How is \\1the role changing\\2\?", "### How is data analysis changing in 2026?"),
    ],
    "303-data-analysis-meaning": [
        (r"### Do \\1employers require proof\\2\?", "### Do employers value data analysis skills?"),
        (r"### Why is understanding the useful\?", "### Why is understanding the meaning of data analysis useful?"),
    ],
    "304-analysis-of-data": [
        (r"### What approaches can the take\?", "### What approaches can the analysis of data take?"),
        (r"### What commonly goes wrong in the \?", "### What commonly goes wrong in the analysis of data?"),
        (r"### How do \\1teams proceed\\2\?", "### How do teams proceed with the analysis of data?"),
    ],
    "310-exploratory-data-analysis": [
        (r"### What techniques are used in \?", "### What techniques are used in exploratory data analysis?"),
        (r"### How do \\1teams proceed\\2\?", "### How do teams proceed with exploratory data analysis?"),
    ],
    "315-data-analysis-example": [
        (r"### How long does \\1training take\\2\?", "### How long does a first data analysis example take?"),
    ],
    "302-data-analysis-definition": [
        (r"### Why does a precise matter\?", "### Why does a precise data analysis definition matter?"),
    ],
}

INFINI_LONG = re.compile(
    r"InfiniSynapse (?:embodies|illustrates|reflects|exemplifies|shows)[^.]{0,800}?\.\s*"
    r"(?:[^.]*\*\*InfiniSQL\*\*[^.]+\.\s*)?"
    r"(?:[^.]*one-click authorization[^.]+\.\s*)?"
    r"(?:We explore[^.]+\.\s*)?"
    r"(?:We explain[^.]+\.\s*)?"
    r"(?:and the \[Stanford HAI AI Index\][^.]+\.\s*)?"
    r"(?:Importantly[^.]+\.\s*)?",
    re.S | re.I,
)

INFINI_SHORT = (
    "For warehouse-scale or multi-source work, supplement fundamentals with governed AI-assisted analysis. "
    "We explain the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis), "
    "and the [Stanford HAI AI Index](https://hai.stanford.edu/ai-index) tracks how quickly agent-assisted analysis matured."
)


def fix_broken_links(text: str) -> str:
    for old, new in MULTI_FIXES:
        text = text.replace(old, new)
    for phrase, slug in sorted(LINK_MAP.items(), key=lambda x: -len(x[0])):
        broken = f"{phrase})"
        if broken in text:
            text = text.replace(broken, f"[{phrase}](/en/blog/{slug})")
    return text


def trim_infini_blocks(text: str) -> str:
    parts = text.split("## Conclusion")
    if len(parts) != 2:
        return INFINI_LONG.sub(INFINI_SHORT + " ", text)
    body, conclusion = parts
    body = INFINI_LONG.sub(INFINI_SHORT + " ", body)
    return body + "## Conclusion" + conclusion


def fix_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    folder = path.parent.name
    text = fix_broken_links(text)
    for pat, repl in FAQ_FIXES.get(folder, []):
        text = re.sub(pat, repl, text)
    text = trim_infini_blocks(text)
    text = re.sub(
        r"(This guide sits under[^\n]+\n)\n+(For related depth in this pillar[^\n]+\n)",
        r"\1\n",
        text,
    )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    fixed = 0
    for art in sorted(PILLAR.glob("[0-9][0-9][0-9]-*/article.md")):
        if fix_article(art):
            fixed += 1
            print(f"fixed {art.parent.name}")
    print(f"\nFixed {fixed} articles")
    if fixed:
        gen = Path(__file__).resolve().parent / "gen-meta-schema-p21-25.py"
        subprocess.run(
            [sys.executable, str(gen), "pillar21-data-analysis-fundamentals"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
