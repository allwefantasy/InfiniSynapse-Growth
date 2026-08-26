#!/usr/bin/env python3
"""Export a Pillar 26-30 keyword inventory CSV (pillar no. / pillar name / keyword).

Merges the planning table in
`SEO/Blog/pillar26-30-topic-cluster-architecture_20260715.md`
(volume, KD, working title) with each article's on-disk
`article-meta.json` (target + secondary keywords) and `article.md` (H1, word count).
"""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]  # InfiniSynapse-Growth (scripts→…→repo)
BLOG = ROOT / "SEO" / "Blog"
ARCH = BLOG / "pillar26-30-topic-cluster-architecture_20260715.md"

PILLARS = {
    26: ("pillar26-data-governance-quality", "Data Governance & Quality"),
    27: ("pillar27-master-data-catalog-lineage", "Master Data, Catalog & Lineage"),
    28: ("pillar28-data-engineering-pipelines", "Cross-Source Data Engineering & Pipelines"),
    29: ("pillar29-warehouse-lakehouse-architecture", "Warehouse, Lakehouse & Architecture"),
    30: ("pillar30-analytics-dashboards-visualization", "Analytics Deliverables, Dashboards & Visualization"),
}
RANGES = {26: (388, 407), 27: (408, 427), 28: (428, 447), 29: (448, 467), 30: (468, 487)}

ROW_RE = re.compile(
    r"^\|\s*(\d{3})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
    r"\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$"
)


def pillar_of(num: int) -> int:
    for p, (lo, hi) in RANGES.items():
        if lo <= num <= hi:
            return p
    raise ValueError(f"folder #{num} outside pillar 26-30 ranges")


def parse_architecture() -> dict:
    plan = {}
    for line in ARCH.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        num = int(m.group(1))
        if not 388 <= num <= 487:
            continue
        title = m.group(7)
        plan[num] = {
            "folder": m.group(2),
            "plan_keyword": m.group(3),
            "volume": int(m.group(4)),
            "kd": int(m.group(5)),
            "slug": m.group(6),
            "title": re.sub(r"\s*\*\*\(HUB\)\*\*", "", title).strip(),
            "is_hub": "(HUB)" in title,
            "sibling_links": m.group(8),
        }
    return plan


def article_stats(article: Path) -> tuple[str, int]:
    text = article.read_text(encoding="utf-8")
    h1 = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), "")
    body = text.split("## TL;DR", 1)[-1]
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    body = re.sub(r"[#>*`|_\-]+", " ", body)
    return h1, len(re.findall(r"[A-Za-z0-9']+", body))


def main() -> None:
    plan = parse_architecture()
    rows = []
    for num in sorted(plan):
        p = pillar_of(num)
        folder_name, pillar_name = PILLARS[p]
        info = plan[num]
        art_dir = BLOG / folder_name / info["folder"]
        meta_path = art_dir / "article-meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        article_md = art_dir / "article.md"
        h1, words = article_stats(article_md) if article_md.exists() else ("", 0)

        rows.append(
            {
                "pillar_no": p,
                "pillar_name": pillar_name,
                "pillar_folder": folder_name,
                "article_no": num,
                "article_type": "hub" if info["is_hub"] else "cluster",
                "target_keyword": meta.get("target_keyword") or info["plan_keyword"],
                "keyword_word_count": len((meta.get("target_keyword") or info["plan_keyword"]).split()),
                "plan_keyword": info["plan_keyword"],
                "search_volume": info["volume"],
                "keyword_difficulty": info["kd"],
                "secondary_keywords": "; ".join(meta.get("secondary", [])),
                "slug": info["slug"],
                "url": f"https://infinisynapse.com/en/blog/{info['slug']}",
                "h1_title": h1 or info["title"],
                "article_word_count": words,
            }
        )

    out = BLOG / "pillar26-30-keyword-inventory.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    summary = out.with_name("pillar26-30-keyword-summary.csv")
    with summary.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(
            ["pillar_no", "pillar_name", "articles", "keywords", "total_search_volume", "avg_kd", "avg_word_count"]
        )
        for p in sorted(PILLARS):
            group = [r for r in rows if r["pillar_no"] == p]
            w.writerow(
                [
                    p,
                    PILLARS[p][1],
                    len(group),
                    len({r["target_keyword"] for r in group}),
                    sum(r["search_volume"] for r in group),
                    round(sum(r["keyword_difficulty"] for r in group) / len(group), 1),
                    round(sum(r["article_word_count"] for r in group) / len(group)),
                ]
            )

    print(f"{len(rows)} rows -> {out.relative_to(ROOT)}")
    print(f"{len(PILLARS)} rows -> {summary.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
