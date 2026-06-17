#!/usr/bin/env python3
"""Rewrite stuffed title/description to natural copy; keyword appears once, unchanged."""
from __future__ import annotations

import importlib.util
import json
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

spec = importlib.util.spec_from_file_location("stuff_audit", BLOG / "audit-keyword-meta-stuffing.py")
stuff_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stuff_mod)

CONNECTOR_DB = {
    "044-connect-supabase-to-ai-data-analyst": "Supabase",
    "045-connect-postgres-to-ai-data-analyst": "PostgreSQL",
    "046-connect-mysql-to-ai-data-analyst": "MySQL",
    "047-connect-snowflake-to-ai-analyst": "Snowflake",
    "048-connect-bigquery-to-ai-data-analyst": "BigQuery",
    "049-connect-databricks-to-ai-analyst": "Databricks",
    "050-connect-mongodb-to-ai-data-analyst": "MongoDB",
    "055-connect-clickhouse-to-ai-analyst": "ClickHouse",
    "056-connect-redshift-to-ai-data-analyst": "Amazon Redshift",
}

CONNECTOR_FILE = {
    "051-ai-data-analysis-google-sheets": ("Google Sheets", "sheets"),
    "052-ai-data-analysis-csv-files": ("CSV files", "files"),
    "053-ai-data-analysis-airtable": ("Airtable", "airtable"),
    "054-ai-analysis-notion-database": ("Notion databases", "notion"),
}

DESC_MAX = 165
TITLE_MAX = 90

# Short H1 when Target keyword alone is long (keyword unchanged; subtitle dropped or moved to desc)
SHORT_TITLES: dict[str, str] = {
    "002-data-agent-manifesto": "The Data Agent Manifesto: Why the First Ship Launches Here",
    "048-connect-bigquery-to-ai-data-analyst": (
        "Google Analytics Bigquery Data Analysis Capabilities: BigQuery Guide (2026)"
    ),
    "056-connect-redshift-to-ai-data-analyst": (
        "Amazon Redshift (2026): Data Integration Platforms Supporting Snowflake Bigquery Redshift"
    ),
    "062-ai-sql-generator": (
        "AI-Assisted Query Generation SQL Python Social Science Data Analysis (2026)"
    ),
    "063-llm-sql-generation-architecture": (
        "AI-Assisted Query Generation SQL Python Social Science Data Analysis (2026)"
    ),
    "068-dialect-aware-sql-generation": (
        "AI-Assisted Query Generation SQL Python Social Science Data Analysis (2026)"
    ),
    "072-ai-excel-formula-generator": (
        "Data Analysis Excel Template Free Download with Formula (2026)"
    ),
    "075-deduplicate-data-with-ai": (
        "AI-Powered CRM Data Cleaning Deduplication Platforms (2026)"
    ),
    "078-ai-financial-modeling-excel": (
        "Microsoft Excel Data Analysis and Business Modeling (2026)"
    ),
    "083-ai-data-analysis-finance-teams": (
        "Best Data Integration Platforms for Finance Teams 2025 2026"
    ),
    "087-ai-data-strategy-cto": (
        "AI-Powered Semantic Layers for Enterprise Data Strategy (2026)"
    ),
}

SHORT_DESCS: dict[str, str] = {
    "002-data-agent-manifesto": (
        "Why the data agent is the first ship of the AI civilization — auditable decisions, "
        "not just running code. Vision grounded in InfiniSynapse."
    ),
    "062-ai-sql-generator": (
        "Compare AI SQL generator categories with a scorecard for autonomy, correctness, "
        "and governance — built for ai-assisted query generation sql python social science data analysis teams."
    ),
    "063-llm-sql-generation-architecture": (
        "Planner, retriever, executor, and auditor layers for ai-assisted query generation "
        "sql python social science data analysis in production SQL agents."
    ),
    "068-dialect-aware-sql-generation": (
        "Cross-warehouse SQL generation patterns for ai-assisted query generation sql python "
        "social science data analysis with dialect-aware validation."
    ),
    "072-ai-excel-formula-generator": (
        "Build reliable Excel analysis templates faster with data analysis excel template "
        "free download with formula patterns, governance controls, and worked examples."
    ),
    "075-deduplicate-data-with-ai": (
        "CRM-grade deduplication workflow for ai-powered crm data cleaning deduplication "
        "platforms with quality controls that scale in 2026."
    ),
    "048-connect-bigquery-to-ai-data-analyst": (
        "Learn google analytics bigquery data analysis capabilities by connecting BigQuery "
        "to an AI data analyst — setup checklist, security controls, validation SQL, and FAQ."
    ),
    "056-connect-redshift-to-ai-data-analyst": (
        "Connect Amazon Redshift to an AI data analyst in 2026. Covers data integration "
        "platforms supporting snowflake bigquery redshift with IAM setup, validation SQL, and FAQ."
    ),
}


