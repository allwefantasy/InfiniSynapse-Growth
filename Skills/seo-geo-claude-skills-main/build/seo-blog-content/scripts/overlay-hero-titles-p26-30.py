#!/usr/bin/env python3
"""Overlay exact article H1 titles onto Pillar 26–30 hero images.

Per blog-hero-cover-spec.md: AI backgrounds may stay, but title text must be
PIL-rendered (never AI typography). Writes hero-*.png + og-cover.png at 1200×630.

Idempotent: first run archives the current art under images/.hero-bg/, then every
run composites from that archive so titles are never double-stacked.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SIZE = (1200, 630)

PILLAR_KICKERS = {
    "pillar26": "GUIDE · 2026",
    "pillar27": "GUIDE · 2026",
    "pillar28": "GUIDE · 2026",
    "pillar29": "GUIDE · 2026",
    "pillar30": "GUIDE · 2026",
}

PILLAR_ACCENT = {
    "pillar26": (45, 212, 191),
    "pillar27": (168, 85, 247),
    "pillar28": (59, 130, 246),
    "pillar29": (34, 211, 238),
    "pillar30": (244, 114, 182),
}


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


def title_font_size(title: str) -> int:
    n = len(title)
    if n <= 42:
        return 48
    if n <= 56:
        return 40
    if n <= 72:
        return 34
    return 30


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


def parse_article(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.+)$", text, re.M)
    img = re.search(r"!\[([^\]]*)\]\(\./images/([^)]+)\)", text)
    title = h1.group(1).strip() if h1 else path.parent.name
    filename = img.group(2).strip() if img else "hero.png"
    return title, filename


def ensure_bg(hero_path: Path) -> Path:
    bg_dir = hero_path.parent / ".hero-bg"
    bg_dir.mkdir(parents=True, exist_ok=True)
    bg_path = bg_dir / hero_path.name
    if not bg_path.is_file() or bg_path.stat().st_size < 1000:
        if hero_path.is_file() and hero_path.stat().st_size > 1000:
            shutil.copyfile(hero_path, bg_path)
        else:
            # Solid fallback if missing
            Image.new("RGB", SIZE, (15, 23, 42)).save(bg_path, format="PNG")
    return bg_path


def prepare_bg(bg_path: Path) -> Image.Image:
    img = Image.open(bg_path).convert("RGB")
    if img.size != SIZE:
        img = img.resize(SIZE, Image.Resampling.LANCZOS)
    return img


def overlay_title(bg: Image.Image, title: str, pillar_key: str) -> Image.Image:
    w, h = SIZE
    base = bg.convert("RGBA")

    accent = PILLAR_ACCENT.get(pillar_key, (96, 165, 250))
    kicker = PILLAR_KICKERS.get(pillar_key, "GUIDE · 2026")

    # Light tech tint only — keep art bright; contrast via neon glow not dark stroke
    wash = Image.new("RGBA", (w, h), (10, 20, 48, 28))
    composed = Image.alpha_composite(base, wash)

    kicker_font = load_font(20, bold=True)
    brand_font = load_font(18, bold=False)
    tsize = title_font_size(title) + 4
    bold = load_font(tsize, bold=True)

    # Measure on a temp draw
    tmp = ImageDraw.Draw(composed)
    max_title_w = int(w * 0.86)
    lines = wrap_text(title, bold, max_title_w, tmp)
    if len(lines) > 4:
        bold = load_font(max(26, tsize - 6), bold=True)
        lines = wrap_text(title, bold, max_title_w, tmp)
        tsize = max(26, tsize - 6)
    lines = lines[:5]
    line_gap = int(tsize * 1.28)
    block_h = len(lines) * line_gap
    kicker_h = 40
    total_h = kicker_h + 10 + block_h
    y0 = (h - total_h) // 2
    cx, cy = w // 2, y0 + total_h // 2

    ar, ag, ab = accent

    # Soft accent bloom only (colored light — never a dark plate/stroke)
    bloom = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bloom)
    rx, ry = int(w * 0.36), int(total_h * 0.8 + 36)
    for i in range(20, 0, -1):
        a = int(3 + (20 - i) * 2.0)
        bd.ellipse(
            [cx - rx * i // 20, cy - ry * i // 20, cx + rx * i // 20, cy + ry * i // 20],
            fill=(ar, ag, ab, min(a, 55)),
        )
    bloom = bloom.filter(ImageFilter.GaussianBlur(radius=26))
    composed = Image.alpha_composite(composed, bloom)

    # Neon core text: colored glow + pure white fill — no black border/shadow
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)

    kw = td.textlength(kicker, font=kicker_font)
    kx, ky = (w - kw) / 2, y0
    for r, a in ((8, 50), (3, 90)):
        glow_k = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gk = ImageDraw.Draw(glow_k)
        gk.text((kx, ky), kicker, fill=(ar, ag, ab, a), font=kicker_font)
        text_layer = Image.alpha_composite(
            text_layer, glow_k.filter(ImageFilter.GaussianBlur(radius=r))
        )
    td = ImageDraw.Draw(text_layer)
    td.text((kx, ky), kicker, fill=(ar, ag, ab, 255), font=kicker_font)

    y = y0 + kicker_h + 10
    for line in lines:
        tw = td.textlength(line, font=bold)
        x = (w - tw) / 2
        for r, a in ((12, 40), (6, 70), (2, 100)):
            glow_t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            gt = ImageDraw.Draw(glow_t)
            gt.text((x, y), line, fill=(ar, ag, ab, a), font=bold)
            text_layer = Image.alpha_composite(
                text_layer, glow_t.filter(ImageFilter.GaussianBlur(radius=r))
            )
        td = ImageDraw.Draw(text_layer)
        td.text((x, y), line, fill=(255, 255, 255, 255), font=bold)
        y += line_gap

    composed = Image.alpha_composite(composed, text_layer)
    draw = ImageDraw.Draw(composed)

    brand = "InfiniSynapse"
    bw = draw.textlength(brand, font=brand_font)
    bx = (w - bw) / 2
    by = h - 52
    draw.text((bx, by), brand, fill=(210, 222, 240, 230), font=brand_font)
    draw.line([(bx, by + 22), (bx + bw, by + 22)], fill=accent + (180,), width=1)

    return composed.convert("RGB")


def main() -> int:
    pillars = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))
    done = 0
    for pillar in pillars:
        key = pillar.name[:8]
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            title, filename = parse_article(art)
            hero_path = art.parent / "images" / filename
            hero_path.parent.mkdir(parents=True, exist_ok=True)
            bg_path = ensure_bg(hero_path)
            bg = prepare_bg(bg_path)
            out = overlay_title(bg, title, key)
            out.save(hero_path, format="PNG", optimize=True)
            og = art.parent / "images" / "og-cover.png"
            shutil.copyfile(hero_path, og)
            done += 1
            print(f"OK {art.parent.name}: {title[:70]}")
    print(f"\nUpdated {done} heroes (+ og-cover.png) with H1 titles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
