#!/usr/bin/env python3
"""Generate hero HTML for pillars from articles_registry.json."""
import importlib.util
import json
import sys
from pathlib import Path

BLOG = Path(__file__).parent

spec = importlib.util.spec_from_file_location(
    "p3vis", BLOG / "pillar3-ai-analyst-tools" / "build-visuals.py"
)
p3vis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p3vis)

spec2 = importlib.util.spec_from_file_location(
    "scaffold", BLOG / "scaffold-pillar-from-registry.py"
)
scaffold = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(scaffold)


def main() -> int:
    targets = sys.argv[1:] or [
        "pillar4-data-source-connectors",
        "pillar5-nl2sql-text-to-sql",
        "pillar6-ai-excel-csv-spreadsheet",
        "pillar7-use-cases-role-industry",
        "pillar8-skills-templates-glossary",
    ]
    total = 0
    for name in targets:
        pillar = BLOG / name
        reg_path = pillar / "articles_registry.json"
        if not reg_path.exists():
            print(f"SKIP {name}")
            continue
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        for i, art in enumerate(reg["articles"]):
            folder = art["folder"]
            title = scaffold.title_from_theme(art["theme"], art["kicker"])
            kicker = art.get("kicker", "Guide · 2026")
            variant = i % len(p3vis.SVG_VARIANTS)
            html = p3vis.hero_cover(title, kicker, variant)
            out = pillar / folder / "visuals" / "hero.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            total += 1
        print(f"  {name}: {len(reg['articles'])} heroes")
    print(f"Built {total} hero HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