def kw_title_case(kw: str) -> str:
    small = {"for", "to", "in", "on", "with", "and", "or", "a", "an", "the", "of", "vs", "bi"}
    parts = kw.split()
    out = []
    for i, p in enumerate(parts):
        low = p.lower()
        if i > 0 and low in small:
            out.append(low)
        elif low == "nl2sql":
            out.append("NL2SQL")
        elif low == "ai":
            out.append("AI")
        elif low == "sql":
            out.append("SQL")
        elif low == "csv":
            out.append("CSV")
        elif low == "cto":
            out.append("CTO")
        elif low == "saas":
            out.append("SaaS")
        elif low == "bigquery":
            out.append("BigQuery")
        elif low == "mysql":
            out.append("MySQL")
        elif "-" in p:
            out.append(
                "-".join(
                    x.capitalize() if x.lower() not in small else x.lower()
                    for x in p.split("-")
                )
            )
        else:
            out.append(p.capitalize())
    return " ".join(out)


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip() if m else ""


def extract_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_desc(text: str) -> str:
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def trim_desc(desc: str, kw: str) -> str:
    desc = re.sub(r"\s*\(\d+\s*chars\)\s*$", "", desc, flags=re.I)
    desc = re.sub(r"\.{2,}$", ".", desc)
    if len(desc) <= DESC_MAX:
        return desc
    cut = desc[:DESC_MAX]
    if kw.lower() not in cut.lower():
        cut = desc[:DESC_MAX].rsplit(" ", 1)[0]
    elif " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut if cut.endswith((".", "!", "?")) else cut + "."


def connector_db_title(kw: str, source: str) -> str:
    kwt = kw_title_case(kw)
    kl = kw.lower()
    if kl == "sql for data analysis":
        return f"SQL for Data Analysis with {source}: Connect to an AI Data Analyst (2026)"
    if kl == "mysql data analysis tools":
        return f"MySQL Data Analysis Tools: Connect MySQL to an AI Data Analyst (2026)"
    if kl == "connect snowflake to no-code bi platform without data engineer":
        return (
            "Connect Snowflake to No-Code BI Platform Without Data Engineer "
            "(2026): AI Analyst Guide"
        )
    if kl == "google analytics bigquery data analysis capabilities":
        return (
            "Google Analytics Bigquery Data Analysis Capabilities: "
            f"Connect {source} to an AI Data Analyst (2026)"
        )
    if kl == "databricks data analytics platform":
        return f"Databricks Data Analytics Platform: Connect to an AI Data Analyst (2026)"
    if kl == "ai database agent for data visualization":
        return f"AI Database Agent for Data Visualization: {source} Connector Guide (2026)"
    if kl == "data integration platforms supporting snowflake bigquery redshift":
        return (
            "How to Connect Amazon Redshift to an AI Data Analyst (2026): "
            "Data Integration Platforms Supporting Snowflake Bigquery Redshift"
        )
    return f"{kwt}: Connect {source} to an AI Data Analyst (2026)"


def connector_db_desc(kw: str, source: str) -> str:
    return trim_desc(
        f"Learn {kw} by connecting {source} to an AI data analyst — setup checklist, "
        "security controls, validation SQL, and FAQ for 2026 teams.",
        kw,
    )


def connector_file_title(kw: str, label: str, slug_key: str) -> str:
    kwt = kw_title_case(kw)
    kl = kw.lower()
    if kl == "data analysis in google sheets":
        return "Data Analysis in Google Sheets (2026): AI Connector Setup Guide"
    if kl == "csv files for data analysis":
        return "CSV Files for Data Analysis (2026): AI Connector Playbook"
    if kl == "airtable data analysis":
        return "Airtable Data Analysis: Practical Workflow Guide (2026)"
    if kl == "ai database agent for data visualization":
        return "AI Database Agent for Data Visualization: Notion Database Guide (2026)"
    return f"{kwt}: {label.title()} Connector Guide (2026)"


def connector_file_desc(kw: str, label: str) -> str:
    return trim_desc(
        f"Learn {kw} on {label} with InfiniSynapse — connector setup, governance controls, "
        "validation SQL, and FAQ for 2026 teams.",
        kw,
    )


def connector_analytics_title(h1: str, kw: str) -> str:
    kl = kw.lower()
    if kl == "financial services data analysis":
        return "Analyze Stripe Data with AI (2026): Financial Services Data Analysis Workflows"
    if kl == "ecommerce data analysis":
        return "Analyze Shopify Data with AI (2026): Ecommerce Data Analysis Workflows"
    return h1


def connector_analytics_desc(kw: str, platform: str) -> str:
    return trim_desc(
        f"Run {kw} workflows on {platform} with InfiniSynapse connectors, memory, "
        "and SQL trace for defensible decisions in 2026.",
        kw,
    )


