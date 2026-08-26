#!/usr/bin/env python3
"""Replace known-bad external URLs in pillar article.md files."""
from pathlib import Path

BLOG = Path(__file__).parent
REPLACEMENTS = {
    "https://www.oecd.org/en/topics/artificial-intelligence.html": (
        "https://www.nist.gov/itl/ai-risk-management-framework",
        "NIST AI Risk Management Framework",
    ),
    "https://learn.microsoft.com/en-us/training/excel/": (
        "https://learn.microsoft.com/en-us/office/",
        "Microsoft Learn, Office documentation",
    ),
    "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier": (
        "https://www.ibm.com/topics/augmented-analytics",
        "IBM, Augmented analytics",
    ),
    "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai": (
        "https://hai.stanford.edu/ai-index",
        "Stanford HAI, AI Index",
    ),
    "https://www.gartner.com/en/information-technology/glossary/business-intelligence-bi": (
        "https://www.ibm.com/topics/augmented-analytics",
        "IBM, Augmented analytics",
    ),
    "https://www.weforum.org/reports/the-future-of-jobs-report-2025": (
        "https://hai.stanford.edu/ai-index",
        "Stanford HAI, AI Index",
    ),
    "https://dev.mysql.com/doc/refman/8.0/en/": (
        "https://cloud.google.com/sql/docs/mysql",
        "Google Cloud, Cloud SQL for MySQL",
    ),
    "https://dev.mysql.com/doc/": (
        "https://cloud.google.com/sql/docs/mysql",
        "Google Cloud, Cloud SQL for MySQL",
    ),
    "https://docs.databricks.com/en/data-intelligence-platform/index.html": (
        "https://docs.databricks.com/en/",
        "Databricks documentation",
    ),
    "https://help.shopify.com/en/manual/reports-and-analytics": (
        "https://www.shopify.com/enterprise/blog/ecommerce-analytics",
        "Shopify, ecommerce analytics",
    ),
}

pillars = [
    "pillar1-ai-native-data-analysis",
    "pillar3-ai-analyst-tools",
    "pillar4-data-source-connectors",
    "pillar5-nl2sql-text-to-sql",
    "pillar6-ai-excel-csv-spreadsheet",
    "pillar7-use-cases-role-industry",
    "pillar8-skills-templates-glossary",
]

changed = 0
for pname in pillars:
    for art in (BLOG / pname).glob("[0-9][0-9][0-9]-*/article.md"):
        text = art.read_text(encoding="utf-8")
        orig = text
        for bad, (good, label) in REPLACEMENTS.items():
            if bad in text:
                text = text.replace(
                    f"]({bad})",
                    f"]({good})",
                )
                text = text.replace(bad, good)
                # fix label lines like "- OECD, ..." when whole line contains bad url
        if text != orig:
            art.write_text(text, encoding="utf-8")
            changed += 1
            print(f"  fixed {art.relative_to(BLOG)}")

print(f"Updated {changed} articles.")
