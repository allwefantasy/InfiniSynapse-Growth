#!/usr/bin/env python3
"""Mechanical EEAT fixes for Pillar 25: broken links, typos, InfiniSynapse trim."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar25-data-analyst-learning-certification"

# phrase (no parens) -> slug
LINK_MAP: dict[str, str] = {
    "what AI-native data analysis means": "ai-native-data-analysis",
    "data analyst skills": "data-analyst-skills",
    "certifications for data analyst": "certifications-for-data-analyst",
    "data analysis certificate": "data-analysis-certificate",
    "data analyst training": "data-analyst-training",
    "data analyst certification guide": "data-analyst-certification-guide",
    "certified data analysis": "certified-data-analysis",
    "data analysis certification": "data-analysis-certification",
    "data analyst certification online": "data-analyst-certification-online",
    "data analysis courses": "data-analysis-courses",
    "data analyst course": "data-analyst-course",
    "data analyst course online": "data-analyst-course-online",
    "data analyst course free": "data-analyst-course-free",
    "data analyst certificate": "data-analyst-certificate",
    "data analyst courses": "data-analyst-courses",
    "data analyst courses online": "data-analyst-courses-online",
    "data analyst bootcamp": "data-analyst-bootcamp",
    "data analysis bootcamp": "data-analysis-bootcamp",
    "how to become a data analyst": "how-to-become-a-data-analyst",
}

# Multi-phrase broken fragments (exact match)
MULTI_FIXES: list[tuple[str, str]] = [
    (
        "see data analysis certification) and data analysis certificate).",
        "see [data analysis certification](/en/blog/data-analysis-certification) and [data analysis certificate](/en/blog/data-analysis-certificate).",
    ),
    (
        "in data analyst certification guide) and certifications for data analyst).",
        "in [data analyst certification guide](/en/blog/data-analyst-certification-guide) and [certifications for data analyst](/en/blog/certifications-for-data-analyst).",
    ),
    (
        "in data analysis courses) and data analyst course).",
        "in [data analysis courses](/en/blog/data-analysis-courses) and [data analyst course](/en/blog/data-analyst-course).",
    ),
    (
        "and data analyst certification online) for paid options",
        "and [data analyst certification online](/en/blog/data-analyst-certification-online) for paid options",
    ),
    (
        "and data analysis certificate)",
        "and [data analysis certificate](/en/blog/data-analysis-certificate)",
    ),
    (
        "and data analyst course online)",
        "and [data analyst course online](/en/blog/data-analyst-course-online)",
    ),
    (
        "and data analyst course)",
        "and [data analyst course](/en/blog/data-analyst-course)",
    ),
    (
        "in certified data analysis) and compare",
        "in [certified data analysis](/en/blog/certified-data-analysis) and compare",
    ),
    (
        "We provide detailed comparisons in certifications for data analyst)",
        "We provide detailed comparisons in [certifications for data analyst](/en/blog/certifications-for-data-analyst)",
    ),
    (
        "Browse certifications for data analyst) for detailed",
        "Browse [certifications for data analyst](/en/blog/certifications-for-data-analyst) for detailed",
    ),
    (
        "See data analysis certificate) for the certificate",
        "See [data analysis certificate](/en/blog/data-analysis-certificate) for the certificate",
    ),
    (
        "read what AI-native data analysis means) and",
        "read [what AI-native data analysis means](/en/blog/ai-native-data-analysis) and",
    ),
    (
        "We explore the paradigm in what AI-native data analysis means)",
        "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis)",
    ),
    (
        "described in data analyst skills)",
        "described in [data analyst skills](/en/blog/data-analyst-skills)",
    ),
    (
        "See data analyst training) for a full comparison",
        "See [data analyst training](/en/blog/data-analyst-training) for a full comparison",
    ),
    (
        "See data analyst certification online) for online-specific",
        "See [data analyst certification online](/en/blog/data-analyst-certification-online) for online-specific",
    ),
    (
        "We map the certification landscape in data analyst certification guide)",
        "We map the certification landscape in [data analyst certification guide](/en/blog/data-analyst-certification-guide)",
    ),
]

TYPO_FIXES: list[tuple[str, str]] = [
    ("this **this credential**", "**data analysis certification**"),
    ("Choose the the training", "Choose the training"),
    ("One this program with", "One program with"),
    ("Many this online program providers", "Many online program providers"),
    ("vendor-neutral the certification if", "vendor-neutral certification if"),
    ("A the credential is not worth", "A credential is not worth"),
    ("A the online course you complete", "An online course you complete"),
    ("program option options", "program options"),
    ("online the class", "online class"),
    ("### What is the best the program credential?", "### What is the best certification program?"),
    ("### Is a the credential worth it?", "### Is a data analyst certificate worth it?"),
    ("### Can I get a the certificate online?", "### Can I get a data analyst certificate online?"),
    ("### What is the alternative to a the bootcamp?", "### What is the alternative to a data analysis bootcamp?"),
    ("### Can I do a the program online?", "### Can I do a data analyst bootcamp online?"),
    ("### How long does a the program take?", "### How long does a data analyst bootcamp take?"),
    ("### Should a the course cover AI tools?", "### Should a data analyst course cover AI tools?"),
    ("### Are paid this course options worth it?", "### Are paid data analyst courses worth it?"),
    ("### What is the best a quality program for beginners?", "### What is the best data analyst course for beginners?"),
    ("Most comprehensive a strong program programs", "Most comprehensive programs"),
    ("Most the certificate programs are", "Most certificate programs are"),
    ("this course selection is not the right choice", "this course is not the right choice"),
]

INFINI_BLOCK = re.compile(
    r"InfiniSynapse (?:exemplifies|addresses|offers)[^.]+\.\s*"
    r"(?:Practicing with it[^.]+\.\s*)?"
    r"(?:We explore the paradigm in[^.]+\)?[^.]*\.)?",
    re.S,
)

INFINI_REPLACEMENT = (
    "Supplement coursework with hands-on AI practice on real datasets. "
    "We explore the paradigm in [what AI-native data analysis means](/en/blog/ai-native-data-analysis), "
    "and the [Stanford HAI AI Index](https://hai.stanford.edu/ai-index) tracks how rapidly these skills have become standard."
)


def fix_broken_links(text: str) -> str:
    for old, new in MULTI_FIXES:
        text = text.replace(old, new)
    # longest phrases first to avoid partial matches
    for phrase, slug in sorted(LINK_MAP.items(), key=lambda x: -len(x[0])):
        broken = f"{phrase})"
        if broken not in text:
            continue
        linked = f"[{phrase}](/en/blog/{slug})"
        # skip if already linked
        if f"]({linked})" in text or f"/en/blog/{slug})" in text:
            text = text.replace(broken, linked)
            continue
        text = text.replace(broken, linked)
    return text


def fix_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = fix_broken_links(text)
    for old, new in TYPO_FIXES:
        text = text.replace(old, new)
    text = INFINI_BLOCK.sub(INFINI_REPLACEMENT + " ", text)
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
            [sys.executable, str(gen), "pillar25-data-analyst-learning-certification"],
            check=True,
        )
        print("Regenerated schema/meta for pillar25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
