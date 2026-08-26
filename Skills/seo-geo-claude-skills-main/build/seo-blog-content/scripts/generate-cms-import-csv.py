#!/usr/bin/env python3
"""Generate blog-cms-import-100.csv: slug, type, card_tag, UI module hints for frontend."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar*"))
PILLARS = [
    p
    for p in PILLARS
    if p.is_dir() and re.match(r"pillar\d+", p.name) and " copy" not in p.name
]

# Pillar 1 slug → (content_type, card_tag, filter_category, ui_module) overrides
PILLAR1_MAP = {
    "ai-for-data-analysis": ("guide", "Guides", "knowledge", "long-form-guide"),
    "data-agent-manifesto": ("manifesto", "Deep Dive", "deep_dive", "long-form-guide"),
    "what-is-a-data-agent": ("what-is", "Guides", "knowledge", "definition-box"),
    "ai-native-data-platform": ("buyer-guide", "Guides", "knowledge", "long-form-guide"),
    "best-agentic-analytics": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
    "autonomous-data-agent": ("what-is", "Guides", "knowledge", "definition-box"),
    "ai-data-analyst": ("role-guide", "Guides", "knowledge", "long-form-guide"),
    "ai-data-analyst-job-description": ("job-template", "Guides", "knowledge", "copy-block"),
    "data-agent-memory": ("deep-dive", "Deep Dive", "deep_dive", "long-form-guide"),
    "fabric-data-agent-vs-copilot": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "ai-native-vs-augmented-analytics": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "ai-data-analysis": ("guide", "Guides", "knowledge", "long-form-guide"),
    "data-agent-glossary": ("glossary", "Guides", "knowledge", "glossary-terms"),
}

# Pillar 3 slug overrides (from INDEX + blog-index-import)
PILLAR3_MAP = {
    "self-hosted-ai-data-analyst": ("deployment-guide", "Deep Dive", "deep_dive", "how-to-steps"),
    "chatgpt-data-analysis-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "julius-ai-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "thoughtspot-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "databricks-genie-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "tableau-pulse-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "perplexity-data-analysis-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "code-interpreter-alternatives": ("alternatives", "Comparisons", "comparisons", "alternatives-matrix"),
    "infinisynapse-vs-julius-ai": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "infinisynapse-vs-chatgpt": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "infinisynapse-vs-databricks-genie": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "julius-ai-vs-chatgpt": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "thoughtspot-vs-databricks-genie": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "infinisynapse-vs-tableau": ("versus", "Comparisons", "comparisons", "versus-scorecard"),
    "infinisynapse-review": ("review", "Tools & Reviews", "tools_reviews", "product-review"),
    "best-ai-tools-for-data-analysis": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
    "ai-data-analysis-tools": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
    "sql-data-analysis-tools": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
    "ai-excel-data-analysis-tools": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
    "ai-data-visualization-tools": ("listicle", "Tools & Reviews", "tools_reviews", "tool-listicle"),
}

# Pillar 8 slug overrides
PILLAR8_MAP = {
    "how-to-evaluate-ai-data-analyst": ("guide", "Tools & Reviews", "tools_reviews", "long-form-guide"),
}

# Pillar 4–7, 9–15 → blog nav filter (see blog-nav-tags.csv)
PILLAR_CATEGORY: dict[int, tuple[str, str]] = {
    4: ("Connectors", "connectors"),
    5: ("NL2SQL", "nl2sql"),
    6: ("Excel & CSV", "excel_csv"),
    7: ("Use Cases", "use_cases"),
    9: ("Guides", "knowledge"),
    10: ("Connectors", "connectors"),
    11: ("Tools & Reviews", "tools_reviews"),
    12: ("Guides", "knowledge"),
    13: ("Deep Dive", "deep_dive"),
    14: ("Guides", "knowledge"),
    15: ("Guides", "knowledge"),
}

TYPE_DEFAULTS: dict[str, tuple[str, str, str]] = {
    "versus": ("Comparisons", "comparisons", "versus-scorecard"),
    "comparison": ("Comparisons", "comparisons", "versus-scorecard"),
    "listicle": ("Tools & Reviews", "tools_reviews", "tool-listicle"),
    "alternatives": ("Comparisons", "comparisons", "alternatives-matrix"),
    "how-to": ("Tutorials", "tutorials", "how-to-steps"),
    "guide": ("Guides", "knowledge", "long-form-guide"),
    "use-case": ("Use Cases", "use_cases", "use-case-persona"),
    "glossary": ("Guides", "knowledge", "glossary-terms"),
    "faq": ("Guides", "knowledge", "faq-hub"),
    "resource": ("Guides", "knowledge", "prompt-resource"),
    "review": ("Tools & Reviews", "tools_reviews", "product-review"),
    "manifesto": ("Deep Dive", "deep_dive", "long-form-guide"),
    "what-is": ("Guides", "knowledge", "definition-box"),
    "buyer-guide": ("Guides", "knowledge", "long-form-guide"),
    "role-guide": ("Guides", "knowledge", "long-form-guide"),
    "job-template": ("Guides", "knowledge", "copy-block"),
    "deep-dive": ("Deep Dive", "deep_dive", "long-form-guide"),
    "deployment-guide": ("Deep Dive", "deep_dive", "how-to-steps"),
}


def read_type_from_readme(art_dir: Path) -> str | None:
    readme = art_dir / "README.md"
    if not readme.is_file():
        return None
    m = re.search(r"\*\*Type\*\*:\s*(.+)", readme.read_text(encoding="utf-8"))
    if not m:
        return None
    return m.group(1).strip().lower().replace(" ", "-").replace("sql-focused-", "").replace(
        "excel-focused-", ""
    ).replace("visualization-focused-", "")


def read_slug(art_dir: Path) -> str:
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Slug\*\*:\s*`([^`]+)`", text)
    if m:
        # slug is the last path segment; tolerate /blog/, /en/blog/ prefixes
        return m.group(1).strip("/").split("/")[-1]
    return art_dir.name.split("-", 1)[1] if "-" in art_dir.name else art_dir.name


def read_keyword(art_dir: Path) -> str:
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1) if m else ""


def read_meta_title(art_dir: Path) -> str:
    path = art_dir / "meta-tags.html"
    if not path.is_file():
        return ""
    m = re.search(r"<title>([^<]+)</title>", path.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def read_meta_description(art_dir: Path) -> str:
    path = art_dir / "meta-tags.html"
    if not path.is_file():
        return ""
    m = re.search(r'<meta name="description" content="([^"]*)"', path.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ""


def read_title(art_dir: Path) -> str:
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def load_manifest_types() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in ("pillar2-articles.json", "pillar4-8-articles.json"):
        path = BLOG / "pillar-manifests" / name
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for pillar in data.get("pillars", []):
            for art in pillar.get("articles", []):
                out[art["slug"]] = art.get("type", "")
    for manifest in BLOG.glob("pillar*/manifest.json"):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for art in data.get("articles", []):
            out[art["slug"]] = art.get("type", out.get(art["slug"], ""))
    return out


def load_import_overrides() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in BLOG.glob("pillar*/blog-index-import.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for post in data.get("posts", []):
            out[post["slug"]] = post
    return out


def normalize_type(raw: str | None) -> str:
    if not raw:
        return "guide"
    t = raw.lower().strip()
    if "versus" in t or t == "versus":
        return "versus"
    if "alternatives" in t or t == "alternatives":
        return "alternatives"
    if "how-to" in t or t == "how-to":
        return "how-to"
    if "use-case" in t:
        return "use-case"
    if "glossary" in t:
        return "glossary"
    if "faq" in t:
        return "faq"
    if "resource" in t:
        return "resource"
    if "comparison" in t:
        return "comparison"
    if "listicle" in t:
        return "listicle"
    if "review" in t:
        return "review"
    if "manifesto" in t:
        return "manifesto"
    if "guide" in t:
        return "guide"
    return t


def resolve_row(
    art_id: str,
    folder: str,
    slug: str,
    pillar: str,
    pillar_num: int,
    content_type: str,
    keyword: str,
    title: str,
    import_post: dict | None,
) -> dict:
    if slug in PILLAR1_MAP:
        content_type, card_tag, filter_cat, ui_module = PILLAR1_MAP[slug]
    elif slug in PILLAR3_MAP:
        content_type, card_tag, filter_cat, ui_module = PILLAR3_MAP[slug]
    elif slug in PILLAR8_MAP:
        content_type, card_tag, filter_cat, ui_module = PILLAR8_MAP[slug]
    elif content_type in TYPE_DEFAULTS:
        card_tag, filter_cat, ui_module = TYPE_DEFAULTS[content_type]
    else:
        card_tag, filter_cat, ui_module = TYPE_DEFAULTS["guide"]

    if pillar_num in PILLAR_CATEGORY and slug not in PILLAR1_MAP and slug not in PILLAR3_MAP and slug not in PILLAR8_MAP:
        card_tag, filter_cat = PILLAR_CATEGORY[pillar_num]

    if import_post:
        card_tag = import_post.get("card_tag", card_tag)
        filter_cat = import_post.get("filter_category", filter_cat)

    return {
        "id": art_id,
        "folder": folder,
        "slug": slug,
        "url": f"/en/blog/{slug}",
        "pillar": pillar,
        "pillar_num": pillar_num,
        "content_type": content_type,
        "card_tag": card_tag,
        "filter_category": filter_cat,
        "ui_module": ui_module,
        "target_keyword": keyword,
        "title": title,
        "source_path": f"SEO/Blog/{pillar}/{folder}",
        "sort_priority": import_post.get("sort_priority", 100 - int(art_id)) if import_post else 100 - int(art_id),
    }


def main() -> None:
    manifest_types = load_manifest_types()
    import_posts = load_import_overrides()
    rows: list[dict] = []

    for pillar_dir in PILLARS:
        pillar = pillar_dir.name
        m = re.search(r"pillar(\d+)", pillar)
        pillar_num = int(m.group(1)) if m else 0
        for art_dir in sorted(pillar_dir.glob("[0-9][0-9][0-9]-*/")):
            if not (art_dir / "article.md").is_file():
                continue
            folder = art_dir.name
            art_id = folder[:3]
            slug = read_slug(art_dir)
            keyword = read_keyword(art_dir)
            h1_title = read_title(art_dir)
            seo_title = read_meta_title(art_dir) or h1_title
            meta_desc = read_meta_description(art_dir)
            ctype = (
                manifest_types.get(slug)
                or read_type_from_readme(art_dir)
                or "guide"
            )
            ctype = normalize_type(ctype)
            rows.append(
                resolve_row(
                    art_id,
                    folder,
                    slug,
                    pillar,
                    pillar_num,
                    ctype,
                    keyword,
                    seo_title,
                    import_posts.get(slug),
                )
            )
            rows[-1]["display_title"] = h1_title or seo_title
            rows[-1]["meta_description"] = meta_desc

    rows.sort(key=lambda r: r["id"])
    fields = [
        "id",
        "folder",
        "slug",
        "url",
        "pillar",
        "pillar_num",
        "content_type",
        "card_tag",
        "filter_category",
        "ui_module",
        "target_keyword",
        "title",
        "display_title",
        "meta_description",
        "source_path",
        "sort_priority",
    ]
    for out_name in ("blog-cms-import-202.csv", "blog-cms-import-100.csv"):
        subset = rows if out_name.endswith("202.csv") else [r for r in rows if int(r["id"]) <= 100]
        out_csv = BLOG / out_name
        with out_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(subset)
        print(f"Wrote {len(subset)} rows → {out_csv}")

    # Summary by ui_module
    from collections import Counter

    c = Counter(r["ui_module"] for r in rows)
    print("\nUI module counts:")
    for k, v in c.most_common():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
