#!/usr/bin/env python3
"""Scaffold pillar folders + per-article bundles from pillar-manifests JSON."""
import json
import shutil
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
DEFAULT_REGISTRY = BLOG / "pillar-manifests" / "pillar4-8-articles.json"
REGISTRY_ALIASES = {
    "pillar2": BLOG / "pillar-manifests" / "pillar2-articles.json",
    "pillar4-8": DEFAULT_REGISTRY,
}
REF_PREVIEW = BLOG / "pillar3-ai-analyst-tools" / "build-preview.py"


def title_from_theme(theme: str, kicker: str) -> str:
    t = theme.replace("_", " ").strip()
    mapping = {
        "connect supabase to ai data analyst": "How to Connect Supabase to an AI Data Analyst: SQL for Data Analysis (2026)",
        "connect postgres to ai data analyst": "How to Connect PostgreSQL to an AI Data Analyst (2026 Guide)",
        "connect mysql to ai data analyst": "How to Connect MySQL to an AI Data Analyst: Tools and Workflow (2026)",
        "connect snowflake to ai analyst": "How to Connect Snowflake to an AI Data Analyst Without a Data Engineer (2026)",
        "connect bigquery to ai data analyst": "Connect BigQuery to an AI Data Analyst: Analytics Capabilities Guide (2026)",
        "connect databricks to ai analyst": "Connect Databricks to an AI Data Analyst: Lakehouse Analytics Platform Guide",
        "connect mongodb to ai data analyst": "Connect MongoDB to an AI Data Analyst for Visualization and Insights (2026)",
        "ai data analysis for google sheets": "AI Data Analysis for Google Sheets: Practical Guide for Analysts (2026)",
        "ai data analysis for csv files": "AI Data Analysis for CSV Files: Workflow Guide for Analysts (2026)",
        "ai data analysis for airtable": "AI Data Analysis for Airtable: Connect, Query, and Report (2026)",
        "ai analysis for notion database": "AI Analysis for Notion Databases: From Tables to Decisions (2026)",
        "connect clickhouse to ai analyst": "Connect ClickHouse to an AI Data Analyst: SQL Analysis at Scale (2026)",
        "connect redshift to ai data analyst": "Connect Amazon Redshift to an AI Data Analyst (2026 Integration Guide)",
        "analyze stripe data with ai": "Analyze Stripe Data with AI: Financial Services Analytics Playbook (2026)",
        "analyze shopify data with ai": "Analyze Shopify Data with AI: Ecommerce Data Analysis Guide (2026)",
        "natural language to sql": "Natural Language to SQL: Complete Guide for Analysts and Engineers (2026)",
        "text to sql llm": "Text-to-SQL with LLMs: Architecture, Tools, and Production Tips (2026)",
        "nl2sql benchmark spider bird": "NL2SQL Benchmarks (Spider, BIRD): What Scores Mean in Production (2026)",
        "ai sql generator": "AI SQL Generator Tools Compared: Query Generation for Real Workloads (2026)",
        "llm sql generation architecture": "LLM SQL Generation Architecture: Design Patterns for Enterprise (2026)",
        "sql rag vs semantic layer": "SQL RAG vs Semantic Layer: Which Approach Wins for Enterprise AI Analytics?",
        "text to sql fine tuning": "Text-to-SQL Fine-Tuning: When Custom Models Beat Prompting (2026)",
        "sql agent vs text to sql": "SQL Agent vs Text-to-SQL: Autonomy, Governance, and Buyer Fit (2026)",
        "nl2sql in production failure modes": "NL2SQL in Production: Failure Modes and Mitigation Playbook (2026)",
        "dialect aware sql generation": "Dialect-Aware SQL Generation: Postgres, Snowflake, BigQuery, and Beyond",
        "clean excel data with ai": "How to Clean Excel Data with AI: Step-by-Step Guide (2026)",
        "ai alternative to pivot table": "AI Alternative to Pivot Tables for Faster Spreadsheet Analysis (2026)",
        "ai vlookup replacement": "AI VLOOKUP Replacement: Smarter Lookup and Join Workflows in Excel",
        "ai excel formula generator": "AI Excel Formula Generator: Templates and Prompt Patterns for Analysts",
        "analyze csv with ai": "How to Analyze CSV Files with AI: From Upload to Insight (2026)",
        "merge multiple csv files with ai": "Merge Multiple CSV Files with AI: Cleaning and Analysis Workflow (2026)",
        "deduplicate data with ai": "Deduplicate Data with AI: CRM and Spreadsheet Cleaning Guide (2026)",
        "ai data cleaning techniques": "AI Data Cleaning Techniques: Framework for Analysts and Engineers (2026)",
        "ai excel chart generator": "AI Excel Chart Generator: Build Decision-Ready Visuals Faster (2026)",
        "ai financial modeling in excel": "AI Financial Modeling in Excel: Business Analysis and Forecasting Guide",
        "excel monthly report automation with ai": "Excel Monthly Report Automation with AI: Template and Workflow (2026)",
        "ai data wrangling tools": "Best AI Data Wrangling Tools and Platforms for Analysts (2026)",
        "ai tools for data analysts": "AI Tools for Data Analysts: Stack Guide and Evaluation Framework (2026)",
        "ai data analysis for product managers": "AI Data Analysis for Product Managers: Metrics Without SQL Overhead",
        "ai data analysis for finance teams": "AI Data Analysis for Finance Teams: Integration and Controls (2026)",
        "ai data analysis for marketing": "AI Data Analysis for Marketing Teams: Campaign and Funnel Analytics (2026)",
        "ai data analysis for operations": "AI Data Analysis for Operations Teams: KPIs, Alerts, and Execution (2026)",
        "ai for data engineers": "AI for Data Engineers: Pipelines, Quality, and Agentic Analytics (2026)",
        "ai data strategy for cto": "AI Data Strategy for CTOs: Semantic Layers and Enterprise Roadmap (2026)",
        "ai data analysis for founders": "AI Data Analysis for Founders: Fast Insights Without a Full Data Team",
        "ai data analysis for ecommerce": "AI Data Analysis for Ecommerce: Revenue, Cohort, and Merchandising KPIs",
        "ai data analysis for saas": "AI Data Analysis for SaaS: Churn, Expansion, and Product-Led Metrics",
        "ai data analysis for financial services": "AI Data Analysis for Financial Services: Compliance-Aware Analytics Guide",
        "ai data analysis for supply chain": "AI Data Analysis for Supply Chain: Inventory, Lead Time, and Risk KPIs",
        "ai data analysis healthcare": "AI Data Analysis in Healthcare: Use Cases, Governance, and Workflow Fit",
        "ai data analysis logistics": "AI Data Analysis in Logistics: Route, Cost, and SLA Decision Support",
        "ai data analysis prompts": "AI Data Analysis Prompts: 30+ Templates for Analysts (2026)",
        "data analysis prompt template": "Data Analysis Prompt Templates: Reusable Frameworks for Teams (2026)",
        "ai data analyst skills": "AI Data Analyst Skills: Competency Map for 2026 Hiring and Upskilling",
        "how to evaluate ai data analyst": "How to Evaluate an AI Data Analyst Tool: Scorecard for Buyers (2026)",
        "ai analytics glossary": "AI Analytics Glossary: 40 Terms Every Data Team Should Know (2026)",
        "data agent faq": "Data Agent FAQ: 12 Answers on Architecture, Memory, and Buyer Fit",
        "code agent vs data agent": "Code Interpreter Data Analysis: Code Agent vs Data Agent (2026)",
        "data agent architecture": "Data Agent LLM Architecture: Layers, Memory, and Production Design (2026)",
        "ai data analyst vs bi tools": "AI Tools for Data Analysts: AI Analyst vs BI Tools Compared (2026)",
        "data agent vs llm chatbot": "Data Agent LLM vs Chatbot: When Conversational AI Is Not Enough (2026)",
        "chatgpt for data analysis limitations": "ChatGPT Data Analysis Limit: What Breaks at Enterprise Scale (2026)",
        "code interpreter vs data agent": "Code Interpreter Data Analysis vs Data Agent: Production Comparison (2026)",
        "databricks genie vs data agent": "Databricks Assistant vs Genie vs Data Agent: Buyer Guide (2026)",
        "ai data analyst vs human analyst": "AI Data Analyst vs Human Analyst: Roles, ROI, and Handoff Model (2026)",
        "governance for ai data analysis": "AI Data Governance for Analytics Teams: Framework and Checklist (2026)",
        "ai data analyst vs traditional bi analyst": "Business Intelligence vs Data Science: AI Analyst vs Traditional BI (2026)",
    }
    return mapping.get(t, t.title() + " (2026)")


