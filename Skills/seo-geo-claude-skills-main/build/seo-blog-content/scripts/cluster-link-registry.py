#!/usr/bin/env python3
"""Theme-cluster internal link registry for 90-article pillar batches."""
from __future__ import annotations

import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"

PILLAR_DIRS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

# Hub pages per theme cluster (Pillar Page). P1 has multiple co-hubs.
PILLAR_PAGE_FOLDERS: dict[str, list[str]] = {
    "pillar1-ai-native-data-analysis": [
        "001-ai-for-data-analysis",
        "004-ai-native-data-platform",
        "007-ai-data-analyst",
        "012-ai-data-analysis",
    ],
    "pillar2-data-agent-vs-alternatives": ["014-code-agent-vs-data-agent"],
    "pillar3-ai-analyst-tools": ["024-best-ai-tools-for-data-analysis"],
    "pillar4-data-source-connectors": ["044-connect-supabase-to-ai-data-analyst"],
    "pillar5-nl2sql-text-to-sql": ["059-natural-language-to-sql"],
    "pillar6-ai-excel-csv-spreadsheet": ["069-clean-excel-data-with-ai"],
    "pillar7-use-cases-role-industry": ["081-ai-tools-for-data-analysts"],
    "pillar8-skills-templates-glossary": ["100-data-agent-faq"],
}

PRIMARY_HUB: dict[str, str] = {k: v[0] for k, v in PILLAR_PAGE_FOLDERS.items()}


def article_title(article_md: Path) -> str:
    for line in article_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return article_md.parent.name.replace("-", " ").title()


def slug_from_folder(folder: str) -> str:
    m = re.match(r"\d{3}-(.+)", folder)
    return m.group(1) if m else folder


def load_cluster(pillar_dir: Path) -> dict:
    folders = sorted(
        p.parent.name
        for p in pillar_dir.glob("[0-9][0-9][0-9]-*/article.md")
    )
    pillar_pages = PILLAR_PAGE_FOLDERS.get(pillar_dir.name, [folders[0]] if folders else [])
    articles: dict[str, dict] = {}
    for folder in folders:
        md = pillar_dir / folder / "article.md"
        slug = slug_from_folder(folder)
        articles[folder] = {
            "slug": slug,
            "url": f"/blog/{slug}",
            "title": article_title(md),
            "is_pillar_page": folder in pillar_pages,
            "is_cluster_page": folder not in pillar_pages,
        }
    return {
        "pillar_dir": pillar_dir.name,
        "folders": folders,
        "pillar_pages": pillar_pages,
        "primary_hub": PRIMARY_HUB.get(pillar_dir.name, folders[0] if folders else ""),
        "articles": articles,
    }


def all_clusters() -> dict[str, dict]:
    return {d.name: load_cluster(d) for d in PILLAR_DIRS if d.is_dir()}


def page_role(folder: str, cluster: dict) -> str:
    if folder in cluster["pillar_pages"]:
        return "pillar_page"
    return "cluster_page"


def required_internal_urls(folder: str, cluster: dict) -> list[tuple[str, str]]:
    """Return list of (title, /blog/slug) required in body prose."""
    role = page_role(folder, cluster)
    arts = cluster["articles"]
    reqs: list[tuple[str, str]] = []

    if role == "pillar_page":
        # All other Pillar Pages in this theme cluster
        for pf in cluster["pillar_pages"]:
            if pf == folder:
                continue
            a = arts[pf]
            reqs.append((a["title"], a["url"]))
        # Single-hub clusters: also surface every cluster sibling from the hub
        if len(cluster["pillar_pages"]) == 1:
            for cf, a in arts.items():
                if cf == folder:
                    continue
                reqs.append((a["title"], a["url"]))
    else:
        hub = cluster["primary_hub"]
        ha = arts[hub]
        reqs.append((ha["title"], ha["url"]))
        siblings = [
            (a["title"], a["url"])
            for cf, a in arts.items()
            if cf != folder and cf not in cluster["pillar_pages"]
        ]
        # Exactly two sibling cluster pages (minimum); pick deterministically by folder hash
        idx = sum(ord(c) for c in folder) % max(1, len(siblings))
        picks: list[tuple[str, str]] = []
        for j in range(min(2, len(siblings))):
            pick = siblings[(idx + j) % len(siblings)]
            if pick not in picks:
                picks.append(pick)
        reqs.extend(picks)
    return reqs
