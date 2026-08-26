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
    BLOG / "pillar9-semantic-layer",
    BLOG / "pillar10-mcp-data-access",
    BLOG / "pillar11-agentic-analytics",
    BLOG / "pillar12-data-trends",
    BLOG / "pillar13-data-privacy-security",
    BLOG / "pillar14-enterprise-data",
    BLOG / "pillar15-data-search",
    BLOG / "pillar16-vibe-coding-workflow",
    BLOG / "pillar17-vibe-coding-stack",
    BLOG / "pillar18-api-integration-vibe-built",
    BLOG / "pillar19-tool-calling-agent-workflows",
    BLOG / "pillar20-data-api-production-readiness",
]

# Hub pages per theme cluster (Pillar Page). P1 has multiple co-hubs.
PILLAR_PAGE_FOLDERS: dict[str, list[str]] = {
    "pillar1-ai-native-data-analysis": [
        "001-ai-for-data-analysis",
    ],
    "pillar2-data-agent-vs-alternatives": ["014-code-agent-vs-data-agent"],
    "pillar3-ai-analyst-tools": ["024-best-ai-tools-for-data-analysis"],
    "pillar4-data-source-connectors": ["044-connect-supabase-to-ai-data-analyst"],
    "pillar5-nl2sql-text-to-sql": ["059-natural-language-to-sql"],
    "pillar6-ai-excel-csv-spreadsheet": ["069-clean-excel-data-with-ai"],
    "pillar7-use-cases-role-industry": ["081-ai-tools-for-data-analysts"],
    "pillar8-skills-templates-glossary": ["100-data-agent-faq"],
    "pillar9-semantic-layer": ["120-semantic-layer"],
    "pillar10-mcp-data-access": ["127-mcp-for-data-analysis"],
    "pillar11-agentic-analytics": ["136-agentic-analytics"],
    "pillar12-data-trends": ["145-what-are-data-trends"],
    "pillar13-data-privacy-security": ["156-data-security-compliance"],
    "pillar14-enterprise-data": ["178-enterprise-data-security-solutions"],
    "pillar15-data-search": ["191-public-data"],
    "pillar16-vibe-coding-workflow": ["283-vibe-coding-best-practices"],
    "pillar17-vibe-coding-stack": ["263-vibe-coding-tools"],
    "pillar18-api-integration-vibe-built": ["203-api-integration-services"],
    "pillar19-tool-calling-agent-workflows": ["223-agentic-orchestration"],
    "pillar20-data-api-production-readiness": ["243-professional-data-api"],
}

PRIMARY_HUB: dict[str, str] = {k: v[0] for k, v in PILLAR_PAGE_FOLDERS.items()}

_BLOG_INDEX_TITLES: dict[str, str] | None = None


def slug_titles_from_index() -> dict[str, str]:
    global _BLOG_INDEX_TITLES
    if _BLOG_INDEX_TITLES is not None:
        return _BLOG_INDEX_TITLES
    titles: dict[str, str] = {}
    index_path = BLOG / "blog-index-import-master.json"
    if index_path.is_file():
        for post in json.loads(index_path.read_text(encoding="utf-8")).get("posts", []):
            slug = post.get("slug", "")
            title = post.get("title", "")
            if slug and title:
                titles[slug] = title
    _BLOG_INDEX_TITLES = titles
    return titles


def strip_deploy_id(text: str) -> str:
    """Remove leading deployment folder id (e.g. '002 ') from display titles."""
    return re.sub(r"^\d{3}\s+", "", text.strip())


def folder_fallback_title(folder: str) -> str:
    m = re.match(r"\d{3}-(.+)", folder)
    base = m.group(1) if m else folder
    return base.replace("-", " ").title()


def article_title(
    article_md: Path,
    slug: str = "",
    registry_title: str | None = None,
) -> str:
    if registry_title:
        return strip_deploy_id(registry_title)
    index_titles = slug_titles_from_index()
    if slug and slug in index_titles:
        return index_titles[slug]
    for line in article_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return strip_deploy_id(line[2:].strip())
    return folder_fallback_title(article_md.parent.name)


def slug_from_folder(folder: str) -> str:
    m = re.match(r"\d{3}-(.+)", folder)
    return m.group(1) if m else folder


def load_cluster(pillar_dir: Path) -> dict:
    registry_path = pillar_dir / "articles_registry.json"
    registry_folders: dict[str, dict] = {}
    if registry_path.is_file():
        for art in json.loads(registry_path.read_text(encoding="utf-8")).get("articles", []):
            folder = art["folder"]
            registry_folders[folder] = {
                "slug": art["slug"],
                "title": art.get("title") or folder.replace("-", " ").title(),
            }

    published_folders = sorted(
        d.name
        for d in pillar_dir.iterdir()
        if re.match(r"\d{3}-", d.name) and d.is_dir() and (d / "article.md").is_file()
    )
    planned_sibling_slugs = {info["slug"] for info in registry_folders.values()}
    pillar_pages = PILLAR_PAGE_FOLDERS.get(
        pillar_dir.name, [published_folders[0]] if published_folders else []
    )
    articles: dict[str, dict] = {}
    for folder in published_folders:
        md = pillar_dir / folder / "article.md"
        slug = registry_folders.get(folder, {}).get("slug") or slug_from_folder(folder)
        reg_title = registry_folders.get(folder, {}).get("title")
        articles[folder] = {
            "slug": slug,
            "url": f"/blog/{slug}",
            "title": article_title(md, slug=slug, registry_title=reg_title),
            "is_pillar_page": folder in pillar_pages,
            "is_cluster_page": folder not in pillar_pages,
        }
        planned_sibling_slugs.add(slug)
    return {
        "pillar_dir": pillar_dir.name,
        "folders": published_folders,
        "planned_sibling_slugs": planned_sibling_slugs,
        "pillar_pages": pillar_pages,
        "primary_hub": PRIMARY_HUB.get(pillar_dir.name, published_folders[0] if published_folders else ""),
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
        # Cluster page must link back to the primary hub. The ">=2 sibling links"
        # requirement is enforced flexibly by audit-internal-links.py (any 2 siblings),
        # so we do NOT mandate specific siblings here (that was brittle and broke
        # whenever cluster membership changed).
        hub = cluster["primary_hub"]
        ha = arts[hub]
        reqs.append((ha["title"], ha["url"]))
    return reqs
