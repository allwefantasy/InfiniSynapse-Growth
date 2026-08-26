#!/usr/bin/env python3
"""DEPRECATED — use build-hub-landing-handoff-pack.py instead.

Hub article = pillar landing page at /en/blog/{hub-slug}. Do NOT build /en/blog/pillar/* pages.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[5]
BLOG = ROOT / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
OUT = BLOG / "pillar-landing-handoff-pack"
PAGES = OUT / "landing-pages"
SITE = "https://infinisynapse.com"

_spec = importlib.util.spec_from_file_location("reg", SCRIPTS / "cluster-link-registry.py")
reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(reg)

# landing_slug, display fields, SEO (title 40-60, description 150-160)
PILLAR_META: list[dict] = [
    {
        "pillar_dir": "pillar1-ai-native-data-analysis",
        "landing_slug": "ai-native-data-analysis",
        "h1": "AI-Native Data Analysis",
        "subtitle": "Data Agents, agentic analytics, and production-grade AI analysis workflows.",
        "meta_title": "AI-Native Data Analysis Guides (2026) | InfiniSynapse",
        "meta_description": "Explore AI-native data analysis in 2026: Data Agents, agentic analytics, and auditable workflows—start with the complete pillar guide and cluster deep dives.",
        "target_keyword": "ai native data analysis",
        "intro": "This topic cluster covers how teams move from copilots and dashboards to **AI-native data analysis**—systems that plan, query, and explain with evidence you can audit. Use the complete guide below, then branch into definitions, architecture, and buyer comparisons.",
    },
    {
        "pillar_dir": "pillar2-data-agent-vs-alternatives",
        "landing_slug": "data-agent-vs-alternatives",
        "h1": "Data Agent vs Alternatives",
        "subtitle": "Compare Data Agents with code agents, chatbots, BI copilots, and legacy analyst workflows.",
        "meta_title": "Data Agent vs Alternatives: 2026 Guides | InfiniSynapse",
        "meta_description": "Compare Data Agents with code agents, chatbots, and BI copilots in 2026. Architecture, governance, and buyer guides for enterprise analytics stack evaluations.",
        "target_keyword": "data agent vs alternatives",
        "intro": "Not every AI analytics product is a **Data Agent**. This cluster explains where code agents, chatbots, and warehouse copilots stop—and what a production Data Agent must add for governance, SQL, and repeatable answers.",
    },
    {
        "pillar_dir": "pillar3-ai-analyst-tools",
        "landing_slug": "ai-analyst-tools",
        "h1": "AI Analyst Tools & Reviews",
        "subtitle": "Tool comparisons, alternatives, and buyer guides for AI data analysis software.",
        "meta_title": "AI Analyst Tools & Reviews (2026) | InfiniSynapse",
        "meta_description": "Compare AI analyst tools and alternatives in 2026: rankings, self-hosted options, and head-to-head reviews with buyer frameworks for SQL and Excel teams.",
        "target_keyword": "ai analyst tools",
        "intro": "Choosing **AI analyst tools** means comparing autonomy, SQL depth, visualization, and governance—not feature checklists alone. Start with the pillar roundup, then open focused comparisons and alternative matrices.",
    },
    {
        "pillar_dir": "pillar4-data-source-connectors",
        "landing_slug": "data-source-connectors",
        "h1": "Data Source Connectors",
        "subtitle": "Connect warehouses, databases, spreadsheets, and SaaS data to an AI data analyst.",
        "meta_title": "Data Source Connectors for AI Analysis | InfiniSynapse",
        "meta_description": "Connect Postgres, Snowflake, BigQuery, MySQL, Sheets, and SaaS to an AI data analyst in 2026—with setup checklists, security controls, and validation SQL.",
        "target_keyword": "connect data source ai analyst",
        "intro": "Connector quality determines whether an AI analyst can answer production questions safely. These guides cover credentials, preflight checks, and SQL trace patterns for each **data source** your team wires into a Data Agent.",
    },
    {
        "pillar_dir": "pillar5-nl2sql-text-to-sql",
        "landing_slug": "nl2sql-text-to-sql",
        "h1": "NL2SQL & Text-to-SQL",
        "subtitle": "Natural language to SQL: architecture, benchmarks, failure modes, and production patterns.",
        "meta_title": "NL2SQL & Text-to-SQL Guides (2026) | InfiniSynapse",
        "meta_description": "NL2SQL and text-to-SQL in 2026: LLM architecture, Spider/BIRD benchmarks, semantic layers vs RAG, dialect-aware SQL, and production failure modes for teams.",
        "target_keyword": "nl2sql text to sql",
        "intro": "**NL2SQL** looks simple in demos and fragile in production. This cluster documents architecture choices, evaluation benchmarks, fine-tuning trade-offs, and the guardrails teams need before exposing natural language query to business users.",
    },
    {
        "pillar_dir": "pillar6-ai-excel-csv-spreadsheet",
        "landing_slug": "ai-excel-csv-spreadsheet",
        "h1": "AI for Excel, CSV & Spreadsheets",
        "subtitle": "Analyze, clean, and automate spreadsheets and CSV files with AI.",
        "meta_title": "AI for Excel & CSV Guides (2026) | InfiniSynapse",
        "meta_description": "Practical AI guides for Excel, CSV, and spreadsheets: clean data, formulas, pivot alternatives, and monthly report automation—updated for 2026 business teams.",
        "target_keyword": "ai excel csv analysis",
        "intro": "Most teams still live in spreadsheets before they adopt a warehouse. These guides show how **AI for Excel and CSV** can clean data, replace pivot tables, generate formulas, and automate recurring reports—with paths to audit-ready agents when you scale.",
    },
    {
        "pillar_dir": "pillar7-use-cases-role-industry",
        "landing_slug": "use-cases-by-role",
        "h1": "AI Data Analysis by Role & Industry",
        "subtitle": "Use-case guides for analysts, PMs, finance, marketing, founders, and regulated industries.",
        "meta_title": "AI Data Analysis by Role & Industry | InfiniSynapse",
        "meta_description": "AI data analysis use cases by role and industry in 2026: finance, marketing, SaaS, healthcare, logistics, and CTO strategy—with workflow patterns per persona.",
        "target_keyword": "ai data analysis use cases",
        "intro": "The same Data Agent stack behaves differently for a product manager, a CFO, or a healthcare compliance lead. Browse **role- and industry-specific** guides to see workflows, metrics, and governance expectations that match your team.",
    },
    {
        "pillar_dir": "pillar8-skills-templates-glossary",
        "landing_slug": "skills-templates-glossary",
        "h1": "Skills, Templates & Glossary",
        "subtitle": "Prompt templates, analyst skills, evaluation checklists, and AI analytics terminology.",
        "meta_title": "AI Data Analysis Skills & Templates | InfiniSynapse",
        "meta_description": "AI data analysis prompts, templates, skills matrices, evaluation checklists, and glossary terms for teams standardizing how humans and agents work with data.",
        "target_keyword": "ai data analysis prompts",
        "intro": "Repeatable analysis needs shared language and reusable prompts—not one-off chat threads. This cluster collects **templates, skills rubrics, evaluation checklists, and glossary definitions** your team can adopt before rolling agents to production.",
    },
    {
        "pillar_dir": "pillar9-semantic-layer",
        "landing_slug": "semantic-layer",
        "h1": "Semantic Layer",
        "subtitle": "Metric definitions, dbt semantic layers, and grounding NL queries for AI agents.",
        "meta_title": "Semantic Layer Guides for AI Analytics | InfiniSynapse",
        "meta_description": "Semantic layer guides for AI analytics in 2026: dbt metrics, architecture requirements, and options for grounding natural language queries on approved terms.",
        "target_keyword": "semantic layer ai analytics",
        "intro": "Agents without a **semantic layer** guess at metric definitions finance already rejected. These guides explain what a semantic layer must provide, how dbt and warehouse models fit, and when to invest before scaling NL access.",
    },
    {
        "pillar_dir": "pillar10-mcp-data-access",
        "landing_slug": "mcp-data-access",
        "h1": "MCP for Data Access",
        "subtitle": "Model Context Protocol patterns for connecting AI agents to databases and tools.",
        "meta_title": "MCP for Data Analysis: 2026 Guides | InfiniSynapse",
        "meta_description": "MCP for data analysis in 2026: connect agents to databases and tools via Model Context Protocol patterns, security boundaries, and production deployment guides.",
        "target_keyword": "mcp for data analysis",
        "intro": "**Model Context Protocol (MCP)** is emerging as a standard way to expose data tools to agents. This cluster covers MCP server design, database access patterns, and how teams combine MCP with SQL agents and governance gates.",
    },
    {
        "pillar_dir": "pillar11-agentic-analytics",
        "landing_slug": "agentic-analytics",
        "h1": "Agentic Analytics",
        "subtitle": "Autonomous analytics agents, orchestration, and buyer guides for agentic BI.",
        "meta_title": "Agentic Analytics Guides (2026) | InfiniSynapse",
        "meta_description": "Agentic analytics in 2026: definitions, orchestration patterns, buyer guides, and production examples for teams replacing dashboards with autonomous agents.",
        "target_keyword": "agentic analytics",
        "intro": "**Agentic analytics** moves beyond single-shot answers to multi-step plans with tool use and audit trails. Explore definition guides, architecture patterns, and comparisons to augmented analytics and traditional BI.",
    },
    {
        "pillar_dir": "pillar12-data-trends",
        "landing_slug": "data-trends",
        "h1": "Data Trends",
        "subtitle": "Analytics, integration, privacy, warehouse, and visualization trends for 2026 planning.",
        "meta_title": "Data Trends for Analytics Teams (2026) | InfiniSynapse",
        "meta_description": "Data trends for analytics teams in 2026: integration, visualization, privacy, and warehouse shifts—with executive definitions and links to specialized guides.",
        "target_keyword": "data trends analytics",
        "intro": "Platform councils need a shared map of **data trends** before approving 2026 budgets. This hub links specialized guides on analytics, integration, visualization, privacy, and warehouse architecture—with citable definitions for roadmap reviews.",
    },
    {
        "pillar_dir": "pillar13-data-privacy-security",
        "landing_slug": "data-privacy-security",
        "h1": "Data Privacy & Security",
        "subtitle": "Privacy trends, compliance frameworks, and security controls for AI analytics.",
        "meta_title": "Data Privacy & Security for AI Analytics | InfiniSynapse",
        "meta_description": "Data privacy and security for AI analytics in 2026: compliance frameworks, access controls, retention policies when agents query live production schemas.",
        "target_keyword": "data privacy ai analytics",
        "intro": "Agent access to live schemas raises **data privacy and security** questions traditional BI never surfaced. These guides cover compliance frameworks, retention, consent, and operational controls for analytics and security stakeholders.",
    },
    {
        "pillar_dir": "pillar14-enterprise-data",
        "landing_slug": "enterprise-data",
        "h1": "Enterprise Data",
        "subtitle": "Enterprise data security, governance, and platform patterns for AI analytics at scale.",
        "meta_title": "Enterprise Data Security Guides (2026) | InfiniSynapse",
        "meta_description": "Enterprise data security and governance for AI analytics in 2026: platform patterns, access models, audit requirements, and solutions for regulated deployments.",
        "target_keyword": "enterprise data security",
        "intro": "Enterprise deployments need more than a capable model—they need **enterprise data** governance, isolation, and auditability. This cluster links security solutions, platform patterns, and rollout checklists for large organizations.",
    },
    {
        "pillar_dir": "pillar15-data-search",
        "landing_slug": "data-search",
        "h1": "Data Search & Discovery",
        "subtitle": "Public data sources, search patterns, and discovery workflows for AI analysis.",
        "meta_title": "Data Search & Public Sources (2026) | InfiniSynapse",
        "meta_description": "Data search and public sources for AI analysis in 2026: discovery workflows, reliability checks, open datasets, and patterns for internal and external evidence.",
        "target_keyword": "public data ai analysis",
        "intro": "Agents increasingly blend warehouse tables with **public data and search**. These guides cover source reliability, discovery workflows, and how to keep external evidence inside the same audit trail as internal SQL.",
    },
]

FAQS: dict[str, list[tuple[str, str]]] = {
    "ai-native-data-analysis": [
        ("What is AI-native data analysis?", "AI-native data analysis means the product is built around agents that plan, query, and explain with auditable SQL and memory—not a chat layer bolted onto a BI tool."),
        ("Where should I start in this cluster?", "Start with the complete pillar guide, then open the definition and architecture articles that match your buying stage."),
    ],
    "ai-excel-csv-spreadsheet": [
        ("Can AI replace Excel entirely?", "For many recurring workflows—cleaning, pivots, formulas, and monthly reports—AI can automate the heavy lifting while Excel remains the interface teams already trust."),
        ("Where should spreadsheet teams start?", "Begin with the Excel cleaning guide, then branch into CSV merge, deduplication, and report automation articles in this cluster."),
    ],
}


def load_blog_index() -> dict:
    return json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))


def posts_for_pillar(posts: list[dict], pillar_dir: str, hub_slug: str) -> list[dict]:
    cluster_posts = [p for p in posts if p.get("pillar_cluster") == pillar_dir]
    cluster_posts.sort(key=lambda p: (-p.get("sort_priority", 0), p.get("slug", "")))
    # Hub first
    hub = [p for p in cluster_posts if p["slug"] == hub_slug]
    rest = [p for p in cluster_posts if p["slug"] != hub_slug]
    return hub + rest


def abs_image(path: str) -> str:
    if path.startswith("http"):
        return path
    return f"{SITE}{path}"


def canonical_url(landing_slug: str) -> str:
    return f"{SITE}/en/blog/pillar/{landing_slug}"


def zh_url(landing_slug: str) -> str:
    return f"{SITE}/zh/blog/pillar/{landing_slug}"


def build_meta_tags(cfg: dict, og_image: str, og_alt: str) -> str:
    slug = cfg["landing_slug"]
    url = canonical_url(slug)
    title = cfg["meta_title"]
    desc = cfg["meta_description"]
    return f"""<!-- Pillar landing page SEO head · {slug} · generated by build-pillar-landing-handoff-pack.py -->
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">

