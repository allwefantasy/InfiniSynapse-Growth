#!/usr/bin/env python3
"""Export a Pillar 1-30 keyword inventory CSV (pillar no. / pillar name / keyword).

Keyword + metric sources differ per pillar generation, so each row records where its
data came from:

  Pillar 1-15  keyword/title  <- `SEO/Blog/Pillar 1-15/blog-cms-import-{202,100}.csv`
               volume/KD      <- `SEO/100页主题集群规划-v1-替换后主关键词版.md` (topics 001-100 only)
               hub flag       <- `SEO/100页关键词验证/keywords-100-master.csv` notes
  Pillar 16-20 keyword/title  <- `SEO/Blog/vibe-coding-handoff-pack/blog-vibe-coding-topics-plan.csv`
               volume/KD      <- `Skills/.../references/seo_pillar_strategy_vibe_coding_api.md`
                                 (joined by per-pillar row order, which matches folder order)
  Pillar 21-25 plan           <- `SEO/Blog/pillar21-25-topic-cluster-architecture_20260708.md`
  Pillar 26-30 plan           <- `SEO/Blog/pillar26-30-topic-cluster-architecture_20260715.md`
  Pillar 21-30 keyword        <- each article's `article-meta.json` (target + secondary)

Article numbers are NOT globally unique: 203-206 exist both in Pillar 1-15 (later
additions) and in the Pillar 16-20 vibe series, so every join is keyed by
(pillar folder, article number).

Run with --check to print join diagnostics instead of a silent best effort.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]  # InfiniSynapse-Growth (scripts→…→repo)
BLOG = ROOT / "SEO" / "Blog"
LEGACY = BLOG / "Pillar 1-15" / "articles"
ARCH_21_25 = BLOG / "pillar21-25-topic-cluster-architecture_20260708.md"
ARCH_26_30 = BLOG / "pillar26-30-topic-cluster-architecture_20260715.md"
PLAN_100 = ROOT / "SEO" / "100页主题集群规划-v1-替换后主关键词版.md"
MASTER_100 = ROOT / "SEO" / "100页关键词验证" / "keywords-100-master.csv"
VIBE_PLAN = BLOG / "vibe-coding-handoff-pack" / "blog-vibe-coding-topics-plan.csv"
VIBE_STRATEGY = (
    ROOT / "Skills" / "seo-geo-claude-skills-main" / "build" / "seo-blog-content"
    / "references" / "seo_pillar_strategy_vibe_coding_api.md"
)
CMS_CSVS = [
    BLOG / "Pillar 1-15" / "blog-cms-import-202.csv",
    BLOG / "Pillar 1-15" / "blog-cms-import-100.csv",
]

# Readable pillar names. 1-8 follow the 100-topic plan headings, 16-20 the vibe
# strategy doc pillar titles, 21-30 the architecture docs' Theme column.
PILLAR_NAMES = {
    1: "AI-Native Data Analysis",
    2: "Data Agent vs Code Agent vs BI vs Copilot",
    3: "AI Data Analyst Tools / Alternatives / vs",
    4: "Data Source Connectors & Integration How-To",
    5: "NL2SQL / Text-to-SQL / AI SQL",
    6: "AI for Excel / CSV / Spreadsheet",
    7: "Use Cases by Role / Industry",
    8: "AI Data Analyst Skills / Templates / Glossary",
    9: "Semantic Layer",
    10: "MCP & Data Access",
    11: "Agentic Analytics",
    12: "Data Trends & Industry News",
    13: "Data Privacy & Security",
    14: "Enterprise Data",
    15: "Data Search & Public Data",
    16: "Vibe Coding Workflow Discipline Before Real API Usage",
    17: "Choosing the Right Vibe Coding Stack and AI App Builder",
    18: "API Integration for Vibe-Built Products",
    19: "Tool Calling and Agent Workflows for Real Product Actions",
    20: "Data APIs and Production Readiness for Vibe-Coded Products",
    21: "Data Analysis Fundamentals",
    22: "Advanced Data Analysis Methods",
    23: "Data Analysis Tools & Software",
    24: "Data Analyst Career & Jobs",
    25: "Data Analyst Learning & Certification",
    26: "Data Governance & Quality",
    27: "Master Data, Catalog & Lineage",
    28: "Cross-Source Data Engineering & Pipelines",
    29: "Warehouse, Lakehouse & Architecture",
    30: "Analytics Deliverables, Dashboards & Visualization",
}

BASE_URL = "https://infinisynapse.com/en/blog/"

# `| 300 | 300-slug | keyword | 201000 | 72 | `slug` | title | …extra cols… |`
ARCH_ROW_RE = re.compile(
    r"^\|\s*(\d{3})\s*\|\s*(\d{3}-[^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
    r"\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|(.*)$"
)


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def scan_articles() -> list[dict]:
    """All article dirs on disk, keyed by (pillar folder, article number)."""
    found = []
    roots = [(LEGACY, range(1, 16)), (BLOG, range(16, 31))]
    for root, wanted in roots:
        for pillar_dir in sorted(root.iterdir()):
            if not pillar_dir.is_dir():
                continue
            m = re.match(r"pillar(\d+)-", pillar_dir.name)
            if not m or int(m.group(1)) not in wanted:
                continue
            for art in sorted(pillar_dir.iterdir()):
                am = re.match(r"^(\d{3})-(.+)$", art.name)
                if not art.is_dir() or not am or not (art / "article.md").exists():
                    continue
                found.append(
                    {
                        "pillar_no": int(m.group(1)),
                        "pillar_folder": pillar_dir.name,
                        "article_no": am.group(1),
                        "folder": art.name,
                        "folder_slug": am.group(2),
                        "path": art,
                    }
                )
    return found


def parse_arch(path: Path) -> dict:
    """Architecture-doc plan rows keyed by article number."""
    plan = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ARCH_ROW_RE.match(line)
        if not m:
            continue
        title, tail = m.group(7), m.group(8)
        plan[m.group(1)] = {
            "keyword": m.group(3),
            "volume": int(m.group(4)),
            "kd": int(m.group(5)),
            "slug": m.group(6),
            "title": re.sub(r"\s*\*\*\(HUB\)\*\*", "", title).strip(),
            "is_hub": "HUB" in title or "**HUB**" in tail,
        }
    return plan


def parse_plan_100() -> dict:
    """Topic 001-100 keyword + volume + KD from the 100-topic cluster plan."""
    out = {}
    topic = None
    for line in PLAN_100.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^###\s*(\d{3})\.\s*(.+)$", line)
        if h:
            topic = h.group(1)
            continue
        if topic is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4 or cells[0] in ("关键词", ":---") or cells[0].startswith(":-"):
            continue
        vol = re.sub(r"[^\d]", "", cells[1])
        kd = re.sub(r"[^\d]", "", cells[2])
        out[topic] = {
            "keyword": cells[0],
            "volume": int(vol) if vol else "",
            "kd": int(kd) if kd else "",
            "intent": cells[3] if len(cells) > 3 else "",
        }
        topic = None
    return out


def parse_vibe_strategy() -> dict:
    """Per-pillar ordered [(keyword, volume, KD)] from the vibe strategy doc.

    Doc pillars 1-5 map to blog pillars 16-20; rows are in the same order as the
    numbered article folders on disk.
    """
    text = VIBE_STRATEGY.read_text(encoding="utf-8")
    doc_to_blog = {1: 16, 2: 17, 3: 18, 4: 19, 5: 20}
    out, current, hub_titles = {}, None, {}
    for line in text.splitlines():
        h = re.match(r"^##\s*Pillar\s*(\d+)\s*—\s*(.+)$", line)
        if h:
            current = doc_to_blog.get(int(h.group(1)))
            if current:
                out[current] = []
            continue
        hub = re.match(r"^\*\*Pillar page \(hub page\):\*\*\s*`([^`]+)`", line)
        if hub and current:
            hub_titles[current] = hub.group(1).strip()
            continue
        row = re.match(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", line)
        if row and current is not None:
            out[current].append(
                {
                    "idea": row.group(2).strip(),
                    "keyword": row.group(3).strip(),
                    "volume": int(row.group(4)),
                    "kd": int(row.group(5)),
                }
            )
    return out, hub_titles


def meta_tags_hints(art_dir: Path) -> dict:
    """Keyword + canonical slug recorded in `meta-tags.html` (used when no CSV row matches)."""
    path = art_dir / "meta-tags.html"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    hints = {}
    m = re.search(r"Target keyword:\s*(.+)", text)
    if not m:
        m = re.search(r"<!--\s*Meta\s*\|[^|]+\|\s*([^->]+?)\s*-->", text)
    if m:
        hints["keyword"] = m.group(1).strip()
    c = re.search(r'rel="canonical"\s+href="[^"]*?/blog/([^"/?#]+)', text)
    if c:
        hints["slug"] = c.group(1)
    return hints


def body_stats(article: Path) -> tuple[str, int]:
    text = article.read_text(encoding="utf-8", errors="ignore")
    h1 = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), "")
    body = text.split("## TL;DR", 1)[-1]
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    body = re.sub(r"[#>*`|_\-]+", " ", body)
    return h1, len(re.findall(r"[A-Za-z0-9']+", body))


def build_rows(diagnostics: list[str]) -> list[dict]:
    arch = {**parse_arch(ARCH_21_25), **parse_arch(ARCH_26_30)}
    plan100 = parse_plan_100()
    vibe_metrics, vibe_hubs = parse_vibe_strategy()

    cms = {}
    for path in CMS_CSVS:  # 202-row pack first; 100-row pack only fills gaps
        for r in read_csv(path):
            cms.setdefault(r["id"].strip(), r)

    legacy_hubs = set()
    for r in read_csv(MASTER_100):
        if "hub" in (r.get("notes") or "").lower():
            legacy_hubs.add(r["no"].strip().zfill(3))

    vibe_plan = {r["编号"].strip(): r for r in read_csv(VIBE_PLAN)}

    articles = scan_articles()
    # vibe metrics join: per pillar, folder order == strategy-doc row order
    vibe_index = {}
    for p in range(16, 21):
        ordered = [a for a in articles if a["pillar_no"] == p]
        rows = vibe_metrics.get(p, [])
        if len(ordered) != len(rows):
            diagnostics.append(
                f"pillar{p}: {len(ordered)} folders vs {len(rows)} strategy-doc rows — metrics left blank"
            )
            continue
        for art, met in zip(ordered, rows):
            vibe_index[(art["pillar_folder"], art["article_no"])] = met

    rows = []
    for art in articles:
        p, num, key = art["pillar_no"], art["article_no"], (art["pillar_folder"], art["article_no"])
        meta_path = art["path"] / "article-meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        h1, words = body_stats(art["path"] / "article.md")

        keyword = plan_keyword = title = slug = url = ""
        volume = kd = intent = ""
        is_hub = False
        kw_src = metric_src = ""

        if p <= 15:
            row = cms.get(num)
            if row and row["folder"].strip() == art["folder"]:
                keyword = row["target_keyword"].strip()
                title = (row["title"] or "").strip()
                slug = row["slug"].strip()
                kw_src = "blog-cms-import"
            else:
                hints = meta_tags_hints(art["path"])
                slug = hints.get("slug") or art["folder_slug"]
                keyword = hints.get("keyword") or slug.replace("-", " ")
                kw_src = "meta-tags" if hints.get("keyword") else "folder-slug-fallback"
                diagnostics.append(
                    f"{art['pillar_folder']}/{art['folder']}: not in CMS import"
                    + (f" (id {num} maps to {row['folder']})" if row else "")
                    + f" — keyword from {kw_src}"
                )
            if num in plan100:
                plan_keyword = plan100[num]["keyword"]
                volume, kd = plan100[num]["volume"], plan100[num]["kd"]
                intent = plan100[num]["intent"]
                metric_src = "100-topic-plan"
            is_hub = num in legacy_hubs
        elif p <= 20:
            row = vibe_plan.get(num)
            if row:
                keyword = row["关键词"].strip()
                title = row["title"].strip()
                slug = row["slug"].strip()
                url = row["完整URL"].strip()
                intent = row["搜索意图"].strip()
                kw_src = "vibe-topics-plan"
                is_hub = title == vibe_hubs.get(p) or (row.get("备注") or "").strip() == "Hub"
            else:
                slug = art["folder_slug"]
                keyword = slug.replace("-", " ")
                kw_src = "folder-slug-fallback"
                diagnostics.append(f"{art['folder']}: missing from vibe topics plan")
            met = vibe_index.get(key)
            if met:
                plan_keyword = met["keyword"]
                volume, kd = met["volume"], met["kd"]
                metric_src = "vibe-strategy-doc"
        else:
            row = arch.get(num)
            keyword = meta.get("target_keyword") or (row["keyword"] if row else art["folder_slug"].replace("-", " "))
            kw_src = "article-meta" if meta.get("target_keyword") else "architecture-doc"
            if row:
                plan_keyword = row["keyword"]
                volume, kd = row["volume"], row["kd"]
                slug, title, is_hub = row["slug"], row["title"], row["is_hub"]
                metric_src = "architecture-doc"
            else:
                slug = art["folder_slug"]
                diagnostics.append(f"{art['folder']}: missing from architecture doc")

        slug = slug or art["folder_slug"]
        rows.append(
            {
                "pillar_no": p,
                "pillar_name": PILLAR_NAMES[p],
                "pillar_folder": art["pillar_folder"],
                "article_no": num,
                "article_type": "hub" if is_hub else "cluster",
                "target_keyword": keyword,
                "keyword_word_count": len(keyword.split()),
                "plan_keyword": plan_keyword,
                "search_volume": volume,
                "keyword_difficulty": kd,
                "search_intent": intent,
                "secondary_keywords": "; ".join(meta.get("secondary", [])),
                "slug": slug,
                "url": url or f"{BASE_URL}{slug}",
                "h1_title": h1 or title,
                "article_word_count": words,
                "keyword_source": kw_src,
                "metrics_source": metric_src,
                "article_path": str((art["path"] / "article.md").relative_to(ROOT)),
            }
        )

    rows.sort(key=lambda r: (r["pillar_no"], r["article_no"]))
    return rows


def write_outputs(rows: list[dict]) -> tuple[Path, Path]:
    inventory = BLOG / "pillar1-30-keyword-inventory.csv"
    with inventory.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = BLOG / "pillar1-30-keyword-summary.csv"
    with summary.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "pillar_no",
                "pillar_name",
                "pillar_folder",
                "articles",
                "hubs",
                "keywords",
                "with_metrics",
                "total_search_volume",
                "avg_kd",
                "avg_word_count",
            ]
        )
        for p in sorted({r["pillar_no"] for r in rows}):
            g = [r for r in rows if r["pillar_no"] == p]
            vols = [int(r["search_volume"]) for r in g if r["search_volume"] != ""]
            kds = [int(r["keyword_difficulty"]) for r in g if r["keyword_difficulty"] != ""]
            w.writerow(
                [
                    p,
                    PILLAR_NAMES[p],
                    g[0]["pillar_folder"],
                    len(g),
                    sum(1 for r in g if r["article_type"] == "hub"),
                    len({r["target_keyword"] for r in g}),
                    len(vols),
                    sum(vols),
                    round(sum(kds) / len(kds), 1) if kds else "",
                    round(sum(r["article_word_count"] for r in g) / len(g)),
                ]
            )
    return inventory, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="print join diagnostics")
    args = ap.parse_args()

    diagnostics: list[str] = []
    rows = build_rows(diagnostics)
    inventory, summary = write_outputs(rows)

    print(f"{len(rows)} rows -> {inventory.relative_to(ROOT)}")
    print(f"{len({r['pillar_no'] for r in rows})} rows -> {summary.relative_to(ROOT)}")
    no_metrics = sum(1 for r in rows if r["search_volume"] == "")
    if no_metrics:
        print(f"note: {no_metrics} rows have no volume/KD source")
    if args.check:
        for d in diagnostics:
            print("  !", d, file=sys.stderr)


if __name__ == "__main__":
    main()
