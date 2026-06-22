#!/usr/bin/env python3
"""Generate a COMPLETE sitemap.xml = existing site URLs + 100 new blog pages.

Existing non-blog URLs (use-cases/*, guides/*) are preserved verbatim from the live
sitemap. The 100 new English blog pages (https://infinisynapse.com/en/blog/{slug})
are appended from seo-meta.json with lastmod from schema dateModified.
Deployable as a full replacement for https://infinisynapse.com/sitemap.xml.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

BLOG = Path(__file__).parent
OUT = BLOG / "sitemap.xml"

# Existing live URLs (from https://infinisynapse.com/sitemap.xml) — preserved verbatim.
EXISTING: list[tuple[str, str, str, str]] = [
    ("https://infinisynapse.com/use-cases/best-ai-tools-for-data-analysis", "2026-05-11", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/best-data-analysis-software", "2026-05-11", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/data-analysis-techniques", "2026-05-11", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/how-to-add-data-analysis-in-excel", "2026-05-11", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/sql-data-analysis-with-ai", "2026-05-11", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/nl2sql", "2026-05-20", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/infinisynapse-vs-vanna-ai", "2026-05-20", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/infinisynapse-vs-text2sql", "2026-05-20", "monthly", "0.8"),
    ("https://infinisynapse.com/use-cases/best-nl2sql-tools-2026", "2026-05-20", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/what-is-agentic-analytics", "2026-05-21", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/what-is-agentic-data-analysis", "2026-05-20", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/rag-data-analysis", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/breaking-data-silos", "2026-05-21", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/sql-data-analysis-with-ai", "2026-05-25", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/agentic-analytics-vs-traditional-bi", "2026-05-21", "monthly", "0.9"),
    ("https://infinisynapse.com/guides/chatbi-vs-agentic-analytics", "2026-05-21", "monthly", "0.9"),
    ("https://infinisynapse.com/guides/chatbi-alternative", "2026-05-21", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/nlp2sql-alternative", "2026-05-21", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/text-to-sql-alternative", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/bi-chatbot-alternative", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/tableau-ai-alternative", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/power-bi-copilot-alternative", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/looker-alternative", "2026-05-22", "monthly", "0.8"),
    ("https://infinisynapse.com/guides/thoughtspot-alternative", "2026-05-22", "monthly", "0.8"),
]

# Blog list page (hub for all new articles)
BLOG_INDEX = ("https://infinisynapse.com/en/blog", "weekly", "0.9")

# Hubs / pillar entries get higher priority
HUB_SLUGS = {
    "ai-for-data-analysis", "ai-data-analysis", "ai-data-analyst", "ai-native-data-platform",
    "best-ai-tools-for-data-analysis", "connect-supabase-to-ai-data-analyst",
    "natural-language-to-sql", "clean-excel-data-with-ai", "ai-tools-for-data-analysts",
    "data-agent-faq",
}


def to_date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).date().isoformat()
    except (ValueError, AttributeError):
        return datetime.now().date().isoformat()


def lastmod_of(article: dict) -> str:
    for item in article.get("jsonld", []):
        if item.get("@type") == "BlogPosting" and item.get("dateModified"):
            return to_date(item["dateModified"])
    mt = article.get("article", {}).get("modified_time") or article.get("article", {}).get("published_time")
    return to_date(mt) if mt else datetime.now().date().isoformat()


def url_block(loc: str, lastmod: str, changefreq: str, priority: str) -> list[str]:
    return [
        "  <url>",
        f"    <loc>{escape(loc)}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
        f"    <changefreq>{changefreq}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ]


def main() -> None:
    data = json.loads((BLOG / "seo-meta.json").read_text(encoding="utf-8"))
    arts = data["articles"]
    today = datetime.now().date().isoformat()

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    # 1. existing site URLs (verbatim)
    for loc, lastmod, cf, prio in EXISTING:
        lines += url_block(loc, lastmod, cf, prio)

    # 2. blog list hub
    lines += url_block(BLOG_INDEX[0], today, BLOG_INDEX[1], BLOG_INDEX[2])

    # 3. 100 new blog articles
    for a in arts:
        loc = a.get("canonical") or a.get("url")
        slug = a.get("slug", "")
        prio = "0.9" if slug in HUB_SLUGS else "0.7"
        lines += url_block(loc, lastmod_of(a), "weekly", prio)

    lines.append("</urlset>")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    total = len(EXISTING) + 1 + len(arts)
    print(f"Wrote {total} URLs -> {OUT}")
    print(f"  existing: {len(EXISTING)}  blog-index: 1  new blog: {len(arts)}")


if __name__ == "__main__":
    main()
