#!/usr/bin/env python3
"""Generate a COMPLETE sitemap.xml = live production URLs + Pillar 16–20 blog pages.

Strategy:
1. Fetch https://infinisynapse.com/sitemap.xml as the authoritative base (all existing pages).
2. Merge / update Pillar 16–20 (203–299) canonical URLs from article meta-tags + schema lastmod.
3. Write SEO/Blog/sitemap.xml — deployable as a full replacement for production.

Offline fallback: SEO/Blog/sitemap-live-baseline.xml (updated whenever live fetch succeeds).
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[5]
BLOG = ROOT / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
OUT = BLOG / "sitemap.xml"
BASELINE = BLOG / "sitemap-live-baseline.xml"
LIVE_URL = "https://infinisynapse.com/sitemap.xml"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

PILLARS_VIBE = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))
PILLARS_P2125 = sorted(BLOG.glob("pillar2[1-5]-*"))
PILLARS_P2630 = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))

HUB_SLUGS_P2125 = {
    "data-analysis-complete-guide",
    "python-data-analysis-guide",
    "data-analysis-tools-guide",
    "data-analyst-guide",
    "data-analyst-certification-guide",
}

HUB_SLUGS_P2630 = {
    "data-governance-frameworks",
    "master-data-management",
    "data-engineering",
    "data-warehouse",
    "data-visualization",
}

_spec = importlib.util.spec_from_file_location("reg", SCRIPTS / "cluster-link-registry.py")
reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(reg)

HUB_SLUGS = {reg.slug_from_folder(folder) for folder in reg.PRIMARY_HUB.values()}


def to_date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).date().isoformat()
    except (ValueError, AttributeError):
        return datetime.now().date().isoformat()


def url_block(loc: str, lastmod: str, changefreq: str, priority: str) -> list[str]:
    return [
        "  <url>",
        f"    <loc>{escape(loc)}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
        f"    <changefreq>{changefreq}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ]


def validate_xml(text: str) -> None:
    parseString(text.encode("utf-8"))


def parse_sitemap_xml(text: str) -> dict[str, dict[str, str]]:
    """Return loc -> {lastmod, changefreq, priority}."""
    root = ET.fromstring(text)
    out: dict[str, dict[str, str]] = {}
    for url_el in root.findall("sm:url", NS):
        loc_el = url_el.find("sm:loc", NS)
        if loc_el is None or not loc_el.text:
            continue
        loc = loc_el.text.rstrip("/")
        lm = url_el.find("sm:lastmod", NS)
        cf = url_el.find("sm:changefreq", NS)
        pr = url_el.find("sm:priority", NS)
        out[loc] = {
            "lastmod": lm.text if lm is not None and lm.text else datetime.now().date().isoformat(),
            "changefreq": cf.text if cf is not None and cf.text else "weekly",
            "priority": pr.text if pr is not None and pr.text else "0.7",
        }
    return out


def fetch_live_sitemap() -> dict[str, dict[str, str]]:
    req = urllib.request.Request(LIVE_URL, headers={"User-Agent": "InfiniSynapse-sitemap-builder/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    BASELINE.write_text(text, encoding="utf-8")
    return parse_sitemap_xml(text)


def load_base_urls() -> tuple[dict[str, dict[str, str]], str]:
    try:
        return fetch_live_sitemap(), "live"
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
        if BASELINE.is_file():
            print(f"Live fetch failed ({exc}); using {BASELINE.name}", file=sys.stderr)
            return parse_sitemap_xml(BASELINE.read_text(encoding="utf-8")), "baseline"
        print(f"Live fetch failed and no baseline: {exc}", file=sys.stderr)
        sys.exit(1)


def lastmod_from_schema(schema_path: Path) -> str:
    if not schema_path.is_file():
        return datetime.now().date().isoformat()
    try:
        data = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return datetime.now().date().isoformat()
    items = data if isinstance(data, list) else [data]
    for item in items:
        if item.get("@type") == "BlogPosting":
            if item.get("dateModified"):
                return to_date(item["dateModified"])
            if item.get("datePublished"):
                return to_date(item["datePublished"])
    return datetime.now().date().isoformat()


def canonical_from_meta(meta_path: Path) -> str:
    if not meta_path.is_file():
        return ""
    text = meta_path.read_text(encoding="utf-8")
    m = re.search(r'<link rel="canonical" href="(https://infinisynapse\.com/en/blog/[^"]+)"', text)
    return m.group(1).rstrip("/") if m else ""


def slug_from_art_dir(art_dir: Path) -> str:
    sidecar = art_dir / "article-meta.json"
    if sidecar.is_file():
        raw = json.loads(sidecar.read_text(encoding="utf-8"))
        slug = raw.get("slug", "")
        if slug.startswith("/blog/"):
            return slug.split("/blog/", 1)[1]
        if slug.startswith("/en/blog/"):
            return slug.split("/en/blog/", 1)[1]
    loc = canonical_from_meta(art_dir / "meta-tags.html")
    if loc:
        return loc.rsplit("/", 1)[-1]
    text = (art_dir / "article.md").read_text(encoding="utf-8")
    sm = re.search(r"\*\*Slug\*\*:\s*`(?:/blog/)?([^`]+)`", text)
    if sm:
        return sm.group(1).strip("/")
    return art_dir.name.split("-", 1)[-1]


def pillar_blog_urls(pillars: list[Path], hub_slugs: set[str] | None = None) -> dict[str, dict[str, str]]:
    """Articles under given pillars: canonical URL + lastmod from schema."""
    urls: dict[str, dict[str, str]] = {}
    for pillar in pillars:
        for art_dir in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            if not (art_dir / "article.md").is_file():
                continue
            loc = canonical_from_meta(art_dir / "meta-tags.html")
            if not loc:
                slug = slug_from_art_dir(art_dir)
                if slug:
                    loc = f"https://infinisynapse.com/en/blog/{slug}"
            if not loc:
                continue
            slug = loc.rsplit("/", 1)[-1]
            is_hub = slug in (hub_slugs or set())
            urls[loc] = {
                "lastmod": lastmod_from_schema(art_dir / "schema.json"),
                "changefreq": "weekly",
                "priority": "0.9" if is_hub else "0.7",
            }
    return urls


def pillar_vibe_urls() -> dict[str, dict[str, str]]:
    return pillar_blog_urls(PILLARS_VIBE, HUB_SLUGS)


def pillar_p2125_urls() -> dict[str, dict[str, str]]:
    return pillar_blog_urls(PILLARS_P2125, HUB_SLUGS_P2125)


def pillar_p2630_urls() -> dict[str, dict[str, str]]:
    return pillar_blog_urls(PILLARS_P2630, HUB_SLUGS_P2630)


def main() -> None:
    base, source = load_base_urls()
    vibe = pillar_vibe_urls()
    p2125 = pillar_p2125_urls()
    p2630 = pillar_p2630_urls()
    today = datetime.now().date().isoformat()

    merged = dict(base)
    added = 0
    updated = 0
    for loc, meta in {**vibe, **p2125, **p2630}.items():
        if loc not in merged:
            merged[loc] = meta
            added += 1
        else:
            merged[loc] = {**merged[loc], **meta}
            updated += 1

    # Ensure blog index exists
    blog_index = "https://infinisynapse.com/en/blog"
    if blog_index not in merged:
        merged[blog_index] = {"lastmod": today, "changefreq": "weekly", "priority": "0.9"}
        added += 1

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc in sorted(merged):
        meta = merged[loc]
        lines += url_block(loc, meta["lastmod"], meta["changefreq"], meta["priority"])

    lines.append("</urlset>")
    xml = "\n".join(lines) + "\n"
    validate_xml(xml)
    OUT.write_text(xml, encoding="utf-8")

    blog_n = sum(1 for u in merged if "/en/blog/" in u or u.endswith("/en/blog"))
    print(f"Wrote {len(merged)} URLs -> {OUT}")
    print(f"  base source: {source} ({len(base)} URLs)")
    print(f"  pillar 16-20: {len(vibe)}")
    print(f"  pillar 21-25: {len(p2125)}")
    print(f"  pillar 26-30: {len(p2630)}")
    print(f"  added {added}, updated {updated}")
    print(f"  blog URLs total: {blog_n}")


if __name__ == "__main__":
    main()
