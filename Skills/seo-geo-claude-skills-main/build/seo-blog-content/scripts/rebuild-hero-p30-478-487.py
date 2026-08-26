#!/usr/bin/env python3
"""Rebuild Pillar 30 heroes for folders 478–487: text-free BG + clear PIL title.

Fixes double titles caused by AI-baked typography in .hero-bg plus a second
PIL overlay. Follows blog-hero-cover-spec.md:
  - exact H1 only (no subtitle paragraph)
  - kicker + brand
  - 1200×630
  - left title block on calm dark area; right abstract geometry
"""
from __future__ import annotations

import math
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR = BLOG / "pillar30-analytics-dashboards-visualization"
SIZE = (1200, 630)
FOLDERS = (
    "478-tableau-data-visualization",
    "479-data-dashboard",
    "480-sql-data-analytics",
    "481-data-visualization-programming",
    "482-data-analytics-platforms",
    "483-data-analytics-platform",
    "484-data-visualization-examples",
    "485-what-is-data-visualization",
    "486-define-analytics",
    "487-data-visualization-services",
)

ACCENT = (244, 114, 182)  # pillar30 rose
BG_DEEP = (7, 11, 20)
BG_MID = (15, 23, 42)
BG_PANEL = (12, 18, 36)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
    )
    for p in paths:
        if Path(p).is_file():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def parse_h1_and_hero(article: Path) -> tuple[str, str]:
    text = article.read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    img = re.search(r"!\[([^\]]*)\]\(\./images/([^)]+)\)", text)
    title = h1.group(1).strip() if h1 else article.parent.name
    filename = img.group(2).strip() if img else f"hero-{article.parent.name.split('-', 1)[-1]}.png"
    return title, filename


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    if not words:
        return [text]
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def title_font_size(title: str) -> int:
    n = len(title)
    if n <= 36:
        return 46
    if n <= 48:
        return 40
    if n <= 62:
        return 34
    return 30


def gradient_bg() -> Image.Image:
    w, h = SIZE
    img = Image.new("RGB", SIZE, BG_DEEP)
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        r = int(BG_DEEP[0] * (1 - t) + BG_MID[0] * t)
        g = int(BG_DEEP[1] * (1 - t) + BG_MID[1] * t)
        b = int(BG_DEEP[2] * (1 - t) + BG_MID[2] * t)
        for x in range(w):
            # slight horizontal drift toward magenta on the right
            u = x / (w - 1)
            rr = min(255, int(r + 18 * u))
            gg = min(255, int(g + 4 * u))
            bb = min(255, int(b + 22 * u))
            px[x, y] = (rr, gg, bb)
    return img


def draw_variant(draw: ImageDraw.ImageDraw, variant: int, accent: tuple[int, int, int]) -> None:
    """Wordless geometry on the right ~46% — unique per article index."""
    w, h = SIZE
    ox = int(w * 0.54)
    ar, ag, ab = accent

    # subtle grid
    for i in range(0, w - ox, 36):
        x = ox + i
        draw.line([(x, 40), (x, h - 40)], fill=(ar, ag, ab, 28), width=1)
    for j in range(0, h, 36):
        draw.line([(ox, j), (w - 24, j)], fill=(ar, ag, ab, 22), width=1)

    if variant % 5 == 0:
        # bars
        base_y = h - 90
        heights = [80, 140, 110, 190, 160, 220, 130, 170]
        bw = 28
        gap = 18
        x0 = ox + 70
        for i, ht in enumerate(heights):
            x = x0 + i * (bw + gap)
            draw.rounded_rectangle(
                [x, base_y - ht, x + bw, base_y],
                radius=6,
                fill=(ar, ag, ab, 140 + (i % 3) * 20),
            )
        draw.line([(ox + 50, base_y), (w - 50, base_y)], fill=(255, 255, 255, 50), width=2)
    elif variant % 5 == 1:
        # nodes / network
        pts = [
            (ox + 90, 160),
            (ox + 220, 120),
            (ox + 340, 180),
            (ox + 160, 280),
            (ox + 300, 320),
            (ox + 420, 260),
            (ox + 250, 420),
        ]
        for a, b in [(0, 1), (1, 2), (0, 3), (3, 4), (2, 5), (4, 6), (5, 6), (1, 4)]:
            draw.line([pts[a], pts[b]], fill=(ar, ag, ab, 110), width=2)
        for x, y in pts:
            draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(ar, ag, ab, 200))
            draw.ellipse([x - 16, y - 16, x + 16, y + 16], outline=(ar, ag, ab, 70), width=2)
    elif variant % 5 == 2:
        # arcs / rings
        cx, cy = ox + 240, h // 2
        for i, rad in enumerate((60, 110, 160, 210)):
            bbox = [cx - rad, cy - rad, cx + rad, cy + rad]
            draw.arc(bbox, start=200 + i * 12, end=480 - i * 8, fill=(ar, ag, ab, 90 + i * 20), width=4)
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(ar, ag, ab, 210))
    elif variant % 5 == 3:
        # scatter + trend
        import random

        rng = random.Random(variant * 17 + 3)
        pts = []
        for i in range(14):
            x = ox + 80 + i * 28 + rng.randint(-6, 6)
            y = 420 - int(i * 16) + rng.randint(-40, 40)
            y = max(100, min(h - 100, y))
            pts.append((x, y))
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(ar, ag, ab, 190))
        draw.line(pts, fill=(ar, ag, ab, 120), width=3)
    else:
        # stacked layers / platform blocks
        y = 140
        for i, ww in enumerate((360, 300, 240, 180)):
            x = ox + 80 + i * 20
            draw.rounded_rectangle(
                [x, y, x + ww, y + 56],
                radius=10,
                fill=(ar, ag, ab, 70 + i * 25),
                outline=(ar, ag, ab, 140),
                width=2,
            )
            y += 70


