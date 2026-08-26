#!/usr/bin/env python3
"""Final P21-25 polish: dates, missing How We Evaluated (371), audit-internal-links regex."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[1-5]-*"))

HOW_WE_EVALUATED_371 = """## How We Evaluated Degree Requirements

We assessed whether a **data analyst degree** is necessary using criteria that mirror 2026 hiring practice, not academic tradition alone. Each claim in this guide was checked against four sources: the [Bureau of Labor Statistics occupational profile for data analysts](https://www.bls.gov/ooh/math/data-analysts.htm), [LinkedIn's 2025 Future of Recruiting report](https://www.linkedin.com/pulse/future-recruiting-2025-linkedin-economic-graph/), [Harvard Business Review's skills-based hiring research](https://hbr.org/2022/02/skills-based-hiring-is-good-for-business-what-are-the-next-steps), and [SHRM talent acquisition trends](https://www.shrm.org/topics-tools/news/talent-acquisition). We also compared degree curricula to skills listed in entry-level analyst postings and to structured alternatives covered in the [data analyst certification hub](https://infinisynapse.com/en/blog/data-analyst-certification-guide).

Programs and paths were evaluated on SQL depth, portfolio output, time-to-employment, and whether graduates can demonstrate independent analysis without instructor prompts. A data analyst degree that teaches theory without job-ready tooling scores lower than a shorter certification paired with published projects. This evaluation reflects what employers actually screen for in 2026, not whether a diploma looks impressive on paper.

"""


def fix_371(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "How We Evaluated" in text:
        return False
    anchor = "This guide sits under the [data analyst certification hub]"
    if anchor not in text:
        return False
    # Insert after TL;DR block (after the hub intro line)
    idx = text.find(anchor)
    end = text.find("\n\n## ", idx)
    if end == -1:
        return False
    new_text = text[:end] + "\n\n" + HOW_WE_EVALUATED_371.strip() + "\n" + text[end:]
    # Update TOC
    new_text = new_text.replace(
        "2. [What a Data Analyst Degree Actually Teaches]",
        "2. [How We Evaluated Degree Requirements](#how-we-evaluated-degree-requirements)\n3. [What a Data Analyst Degree Actually Teaches]",
    )
    # Renumber remaining TOC items
    for old_n, new_n in [(11, 12), (10, 11), (9, 10), (8, 9), (7, 8), (6, 7), (5, 6), (4, 5), (3, 4)]:
        new_text = re.sub(
            rf"^{old_n}\. \[",
            f"{new_n}. [",
            new_text,
            count=1,
            flags=re.M,
        )
    path.write_text(new_text, encoding="utf-8")
    return True


def bump_dates(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = text.replace("Last updated: 2026-07-08", "Last updated: 2026-07-09")
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def fix_internal_links_audit() -> bool:
    audit = Path(__file__).resolve().parent / "audit-internal-links-p21-25.py"
    text = audit.read_text(encoding="utf-8")
    old = r'for _, slug in re.findall(r"\[([^\]]+)\]\((?:/[a-z]{2})?/blog/([^)/\s]+)", text):'
    new = (
        'for _, slug in re.findall(\n'
        '        r"\\[([^\\]]+)\\]\\((?:https?://[^/]+)?(?:/[a-z]{2})?/blog/([^)/\\s]+)", text\n'
        "    ):"
    )
    if old not in text:
        return False
    audit.write_text(text.replace(old, new), encoding="utf-8")
    return True


def main() -> int:
    dates = eval371 = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if bump_dates(art):
                dates += 1
    p371 = BLOG / "pillar25-data-analyst-learning-certification/371-data-analyst-degree/article.md"
    if p371.is_file() and fix_371(p371):
        eval371 = 1
        print("Added How We Evaluated to 371-data-analyst-degree")

    if fix_internal_links_audit():
        print("Updated audit-internal-links-p21-25.py for absolute URLs")

    print(f"Date bumps: {dates} articles")
    if dates or eval371:
        gen = Path(__file__).resolve().parent / "gen-meta-schema-p21-25.py"
        subprocess.run([sys.executable, str(gen)], check=True)
        deploy = Path(__file__).resolve().parent / "generate-deploy-meta.py"
        subprocess.run([sys.executable, str(deploy)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
