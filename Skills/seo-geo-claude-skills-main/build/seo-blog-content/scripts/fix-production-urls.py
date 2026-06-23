#!/usr/bin/env python3
"""Migrate blog SEO URLs to production: infinisynapse.com/en/blog/{slug}.

Updates per article (100 pillars):
  article.md   — Slug field + internal /blog/ links → /en/blog/
  meta-tags.html — canonical, hreflang, og:url, og:image domain, etc.
  schema.json    — @id, image, author, publisher URLs
  preview.html   — same as meta (if present)
  head.html      — regenerated after meta/schema fix

Also updates blog-index-import-master.json, blog-cms-import-100.csv, seo-meta.json.

Run after content edits, before build-frontend-handoff.py:
  python3 fix-production-urls.py
  python3 generate-deploy-meta.py
  python3 generate-blog-index-master.py
  python3 build-frontend-handoff.py
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from url_config import DOMAIN, LOCALE_EN, LOCALE_ZH, SITE, blog_path_en, blog_url_en, blog_url_zh

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
OLD_DOMAIN = "infinisynapse.cn"
ARTICLE_FILES = ("article.md", "meta-tags.html", "schema.json", "preview.html", "head.html")


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def swap_domain(text: str) -> str:
    return text.replace(OLD_DOMAIN, DOMAIN).replace(f"app.{OLD_DOMAIN}", f"app.{DOMAIN}")


def fix_blog_page_urls(text: str) -> str:
    """https://infinisynapse.com/blog/{slug} → /en/blog/  (skip /blog/assets/)"""
    text = re.sub(
        rf"https://{re.escape(DOMAIN)}/blog/(?!assets/)",
        f"https://{DOMAIN}/{LOCALE_EN}/blog/",
        text,
    )
    # hreflang zh already uses /zh/blog/ — ensure domain only
    return text


def fix_relative_blog_links(text: str) -> str:
    """Markdown internal links: (/blog/slug) → (/en/blog/slug).

    Skips /blog/assets/ and the **Slug** metadata line (slug is an identifier,
    not a URL — it must stay bare so slug parsers don't double-prefix it).
    """
    out_lines = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("**Slug**"):
            out_lines.append(line)  # leave slug identifier untouched
            continue
        out_lines.append(
            re.sub(r"(?<![/\w])/blog/(?!assets/|en/blog/)", f"/{LOCALE_EN}/blog/", line)
        )
    return "".join(out_lines)


def fix_meta_hreflang(text: str, slug: str) -> str:
    """Ensure en + x-default → /en/blog/slug; zh-CN → /zh/blog/slug."""
    en = blog_url_en(slug)
    zh = blog_url_zh(slug)
    text = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]*"',
        f'<link rel="alternate" hreflang="en" href="{en}"',
        text,
    )
    text = re.sub(
        r'<link rel="alternate" hreflang="zh-CN" href="[^"]*"',
        f'<link rel="alternate" hreflang="zh-CN" href="{zh}"',
        text,
    )
    text = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="[^"]*"',
        f'<link rel="alternate" hreflang="x-default" href="{en}"',
        text,
    )
    text = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="{en}"',
        text,
    )
    text = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{en}"',
        text,
    )
    return text


def extract_slug_from_meta(text: str) -> str | None:
    m = re.search(rf'https://{re.escape(DOMAIN)}/{LOCALE_EN}/blog/([^"/]+)', text)
    if m:
        return m.group(1)
    m = re.search(rf'https://{re.escape(DOMAIN)}/blog/([^"/]+)', text)
    return m.group(1) if m else None


def fix_schema_json(path: Path, slug: str) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    en = blog_url_en(slug)
    changed = False
    for item in data:
        if item.get("@type") == "BlogPosting":
            if item.get("mainEntityOfPage", {}).get("@id") != en:
                item.setdefault("mainEntityOfPage", {})["@id"] = en
                item["mainEntityOfPage"]["@type"] = "WebPage"
                changed = True
            if "author" in item and isinstance(item["author"], dict):
                item["author"]["url"] = f"{SITE}/{LOCALE_EN}/about"
                changed = True
            if "publisher" in item and isinstance(item["publisher"], dict):
                logo = item["publisher"].get("logo", {})
                if isinstance(logo, dict):
                    logo["url"] = f"{SITE}/logo.png"
                    changed = True
            if "image" in item and isinstance(item["image"], list):
                item["image"] = [swap_domain(fix_blog_page_urls(u)) for u in item["image"]]
                changed = True
        if item.get("@type") == "BreadcrumbList":
            for el in item.get("itemListElement", []):
                it = el.get("item", {})
                if isinstance(it, dict) and "item" in it:
                    it["item"] = swap_domain(fix_blog_page_urls(fix_relative_blog_links(it["item"])))
                    changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def process_text_file(path: Path, slug_hint: str | None = None) -> str | None:
    text = path.read_text(encoding="utf-8")
    original = text
    text = swap_domain(text)
    text = fix_blog_page_urls(text)
    if path.name == "article.md":
        text = fix_relative_blog_links(text)
    slug = slug_hint or extract_slug_from_meta(text)
    if slug and path.name in ("meta-tags.html", "preview.html", "head.html"):
        text = fix_meta_hreflang(text, slug)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return slug


def slug_from_folder(folder: str) -> str:
    return folder.split("-", 1)[1] if "-" in folder else folder


def fix_articles() -> int:
    n = 0
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            slug = slug_from_folder(art.name)
            for name in ARTICLE_FILES:
                p = art / name
                if p.is_file():
                    process_text_file(p, slug)
            fix_schema_json(art / "schema.json", slug)
            n += 1
    return n


def fix_json_index(path: Path) -> None:
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_site"] = SITE
    data["_blog_url_pattern"] = f"{SITE}/{LOCALE_EN}/blog/{{slug}}"
    for post in data.get("posts", []):
        slug = post.get("slug", "")
        if slug:
            post["url"] = blog_path_en(slug)
            if "canonical" in post:
                post["canonical"] = blog_url_en(slug)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fix_csv(path: Path) -> None:
    if not path.is_file():
        return
    rows = []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        for row in reader:
            slug = row.get("slug", "")
            if slug:
                row["url"] = blog_path_en(slug)
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    count = fix_articles()
    fix_json_index(BLOG / "blog-index-import-master.json")
    fix_csv(BLOG / "blog-cms-import-100.csv")
    # pillar1/3 import json
    for p in BLOG.glob("pillar*/blog-index-import.json"):
        fix_json_index(p)
    print(f"Updated {count} article folders → {SITE}/{LOCALE_EN}/blog/{{slug}}")
    print("Next: python3 generate-deploy-meta.py && python3 generate-blog-index-master.py && python3 build-frontend-handoff.py")


if __name__ == "__main__":
    main()
