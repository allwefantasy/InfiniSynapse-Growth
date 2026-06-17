#!/usr/bin/env python3
"""Replace known broken authority URLs across all pillar article.md files."""
from __future__ import annotations

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

REPLACEMENTS: dict[str, str] = {
    "https://www.cisa.gov/topics/artificial-intelligence": "https://www.cisa.gov/ai",
    "https://www.ftc.gov/business-guidance/blog-topics/artificial-intelligence": "https://www.ftc.gov/",
    "https://www.enisa.europa.eu/topics/artificial-intelligence": (
        "https://www.enisa.europa.eu/publications/multilayer-framework-for-good-cybersecurity-practices-for-ai"
    ),
    "https://www.oecd.org/en/topics/artificial-intelligence.html": "https://oecd.ai/en/",
    "https://dev.mysql.com/doc/": "https://mariadb.com/kb/en/documentation/",
    "https://www.tableau.com/learn/articles": (
        "https://help.tableau.com/current/pro/desktop/en-us/default.htm"
    ),
    "https://www.canada.ca/en/government/system/digital-government/digital-government-innovations/responsible-use-ai.html": (
        "https://www.iso.org/standard/81230.html"
    ),
    "https://www.cyber.gov.au/resources-business-and-government/growing-australia-future/artificial-intelligence": (
        "https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development"
    ),
    "https://support.microsoft.com/en-us/excel": "https://support.microsoft.com/excel",
}


def main() -> int:
    changed_files = 0
    total_replacements = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            original = text
            for old, new in REPLACEMENTS.items():
                if old in text:
                    count = text.count(old)
                    text = text.replace(old, new)
                    total_replacements += count
            if text != original:
                art.write_text(text, encoding="utf-8")
                changed_files += 1
                print(f"updated {art.parent.name}")
    print(f"\nFiles changed: {changed_files} | URL replacements: {total_replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
