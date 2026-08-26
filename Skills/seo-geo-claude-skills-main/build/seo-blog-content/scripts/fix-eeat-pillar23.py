#!/usr/bin/env python3
"""Mechanical EEAT fixes for Pillar 23: broken links, FAQ placeholders, InfiniSynapse trim."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar23-data-analysis-tools-software"

LINK_MAP: dict[str, str] = {
    "what AI-native data analysis means": "ai-native-data-analysis",
    "data analysis tools": "data-analysis-tools-guide",
    "data analysis software": "data-analysis-software",
    "data analysis tool": "data-analysis-tool",
    "excel data analysis tool": "excel-data-analysis-tool",
    "tableau data analysis tool": "tableau-data-analysis-tool",
    "tableau public data analysis": "tableau-public-data-analysis",
    "data analysis complete guide": "data-analysis-complete-guide",
    "natural language to SQL": "natural-language-to-sql",
    "ai-excel data cleaning": "ai-excel-data-cleaning",
    "how to clean Excel data with AI": "ai-excel-data-cleaning",
}

MULTI_FIXES: list[tuple[str, str]] = [
    ("read what AI-native data analysis means) and", "read [what AI-native data analysis means](/en/blog/ai-native-data-analysis) and"),
    ("see what AI-native data analysis means) and", "see [what AI-native data analysis means](/en/blog/ai-native-data-analysis) and"),
    ("We explain the paradigm in what AI-native data analysis means)", "We explain the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("in what AI-native data analysis means)", "in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
]

FAQ_FIXES: dict[str, list[tuple[str, str]]] = {
    "334-data-analysis-tools-guide": [
        (r"### What are the \\1options\\2\?\n", "### What are the main categories of data analysis tools?\n"),
        (r"### Do \\1employers require proof\\2\?", "### How do I prove a data analysis tool choice to stakeholders?"),
        (r"### How is \\1the role changing\\2\?", "### How are data analysis tools changing in 2026?"),
    ],
    "335-data-analysis-software": [
        (r"### What is the best \\1path\\2\?", "### What is the best data analysis software for beginners?"),
        (r"### Can \\1AI assist\\2\?", "### Can AI assist with data analysis software workflows?"),
        (r"### How is \\1the role changing\\2\?", "### How is data analysis software changing in 2026?"),
    ],
    "336-data-analysis-tool": [
        (r"### What is the best \\1path\\2\?", "### What is the best data analysis tool to start with?"),
        (r"### What makes \\1a strong fit\\2\?", "### What makes a data analysis tool a strong fit?"),
    ],
    "337-tools-for-data-analysis": [
        (r"### Do \\1employers require proof\\2\?", "### Do teams need proof before adopting tools for data analysis?"),
        (r"### Which \\1options fit beginners\\2\?", "### Which tools for data analysis fit beginners?"),
    ],
    "338-software-for-data-analysis": [
        (r"### What is the best \\1path\\2\?", "### What is the best software for data analysis?"),
        (r"### How does \\1it help\\2\?", "### How does AI-native software help data analysis?"),
    ],
    "339-data-analysis-platform": [
        (r"### How is \\1the role changing\\2\?", "### How are data analysis platforms changing in 2026?"),
        (r"### Do \\1employers require proof\\2\?", "### What proof do buyers need before choosing a data analysis platform?"),
        (r"### What makes \\1a strong fit\\2\?", "### What makes a data analysis platform a strong fit?"),
    ],
    "340-data-analysis-platforms": [
        (r"### What are the \\1options\\2\?", "### What are the main data analysis platforms in 2026?"),
        (r"### Do \\1employers require proof\\2\?", "### What should buyers validate before adopting data analysis platforms?"),
        (r"### Can \\1AI assist\\2\?", "### Can AI assist across data analysis platforms?"),
        (r"### How does \\1it help\\2\?", "### How does an AI-native platform help analysis teams?"),
    ],
    "341-analytical-tools-for-data-analysis": [
        (r"### Do \\1employers require proof\\2\?", "### How do teams evaluate analytical tools for data analysis?"),
    ],
    "343-tableau-public-data-analysis": [
        (r"### What are the \\1options\\2\?", "### What are the alternatives to Tableau Public for data analysis?"),
    ],
    "349-excel-data-analysis-toolpak": [
        (r"### How do I \\1get started\\2\?", "### How do I get started with the Excel Data Analysis ToolPak?"),
        (r"### What are the \\1options\\2\?", "### What are alternatives to the Excel Data Analysis ToolPak?"),
    ],
}

INFINI_LONG = re.compile(
    r"InfiniSynapse is (?:built for|representative|not an NLP2SQL)[^.]{0,800}?\.\s*"
    r"(?:It is not an NLP2SQL[^.]+\.\s*)?"
    r"(?:[^.]*\*\*InfiniSQL\*\*[^.]+\.\s*)?"
    r"(?:With InfiniSynapse[^.]+\.\s*)?"
    r"(?:Unlike the[^.]+\.\s*)?"
    r"(?:Analyst[^.]+\.\s*)?",
    re.S | re.I,
)

INFINI_SHORT = (
    "For warehouse-scale or multi-source work, supplement spreadsheets or BI tools with hands-on AI practice. "
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
    """Replace long mid-body InfiniSynapse blocks; keep Conclusion CTA."""
    parts = text.split("## Conclusion")
    if len(parts) != 2:
        return INFINI_LONG.sub(INFINI_SHORT + " ", text)
    body, conclusion = parts
    body = INFINI_LONG.sub(INFINI_SHORT + " ", body)
    # remove duplicate promo paragraphs in body mentioning InfiniSynapse web app
    body = re.sub(
        r"For recurring, multi-source[^.]+\. InfiniSynapse is a strong alternative[^.]+\.",
        "",
        body,
        flags=re.S,
    )
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
            [sys.executable, str(gen), "pillar23-data-analysis-tools-software"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
