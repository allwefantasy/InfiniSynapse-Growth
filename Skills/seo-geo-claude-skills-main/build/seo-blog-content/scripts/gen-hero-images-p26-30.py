#!/usr/bin/env python3
"""Generate hero PNGs (1200x630) + og-cover copies for Pillars 26-30 from article.md alt text + H1.

Mirrors gen-hero-images-p21-25.py: self-contained PIL renderer (no external API).
Each article gets images/hero-<slug>.png plus a byte-identical images/og-cover.png,
matching the og:image / twitter:image references written into meta-tags.html.
"""
from __future__ import annotations

import hashlib
import random
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SIZE = (1200, 630)

PILLAR_THEMES = {
    "pillar26": {
        "label": "Data Governance & Quality",
        "bg": (14, 30, 38),
        "bg2": (18, 74, 80),
        "accent": (45, 212, 191),
        "accent2": (94, 234, 212),
    },
    "pillar27": {
        "label": "Master Data & Metadata",
        "bg": (26, 18, 44),
        "bg2": (72, 40, 120),
        "accent": (168, 85, 247),
        "accent2": (216, 180, 254),
    },
    "pillar28": {
        "label": "Data Engineering & Pipelines",
        "bg": (10, 24, 44),
        "bg2": (22, 60, 110),
        "accent": (59, 130, 246),
        "accent2": (147, 197, 253),
    },
    "pillar29": {
        "label": "Warehouse, Lake & Lakehouse",
        "bg": (8, 32, 40),
        "bg2": (14, 80, 92),
        "accent": (34, 211, 238),
        "accent2": (103, 232, 249),
    },
    "pillar30": {
        "label": "Analytics & Visualization",
        "bg": (34, 14, 40),
        "bg2": (110, 28, 90),
        "accent": (244, 114, 182),
        "accent2": (249, 168, 212),
    },
}


def load_fonts() -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    bold = regular = None
    for p in candidates:
        if Path(p).is_file():
            if "Bold" in p or bold is None:
                try:
                    bold = ImageFont.truetype(p, 46)
                except OSError:
                    pass
            if "Bold" not in p:
                try:
                    regular = ImageFont.truetype(p, 24)
                except OSError:
                    pass
    if bold is None:
        bold = ImageFont.load_default()
    if regular is None:
        regular = ImageFont.load_default()
    small = regular
    try:
        small = ImageFont.truetype(candidates[1] if Path(candidates[1]).is_file() else candidates[0], 18)
    except OSError:
        small = regular
    return bold, regular, small


def parse_article(article_path: Path) -> tuple[str, str, str]:
    text = article_path.read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    img = re.search(r"!\[([^\]]*)\]\(\./images/([^)]+)\)", text)
    title = h1.group(1).strip() if h1 else article_path.parent.name
    alt = img.group(1).strip() if img else title
    filename = img.group(2).strip() if img else "hero.png"
    return title, alt, filename


def theme_for(pillar_name: str) -> dict:
    key = pillar_name[:8]
    return PILLAR_THEMES.get(key, PILLAR_THEMES["pillar26"])


