#!/usr/bin/env python3
"""Generate quickcreator-seo-fields.csv — per-article values to paste into QuickCreator's SEO panel.

Fixes the 4 On-Page issues that QuickCreator flags when content is imported without meta:
  Canonical URL, Meta Description (150-160), Social Media Meta Tags (OG/Twitter).
The H1 fix is an editor action (see h1_fix column) — QuickCreator already renders the title as H1,
so the body's leading "# ..." heading must be removed in the editor.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

BLOG = Path(__file__).parent


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def g(pat: str, text: str) -> str:
    m = re.search(pat, text)
    return (m.group(1) if m else "").replace("&quot;", '"').strip()


def first_h1(md: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else ""


def main() -> None:
    rows = []
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            html_path = art / "meta-tags.html"
            md_path = art / "article.md"
            if not html_path.is_file() or not md_path.is_file():
                continue
            h = html_path.read_text(encoding="utf-8")
            md = md_path.read_text(encoding="utf-8")
            slug = g(r'<link rel="canonical" href="https://infinisynapse\.cn/blog/([^"]+)"', h)
            rows.append({
                "id": art.name[:3],
                "slug": slug,
                "page_url": g(r'<link rel="canonical" href="([^"]+)"', h),
                "meta_title": g(r"<title>([^<]+)</title>", h),
                "meta_description": g(r'<meta name="description" content="([^"]+)"', h),
                "canonical_url": g(r'<link rel="canonical" href="([^"]+)"', h),
                "og_title": g(r'<meta property="og:title" content="([^"]+)"', h),
                "og_description": g(r'<meta property="og:description" content="([^"]+)"', h),
                "og_image": g(r'<meta property="og:image" content="([^"]+)"', h),
                "twitter_title": g(r'<meta name="twitter:title" content="([^"]+)"', h),
                "twitter_description": g(r'<meta name="twitter:description" content="([^"]+)"', h),
                "twitter_image": g(r'<meta name="twitter:image" content="([^"]+)"', h),
                "h1_fix": f"Delete body heading '# {first_h1(md)}' (QuickCreator title is the H1)",
            })

    rows.sort(key=lambda r: r["id"])
    out = BLOG / "quickcreator-seo-fields.csv"
    fields = [
        "id", "slug", "page_url", "meta_title", "meta_description", "canonical_url",
        "og_title", "og_description", "og_image",
        "twitter_title", "twitter_description", "twitter_image", "h1_fix",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {out}")

    # quick integrity report
    bad_desc = [r["id"] for r in rows if not (150 <= len(r["meta_description"]) <= 160)]
    no_canon = [r["id"] for r in rows if not r["canonical_url"]]
    no_og = [r["id"] for r in rows if not r["og_image"]]
    print(f"  desc out of range: {len(bad_desc)} {bad_desc}")
    print(f"  missing canonical: {len(no_canon)}")
    print(f"  missing og:image:  {len(no_og)}")


if __name__ == "__main__":
    main()
