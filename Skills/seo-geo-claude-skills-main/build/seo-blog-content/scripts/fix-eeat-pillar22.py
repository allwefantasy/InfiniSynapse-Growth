#!/usr/bin/env python3
"""Mechanical EEAT fixes for Pillar 22: broken links, FAQ placeholders, InfiniSynapse trim."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar22-advanced-data-analysis-methods"

LINK_MAP: dict[str, str] = {
    "what AI-native data analysis means": "ai-native-data-analysis",
    "natural language to SQL": "natural-language-to-sql",
    "data analysis complete guide": "data-analysis-complete-guide",
    "python data analysis guide": "python-data-analysis-guide",
    "python for data analysis": "python-for-data-analysis",
    "data analysis with python": "data-analysis-with-python",
    "sql data analysis": "sql-data-analysis",
    "data analysis using sql": "data-analysis-using-sql",
    "r data analysis": "r-data-analysis",
    "qualitative data analysis": "qualitative-data-analysis",
}

MULTI_FIXES: list[tuple[str, str]] = [
    ("in what AI-native data analysis means)", "in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore the paradigm in what AI-native data analysis means)", "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore this in what AI-native data analysis means)", "We explore this in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore the accessible paradigm in what AI-native data analysis means)", "We explore the accessible paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
]

FAQ_FIXES: dict[str, list[tuple[str, str]]] = {
    "318-python-for-data-analysis": [
        (r"### Is formal training worth it\\1\?", "### Is formal Python training worth it for data analysis?"),
        (r"### How long does \\1training take\\2\?", "### How long does Python for data analysis training take?"),
        (r"### How do \\1teams proceed\\2\?", "### How do teams adopt Python for data analysis?"),
    ],
    "319-data-analysis-with-python": [
        (r"### Is formal training worth it\\1\?", "### Is formal training worth it for data analysis with Python?"),
        (r"### What is the workflow \?", "### What is the data analysis with Python workflow?"),
        (r"### Can \\1AI assist\\2\?", "### Can AI assist data analysis with Python?"),
    ],
    "320-sql-data-analysis": [
        (r"### Why are joins important in \?", "### Why are joins important in SQL data analysis?"),
        (r"### What are common mistakes in \?", "### What are common mistakes in SQL data analysis?"),
    ],
    "317-python-data-analysis-guide": [
        (r"### What libraries are used \?", "### What libraries are used for Python data analysis?"),
    ],
    "324-qualitative-research-data-analysis": [
        (r"### How does \\1it help\\2\?", "### How does AI help qualitative research data analysis?"),
    ],
    "329-spatial-data-analysis": [
        (r"### How does \\1it help\\2\?", "### How does AI help spatial data analysis?"),
    ],
    "330-topological-data-analysis": [
        (r"### How does \\1it help\\2\?", "### How does AI help topological data analysis?"),
    ],
    "331-bayesian-data-analysis": [
        (r"### Is formal training worth it\\1\?", "### Is formal training worth it for Bayesian data analysis?"),
    ],
    "332-predictive-data-analysis": [
        (r"### How does \\1it help\\2\?", "### How does AI help predictive data analysis?"),
    ],
    "333-financial-data-analysis": [
        (r"### How does \\1it help\\2\?", "### How does AI help financial data analysis?"),
    ],
}

INFINI_LONG = re.compile(
    r"InfiniSynapse (?:is not an NLP2SQL|illustrates|reflects|represents|embodies|embodies)[^.]{0,800}?\.\s*"
    r"(?:[^.]*\*\*InfiniSQL\*\*[^.]+\.\s*)?"
    r"(?:[^.]*one-click authorization[^.]+\.\s*)?"
    r"(?:We explore[^.]+\.\s*)?"
    r"(?:and the \[Stanford HAI AI Index\][^.]+\.\s*)?"
    r"(?:Scripted analysis should follow[^.]+\.\s*)?",
    re.S | re.I,
)

INFINI_SHORT = (
    "For warehouse-scale or multi-source work, supplement hand-written code with governed AI-assisted analysis. "
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
    # Remove dedicated InfiniSQL sections from body
    body = re.sub(
        r"## The InfiniSQL Approach\s*.+?(?=\n## )",
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
    text = re.sub(r"foR analysis", "for analysis", text)
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
            [sys.executable, str(gen), "pillar22-advanced-data-analysis-methods"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