def usecase_desc(kw: str) -> str:
    return trim_desc(
        f"Pain points, KPI scorecard, workflow playbook, tool fit, and a 30-day rollout "
        f"guide for {kw} in 2026.",
        kw,
    )


def tools_desc(kw: str, h1: str) -> str:
    hl = h1.lower()
    if "review" in hl or "scorecard" in hl:
        return trim_desc(
            f"Honest scorecard for {kw} in 2026 — autonomy, SQL depth, memory, "
            "governance, pricing fit, and buyer rollout guidance.",
            kw,
        )
    if "alternatives" in hl or " vs " in hl:
        return trim_desc(
            f"Compare {kw} options in 2026 with autonomy, governance, SQL depth, "
            "memory, and deployment fit for analyst teams.",
            kw,
        )
    return trim_desc(
        f"Compare {kw} in 2026 across autonomy, SQL depth, memory, governance, "
        "and rollout fit for production analyst teams.",
        kw,
    )


def nl2sql_desc(kw: str, h1: str) -> str:
    topic = h1.split(":", 1)[-1].strip() if ":" in h1 else "production NL2SQL"
    return trim_desc(
        f"{topic}. Practical guidance on {kw} for data teams in 2026.",
        kw,
    )


def glossary_faq_desc(kw: str, h1: str) -> str:
    if "glossary" in h1.lower():
        return trim_desc(
            f"Fifteen citable analytics terms anchored on {kw}, including autonomy, "
            "distillation, InfiniSQL, and InfiniRAG for 2026 teams.",
            kw,
        )
    if "faq" in h1.lower():
        return trim_desc(
            f"Fourteen deep answers on {kw}, architecture, memory, governance, "
            "and buyer fit for 2026 data teams.",
            kw,
        )
    if "prompt" in h1.lower():
        return trim_desc(
            f"Thirty-plus reusable templates for {kw}, organized by analysis task "
            "with governance notes for 2026 teams.",
            kw,
        )
    return trim_desc(
        f"Practical reference on {kw} with workflow patterns and governance notes for 2026 teams.",
        kw,
    )


def excel_desc(kw: str, h1: str) -> str:
    topic = h1.split(":", 1)[-1].strip() if ":" in h1 else "spreadsheet analysis"
    return trim_desc(
        f"{topic} — a practical 2026 playbook for {kw} with governance controls and worked examples.",
        kw,
    )


def naturalize(name: str, kw: str, h1: str, desc: str) -> tuple[str, str]:
    if name in SHORT_TITLES:
        new_h1 = SHORT_TITLES[name]
        new_desc = SHORT_DESCS.get(name, desc)
        return new_h1, new_desc

    kl = kw.lower()

    if name in CONNECTOR_DB:
        source = CONNECTOR_DB[name]
        return connector_db_title(kw, source), connector_db_desc(kw, source)

    if name in CONNECTOR_FILE:
        label, _ = CONNECTOR_FILE[name]
        return connector_file_title(kw, label, name), connector_file_desc(kw, label)

    if name in ("057-analyze-stripe-data-with-ai", "058-analyze-shopify-data-with-ai"):
        platform = "Stripe" if "stripe" in name else "Shopify"
        return (
            connector_analytics_title(h1, kw),
            connector_analytics_desc(kw, platform),
        )

    if name == "044-connect-supabase-to-ai-data-analyst" and kl == "sql for data analysis":
        return (
            "SQL for Data Analysis with Supabase: Connect to an AI Data Analyst (2026)",
            trim_desc(
                f"Learn {kw} by connecting Supabase to an AI data analyst — setup checklist, "
                "security controls, validation SQL, and FAQ for 2026 teams.",
                kw,
            ),
        )

    if re.match(r"08[1-9]-|09[0-4]-", name):
        return h1, usecase_desc(kw)

    if re.match(r"02[4-9]|03[0-9]|04[0-3]", name):
        return h1, tools_desc(kw, h1)

    if re.match(r"05[9-9]|06[0-8]", name):
        new_h1 = h1
        if kl == "integrate natural language data analysis with sql and python":
            new_h1 = (
                "Integrate Natural Language Data Analysis with SQL and Python "
                "(2026): Production Playbook"
            )
        elif kl == "text to sql agent for data visualization" and ":" in h1:
            base = h1.split(":", 1)[1].strip()
            new_h1 = f"Text to SQL Agent for Data Visualization: {base}"
        elif re.match(r"^Ai-", h1):
            new_h1 = kw_title_case(kw) + (":" + h1.split(":", 1)[1] if ":" in h1 else "")
        return new_h1, nl2sql_desc(kw, new_h1)

    if re.match(r"06[9-9]|07[0-9]|080", name):
        new_h1 = h1
        if re.match(r"^Ai-|^Csv ", h1):
            new_h1 = kw_title_case(kw) + (":" + h1.split(":", 1)[1] if ":" in h1 else "")
        return new_h1, excel_desc(kw, new_h1)

    if re.match(r"09[5-9]|100", name):
        return h1, glossary_faq_desc(kw, h1)

    if re.match(r"01[3-3]", name) and kl == "what is a data agent":
        return h1, glossary_faq_desc(kw, h1)

    # pillar1 / fallback: fix duplicate-prefix descriptions only
    if h1.lower().startswith(kl) and desc.lower().startswith(kw_title_case(kw).lower()):
        rest = desc.split(":", 1)[-1].strip() if ":" in desc else desc
        return h1, trim_desc(
            f"{rest} A practical 2026 guide covering {kw} for data teams.",
            kw,
        )
    return h1, desc


