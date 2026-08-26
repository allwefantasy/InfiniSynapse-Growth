#!/usr/bin/env python3
"""Mechanical EEAT fixes for Pillar 24: broken links, FAQ placeholders, InfiniSynapse trim."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar24-data-analyst-career-jobs"

LINK_MAP: dict[str, str] = {
    "what AI-native data analysis means": "ai-native-data-analysis",
    "data analyst skills": "data-analyst-skills",
    "data analyst jobs": "data-analyst-jobs",
    "data analyst salary": "data-analyst-salary",
    "data analyst pay": "data-analyst-pay",
    "data analyst guide": "data-analyst-guide",
    "data analyst resume": "data-analyst-resume",
    "data analyst interview questions": "data-analyst-interview-questions",
    "data analyst job description": "data-analyst-job-description",
    "how to become a data analyst": "how-to-become-a-data-analyst",
    "how to become a analyst": "how-to-become-a-data-analyst",
    "entry-level data analyst jobs": "entry-level-data-analyst-jobs",
    "entry level data analyst jobs": "entry-level-data-analyst-jobs",
    "junior data analyst jobs": "junior-data-analyst-jobs",
    "remote data analyst jobs": "remote-data-analyst-jobs",
    "data analyst internship": "data-analyst-internship",
    "what does a data analyst do": "what-does-a-data-analyst-do",
    "what does a analyst do": "what-does-a-data-analyst-do",
    "what do data analysts do": "what-do-data-analysts-do",
    "what is a data analyst": "what-is-a-data-analyst",
    "data analyst vs data scientist": "data-analyst-vs-data-scientist",
    "senior data analyst salary": "senior-data-analyst-salary",
    "the analyst job description": "data-analyst-job-description",
    "the data analyst job description": "data-analyst-job-description",
    "analyst skills": "data-analyst-skills",
    "analyst salary": "data-analyst-salary",
    "analyst pay": "data-analyst-pay",
    "remote analyst jobs": "remote-data-analyst-jobs",
    "data analyst interview questions": "data-analyst-interview-questions",
}

MULTI_FIXES: list[tuple[str, str]] = [
    ("read what AI-native data analysis means) and", "read [what AI-native data analysis means](/en/blog/ai-native-data-analysis) and"),
    ("see what AI-native data analysis means) and", "see [what AI-native data analysis means](/en/blog/ai-native-data-analysis) and"),
    ("We explore this in what AI-native data analysis means)", "We explore this in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("We explore the paradigm in what AI-native data analysis means)", "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("in what AI-native data analysis means)", "in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("learn them early; see what AI-native data analysis means)", "learn them early; see [what AI-native data analysis means](/en/blog/ai-native-data-analysis)"),
    ("we cover in remote data analyst jobs)", "we cover in [remote data analyst jobs](/en/blog/remote-data-analyst-jobs)"),
    ("we cover these in entry-level data analyst jobs)", "we cover these in [entry-level data analyst jobs](/en/blog/entry-level-data-analyst-jobs)"),
    ("our data analyst interview questions) guide", "our [data analyst interview questions](/en/blog/data-analyst-interview-questions) guide"),
    ("and data analyst resume) covers", "and [data analyst resume](/en/blog/data-analyst-resume) covers"),
]

FAQ_FIXES: dict[str, list[tuple[str, str]]] = {
    "354-data-analyst-salary": [
        (r"### How can I \\1improve outcomes\\2\?", "### How can I increase my data analyst salary?"),
        (r"### How do I \\1get started\\2\?", "### How do I benchmark a data analyst salary?"),
    ],
    "359-data-analyst-job-description": [
        (r"### How do I \\1get started\\2\?", "### How do I write a data analyst job description?"),
        (r"### How is \\1the role changing\\2\?", "### How is the data analyst job description changing in 2026?"),
    ],
    "360-entry-level-data-analyst-jobs": [
        (r"### Do \\1employers require proof\\2\?", "### Do employers require a portfolio for entry level data analyst jobs?"),
    ],
    "362-data-analyst-internship": [
        (r"### Where can I \\1find openings\\2\?", "### Where can I find a data analyst internship?"),
        (r"### Do \\1employers require proof\\2\?", "### Do data analyst internships require prior experience?"),
    ],
    "363-junior-data-analyst-jobs": [
        (r"### How do I \\1get started\\2\?", "### How do I land junior data analyst jobs?"),
        (r"### How is \\1the role changing\\2\?", "### How are junior data analyst jobs changing in 2026?"),
    ],
    "365-data-analyst-resume": [
        (r"### Do \\1employers require proof\\2\?", "### Do employers read every data analyst resume?"),
        (r"### How do I \\1get started\\2\?", "### How do I start writing a data analyst resume?"),
    ],
    "368-data-analyst-pay": [
        (r"### How can I \\1improve outcomes\\2\?", "### How can I improve my data analyst pay?"),
        (r"### How do I \\1get started\\2\?", "### How do I benchmark data analyst pay?"),
    ],
}

INFINI_BLOCK = re.compile(
    r"InfiniSynapse (?:is |illustrates |reflects |embodies |is an example|is representative)[^.]+\.\s*"
    r"(?:It is not an NLP2SQL[^.]+\.\s*)?"
    r"(?:[^.]*\*\*InfiniSQL\*\*[^.]+\.\s*)?"
    r"(?:[^.]*We explore[^.]+\.\s*)?"
    r"(?:[^.]*Stanford HAI AI Index[^.]+\.\s*)?"
    r"(?:[^.]*documents how[^.]+\.\s*)?",
    re.S,
)

INFINI_REPLACEMENT = (
    "Supplement your preparation with hands-on AI practice on real datasets. "
    "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis), "
    "and the [Stanford HAI AI Index](https://hai.stanford.edu/ai-index) tracks how rapidly these skills have become standard."
)

# Shorter variant for "This is where modern tooling" blocks
INFINI_BLOCK2 = re.compile(
    r"This is where modern tooling helps regardless of sector\. InfiniSynapse is not[^.]+\.\s*"
    r"Because the shared workflow[^.]+\.\s*"
    r"We explore the paradigm in \[[^\]]+\]\([^)]+\), and the \[Stanford HAI AI Index\][^.]+\.",
    re.S,
)


def fix_broken_links(text: str) -> str:
    for old, new in MULTI_FIXES:
        text = text.replace(old, new)
    for phrase, slug in sorted(LINK_MAP.items(), key=lambda x: -len(x[0])):
        broken = f"{phrase})"
        if broken in text:
            text = text.replace(broken, f"[{phrase}](/en/blog/{slug})")
    return text


def fix_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    folder = path.parent.name
    text = fix_broken_links(text)
    for pat, repl in FAQ_FIXES.get(folder, []):
        text = re.sub(pat, repl, text)
    text = INFINI_BLOCK2.sub(INFINI_REPLACEMENT, text)
    text = INFINI_BLOCK.sub(INFINI_REPLACEMENT + " ", text)
    # collapse duplicate sibling intro blocks
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
            [sys.executable, str(gen), "pillar24-data-analyst-career-jobs"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
