#!/usr/bin/env python3
"""Generate all Vibe Coding SEO articles (203-299) from blog-vibe-coding-topics-plan.csv."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from datetime import datetime
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PLAN = BLOG / "blog-vibe-coding-topics-plan.csv"
SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_hdr)
HIGH_DR = _hdr.HIGH_DR_SOURCES

HUB_SLUGS = {
    "pillar18-api-integration-vibe-built": "api-integration-services",
    "pillar19-tool-calling-agent-workflows": "agentic-orchestration",
    "pillar20-data-api-production-readiness": "professional-data-api",
    "pillar17-vibe-coding-stack": "vibe-coding-tools",
    "pillar16-vibe-coding-workflow": "vibe-coding-best-practices",
}

PILLAR_BRIDGE = {
    "pillar18-api-integration-vibe-built": (
        "As integrations multiply, stable API infrastructure, structured auth, and maintainable orchestration "
        "become the real product need—not more prompts."
    ),
    "pillar19-tool-calling-agent-workflows": (
        "Tool calling only becomes reliable when the API layer, auth model, data model, and execution system "
        "underneath are stable."
    ),
    "pillar20-data-api-production-readiness": (
        "This is where the product stops being a demo and becomes dependable infrastructure buyers can trust."
    ),
    "pillar17-vibe-coding-stack": (
        "Every app builder helps you prototype fast; the bottleneck appears when you need secure data access, "
        "external systems, or agent actions."
    ),
    "pillar16-vibe-coding-workflow": (
        "As soon as the workflow touches external systems, you need API governance, data access control, "
        "and production checks."
    ),
}

INFINI_LINKS = [
    ("/en/blog/what-is-a-data-agent", "What Is a Data Agent"),
    ("/en/blog/api-integration-tools-reddit", "API integration tools for vibe-coded apps"),
    ("/en/blog/tool-calling-reddit", "tool calling in production"),
    ("/en/blog/production-readiness-reddit-checklist", "production readiness checklist"),
    ("/en/blog/cursor-ai-for-vibe-coding-reddit", "Cursor AI for vibe coding"),
]


def load_plan() -> list[dict]:
    with PLAN.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def group_by_pillar(rows: list[dict]) -> dict[str, list[dict]]:
    g: dict[str, list[dict]] = {}
    for r in rows:
        g.setdefault(r["pillar_folder"], []).append(r)
    return g


def pick_links(article_idx: int, n: int = 8) -> list[dict]:
    out = []
    used = set()
    for i in range(n):
        j = (article_idx * 7 + i * 11) % len(HIGH_DR)
        src = HIGH_DR[j]
        if src["url"] in used:
            j = (j + 13) % len(HIGH_DR)
            src = HIGH_DR[j]
        used.add(src["url"])
        weave = src["weave"].format(url=src["url"])
        out.append({"weave": weave, "url": src["url"]})
    return out


def kw_bounds(kw: str) -> tuple[int, int]:
    n = len(kw.split())
    if n <= 3:
        return (14, 22)
    if n <= 5:
        return (8, 14)
    return (5, 10)


def meta_desc(keyword: str, slug: str, is_hub: bool) -> str:
    templates = [
        f"{keyword.title() if len(keyword) < 40 else keyword}: guide for vibe-coded teams—architecture, scorecard, and InfiniSynapse API patterns. FAQ.",
        f"Learn {keyword} for AI-built products: compare approaches, avoid backend chaos, and connect InfiniSynapse Server API. See FAQ.",
        f"{keyword} in 2026: practical guide for builders moving from prototype to production API and data infrastructure.",
    ]
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    desc = templates[h % len(templates)]
    if len(desc) < 150:
        desc = desc + " Covers governance, testing, and rollout."
    if len(desc) > 160:
        desc = desc[:157] + "..."
    if keyword.lower() not in desc.lower():
        desc = f"{keyword}: " + desc
        if len(desc) > 160:
            desc = desc[:157] + "..."
    return desc


def sibling_links(pillar_rows: list[dict], current_slug: str, hub_slug: str) -> list[tuple[str, str]]:
    links = []
    for r in pillar_rows:
        if r["slug"] == current_slug:
            continue
        if r["slug"] == hub_slug:
            links.insert(0, (f"/en/blog/{hub_slug}", r["title"]))
        else:
            links.append((f"/en/blog/{r['slug']}", r["title"]))
    return links[:4]


def paragraph(keyword: str, topic: str, variant: int) -> str:
    k = f"**{keyword}**"
    bodies = [
        f"{k} matters most when a vibe-coded UI already looks finished but nothing behind it can survive real traffic, real credentials, or real latency profiles.",
        f"Teams researching {k} usually discover the gap after the first Stripe webhook, OAuth redirect, or six-minute agent job—not during the initial Cursor session.",
        f"A practical {k} rollout separates synchronous UI calls from async data work, keeps secrets off the client, and validates every vendor payload before it touches business logic.",
        f"Buyers evaluating {k} should score auth hygiene, schema validation, observability, and async routing before comparing feature checklists.",
        f"{k.title() if len(keyword) < 30 else keyword} fails in production when builders treat integration as a single `fetch()` instead of a managed layer with retries and audit trails.",
        f"InfiniSynapse Server API fits {k} scenarios that need multi-step analysis, workspace artifacts, and SSE progress—without standing up queues and sandboxes yourself.",
    ]
    return bodies[variant % len(bodies)]


def build_faq(keyword: str, is_hub: bool) -> list[tuple[str, str]]:
    q = keyword
    return [
        (
            "Definition and scope",
            f"{q.title() if len(q) < 40 else q} is the production layer that connects vibe-coded frontends to external APIs, data systems, and agent backends with auth, retries, and observability—not a one-off script.",
        ),
        (
            "When teams should prioritize it",
            f"You need {q} the moment a prototype touches customer data, payments, or long-running jobs. Before that, a thin proxy and environment-scoped keys may be enough.",
        ),
        (
            "How InfiniSynapse fits",
            f"InfiniSynapse Server API handles data-agent workloads—SSE tasks, workspace downloads, federated queries—so your {q} stack can route heavy analysis to managed infrastructure instead of stretching serverless timeouts.",
        ),
        (
            "First improvement step",
            f"Inventory external dependencies, classify sync vs async calls, and move API keys into a secret store before adding features. Most {q} incidents trace back to skipping that sequence.",
        ),
        (
            "Typical rollout timeline",
            f"A focused {q} pilot—one workflow, contract tests, structured logging—typically takes one to two weeks for a small team. Full production hardening adds review gates and monitoring.",
        ),
    ]


def build_article(row: dict, pillar_rows: list[dict], article_idx: int, is_hub: bool) -> str:
    kw = row["关键词"]
    title = row["title"]
    slug = row["slug"]
    pillar = row["pillar_folder"]
    hub_slug = HUB_SLUGS[pillar]
    links = pick_links(article_idx)
    sibs = sibling_links(pillar_rows, slug, hub_slug)
    lo, hi = kw_bounds(kw)
    target_kw_count = lo + (article_idx % (hi - lo + 1))

    lines = [
        f"# {title}",
        "",
        "> **By the InfiniSynapse Data Team** · **Last updated: 2026-06-23** · "
        "*We build InfiniSynapse and document production patterns for vibe-coded products moving to real APIs and data infrastructure.*",
        "",
        f"![Hero image for {slug}](./images/hero-{slug}.png)",
        "",
        f"**Meta Description**: {meta_desc(kw, slug, is_hub)}",
        "",
        f"**Slug**: `/blog/{slug}`",
        "",
        f"**Target keyword**: `{kw}`",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
        "1. [TL;DR](#tldr)",
        "2. [Key Definition](#key-definition)",
        "3. [Why This Matters for Vibe-Coded Products](#why-this-matters-for-vibe-coded-products)",
        "4. [Core Framework](#core-framework)",
        "5. [Comparison and Options](#comparison-and-options)",
        "6. [Implementation Workflow](#implementation-workflow)",
        "7. [InfiniSynapse Connection](#infinisynapse-connection)",
        "8. [Scorecard](#scorecard)",
        "9. [Failure Modes](#failure-modes)",
        "10. [FAQ](#frequently-asked-questions)",
        "11. [Conclusion](#conclusion)",
        "",
        "---",
        "",
        "## TL;DR",
        "",
        f"> **{kw}** is a production concern for every team that vibe-coded a UI before wiring auth, data, payments, or agent backends.",
        "",
        f"**Who this is for**: founders and builders using Cursor, Replit, v0, or Claude Code who now need dependable integrations. "
        f"**What you'll learn**: definition, comparison table, rollout steps, scorecard, and how InfiniSynapse Server API fits long-running data workflows.",
        "",
        f"For pillar context see [{hub_slug.replace('-', ' ').title()}](/en/blog/{hub_slug}).",
        "",
        "---",
        "",
        "## Key Definition",
        "",
        f"> **Key Definition**: **{kw}** describes how AI-built products connect to external capabilities—APIs, databases, payment rails, and agent runtimes—with governance appropriate for real users, not demo traffic.",
        "",
        paragraph(kw, title, 0),
        "",
        links[0]["weave"],
        "",
        "---",
        "",
        "## Why This Matters for Vibe-Coded Products",
        "",
        "### The prototype-to-product cliff",
        "",
        paragraph(kw, title, 1),
        "",
        PILLAR_BRIDGE[pillar],
        "",
        "### What breaks first in production",
        "",
        "| Signal | Demo behavior | Production expectation |",
        "|--------|---------------|------------------------|",
        "| Auth | Key in `.env.local` | Secret manager + scoped tokens |",
        "| Latency | Blocking UI thread | Async jobs + progress UI |",
        "| Errors | Console log | Structured codes + alerts |",
        "| Data | Mock JSON | Validated vendor schemas |",
        "| Agents | Single prompt | Tool calling + audit trail |",
        "",
        links[1]["weave"],
        "",
        f"Compare integration patterns in [{sibs[1][1] if len(sibs) > 1 else 'related guide'}]({sibs[1][0] if len(sibs) > 1 else f'/en/blog/{hub_slug}'}).",
        "",
        "---",
        "",
        "## Core Framework",
        "",
        f"A mature **{kw}** stack decomposes into five layers builders can implement incrementally:",
        "",
        "### Layer 1: Discovery and inventory",
        "",
        paragraph(kw, title, 2),
        "",
        "### Layer 2: Transport and protocol choice",
        "",
        "Classify each dependency as REST, webhook, SSE, or batch. Anything over five seconds belongs off the request thread from day one.",
        "",
        "### Layer 3: Auth and secret management",
        "",
        paragraph(kw, title, 3),
        "",
        links[2]["weave"],
        "",
        "### Layer 4: Orchestration and transformation",
        "",
        "Map vendor payloads to typed internal models before they reach UI components or agent prompts.",
        "",
        "### Layer 5: Observability and review",
        "",
        paragraph(kw, title, 4),
        "",
        "---",
        "",
        "## Comparison and Options",
        "",
        f"When evaluating **{kw}**, teams usually choose among four patterns:",
        "",
        "| Pattern | Best for | Limit at scale |",
        "|---------|----------|----------------|",
        "| Hand-rolled clients | Unique APIs | Retry/observability debt |",
        "| iPaaS (Zapier/Make) | Simple triggers | Complex auth + long jobs |",
        "| API gateway | Multi-service teams | Ops overhead for solo builders |",
        "| Data agent backend | Analysis + files + PDFs | Requires proxy discipline |",
        "",
        links[3]["weave"],
        "",
        f"See also [{INFINI_LINKS[article_idx % len(INFINI_LINKS)][1]}]({INFINI_LINKS[article_idx % len(INFINI_LINKS)][0]}).",
        "",
        "---",
        "",
        "## Implementation Workflow",
        "",
        f"Roll out **{kw}** in this order to avoid rebuilding after the first outage:",
        "",
        "**Step 1 — Inventory**",
        "",
        "List every external system, its auth model, rate limits, and expected latency.",
        "",
        "**Step 2 — Classify sync vs async**",
        "",
        paragraph(kw, title, 5),
        "",
        "**Step 3 — Proxy and secrets**",
        "",
        "Never expose vendor keys in the browser. Route calls through your backend with structured error shapes.",
        "",
        "**Step 4 — Contract tests**",
        "",
        "Validate schemas on every boundary; treat drift as a hard failure with alerts.",
        "",
        links[4]["weave"],
        "",
        "**Step 5 — Production monitoring**",
        "",
        "Log provider, endpoint, status, and latency per call before you invite beta users.",
        "",
        "---",
        "",
        "## InfiniSynapse Connection",
        "",
        "InfiniSynapse targets vibe-coded products that need **data agent** capabilities behind a thin UI:",
        "",
        "- **Server API**: SSE subscription, `newTask`, workspace artifact download",
        "- **InfiniSQL + InfiniRAG**: federated queries and business definitions bound to sources",
        "- **Multi-entry parity**: web app, API, and CLI (`agent_infini`) for the same task timeline",
        "",
        paragraph(kw, title, article_idx % 6),
        "",
        f"For hands-on integration patterns, read [{sibs[0][1]}]({sibs[0][0]}) and [{sibs[2][1] if len(sibs) > 2 else 'API integration tools'}]({sibs[2][0] if len(sibs) > 2 else '/en/blog/api-integration-tools-reddit'}).",
        "",
        links[5]["weave"],
        "",
        "---",
        "",
        "## Scorecard",
        "",
        f"Rate your **{kw}** readiness before public launch (1 point each):",
        "",
        "| Check | Pass? |",
        "|-------|-------|",
        "| Secrets not in git | |",
        "| Async routing for long jobs | |",
        "| Schema validation on responses | |",
        "| Retries with backoff on outbound calls | |",
        "| Structured logging per external provider | |",
        "| Contract or integration tests in CI | |",
        "| User-safe error messages (no raw vendor dumps) | |",
        "| Rate-limit handling tested | |",
        "",
        "**8+**: production-ready for beta. **5–7**: closed pilot only. **Below 5**: demo stage.",
        "",
        "---",
        "",
        "## Failure Modes",
        "",
        "### Failure 1: Synchronous everything",
        "",
        f"Blocking the UI on **{kw}** calls that exceed serverless timeouts is the most common vibe-coding regression.",
        "",
        "### Failure 2: Key sprawl",
        "",
        "Multiple copies of the same API key across laptops, CI, and hosting panels make rotation impossible.",
        "",
        "### Failure 3: Untested auth failures",
        "",
        links[6]["weave"],
        "",
        "### Failure 4: Building infra instead of product",
        "",
        "Custom task queues and sandboxes consume weeks that a data-agent API or workflow engine could absorb.",
        "",
        "---",
        "",
    ]

    if is_hub:
        lines.extend([
            "## Cluster Guides in This Pillar",
            "",
            "| Slug | Topic |",
            "|------|-------|",
        ])
        for r in pillar_rows[:12]:
            if r["slug"] != slug:
                lines.append(f"| `/en/blog/{r['slug']}` | {r['title'][:60]} |")
        lines.extend(["", "---", ""])

    lines.extend(["## Frequently Asked Questions", ""])
    for q, a in build_faq(kw, is_hub):
        lines.extend([f"### {q}", "", a, ""])

    lines.extend([
        "",
        "---",
        "",
        "## Conclusion",
        "",
        f"**{kw.title() if len(kw) < 36 else kw}** is how vibe-coded products earn trust after the UI demo ends.",
        "",
        paragraph(kw, title, (article_idx + 3) % 6),
        "",
        "Priority order: secrets first, async second, validation third, observability fourth, then route data-heavy work to the right backend.",
        "",
        f"Explore the pillar hub at [/en/blog/{hub_slug}](/en/blog/{hub_slug}) and ship the next integration deliberately—not as an afterthought.",
        "",
    ])

    text = "\n".join(lines)
    # Boost keyword density if needed
    body_start = text.find("## TL;DR")
    body = text[body_start:]
    count = len(re.findall(re.escape(kw.lower()), body.lower()))
    while count < target_kw_count:
        insert = f"\n\nTeams shipping **{kw}** should treat observability and contract tests as part of the feature—not a post-launch chore.\n"
        text = text.replace("\n## Conclusion\n", insert + "\n## Conclusion\n", 1)
        body = text[body_start:]
        count = len(re.findall(re.escape(kw.lower()), body.lower()))
        if count >= target_kw_count:
            break
        target_kw_count -= 1  # safety

    return text


def build_meta_tags(row: dict, desc: str) -> str:
    slug = row["slug"]
    title = row["title"]
    kw = row["关键词"]
    url = f"https://infinisynapse.com/en/blog/{slug}"
    img = f"https://infinisynapse.com/en/blog/{row['pillar_folder']}/{row['编号']}-{slug}/images/hero-{slug}.png"
    section = row["Pillar主题"].split("·")[-1].strip()
    return f"""<!--
  Meta Tags Package
  Page: {title}
  Generated: 2026-06-23
  Target keyword: {kw}
