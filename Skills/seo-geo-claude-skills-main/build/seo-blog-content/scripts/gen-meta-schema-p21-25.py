#!/usr/bin/env python3
"""Generate schema.json + meta-tags.html from each article.md in Pillars 21-25.

Reads H1 + Meta Description from article.md; slug/keyword from article-meta.json.
"""
import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from article_keyword_meta import read_meta

ROOT = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
BASE_URL = "https://infinisynapse.com"
PUB_DATE = "2026-07-08T10:00:00+08:00"

SECTION = {
    "pillar21-data-analysis-fundamentals": "Data Analysis Fundamentals",
    "pillar22-advanced-data-analysis-methods": "Advanced Data Analysis Methods",
    "pillar23-data-analysis-tools-software": "Data Analysis Tools & Software",
    "pillar24-data-analyst-career-jobs": "Data Analyst Career & Jobs",
    "pillar25-data-analyst-learning-certification": "Data Analyst Learning & Certification",
    "pillar26-data-governance-quality": "Data Governance & Quality",
    "pillar27-master-data-catalog-lineage": "Master Data, Catalog & Lineage",
    "pillar28-data-engineering-pipelines": "Data Engineering & Pipelines",
    "pillar29-warehouse-lakehouse-architecture": "Warehouse, Lakehouse & Architecture",
    "pillar30-analytics-dashboards-visualization": "Analytics, Dashboards & Visualization",
}
PUB_DATE_BY_PILLAR = {
    "pillar26-data-governance-quality": "2026-07-15T10:00:00+08:00",
    "pillar27-master-data-catalog-lineage": "2026-07-15T10:00:00+08:00",
    "pillar28-data-engineering-pipelines": "2026-07-15T10:00:00+08:00",
    "pillar29-warehouse-lakehouse-architecture": "2026-07-15T10:00:00+08:00",
    "pillar30-analytics-dashboards-visualization": "2026-07-15T10:00:00+08:00",
}


def clean(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # links -> anchor text
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def parse(article_path: Path):
    md = article_path.read_text(encoding="utf-8")
    meta = read_meta(article_path)
    slug_raw = meta.get("slug", "").replace("/blog/", "")
    h1 = re.search(r"^#\s+(.+)$", md, re.M)
    desc = re.search(r"\*\*Meta Description\*\*:\s*(.+)", md)
    hero = re.search(r"!\[([^\]]*)\]\(\./images/([^)]+)\)", md)
    faqs = []
    m = re.search(r"##\s+Frequently Asked Questions\s*(.+?)(?=\n##\s|\Z)", md, re.S)
    if m:
        block = m.group(1)
        for q in re.finditer(r"###\s+(.+?)\n(.+?)(?=\n###\s|\Z)", block, re.S):
            faqs.append((clean(q.group(1)), clean(q.group(2))))
    return {
        "h1": h1.group(1).strip() if h1 else "",
        "desc": clean(desc.group(1)) if desc else "",
        "slug": slug_raw,
        "kw": meta.get("target_keyword", ""),
        "hero_alt": hero.group(1).strip() if hero else (h1.group(1).strip() if h1 else ""),
        "hero_file": hero.group(2).strip() if hero else "",
        "faqs": faqs,
    }


def build_schema(d, pillar, folder):
    pub = PUB_DATE_BY_PILLAR.get(pillar, PUB_DATE)
    img = f"{BASE_URL}/en/blog/{pillar}/{folder}/images/{d['hero_file']}"
    url = f"{BASE_URL}/en/blog/{d['slug']}"
    blog = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": d["h1"],
        "description": d["desc"],
        "image": [img],
        "datePublished": pub,
        "dateModified": pub,
        "author": {"@type": "Organization", "name": "InfiniSynapse Data Team",
                    "url": f"{BASE_URL}/en/about"},
        "publisher": {"@type": "Organization", "name": "InfiniSynapse",
                       "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/logo.png"}},
        "mainEntityOfPage": url,
        "about": [{"@type": "Thing", "name": d["kw"]}],
        "keywords": d["kw"],
        "url": url,
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in d["faqs"]]}
    return [blog, faq]


def build_meta(d, pillar, folder):
    pub = PUB_DATE_BY_PILLAR.get(pillar, PUB_DATE)
    img = f"{BASE_URL}/en/blog/{pillar}/{folder}/images/{d['hero_file']}"
    url = f"{BASE_URL}/en/blog/{d['slug']}"
    sec = SECTION.get(pillar, "Data Analysis")
    return f"""<!--
  Meta Tags Package
  Page: {d['h1']}
  Generated: 2026-07-08
  Target keyword: {d['kw']}
-->

<title>{d['h1']}</title>
<meta name="description" content="{d['desc']}" />
<link rel="canonical" href="{url}" />

<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="InfiniSynapse Data Team">
<meta http-equiv="content-language" content="en">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{BASE_URL}/zh/blog/{d['slug']}">
<link rel="alternate" hreflang="x-default" href="{url}">

<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{d['h1']}">
<meta property="og:description" content="{d['desc']}" />
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{d['hero_alt']}">
<meta property="og:site_name" content="InfiniSynapse Blog">
<meta property="og:locale" content="en_US">

<meta property="article:published_time" content="{pub}">
<meta property="article:modified_time" content="{pub}">
<meta property="article:author" content="{BASE_URL}/about">
<meta property="article:section" content="{sec}">
<meta property="article:tag" content="{d['kw']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@InfiniSynapse">
<meta name="twitter:title" content="{d['h1']}">
<meta name="twitter:description" content="{d['desc']}" />
<meta name="twitter:image" content="{img}">
"""


def main():
    targets = sys.argv[1:] or sorted(SECTION)
    count = 0
    for pillar in targets:
        pdir = ROOT / pillar
        if not pdir.is_dir():
            continue
        for folder in sorted(pdir.iterdir()):
            art = folder / "article.md"
            if not art.is_file():
                continue
            d = parse(art)
            if not (d["h1"] and d["slug"] and d["kw"]):
                print(f"SKIP (missing fields): {folder.name}")
                continue
            (folder / "schema.json").write_text(
                json.dumps(build_schema(d, pillar, folder.name), indent=2,
                           ensure_ascii=False) + "\n", encoding="utf-8")
            (folder / "meta-tags.html").write_text(
                build_meta(d, pillar, folder.name), encoding="utf-8")
            count += 1
            print(f"OK {folder.name}  faqs={len(d['faqs'])}  kw='{d['kw']}'")
    print(f"\nGenerated meta+schema for {count} articles.")


if __name__ == "__main__":
    main()