def build_clean_bg(variant: int) -> Image.Image:
    base = gradient_bg().convert("RGBA")
    # right-side glow
    bloom = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    cx, cy = int(SIZE[0] * 0.72), SIZE[1] // 2
    for i in range(24, 0, -1):
        a = int(2 + (24 - i) * 1.6)
        bd.ellipse(
            [cx - 18 * i, cy - 14 * i, cx + 18 * i, cy + 14 * i],
            fill=(*ACCENT, min(a, 40)),
        )
    bloom = bloom.filter(ImageFilter.GaussianBlur(radius=28))
    composed = Image.alpha_composite(base, bloom)

    geo = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw_variant(ImageDraw.Draw(geo), variant, ACCENT)
    composed = Image.alpha_composite(composed, geo)

    # left calm panel (opaque) — guarantees no leftover AI text ever shows
    panel = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    split = int(SIZE[0] * 0.56)
    for x in range(split + 80):
        if x < split:
            alpha = 245
        else:
            alpha = int(245 * (1 - (x - split) / 80))
        pd.line([(x, 0), (x, SIZE[1])], fill=(*BG_PANEL, alpha))
    composed = Image.alpha_composite(composed, panel)
    return composed.convert("RGB")


def overlay_title(bg: Image.Image, title: str) -> Image.Image:
    w, h = SIZE
    composed = bg.convert("RGBA")
    draw = ImageDraw.Draw(composed)

    # Year lives in H1 when present — kicker stays type-only to avoid "2026" twice
    kicker = "GUIDE"
    kicker_font = load_font(18, bold=True)
    brand_font = load_font(18, bold=False)
    tsize = title_font_size(title)
    bold = load_font(tsize, bold=True)

    left = 64
    max_title_w = int(w * 0.50)
    lines = wrap_text(title, bold, max_title_w, draw)
    if len(lines) > 4:
        tsize = max(28, tsize - 6)
        bold = load_font(tsize, bold=True)
        lines = wrap_text(title, bold, max_title_w, draw)
    lines = lines[:4]
    line_gap = int(tsize * 1.22)

    # kicker
    ky = 150
    draw.text((left, ky), kicker, fill=(*ACCENT, 255), font=kicker_font)

    # title — white, left aligned, single block (no subtitle)
    y = ky + 36
    for line in lines:
        # soft glow
        for r, a in ((10, 45), (4, 80)):
            glow = Image.new("RGBA", SIZE, (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.text((left, y), line, fill=(*ACCENT, a), font=bold)
            composed = Image.alpha_composite(
                composed, glow.filter(ImageFilter.GaussianBlur(radius=r))
            )
        draw = ImageDraw.Draw(composed)
        draw.text((left, y), line, fill=(241, 245, 249, 255), font=bold)
        y += line_gap

    # brand bottom-left only (no "Data Team" pill, no duplicate year stamp)
    brand = "InfiniSynapse"
    by = h - 56
    draw.text((left, by), brand, fill=(203, 213, 225, 230), font=brand_font)
    bw = draw.textlength(brand, font=brand_font)
    draw.line([(left, by + 22), (left + bw, by + 22)], fill=(*ACCENT, 200), width=2)

    return composed.convert("RGB")


def main() -> int:
    updated = 0
    for i, folder in enumerate(FOLDERS):
        art_dir = PILLAR / folder
        article = art_dir / "article.md"
        if not article.is_file():
            print(f"SKIP missing {folder}")
            continue
        title, filename = parse_h1_and_hero(article)
        img_dir = art_dir / "images"
        img_dir.mkdir(parents=True, exist_ok=True)
        hero_path = img_dir / filename
        bg_dir = img_dir / ".hero-bg"
        bg_dir.mkdir(parents=True, exist_ok=True)
        bg_path = bg_dir / filename

        clean = build_clean_bg(variant=i)
        clean.save(bg_path, format="PNG", optimize=True)

        out = overlay_title(clean, title)
        out.save(hero_path, format="PNG", optimize=True)
        shutil.copyfile(hero_path, img_dir / "og-cover.png")
        updated += 1
        print(f"OK {folder}: {title}")

    print(f"\nRebuilt {updated} heroes with text-free backgrounds + clear H1 overlays")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
