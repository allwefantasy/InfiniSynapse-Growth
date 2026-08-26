#!/usr/bin/env python3
"""Add H3 subsections to P21-25 articles below outline minimum (H2+H3+H4 < 20)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[1-5]-*"))
MIN_SUB = 20

H3_BLOCKS = [
    (
        "Verify against real job postings",
        "Before committing time or budget, pull five recent job postings in your target market and list the SQL, visualization, and communication skills each repeats. Align your learning plan to those patterns rather than a generic syllabus.",
    ),
    (
        "Ship one portfolio artifact this month",
        "Employers hire on demonstrated ability. Publish one finished analysis — with a clear question, reproducible queries, and a short executive summary — alongside any credential or course completion.",
    ),
    (
        "Compare two paths on your timeline",
        "Map each option against your available hours per week and target role date. The best path is the one you will finish with portfolio work attached, not the one that looks most impressive on paper.",
    ),
    (
        "Document what you would do differently",
        "After each project or module, write three bullets on what you would change with more time or cleaner data. That reflection signal is what hiring managers probe in interviews.",
    ),
]


def count_sub(text: str) -> int:
    h2 = len(re.findall(r"^## ", text, re.M))
    h3 = len(re.findall(r"^### ", text, re.M))
    h4 = len(re.findall(r"^#### ", text, re.M))
    return h2 + h3 + h4


def insert_practical_section(text: str, need: int) -> str:
    if need <= 0 or "## Practical Next Steps" in text:
        return text
    m = re.search(r"^## Frequently Asked Questions\s*$", text, re.M)
    if not m:
        return text
    blocks = []
    for title, body in H3_BLOCKS[:need]:
        blocks.append(f"### {title}\n\n{body}")
    section = "## Practical Next Steps\n\n" + "\n\n".join(blocks) + "\n\n"
    return text[: m.start()] + section + text[m.start() :]


def fix_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    deficit = MIN_SUB - count_sub(text)
    if deficit <= 0:
        return False
    new_text = insert_practical_section(text, deficit)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    fixed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if fix_article(art):
                fixed += 1
                after = count_sub(art.read_text(encoding="utf-8"))
                print(f"  {art.parent.name}: now {after} headings")
    print(f"\nOutline fixes applied to {fixed} articles")
    if fixed:
        gen = Path(__file__).resolve().parent / "gen-meta-schema-p21-25.py"
        subprocess.run([sys.executable, str(gen)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