def hero_filename(slug: str) -> str:
    return f"hero-{slug}.png"


def scaffold_pillar(pillar: dict) -> None:
    root = BLOG / pillar["folder"]
    root.mkdir(parents=True, exist_ok=True)
    articles = pillar["articles"]
    registry = {
        "pillar": pillar["folder"],
        "generated": "2026-06-09",
        "source_plan": "100页主题集群规划-v1-替换后主关键词版.md · Pillar " + str(pillar["pillar_num"]),
        "articles": articles,
    }
    (root / "articles_registry.json").write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if REF_PREVIEW.exists() and not (root / "build-preview.py").exists():
        shutil.copy2(REF_PREVIEW, root / "build-preview.py")

    for i, art in enumerate(articles):
        adir = root / art["folder"]
        (adir / "images").mkdir(parents=True, exist_ok=True)
        (adir / "visuals").mkdir(parents=True, exist_ok=True)
        gitkeep = adir / "images" / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")
        title = title_from_theme(art["theme"], art["kicker"])
        art["_title"] = title
        readme = f"""# {art['id']} · {title} — Deliverable Bundle

**Article ID**: {art['id']}
**Slug**: `/blog/{art['slug']}`
**Primary keyword**: `{art['keyword']}`
**Type**: {art['type']}
**Pillar**: {pillar['name']}

## Files

- `article.md` — Long-form article (2000–2500 words)
- `meta-tags.html` — SEO + OG tags
- `schema.json` — BlogPosting + FAQPage
- `audit.md` — CORE-EEAT gate report
- `images/{hero_filename(art['slug'])}` — Hero cover 1200×630

## Gates

Run from repo root:

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/{pillar['folder']}/{art['folder']}
python3 SEO/Blog/audit-eeat.py SEO/Blog/{pillar['folder']}/{art['folder']}
```
"""
        (adir / "README.md").write_text(readme, encoding="utf-8")

    # INDEX.md
    lines = [
        f"# {pillar['name']}",
        "",
        f"> Pillar {pillar['pillar_num']} · Articles {articles[0]['id']}–{articles[-1]['id']} · Generated 2026-06-09",
        "",
        "| ID | Folder | Slug | Keyword | Vol | KD | Type |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for art in articles:
        vol = art.get("volume")
        kd = art.get("kd")
        lines.append(
            f"| {art['id']} | [{art['folder']}](./{art['folder']}/) | `/blog/{art['slug']}` | {art['keyword']} | {vol if vol is not None else '—'} | {kd if kd is not None else '—'} | {art['type']} |"
        )
    (root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  scaffolded {pillar['folder']}: {len(articles)} article folders")


def main() -> int:
    reg_path = DEFAULT_REGISTRY
    if len(sys.argv) > 1 and sys.argv[1] in REGISTRY_ALIASES:
        reg_path = REGISTRY_ALIASES[sys.argv[1]]
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    pillars = data["pillars"]
    if len(sys.argv) > 1:
        want = set(sys.argv[1:])
        pillars = [p for p in pillars if p["id"] in want or p["folder"] in want]
    for pillar in pillars:
        scaffold_pillar(pillar)
    print(f"Done. {sum(len(p['articles']) for p in pillars)} folders across {len(pillars)} pillars.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
