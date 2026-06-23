#!/usr/bin/env python3
"""Generate blog-nav-tags.csv — Blog page filter pills for frontend."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"

# Must match generate-blog-index-master.py
NAV_META = [
    ("all", "All", "全部", "", 0, True),
    ("comparisons", "Comparisons & Alternatives", "对比与替代", "Comparisons", 1, True),
    ("knowledge", "Knowledge Base & Explainers", "知识科普与概念", "Guides", 2, True),
    ("connectors", "Data Connectors & Integrations", "数据连接与集成", "Connectors", 3, True),
    ("use_cases", "Use Cases & Industries", "角色与行业场景", "Use Cases", 4, True),
    ("excel_csv", "Excel & Spreadsheet AI", "Excel 与表格 AI", "Excel & CSV", 5, True),
    ("nl2sql", "NL2SQL & Text-to-SQL", "自然语言转 SQL", "NL2SQL", 6, True),
    ("tools_reviews", "Tools & Reviews", "工具与评测", "Tools & Reviews", 7, True),
    ("deep_dive", "Technical Deep Dives", "技术深度", "Deep Dive", 8, True),
    ("tutorials", "Tutorials & Best Practices", "教程与最佳实践", "Tutorials", 9, False),
]

CARD_TAG_BY_FILTER = {row[0]: row[3] for row in NAV_META if row[3]}


def load_counts() -> dict[str, int]:
    master = json.loads((BLOG / "blog-index-import-master.json").read_text(encoding="utf-8"))
    c = Counter(p["filter_category"] for p in master["posts"])
    return {"all": len(master["posts"]), **dict(c)}


def main() -> None:
    counts = load_counts()
    rows = []
    for key, en, zh, card, order, show in NAV_META:
        rows.append({
            "filter_category": key,
            "nav_label_en": en,
            "nav_label_zh": zh,
            "card_tag_default": card,
            "article_count_100": counts.get(key, 0),
            "nav_sort_order": order,
            "show_in_nav": "true" if show else "false",
            "notes": "隐藏：篇数过少，可合并到 Connectors" if key == "tutorials" and counts.get(key, 0) <= 2 else "",
        })

    fields = [
        "filter_category",
        "nav_label_en",
        "nav_label_zh",
        "card_tag_default",
        "article_count_100",
        "nav_sort_order",
        "show_in_nav",
        "notes",
    ]
    for path in (
        BLOG / "blog-nav-tags.csv",
        BLOG / "frontend-package" / "blog-nav-tags.csv",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote → {path}")

    print("\nCounts (100 articles):")
    for r in rows:
        if r["show_in_nav"] == "true":
            print(f"  {r['nav_label_en']} ({r['article_count_100']})")


if __name__ == "__main__":
    main()