-->

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">

<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="InfiniSynapse Data Team">
<meta http-equiv="content-language" content="en">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="https://infinisynapse.com/zh/blog/{slug}">
<link rel="alternate" hreflang="x-default" href="{url}">

<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{title}">
<meta property="og:site_name" content="InfiniSynapse Blog">
<meta property="og:locale" content="en_US">

<meta property="article:published_time" content="2026-06-24T10:00:00+08:00">
<meta property="article:modified_time" content="2026-06-24T10:00:00+08:00">
<meta property="article:author" content="https://infinisynapse.com/about">
<meta property="article:section" content="{section}">
<meta property="article:tag" content="{kw}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@InfiniSynapse">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
"""


def build_schema(row: dict, desc: str, faqs: list[tuple[str, str]]) -> str:
    slug = row["slug"]
    title = row["title"]
    kw = row["关键词"]
    url = f"https://infinisynapse.com/en/blog/{slug}"
    img = f"https://infinisynapse.com/en/blog/{row['pillar_folder']}/{row['编号']}-{slug}/images/hero-{slug}.png"
    faq_entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faqs[:5]
    ]
    data = [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": desc,
            "image": [img],
            "datePublished": "2026-06-24T10:00:00+08:00",
            "dateModified": "2026-06-24T10:00:00+08:00",
            "author": {
                "@type": "Organization",
                "name": "InfiniSynapse Data Team",
                "url": "https://infinisynapse.com/en/about",
            },
            "publisher": {
                "@type": "Organization",
                "name": "InfiniSynapse",
                "logo": {"@type": "ImageObject", "url": "https://infinisynapse.com/logo.png"},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "about": [{"@type": "Thing", "name": kw}],
            "keywords": kw,
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities,
        },
    ]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


SKIP_EXISTING = {
    "203-api-integration-services",
    "204-integration-software",
    "206-api-integration-tools",
    "218-manage-multiple-api-integrations",
    "221-api-integration-testing",
    "223-agentic-orchestration",
    "224-tool-calling",
}


def existing_word_count(path: Path) -> int:
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    t = re.sub(r"^#+\s+", "", body, flags=re.M)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))


def main() -> int:
    rows = load_plan()
    by_pillar = group_by_pillar(rows)
    written = skipped = 0
    for idx, row in enumerate(rows):
        adir = BLOG / row["pillar_folder"] / f"{row['编号']}-{row['slug']}"
        adir.mkdir(parents=True, exist_ok=True)
        (adir / "images").mkdir(exist_ok=True)
        art_path = adir / "article.md"
        folder = f"{row['编号']}-{row['slug']}"
        if folder in SKIP_EXISTING:
            skipped += 1
            continue
        is_hub = "Hub" in row.get("备注", "")
        pillar_rows = by_pillar[row["pillar_folder"]]
        md = build_article(row, pillar_rows, idx, is_hub)
        desc = meta_desc(row["关键词"], row["slug"], is_hub)
        # sync meta in md
        md = re.sub(
            r"\*\*Meta Description\*\*:.*",
            f"**Meta Description**: {desc}",
            md,
            count=1,
        )
        faqs = build_faq(row["关键词"], is_hub)
        art_path.write_text(md, encoding="utf-8")
        (adir / "meta-tags.html").write_text(build_meta_tags(row, desc), encoding="utf-8")
        (adir / "schema.json").write_text(build_schema(row, desc, faqs), encoding="utf-8")
        written += 1
        print(f"WROTE {row['编号']}-{row['slug']}")
    print(f"\nDone: wrote {written}, skipped {skipped} (already complete)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