<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="InfiniSynapse Data Team">
<meta http-equiv="content-language" content="en">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{zh_url(slug)}">
<link rel="alternate" hreflang="x-default" href="{url}">

<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{escape(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(og_alt)}">
<meta property="og:site_name" content="InfiniSynapse Blog">
<meta property="og:locale" content="en_US">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@InfiniSynapse">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(desc)}">
<meta name="twitter:image" content="{escape(og_image)}">
<meta name="twitter:image:alt" content="{escape(og_alt)}">
"""


def build_schema(cfg: dict, articles: list[dict], hub: dict) -> list[dict]:
    slug = cfg["landing_slug"]
    url = canonical_url(slug)
    today = datetime.now().date().isoformat()
    items = []
    for i, p in enumerate(articles, start=1):
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "url": f"{SITE}/en/blog/{p['slug']}",
                "name": p["title"],
            }
        )
    return [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/en/blog"},
                {"@type": "ListItem", "position": 3, "name": cfg["h1"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": url,
            "url": url,
            "name": cfg["h1"],
            "description": cfg["meta_description"],
            "dateModified": today,
            "publisher": {
                "@type": "Organization",
                "name": "InfiniSynapse",
                "url": SITE,
            },
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(items),
                "itemListElement": items,
            },
        },
    ]


def _faq_blocks(cfg: dict, hub: dict) -> list[tuple[str, str]]:
    return FAQS.get(cfg["landing_slug"], [
        (f"What is covered in {cfg['h1']}?", cfg["subtitle"]),
        (
            "Where should I start?",
            f"Open the complete guide linked above ({hub['title']}), then return here to pick a specialized article.",
        ),
    ])


def build_body(cfg: dict, articles: list[dict], hub: dict, all_landings: list[dict]) -> str:
    hub_title = hub["title"]
    hub_slug = hub["slug"]
    lines = [
        cfg["intro"],
        "",
        "## Start with the complete guide",
        "",
        f"If you are new to this topic, start with [{hub_title}](/en/blog/{hub_slug}) — "
        f"the pillar overview that links every specialized guide in this cluster.",
        "",
        "## All guides in this topic",
        "",
        f"**{len(articles)} guides** in this cluster:",
        "",
    ]
    for p in articles:
        lines.append(f"- [{p['title']}](/en/blog/{p['slug']}) — {p['excerpt']}")
    lines.extend(["", "## Frequently asked questions", ""])
    for q, a in _faq_blocks(cfg, hub):
        lines.extend([f"### {q}", "", a, ""])
    lines.extend(["", "## Explore other topic clusters", ""])
    for other in all_landings:
        if other["landing_slug"] == cfg["landing_slug"]:
            continue
        lines.append(
            f"- [{other['h1']}](/en/blog/pillar/{other['landing_slug']}) — {other['subtitle']}"
        )
    lines.append("")
    return "\n".join(lines)


def build_body_cms(cfg: dict, articles: list[dict], hub: dict, all_landings: list[dict]) -> str:
    """QuickCreator / card-grid template: H2 sections without duplicating the card list."""
    hub_title = hub["title"]
    hub_slug = hub["slug"]
    n = len(articles)
    lines = [
        cfg["intro"],
        "",
        "## Start with the complete guide",
        "",
        f"If you are new to this topic, start with [{hub_title}](/en/blog/{hub_slug}) — "
        f"the pillar overview that links every specialized guide in this cluster.",
        "",
        "## All guides in this topic",
        "",
        f"**{n} guides** in this cluster. Use the article cards below, or open the complete guide above first.",
        "",
        "<!-- CARD_GRID: render articles.json here; card titles should be H3 -->",
        "",
        "## Frequently asked questions",
        "",
    ]
    for q, a in _faq_blocks(cfg, hub):
        lines.extend([f"### {q}", "", a, ""])
    lines.extend(["", "## Explore other topic clusters", ""])
    for other in all_landings:
        if other["landing_slug"] == cfg["landing_slug"]:
            continue
        lines.append(
            f"- [{other['h1']}](/en/blog/pillar/{other['landing_slug']}) — {other['subtitle']}"
        )
    lines.append("")
    return "\n".join(lines)


def meta_field(pat: str, meta: str) -> str:
    m = re.search(pat, meta)
    return (m.group(1) if m else "").replace("&quot;", '"').strip()


def qc_row(cfg: dict, meta: str, hub: dict, article_count: int) -> dict:
    slug = cfg["landing_slug"]
    url = canonical_url(slug)
    return {
        "landing_slug": slug,
        "page_url": url,
        "display_h1": cfg["h1"],
        "subtitle": cfg["subtitle"],
        "seo_title": cfg["meta_title"],
        "meta_description": cfg["meta_description"],
        "canonical_url": url,
        "og_title": meta_field(r'<meta property="og:title" content="([^"]+)"', meta),
        "og_description": meta_field(r'<meta property="og:description" content="([^"]+)"', meta),
        "og_image": meta_field(r'<meta property="og:image" content="([^"]+)"', meta),
        "twitter_title": meta_field(r'<meta name="twitter:title" content="([^"]+)"', meta),
        "twitter_description": meta_field(r'<meta name="twitter:description" content="([^"]+)"', meta),
        "twitter_image": meta_field(r'<meta name="twitter:image" content="([^"]+)"', meta),
        "badge_label": f"{article_count} GUIDES",
        "hub_slug": hub["slug"],
        "body_paste_file": "body-cms.md",
        "qc_notes": (
            "Page Title/H1=display_h1; SEO Title=seo_title (40-60 chars); "
            "paste body-cms.md for H2; badge=badge_label only (no pillar number)"
        ),
    }


def write_qc_fix_guide() -> None:
    text = """# QuickCreator · Pillar 落地页 SEO 集体修复（15 页）

> 数据表：**`quickcreator-pillar-landing-seo-fields.csv`**（每页一行，照着粘贴）  
> 正文：**`landing-pages/{landing_slug}/body-cms.md`**（含 H2，配合卡片网格）

## 问题根因

落地页在 QuickCreator 里只填了短标题（如 `Enterprise Data`），**没有把 SEO 字段和 H2 正文接进 CMS**：

| QuickCreator 报错 | 修复 |
|---|---|
| ❌ Canonical URL 缺失 | 填 `canonical_url` |
| ❌ Meta Title 不在 40–60 | **SEO 标题**用 `seo_title`，不要用短 `display_h1` |
| ❌ Meta Description 不在 150–160 | 填 `meta_description` |
| ❌ 缺少 H2 | 粘贴 `body-cms.md`（含 4 个 H2 区块） |
| ❌ 社交标签缺失 | 填 `og_*` / `twitter_*` |
| UI 显示 `14` / `06` 编号 | 徽章改为 `badge_label`（如 `13 GUIDES`） |

## 每页修复步骤（约 3 分钟）

1. **页面标题（H1 展示）** → `display_h1`（可较短，如 Enterprise Data）
2. **副标题** → `subtitle`
3. **SEO 设置 → Title / Meta Title** → `seo_title`（40–60 字符，含品牌）
4. **SEO 设置 → Meta Description** → `meta_description`
5. **SEO 设置 → Canonical URL** → `canonical_url`（无尾斜杠）
6. **社交分享** → `og_title` / `og_description` / `og_image`（Twitter 同值）
7. **正文编辑器** → 粘贴 `body-cms.md` 全文；**卡片网格**放在 `<!-- CARD_GRID -->` 注释处
8. **徽章文案** → 仅 `badge_label`，删除 pillar 编号

> 若站点支持直接注入 `<head>`：用 `head.html` 一次性覆盖 canonical / description / og / twitter / JSON-LD。

## 验收（15/15 页）

- [ ] On-Page SEO 面板 5 项全绿
- [ ] 页面仅 1 个 H1（= display_h1）
- [ ] 至少 3 个 H2（Start here / All guides / FAQ / Explore）
- [ ] 无 `#` 开头正文标题（避免双 H1）
- [ ] 徽章无 `06` / `14` 等内部编号

---

*生成脚本：`build-pillar-landing-handoff-pack.py` · 审计：`audit-pillar-landing-onpage.py`*
"""
    (OUT / "QUICKCREATOR-PILLAR-LANDING-FIX.md").write_text(text, encoding="utf-8")


def build_head_html(meta: str, schema: list) -> str:
    schema_text = json.dumps(schema, ensure_ascii=False, indent=2)
    return (
        f"{meta.strip()}\n\n"
        f'<script type="application/ld+json">\n{schema_text}\n</script>\n'
    )


def validate_seo(cfg: dict) -> None:
    t = cfg["meta_title"]
    d = cfg["meta_description"]
    if not (40 <= len(t) <= 60):
        raise ValueError(f"meta_title length {len(t)} for {cfg['landing_slug']}: {t!r}")
    if not (150 <= len(d) <= 160):
        raise ValueError(f"meta_description length {len(d)} for {cfg['landing_slug']}: {d!r}")


def build_sitemap_snippet(records: list[dict]) -> str:
    today = datetime.now().date().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for r in records:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(r['url'])}</loc>",
                f"    <lastmod>{today}</lastmod>",
                "    <changefreq>weekly</changefreq>",
                "    <priority>0.8</priority>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    xml = "\n".join(lines) + "\n"
    parseString(xml.encode("utf-8"))
    return xml


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    PAGES.mkdir(parents=True)

    blog = load_blog_index()
    posts = blog["posts"]
    hub_by_pillar = {
        pd.name: reg.slug_from_folder(reg.PRIMARY_HUB[pd.name]) for pd in reg.PILLAR_DIRS
    }

    master_pages: list[dict] = []
    manifest_rows: list[dict] = []
    qc_rows: list[dict] = []

    for cfg in PILLAR_META:
        validate_seo(cfg)
        pillar_dir = cfg["pillar_dir"]
        hub_slug = hub_by_pillar[pillar_dir]
        cluster = posts_for_pillar(posts, pillar_dir, hub_slug)
        if not cluster:
            raise SystemExit(f"No posts for {pillar_dir}")
        hub = cluster[0]
        og_image = abs_image(hub.get("hero_image", ""))
        og_alt = f"{cfg['h1']} — InfiniSynapse topic cluster"

        page_dir = PAGES / cfg["landing_slug"]
        page_dir.mkdir()

        meta = build_meta_tags(cfg, og_image, og_alt)
        schema = build_schema(cfg, cluster, hub)
        body = build_body(cfg, cluster, hub, PILLAR_META)
        body_cms = build_body_cms(cfg, cluster, hub, PILLAR_META)
        head = build_head_html(meta, schema)

        (page_dir / "meta-tags.html").write_text(meta, encoding="utf-8")
        (page_dir / "head.html").write_text(head, encoding="utf-8")
        (page_dir / "schema.json").write_text(
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (page_dir / "body.md").write_text(body, encoding="utf-8")
        (page_dir / "body-cms.md").write_text(body_cms, encoding="utf-8")
        qc_rows.append(qc_row(cfg, meta, hub, len(cluster)))
        (page_dir / "cms-settings.json").write_text(
            json.dumps(
                {
                    "display_h1": cfg["h1"],
                    "subtitle": cfg["subtitle"],
                    "seo_title": cfg["meta_title"],
                    "meta_description": cfg["meta_description"],
                    "canonical_url": canonical_url(cfg["landing_slug"]),
                    "badge_label": f"{len(cluster)} GUIDES",
                    "article_count": len(cluster),
                    "hub_slug": hub_slug,
                    "hub_url": f"/en/blog/{hub_slug}",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        articles_payload = [
            {
                "slug": p["slug"],
                "title": p["title"],
                "excerpt": p["excerpt"],
                "url": f"/en/blog/{p['slug']}",
                "card_tag": p.get("card_tag", ""),
                "display_date": p.get("display_date", ""),
                "hero_image": p.get("hero_image", ""),
                "is_hub": p["slug"] == hub_slug,
            }
            for p in cluster
        ]
        (page_dir / "articles.json").write_text(
            json.dumps(articles_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        page_record = {
            "landing_slug": cfg["landing_slug"],
            "pillar_dir": pillar_dir,
            "h1": cfg["h1"],
            "subtitle": cfg["subtitle"],
            "meta_title": cfg["meta_title"],
            "meta_description": cfg["meta_description"],
            "target_keyword": cfg["target_keyword"],
            "canonical_url": canonical_url(cfg["landing_slug"]),
            "url_path": f"/en/blog/pillar/{cfg['landing_slug']}",
            "hub_slug": hub_slug,
            "hub_title": hub["title"],
            "hub_url": f"/en/blog/{hub_slug}",
            "article_count": len(cluster),
            "og_image": og_image,
            "source_path": f"SEO/Blog/pillar-landing-handoff-pack/landing-pages/{cfg['landing_slug']}",
        }
        master_pages.append(page_record)
        manifest_rows.append(
            {
                "landing_slug": cfg["landing_slug"],
                "pillar_dir": pillar_dir,
                "完整URL": page_record["canonical_url"],
                "h1": cfg["h1"],
                "meta_title": cfg["meta_title"],
                "hub_slug": hub_slug,
                "article_count": len(cluster),
                "source_path": page_record["source_path"],
            }
        )

    master = {
        "_comment": "15 pillar landing pages for /en/blog/pillar/{landing_slug}",
        "_generated_by": "build-pillar-landing-handoff-pack.py",
        "_generated_at": datetime.now().isoformat(timespec="seconds"),
        "page_count": len(master_pages),
        "url_pattern": "/en/blog/pillar/{landing_slug}",
        "pages": master_pages,
    }
    (OUT / "pillar-landing-pages-master.json").write_text(
        json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (OUT / "deploy-manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
        w.writeheader()
        w.writerows(manifest_rows)

    qc_fields = list(qc_rows[0].keys())
    with (OUT / "quickcreator-pillar-landing-seo-fields.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=qc_fields)
        w.writeheader()
        w.writerows(qc_rows)

    write_qc_fix_guide()

    sitemap = build_sitemap_snippet([{"url": r["完整URL"]} for r in manifest_rows])
    (OUT / "sitemap-pillar-landings.xml").write_text(sitemap, encoding="utf-8")

    # Copy full site sitemap if present (includes 15 landings after build-sitemap.py)
    subprocess.run(
        [sys.executable, str(SCRIPTS / "build-sitemap.py")],
        check=True,
        cwd=ROOT,
    )
    full_sitemap = BLOG / "sitemap.xml"
    if full_sitemap.is_file():
        shutil.copy2(full_sitemap, OUT / "sitemap.xml")

    readme = f"""# Pillar 落地页 · 程序员交付包（15 页）

> **路由**：`https://infinisynapse.com/en/blog/pillar/{{landing_slug}}`  
> **页面类型**：主题索引页（CollectionPage），不是长文 BlogPosting。

## 包内结构

```
pillar-landing-handoff-pack/
├── README.md
├── QUICKCREATOR-PILLAR-LANDING-FIX.md  ← QuickCreator 15 页集体修复指南
├── quickcreator-pillar-landing-seo-fields.csv  ← 逐页粘贴 SEO 字段
├── deploy-manifest.csv              ← 15 页部署清单
├── pillar-landing-pages-master.json ← 前端/CMS 可 import 的全量元数据
├── sitemap-pillar-landings.xml      ← 15 个 URL（可合并进主 sitemap）
├── sitemap.xml                      ← 全站 sitemap（含 202 博客 + 15 落地页，若已生成）
└── landing-pages/
    └── {{landing_slug}}/
        ├── body-cms.md      ← QuickCreator 正文（含 H2；卡片网格插 CARD_GRID 处）
        ├── body.md          ← 静态站完整正文（含文章列表）
        ├── cms-settings.json← display_h1 / seo_title / badge_label 等
        ├── meta-tags.html   ← SEO head 片段
        ├── head.html        ← meta-tags + JSON-LD（推荐整段注入 <head>）
        ├── schema.json      ← BreadcrumbList + CollectionPage + ItemList
        └── articles.json    ← 卡片网格数据（含 is_hub 标记）
```

## QuickCreator 集体修复（当前 5 项报错）

见 **`QUICKCREATOR-PILLAR-LANDING-FIX.md`**，按 **`quickcreator-pillar-landing-seo-fields.csv`** 逐页粘贴：

1. **SEO Title** = `seo_title`（40–60 字符）— 不要用短 H1 当 SEO 标题
2. **Canonical** = `canonical_url`
3. **Meta Description** = `meta_description`（150–160）
4. **OG/Twitter** = CSV 中 `og_*` / `twitter_*`
5. **H2** = 粘贴 `body-cms.md`；卡片网格放在 `CARD_GRID` 注释处
6. **徽章** = `badge_label`（如 `13 GUIDES`），去掉 `06` / `14` 等编号

## 部署步骤

1. 打开 **`deploy-manifest.csv`**，按 `完整URL` 创建 **15 个新路由**（此前不存在）。
2. 每页装配（与博客详情页相同流水线）：
   - **H1** ← `pillar-landing-pages-master.json` 中该页的 `h1`（仅 1 个 H1）
   - **Subtitle** ← `subtitle`（可选副标题，非 H1）
   - **正文** ← 渲染 `body.md`（含 H2/H3；**不要**再渲染第二个 H1）
   - **`<head>`** ← 注入 `head.html`（含 canonical、description 150–160、og、twitter、JSON-LD）
   - **卡片列表** ← 读 `articles.json`；`is_hub: true` 的条目在 UI 上作为「Start here」推荐位
3. **面包屑**：Home / Blog / {{h1}}
4. **列表页 `/en/blog`**：为每个 pillar 增加入口链到对应落地页（slug 见 master JSON）。
5. **Sitemap**：用包内 **`sitemap.xml`** 整体替换线上 sitemap；或仅合并 **`sitemap-pillar-landings.xml`** 的 15 个 URL。
6. **UI**：不要显示 pillar 编号（如 `06`）；只显示 `{{article_count}} guides` 或类似文案。

## 页面清单

| landing_slug | H1 | 文章数 | Hub 长文 |
|---|---|---:|---|
"""
    for r in manifest_rows:
        readme += f"| `{r['landing_slug']}` | {r['h1']} | {r['article_count']} | `{r['hub_slug']}` |\n"

    readme += """
## 验收（每页）

```bash
curl -s "https://infinisynapse.com/en/blog/pillar/{landing_slug}" | grep -E 'canonical|og:title|application/ld\\+json'
```

- [ ] 仅 1 个 H1
- [ ] 至少 2 个 H2（Start here / All guides / FAQ）
- [ ] canonical 无尾斜杠
- [ ] meta description 150–160 字符
- [ ] og + twitter 齐全
- [ ] 卡片数与 `articles.json` 一致
- [ ] Hub 文章有「Start here」入口

## 与 Hub 长文的关系

- **落地页** = 主题索引（本包）
- **Hub 长文** = 深度总览（已在 `programmer-handoff-pack` / 线上 `/en/blog/{{hub_slug}}`）

两者互链：落地页正文已链到 Hub；Hub 文章内的 Cluster 表格链回各 Cluster 文。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    zip_path = OUT.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in OUT.rglob("*"):
            if path.is_file() and path != zip_path:
                zf.write(path, path.relative_to(OUT.parent))

    print(f"Wrote {len(master_pages)} landing pages -> {OUT}")
    print(f"Zip -> {zip_path}")
    print(f"Sitemap snippet -> {OUT / 'sitemap-pillar-landings.xml'}")


if __name__ == "__main__":
    main()
