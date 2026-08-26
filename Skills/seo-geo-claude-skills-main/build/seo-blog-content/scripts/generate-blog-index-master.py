#!/usr/bin/env python3
"""Generate blog-index-import-master.json — all published posts for frontend list page."""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"

_spec = importlib.util.spec_from_file_location("cms_csv", Path(__file__).parent / "generate-cms-import-csv.py")
_cms = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_cms)

PILLARS = _cms.PILLARS
load_import_overrides = _cms.load_import_overrides
load_manifest_types = _cms.load_manifest_types
normalize_type = _cms.normalize_type
read_keyword = _cms.read_keyword
read_slug = _cms.read_slug
read_title = _cms.read_title
read_type_from_readme = _cms.read_type_from_readme
resolve_row = _cms.resolve_row

MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

CATEGORY_LABELS = {
    "all": {"en": "All", "es": "Todos"},
    "comparisons": {"en": "Comparisons & Alternatives", "es": "Comparativas y alternativas"},
    "knowledge": {"en": "Knowledge Base & Explainers", "es": "Base de conocimiento y explicaciones"},
    "connectors": {"en": "Data Connectors & Integrations", "es": "Conectores e integraciones de datos"},
    "use_cases": {"en": "Use Cases & Industries", "es": "Casos de uso e industrias"},
    "excel_csv": {"en": "Excel & Spreadsheet AI", "es": "Excel y hojas de cálculo con IA"},
    "nl2sql": {"en": "NL2SQL & Text-to-SQL", "es": "NL2SQL y Text-to-SQL"},
    "tools_reviews": {"en": "Tools & Reviews", "es": "Herramientas y reseñas"},
    "deep_dive": {"en": "Technical Deep Dives", "es": "Análisis técnico a fondo"},
    "tutorials": {"en": "Tutorials & Best Practices", "es": "Tutoriales y buenas prácticas"},
}

# Blog nav pill order (excluding all)
NAV_CATEGORY_ORDER = [
    "comparisons",
    "knowledge",
    "connectors",
    "use_cases",
    "excel_csv",
    "nl2sql",
    "tools_reviews",
    "deep_dive",
    "tutorials",
]


def read_meta_tags(art_dir: Path) -> dict[str, str]:
    path = art_dir / "meta-tags.html"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    m = re.search(r"<title>([^<]+)</title>", text)
    if m:
        out["title"] = m.group(1).strip()
    m = re.search(r'<meta name="description" content="([^"]+)"', text)
    if m:
        out["description"] = m.group(1).strip()
    m = re.search(r'<meta property="og:image" content="([^"]+)"', text)
    if m:
        out["og_image"] = m.group(1).strip()
    m = re.search(r'<meta property="article:published_time" content="([^"]+)"', text)
    if m:
        out["published_at"] = m.group(1).strip()
    return out


def read_schema_dates(art_dir: Path) -> str | None:
    path = art_dir / "schema.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    for item in data:
        if item.get("@type") == "BlogPosting":
            return item.get("datePublished")
    return None


def format_display_date(iso: str) -> str:
    # 2026-06-12T10:00:00+08:00 → 12 JUN 2026
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return iso[:10]
    return f"{dt.day:02d} {MONTHS[dt.month - 1]} {dt.year}"


def hero_image_path(pillar_num: int, slug: str, art_dir: Path, og_image: str | None) -> str:
    standard = f"/blog/assets/pillar{pillar_num}/{slug}/hero.png"
    images = art_dir / "images"
    if images.is_dir():
        heroes = sorted(images.glob("hero*.png"))
        if heroes:
            name = heroes[0].name
            if name == "hero.png":
                return standard
            return f"/blog/assets/pillar{pillar_num}/{slug}/{name}"
    return standard


def build_posts() -> list[dict]:
    manifest_types = load_manifest_types()
    import_posts = load_import_overrides()
    posts: list[dict] = []

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
            ctype = normalize_type(
                manifest_types.get(slug) or read_type_from_readme(art_dir) or "guide"
            )
            row = resolve_row(
                art_id, folder, slug, pillar, pillar_num, ctype, keyword, h1_title,
                import_posts.get(slug),
            )
            override = import_posts.get(slug, {})
            meta = read_meta_tags(art_dir)

            title = override.get("title") or meta.get("title") or h1_title
            excerpt = override.get("excerpt") or meta.get("description") or ""
            published_at = (
                override.get("published_at")
                or meta.get("published_at")
                or read_schema_dates(art_dir)
                or "2026-06-12T10:00:00+08:00"
            )
            display_date = override.get("display_date") or format_display_date(published_at)
            hero = override.get("hero_image") or hero_image_path(
                pillar_num, slug, art_dir, meta.get("og_image")
            )
            sort_priority = override.get("sort_priority", row["sort_priority"])
            featured = override.get("featured", sort_priority >= 118)

            post_id = override.get("id") or f"pillar{pillar_num}-{art_id}"

            posts.append({
                "id": post_id,
                "slug": slug,
                "url": f"/blog/{slug}",
                "title": title,
                "excerpt": excerpt,
                "card_tag": row["card_tag"],
                "filter_category": row["filter_category"],
                "content_type": row["content_type"],
                "ui_module": row["ui_module"],
                "target_keyword": keyword,
                "published_at": published_at,
                "display_date": display_date,
                "hero_image": hero,
                "source_folder": folder,
                "source_path": row["source_path"],
                "sort_priority": sort_priority,
                "featured": featured,
                "pillar_cluster": pillar,
                "pillar_num": pillar_num,
            })

    posts.sort(key=lambda p: (-p["sort_priority"], p["id"]))
    return posts


def category_counts(posts: list[dict]) -> dict[str, int]:
    c = Counter(p["filter_category"] for p in posts)
    counts = {"all": len(posts)}
    for key in NAV_CATEGORY_ORDER:
        counts[key] = c.get(key, 0)
    return counts


def main() -> None:
    posts = build_posts()
    counts = category_counts(posts)
    labels = {
        key: {**CATEGORY_LABELS[key], "count_after_import": counts[key]}
        for key in CATEGORY_LABELS
    }

    out = {
        "_comment": "博客列表页卡片数据 · 全量已发布文章 · 对齐 infinisynapse.cn/blog 现有 UI",
        "_usage": (
            "前端 import 此文件 posts 数组作为 blogPosts 数据源；"
            "详情页用 source_path 下 article.md + meta-tags.html + schema.json；"
            "ui_module 决定详情页内容区块变体（见 FRONTEND-DEPLOY-GUIDE.md §5）"
        ),
        "_generated_by": "Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/generate-blog-index-master.py",
        "locale_ui": "es",
        "locale_content": "en",
        "article_count": len(posts),
        "category_labels": labels,
        "posts": posts,
    }

    out_path = BLOG / "blog-index-import-master.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(posts)} posts → {out_path}")
    print("\nCategory counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
