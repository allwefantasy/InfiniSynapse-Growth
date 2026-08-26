#!/usr/bin/env python3
"""Build hero + body table HTML for P21-25 articles."""
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR_STYLE = {
    "pillar21": {"accent": "#38bdf8", "accent2": "#2563eb", "glow": "rgba(56,189,248,0.22)"},
    "pillar22": {"accent": "#a78bfa", "accent2": "#6d28d9", "glow": "rgba(167,139,250,0.22)"},
    "pillar23": {"accent": "#34d399", "accent2": "#059669", "glow": "rgba(52,211,153,0.22)"},
    "pillar24": {"accent": "#f59e0b", "accent2": "#d97706", "glow": "rgba(245,158,11,0.22)"},
    "pillar25": {"accent": "#818cf8", "accent2": "#4f46e5", "glow": "rgba(129,140,248,0.22)"},
}

SVG_VARIANTS = [
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <circle cx="210" cy="210" r="150" fill="none" stroke="ACCENT" stroke-width="2" opacity="0.5"/>
      <circle cx="210" cy="210" r="95" fill="none" stroke="ACCENT2" stroke-width="2" opacity="0.7"/>
      <circle cx="210" cy="210" r="40" fill="ACCENT" opacity="0.35"/>
      <line x1="60" y1="210" x2="360" y2="210" stroke="ACCENT" stroke-width="1.5" opacity="0.4"/>
      <line x1="210" y1="60" x2="210" y2="360" stroke="ACCENT" stroke-width="1.5" opacity="0.4"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <rect x="70" y="250" width="55" height="110" rx="6" fill="ACCENT" opacity="0.55"/>
      <rect x="140" y="190" width="55" height="170" rx="6" fill="ACCENT2" opacity="0.65"/>
      <rect x="210" y="140" width="55" height="220" rx="6" fill="ACCENT" opacity="0.75"/>
      <rect x="280" y="200" width="55" height="160" rx="6" fill="ACCENT2" opacity="0.5"/>
      <circle cx="350" cy="90" r="28" fill="ACCENT" opacity="0.3"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <polygon points="210,50 360,320 60,320" fill="none" stroke="ACCENT" stroke-width="2" opacity="0.55"/>
      <polygon points="210,110 300,290 120,290" fill="ACCENT2" opacity="0.18"/>
      <circle cx="210" cy="200" r="18" fill="ACCENT" opacity="0.8"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <path d="M60 300 Q140 80 210 220 T360 120" fill="none" stroke="ACCENT" stroke-width="3" opacity="0.7"/>
      <circle cx="60" cy="300" r="8" fill="ACCENT2"/>
      <circle cx="210" cy="220" r="8" fill="ACCENT"/>
      <circle cx="360" cy="120" r="8" fill="ACCENT2"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <rect x="100" y="100" width="220" height="220" rx="24" fill="none" stroke="ACCENT" stroke-width="2" opacity="0.5" transform="rotate(12 210 210)"/>
      <rect x="130" y="130" width="160" height="160" rx="18" fill="ACCENT2" opacity="0.2" transform="rotate(-8 210 210)"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <line x1="210" y1="80" x2="120" y2="300" stroke="ACCENT" stroke-width="2" opacity="0.5"/>
      <line x1="210" y1="80" x2="300" y2="300" stroke="ACCENT" stroke-width="2" opacity="0.5"/>
      <line x1="120" y1="300" x2="300" y2="300" stroke="ACCENT2" stroke-width="2" opacity="0.5"/>
      <circle cx="210" cy="80" r="22" fill="ACCENT" opacity="0.6"/>
      <circle cx="120" cy="300" r="22" fill="ACCENT2" opacity="0.6"/>
      <circle cx="300" cy="300" r="22" fill="ACCENT" opacity="0.6"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <ellipse cx="210" cy="210" rx="160" ry="90" fill="none" stroke="ACCENT" stroke-width="2" opacity="0.45"/>
      <ellipse cx="210" cy="210" rx="90" ry="160" fill="none" stroke="ACCENT2" stroke-width="2" opacity="0.45"/>
    </svg>""",
    """<svg viewBox="0 0 420 420" width="420" height="420">
      <rect x="80" y="80" width="70" height="70" rx="10" fill="ACCENT" opacity="0.45"/>
      <rect x="170" y="80" width="70" height="70" rx="10" fill="ACCENT2" opacity="0.35"/>
      <rect x="260" y="80" width="70" height="70" rx="10" fill="ACCENT" opacity="0.55"/>
      <rect x="125" y="170" width="70" height="70" rx="10" fill="ACCENT2" opacity="0.5"/>
      <rect x="215" y="170" width="70" height="70" rx="10" fill="ACCENT" opacity="0.4"/>
    </svg>""",
]


def pillar_key(path: Path) -> str:
    return path.parts[-3][:8] if len(path.parts) >= 3 else "pillar21"


def kicker_from_folder(folder: str, h1: str) -> str:
    n = folder.lower()
    if "complete-guide" in n or n.endswith("-guide"):
        return "Guide · 2026"
    if "definition" in n:
        return "Definition"
    if "-vs-" in n or "vs-" in n:
        return "Comparison"
    if "salary" in n or "pay" in n:
        return "Salary · 2026"
    if "interview" in n:
        return "Interview Prep"
    if "resume" in n:
        return "Career Guide"
    if "bootcamp" in n or "course" in n or "certification" in n or "certificate" in n or "training" in n or "degree" in n:
        return "Learning Guide"
    if "example" in n:
        return "Examples"
    if "process" in n:
        return "Process"
    if "types" in n:
        return "Framework"
    if "tool" in n or "software" in n or "platform" in n or "excel" in n or "tableau" in n:
        return "Tools · 2026"
    if "job" in n or "internship" in n or "career" in n:
        return "Career · 2026"
    if "method" in n or "technique" in n:
        return "Methods"
    if "what-is" in n or "what-" in n:
        return "Explainer · 2026"
    return "Guide · 2026"


def title_font_size(title: str) -> int:
    n = len(title)
    if n <= 42:
        return 42
    if n <= 55:
        return 36
    if n <= 68:
        return 32
    return 28


def hero_html(title: str, kicker: str, style: dict, variant_idx: int) -> str:
    fs = title_font_size(title)
    svg = SVG_VARIANTS[variant_idx % len(SVG_VARIANTS)]
    svg = svg.replace("ACCENT2", style["accent2"]).replace("ACCENT", style["accent"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
body {{
  width: 1200px; height: 630px; margin: 0; padding: 0; overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: linear-gradient(135deg, #070b14 0%, #0f172a 55%, #151030 100%);
  color: #f1f5f9;
}}
.wrap {{
  width: 100%; height: 100%;
  display: grid;
  grid-template-columns: 54% 46%;
}}
.left {{
  padding: 56px 48px 56px 64px;
  display: flex; flex-direction: column; justify-content: space-between;
}}
.kicker {{
  font-size: 13px; font-weight: 700; letter-spacing: 0.14em;
  text-transform: uppercase; color: {style["accent"]};
}}
h1 {{
  margin: 20px 0 0; font-size: {fs}px; line-height: 1.12; font-weight: 700;
  color: #f1f5f9; text-shadow: 0 2px 24px rgba(0,0,0,0.45);
  max-width: 620px;
}}
.brand {{
  font-size: 14px; font-weight: 600; letter-spacing: 0.06em;
  color: #94a3b8;
}}
.right {{
  position: relative;
  background:
    radial-gradient(ellipse 500px 380px at 60% 45%, {style["glow"]}, transparent 70%),
    linear-gradient(180deg, rgba(255,255,255,0.02), transparent);
  border-left: 1px solid rgba(255,255,255,0.06);
}}
.grid {{
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 40px 40px; opacity: 0.35;
}}
.art {{
  position: absolute; right: 24px; top: 50%; transform: translateY(-50%);
  filter: drop-shadow(0 0 40px {style["glow"]});
}}
</style>
</head>
<body>
<div class="wrap">
  <div class="left">
    <div>
      <div class="kicker">{html.escape(kicker)}</div>
      <h1>{html.escape(title)}</h1>
    </div>
    <div class="brand">InfiniSynapse</div>
  </div>
  <div class="right">
    <div class="grid"></div>
    <div class="art">{svg}</div>
  </div>
</div>
</body>
</html>
"""


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


def score_table(t: dict) -> int:
    h = " ".join(t["header"]).lower()
    score = len(t["rows"]) * len(t["header"])
    bonus_words = (
        "factor", "check", "type", "tool", "step", "skill", "role", "salary",
        "course", "certification", "comparison", "guide", "method", "feature",
        "level", "format", "cost", "focus", "question", "industry",
    )
    for w in bonus_words:
        if w in h:
            score += 8
    if len(t["rows"]) >= 4:
        score += 10
    return score


def pick_table(tables: list[dict]) -> dict | None:
    if not tables:
        return None
    return max(tables, key=score_table)


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


def hero_image_name(text: str) -> str:
    m = re.search(r"!\[[^\]]*\]\(\./images/(hero-[^)]+\.png)\)", text)
    if not m:
        raise ValueError("missing hero image ref")
    return m.group(1)


def table_image_slug(folder: str) -> str:
    return f"table-{folder}.png"


def iter_articles():
    for art in sorted(BLOG.glob("pillar2[1-5]-*/[0-9][0-9][0-9]-*/article.md")):
        yield art


def build_heroes() -> int:
    n = 0
    for i, art in enumerate(iter_articles()):
        folder = art.parent.name
        text = art.read_text(encoding="utf-8")
        title = read_h1(text)
        pk = pillar_key(art)
        style = PILLAR_STYLE.get(pk, PILLAR_STYLE["pillar21"])
        kicker = kicker_from_folder(folder, title)
        out = art.parent / "visuals" / "hero.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(hero_html(title, kicker, style, i), encoding="utf-8")
        n += 1
    print(f"Built {n} hero.html files")
    return n


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
        block = [
            "",
            f"![{alt}]({marker.replace('./', './')})",
            "",
        ]
        new_lines = lines[:insert_at] + block + lines[insert_at:]
        art.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        n += 1
    print(f"Inserted table images in {n} articles")
    return n


def main() -> int:
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("heroes", "all"):
        build_heroes()
    if cmd in ("tables", "all"):
        build_tables()
    if cmd in ("insert", "all"):
        insert_table_images()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
