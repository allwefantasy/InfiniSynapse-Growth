#!/usr/bin/env python3
"""Build body table visuals for Pillars 26-30: HTML templates + insert image refs in article.md."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))


def parse_md_tables(text: str) -> list[dict]:
    tables: list[dict] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and re.match(
            r"^\|[-: |]+\|$", lines[i + 1].strip()
        ):
            start = i
            header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            tables.append({"start": start, "header": header, "rows": rows})
        else:
            i += 1
    return tables


def is_scorecard(t: dict) -> bool:
    h = [c.lower() for c in t["header"]]
    return len(h) == 2 and "check" in h[0] and "pass" in h[1]


def is_cluster_index(t: dict) -> bool:
    h = " ".join(t["header"]).lower()
    return "guide" in h and "focus" in h and len(t["rows"]) >= 10


def score_table(t: dict) -> int:
    if is_scorecard(t) or is_cluster_index(t):
        return -1
    h = " ".join(t["header"]).lower()
    score = len(t["rows"]) * len(t["header"])
    bonus_words = (
        "factor", "check", "type", "tool", "step", "skill", "role", "capability",
        "layer", "question", "comparison", "model", "architecture", "dimension",
        "level", "format", "focus", "stage", "component", "offering", "category",
        "origin", "fit", "stores", "framework",
    )
    for w in bonus_words:
        if w in h:
            score += 8
    if 3 <= len(t["rows"]) <= 8:
        score += 10
    if len(t["header"]) >= 3:
        score += 6
    return score


def pick_table(tables: list[dict]) -> dict | None:
    candidates = [t for t in tables if score_table(t) >= 0]
    if not candidates:
        return None
    return max(candidates, key=score_table)


def table_visual_html(title: str, header: list[str], rows: list[list[str]]) -> str:
    ths = "".join(f"<th>{html.escape(c)}</th>" for c in header)
    trs = []
    for r in rows:
        cells = r + [""] * (len(header) - len(r))
        tds = "".join(f"<td>{html.escape(c)}</td>" for c in cells[: len(header)])
        trs.append(f"<tr>{tds}</tr>")
    body = "\n".join(trs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
body {{
  width: 1200px; height: 720px; margin: 0; padding: 32px 40px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
  color: #0f172a;
}}
.cap {{
  font-size: 28px; font-weight: 700; margin: 0 0 20px; color: #1e3a8a;
}}
.sheet {{
  background: #fff; border-radius: 12px; overflow: hidden;
  box-shadow: 0 8px 32px rgba(30,58,138,0.12);
  border: 1px solid #dbeafe;
}}
table {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
th {{
  background: linear-gradient(180deg, #1e3a8a, #1e40af);
  color: #e0f2fe; text-align: left; padding: 14px 16px; font-weight: 600;
}}
td {{
  padding: 12px 16px; border-bottom: 1px solid #e2e8f0; vertical-align: top;
  line-height: 1.45;
}}
tr:nth-child(even) td {{ background: #f8fafc; }}
tr:last-child td {{ border-bottom: none; }}
.foot {{
  margin-top: 14px; font-size: 13px; color: #64748b;
}}
</style>
</head>
<body>
<div class="cap">{html.escape(title)}</div>
<div class="sheet">
<table>
<thead><tr>{ths}</tr></thead>
<tbody>
{body}
</tbody>
</table>
</div>
<div class="foot">InfiniSynapse · Reference data table · 2026</div>
</body>
</html>
"""


def read_h1(text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.M)
    if not m:
        raise ValueError("missing H1")
    return m.group(1).strip()


def table_image_slug(folder: str) -> str:
    return f"table-{folder}.png"


def iter_articles():
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            yield art


def build_tables() -> int:
    n = 0
    for art in iter_articles():
        folder = art.parent.name
        text = art.read_text(encoding="utf-8")
        title = read_h1(text)
        tables = parse_md_tables(text)
        chosen = pick_table(tables)
        if not chosen:
            continue
        slug = table_image_slug(folder)
        out = art.parent / "visuals" / slug.replace(".png", ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        cap = title if len(title) <= 72 else title[:69] + "..."
        out.write_text(
            table_visual_html(cap, chosen["header"], chosen["rows"]),
            encoding="utf-8",
        )
        n += 1
    print(f"Built {n} table HTML files")
    return n


def insert_table_images() -> int:
    n = 0
    for art in iter_articles():
        folder = art.parent.name
        text = art.read_text(encoding="utf-8")
        slug = table_image_slug(folder)
        marker = f"./images/{slug}"
        if marker in text:
            continue
        tables = parse_md_tables(text)
        chosen = pick_table(tables)
        if not chosen:
            continue
        lines = text.splitlines()
        insert_at = chosen["start"]
        h = " ".join(chosen["header"][:2]).lower()
        alt = f"Visual data table: {h}" if h else f"Visual reference table for {folder}"
        block = ["", f"![{alt}]({marker})", ""]
        new_lines = lines[:insert_at] + block + lines[insert_at:]
        art.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        n += 1
    print(f"Inserted table images in {n} articles")
    return n


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("tables", "all"):
        build_tables()
    if cmd in ("insert", "all"):
        insert_table_images()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
