#!/usr/bin/env python3
"""Scaffold article folders 101–202 from SEO/Blog/blog-next-topics-plan.csv."""
from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PLAN = BLOG / "blog-next-topics-plan.csv"
REF_PREVIEW = BLOG / "pillar3-ai-analyst-tools" / "build-preview.py"

PILLAR_MAP = {
    "Pillar 1 · AI-Native": "pillar1-ai-native-data-analysis",
    "Pillar 3 · Tools/Alternatives": "pillar3-ai-analyst-tools",
    "Pillar 5 · NL2SQL": "pillar5-nl2sql-text-to-sql",
    "Pillar 7 · Use Cases/Channel": "pillar7-use-cases-role-industry",
    "Pillar 9 · Semantic Layer": "pillar9-semantic-layer",
    "Pillar 10 · MCP": "pillar10-mcp-data-access",
    "Pillar 11 · Agentic Analytics": "pillar11-agentic-analytics",
    "Pillar 12 · Data Trends": "pillar12-data-trends",
    "Pillar 13 · Data Privacy & Security": "pillar13-data-privacy-security",
    "Pillar 14 · Enterprise Data": "pillar14-enterprise-data",
    "Pillar 15 · Data Search": "pillar15-data-search",
}

HUB_IDS = {"120", "127", "136", "145", "156", "178", "191"}


def hero_name(slug: str) -> str:
    return f"hero-{slug}.png"


def stub_readme(row: dict, pillar_folder: str) -> str:
    return f"""# {row['编号']} · {row['title']} — Deliverable Bundle

**Article ID**: {row['编号']}
**Slug**: `/blog/{row['slug']}`
**Primary keyword**: `{row['关键词']}`
**Pillar**: {row['Pillar主题']}
**Priority**: {row['优先级']}

## Files

- `article.md` — Long-form article (1900–2800 words)
- `meta-tags.html` — SEO + OG tags
- `schema.json` — BlogPosting + FAQPage
- `images/{hero_name(row['slug'])}` — Hero cover 1200×630

## Gates

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/audit-wordcount.py" SEO/Blog/{pillar_folder}/{row['编号']}-{row['slug']}
python3 "$S/audit-outline-structure.py" SEO/Blog/{pillar_folder}
```
"""


def main() -> int:
    rows = list(csv.DictReader(PLAN.open(encoding="utf-8-sig")))
    by_pillar: dict[str, list[dict]] = {}
    for row in rows:
        pf = PILLAR_MAP[row["Pillar主题"]]
        by_pillar.setdefault(pf, []).append(row)

    for pillar_folder, articles in by_pillar.items():
        root = BLOG / pillar_folder
        root.mkdir(parents=True, exist_ok=True)
        if REF_PREVIEW.exists() and not (root / "build-preview.py").exists():
            shutil.copy2(REF_PREVIEW, root / "build-preview.py")

        registry = {
            "pillar": pillar_folder,
            "generated": "2026-06-23",
            "source_plan": "blog-next-topics-plan.csv",
            "articles": [
                {
                    "id": r["编号"],
                    "folder": f"{r['编号']}-{r['slug']}",
                    "slug": r["slug"],
                    "keyword": r["关键词"],
                    "title": r["title"],
                    "priority": r["优先级"],
                    "is_hub": r["编号"] in HUB_IDS or "Hub" in r.get("备注", ""),
                }
                for r in articles
            ],
        }
        (root / "articles_registry.json").write_text(
            json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        index_lines = [
            f"# {pillar_folder}",
            "",
            f"> Articles {articles[0]['编号']}–{articles[-1]['编号']} · blog-next-topics-plan.csv",
            "",
            "| ID | Folder | Slug | Keyword | Priority |",
            "|---|---|---|---|---|",
        ]
        for r in articles:
            index_lines.append(
                f"| {r['编号']} | [{r['编号']}-{r['slug']}](./{r['编号']}-{r['slug']}/) "
                f"| `/blog/{r['slug']}` | {r['关键词']} | {r['优先级']} |"
            )
        (root / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

        for r in articles:
            adir = root / f"{r['编号']}-{r['slug']}"
            (adir / "images").mkdir(parents=True, exist_ok=True)
            (adir / "visuals").mkdir(parents=True, exist_ok=True)
            gitkeep = adir / "images" / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.write_text("", encoding="utf-8")
            readme = adir / "README.md"
            if not readme.exists():
                readme.write_text(stub_readme(r, pillar_folder), encoding="utf-8")

        print(f"  {pillar_folder}: {len(articles)} folders")

    print(f"Done. {len(rows)} article folders across {len(by_pillar)} pillars.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