def gradient_bg(w: int, h: int, c1: tuple[int, int, int], c2: tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGB", (w, h), c1)
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return base


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines[:3]


def seed_from(name: str) -> random.Random:
    h = hashlib.md5(name.encode()).hexdigest()
    return random.Random(int(h[:8], 16))


def draw_decor(w: int, h: int, accent: tuple, accent2: tuple, rng: random.Random, pattern: int) -> Image.Image:
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    if pattern == 0:
        for i in range(8):
            x0 = 620 + i * 55
            bh = rng.randint(60, 220)
            od.rectangle([x0, 380 - bh, x0 + 36, 380], fill=accent + (140,))
        od.line([(600, 400), (1050, 400)], fill=accent2 + (180,), width=2)
    elif pattern == 1:
        for _ in range(35):
            x, y = rng.randint(580, 1120), rng.randint(120, 500)
            r = rng.randint(4, 10)
            od.ellipse([x - r, y - r, x + r, y + r], fill=accent2 + (rng.randint(80, 160),))
        od.line([(600, 300), (900, 180), (1100, 320)], fill=accent + (200,), width=3)
    elif pattern == 2:
        for i in range(6):
            y = 140 + i * 55
            od.line([(640, y), (rng.randint(900, 1100), y + rng.randint(-30, 30))], fill=accent + (120,), width=2)
        for i in range(5):
            od.rectangle([700 + i * 70, 420, 740 + i * 70, 460], outline=accent2 + (160,), width=2)
    elif pattern == 3:
        cx, cy = 880, 290
        for i in range(5):
            radius = 40 + i * 38
            od.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=accent + (90,), width=2)
    elif pattern == 4:
        pts = [(650, 420), (760, 260), (900, 350), (1020, 200), (1100, 380)]
        od.polygon(pts, outline=accent2 + (200,), fill=accent + (40,))
        for px, py in pts:
            od.ellipse([px - 6, py - 6, px + 6, py + 6], fill=accent2 + (220,))
    elif pattern == 5:
        for row in range(4):
            for col in range(7):
                x = 650 + col * 55
                y = 160 + row * 70
                fill = accent if (row + col) % 2 == 0 else accent2
                od.rectangle([x, y, x + 40, y + 50], fill=fill + (rng.randint(50, 110),))
    else:
        for i in range(12):
            x1, y1 = rng.randint(620, 1080), rng.randint(140, 440)
            x2, y2 = rng.randint(620, 1080), rng.randint(140, 440)
            od.line([(x1, y1), (x2, y2)], fill=accent + (60,), width=1)
        od.rectangle([700, 180, 1080, 460], outline=accent2 + (140,), width=2)

    return overlay


def render_hero(title: str, alt: str, pillar_name: str, folder_name: str) -> Image.Image:
    theme = theme_for(pillar_name)
    w, h = SIZE
    img = gradient_bg(w, h, theme["bg"], theme["bg2"])

    rng = seed_from(folder_name)
    pattern = rng.randint(0, 6)
    overlay = draw_decor(w, h, theme["accent"], theme["accent2"], rng, pattern)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    bold, regular, small = load_fonts()

    draw.rounded_rectangle([48, 48, 360, 92], radius=18, fill=theme["accent"] + (40,), outline=theme["accent"], width=2)
    draw.text((64, 58), theme["label"], fill=theme["accent2"], font=small)

    title_lines = wrap_text(title, bold, 680, draw)
    y = 130
    for line in title_lines:
        draw.text((64, y), line, fill=(248, 250, 252), font=bold)
        y += 54

    alt_short = alt if len(alt) <= 120 else alt[:117] + "..."
    sub_lines = wrap_text(alt_short, regular, 700, draw)
    y = max(y + 10, 300)
    for line in sub_lines:
        draw.text((64, y), line, fill=(203, 213, 225), font=regular)
        y += 32

    draw.rounded_rectangle([48, h - 72, 290, h - 28], radius=14, fill=(15, 23, 42))
    draw.text((68, h - 62), "InfiniSynapse Data Team", fill=(148, 163, 184), font=small)
    draw.text((w - 210, h - 62), "2026 Guide", fill=theme["accent2"], font=small)

    return img


def main() -> int:
    created = skipped = copies = 0
    pillars = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))
    for pillar in pillars:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            title, alt, filename = parse_article(art)
            out_dir = art.parent / "images"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / filename
            og_path = out_dir / "og-cover.png"
            if out_path.is_file() and out_path.stat().st_size > 8000:
                skipped += 1
            else:
                hero = render_hero(title, alt, pillar.name, art.parent.name)
                hero.save(out_path, format="PNG", optimize=True)
                created += 1
                print(f"OK {art.parent.name} -> images/{filename} ({out_path.stat().st_size // 1024}KB)")
            if not og_path.is_file() or og_path.stat().st_size < 8000:
                shutil.copyfile(out_path, og_path)
                copies += 1
    print(f"\nCreated: {created} | Skipped (existing): {skipped} | og-cover copies: {copies}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