def set_h1(text: str, h1: str) -> str:
    return re.sub(r"^# .+$", f"# {h1}", text, count=1, flags=re.M)


def set_desc(text: str, desc: str) -> str:
    return re.sub(
        r"\*\*Meta Description\*\*:\s*.+$",
        f"**Meta Description**: {desc}",
        text,
        count=1,
        flags=re.M,
    )


def sync_meta_tags(path: Path, title: str, desc: str) -> bool:
    meta = path / "meta-tags.html"
    if not meta.is_file():
        return False
    mt = meta.read_text(encoding="utf-8")
    orig = mt
    for pat, repl in (
        (r"<title>[^<]*</title>", f"<title>{title}</title>"),
        (r'(<meta\s+name="description"\s+content=")[^"]*(")', rf"\g<1>{desc}\2"),
        (r'(<meta\s+property="og:title"\s+content=")[^"]*(")', rf"\g<1>{title}\2"),
        (r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")', rf"\g<1>{title}\2"),
        (r'(<meta\s+property="og:description"\s+content=")[^"]*(")', rf"\g<1>{desc}\2"),
        (r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', rf"\g<1>{desc}\2"),
    ):
        mt = re.sub(pat, repl, mt, count=1, flags=re.I)
    if mt != orig:
        meta.write_text(mt, encoding="utf-8")
        return True
    return False


def sync_schema(path: Path, title: str, desc: str) -> bool:
    schema = path / "schema.json"
    if not schema.is_file():
        return False
    data = json.loads(schema.read_text(encoding="utf-8"))
    changed = False
    for block in data:
        if block.get("@type") == "BlogPosting":
            if block.get("headline") != title:
                block["headline"] = title
                changed = True
            if block.get("description") != desc:
                block["description"] = desc
                changed = True
        if block.get("@type") == "BreadcrumbList":
            for item in block.get("itemListElement", []):
                if item.get("position") == 3 and item.get("name") != title:
                    item["name"] = title
                    changed = True
    if changed:
        schema.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def process(article: Path, force: bool = False) -> bool:
    text = article.read_text(encoding="utf-8")
    kw = extract_keyword(text)
    if not kw:
        return False
    h1 = extract_h1(text)
    desc = extract_desc(text)
    name = article.parent.name
    fails = stuff_mod.audit_article(article)
    if name in SHORT_TITLES or name in SHORT_DESCS:
        force = True
    if not fails and not force:
        return False

    new_h1, new_desc = naturalize(article.parent.name, kw, h1, desc)

    if kw.lower() not in new_h1.lower():
        kwt = kw_title_case(kw)
        if len(new_h1) + len(kwt) + 3 <= 90:
            new_h1 = f"{new_h1}: {kwt}"
        else:
            new_h1 = f"{kwt}: {new_h1}"

    if kw.lower() not in new_desc.lower():
        new_desc = trim_desc(
            f"{new_desc} Covers {kw} for 2026 teams.",
            kw,
        )

    new_text = text
    if new_h1 != h1:
        new_text = set_h1(new_text, new_h1)
    if new_desc != desc:
        new_text = set_desc(new_text, new_desc)

    changed = new_text != text
    if changed:
        article.write_text(new_text, encoding="utf-8")

    folder = article.parent
    meta_changed = sync_meta_tags(folder, new_h1, new_desc)
    schema_changed = sync_schema(folder, new_h1, new_desc)
    return changed or meta_changed or schema_changed


def main() -> int:
    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--force"]
    targets: list[Path] = []
    if args:
        for arg in args:
            p = Path(arg)
            if p.is_dir():
                targets.extend(sorted(p.glob("[0-9][0-9][0-9]-*/article.md")))
            elif p.is_file():
                targets.append(p)
    else:
        for pillar in PILLARS:
            if pillar.is_dir():
                targets.extend(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")))

    n = 0
    for art in targets:
        if process(art, force=force):
            n += 1
            print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {n} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
