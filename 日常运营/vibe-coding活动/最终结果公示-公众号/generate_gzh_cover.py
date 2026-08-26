#!/usr/bin/env python3
"""WeChat cover in the same visual language as the winners-list poster."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ART = Path(__file__).resolve().parent
OUT_WIDE = ART / "images" / "00-cover-2.35x1.png"
OUT_SQ = ART / "images" / "00-cover-1x1.png"
FONT = "/System/Library/Fonts/PingFang.ttc"
BRAND_ROOT = Path(
    "/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/"
    "日常运营/vibe-coding活动/收官公示-公众号/visuals/samples/brands"
)
INFINISYNAPSE_LOGO = BRAND_ROOT / "cert-logo-infinisynapse.png"
CSDN_LOGO = BRAND_ROOT / "cert-logo-csdn.png"

# Same tokens as generate_final_announcement_v2.py
PAPER = (245, 242, 234)
INK = (20, 20, 18)
BLUE = (42, 83, 255)
CORAL = (255, 91, 55)
LIME = (184, 242, 54)
PINK = (255, 79, 168)
WHITE = (255, 255, 252)
GRAY = (218, 215, 207)
GRID = (230, 226, 217)


def font(size: int, index: int = 8) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=index)


def tw(draw, text, fnt) -> int:
    return round(draw.textlength(text, font=fnt))


def logo_with_transparency(path: Path, max_width: int, max_height: int) -> Image.Image:
    source = Image.open(path).convert("RGBA")
    pixels = source.load()
    bg = source.getpixel((source.width - 1, 0))[:3]
    for y in range(source.height):
        for x in range(source.width):
            red, green, blue, _ = pixels[x, y]
            distance = abs(red - bg[0]) + abs(green - bg[1]) + abs(blue - bg[2])
            alpha = max(0, min(255, (distance - 10) * 12))
            pixels[x, y] = (red, green, blue, alpha)
    scale = min(max_width / source.width, max_height / source.height)
    return source.resize(
        (round(source.width * scale), round(source.height * scale)),
        Image.Resampling.LANCZOS,
    )


def paper_bg(w: int, h: int, rail: int = 36, step: int = 90) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (w, h), PAPER)
    draw = ImageDraw.Draw(image)
    for x in range(90, w, step):
        draw.line((x, 0, x, h), fill=GRID, width=1)
    for y in range(0, h, step):
        draw.line((0, y, w, y), fill=GRID, width=1)
    draw.rectangle((0, 0, rail, h), fill=INK)
    return image, draw


def host_bar(image, draw, x0, y0, x1, y1):
    draw.rectangle((x0, y0, x1, y1), fill=WHITE, outline=INK, width=3)
    draw.rectangle((x0, y0, x0 + 186, y1), fill=BLUE)
    draw.text((x0 + 22, y0 + 16), "主办方", font=font(22), fill=WHITE)
    draw.text((x0 + 22, y0 + 52), "HOSTED BY", font=font(14, 5), fill=WHITE)
    infini = logo_with_transparency(INFINISYNAPSE_LOGO, 300, 52)
    csdn = logo_with_transparency(CSDN_LOGO, 168, 50)
    image.paste(infini, (x0 + 210, y0 + 18), infini)
    mid = x0 + 210 + infini.width + 28
    draw.text((mid, y0 + (y1 - y0) / 2), "×", font=font(30, 5), fill=INK, anchor="mm")
    image.paste(csdn, (mid + 22, y0 + 20), csdn)
    tx = mid + 22 + csdn.width + 28
    draw.text((tx, y0 + 16), "首届 Vibe Coding", font=font(24), fill=INK)
    draw.text((tx, y0 + 52), "泛数据分析应用开发大赛", font=font(20, 5), fill=BLUE)


def render_wide():
    w, h = 1800, 766
    image, draw = paper_bg(w, h, rail=40)
    host_bar(image, draw, 70, 28, 1730, 122)

    draw.text((70, 146), "PAN-DATA ANALYSIS APPLICATION CONTEST", font=font(18, 5), fill=BLUE)
    draw.text((70, 172), "VIBE", font=font(118), fill=INK)
    vibe_w = tw(draw, "VIBE", font(118))
    draw.text((70 + vibe_w + 28, 172), "CODING", font=font(118), fill=CORAL)
    draw.text((76, 318), "大赛最终获奖名单", font=font(64), fill=INK)

    draw.rectangle((1228, 146, 1730, 412), fill=LIME, outline=INK, width=4)
    draw.text((1264, 164), "FINAL", font=font(58), fill=INK)
    draw.text((1264, 236), "RESULTS", font=font(58), fill=INK)
    draw.text((1268, 330), "62 WINNERS", font=font(28), fill=INK)

    stats = [("02", "一等奖", CORAL), ("04", "二等奖", BLUE), ("06", "三等奖", LIME), ("50", "优秀奖", PINK)]
    gap = 16
    stat_w = (1730 - 70 - gap * 3) // 4
    y = 444
    for i, (num, label, color) in enumerate(stats):
        x = 70 + i * (stat_w + gap)
        draw.rectangle((x, y, x + stat_w, y + 168), fill=color, outline=INK, width=3)
        fill = INK if color == LIME else WHITE
        draw.text((x + 22, y + 8), num, font=font(72), fill=fill)
        draw.text((x + 24, y + 112), label, font=font(28), fill=fill)

    draw.rectangle((70, 640, 1730, 738), fill=INK)
    draw.text((94, 658), "FINAL RESULT / 最终结果", font=font(26), fill=LIME)
    draw.text((94, 700), "InfiniSynapse × CSDN  Vibe Coding 大赛最终获奖名单现已公布", font=font(22, 5), fill=WHITE)

    image.save(OUT_WIDE, "PNG", optimize=True)
    image.save(ART / "images" / "00-cover.png", "PNG", optimize=True)
    print(f"saved {OUT_WIDE} {image.size}")
    return image


def render_square():
    w = h = 1080
    image, draw = paper_bg(w, h, rail=28, step=72)
    host_bar(image, draw, 52, 28, 1028, 118)

    draw.text((52, 142), "PAN-DATA ANALYSIS APPLICATION CONTEST", font=font(16, 5), fill=BLUE)
    draw.text((52, 168), "VIBE", font=font(86), fill=INK)
    vibe_w = tw(draw, "VIBE", font(86))
    draw.text((52 + vibe_w + 16, 168), "CODING", font=font(86), fill=CORAL)
    draw.text((56, 276), "大赛最终获奖名单", font=font(46), fill=INK)

    draw.rectangle((720, 142, 1028, 360), fill=LIME, outline=INK, width=4)
    draw.text((748, 158), "FINAL", font=font(36), fill=INK)
    draw.text((748, 210), "RESULTS", font=font(36), fill=INK)
    draw.text((752, 286), "62 WINNERS", font=font(20), fill=INK)

    stats = [("02", "一等奖", CORAL), ("04", "二等奖", BLUE), ("06", "三等奖", LIME), ("50", "优秀奖", PINK)]
    gap = 12
    stat_w = (1028 - 52 - gap * 3) // 4
    y = 400
    for i, (num, label, color) in enumerate(stats):
        x = 52 + i * (stat_w + gap)
        draw.rectangle((x, y, x + stat_w, y + 220), fill=color, outline=INK, width=3)
        fill = INK if color == LIME else WHITE
        draw.text((x + 16, y + 16), num, font=font(64), fill=fill)
        draw.text((x + 18, y + 150), label, font=font(26), fill=fill)

    draw.rectangle((52, 656, 1028, 820), fill=WHITE, outline=INK, width=3)
    draw.rectangle((52, 656, 220, 820), fill=BLUE)
    draw.text((76, 698), "62", font=font(56), fill=WHITE)
    draw.text((76, 770), "席位", font=font(24), fill=WHITE)
    draw.text((252, 690), "2 个一等奖 · 4 个二等奖", font=font(30), fill=INK)
    draw.text((252, 750), "6 个三等奖 · 50 个优秀奖", font=font(30), fill=INK)

    draw.rectangle((52, 852, 1028, 1036), fill=INK)
    draw.text((76, 880), "FINAL RESULT / 最终结果", font=font(24), fill=LIME)
    draw.text((76, 932), "InfiniSynapse × CSDN  Vibe Coding 大赛", font=font(22, 5), fill=WHITE)
    draw.text((76, 978), "完整获奖名单现已公布", font=font(22, 5), fill=WHITE)

    image.save(OUT_SQ, "PNG", optimize=True)
    print(f"saved {OUT_SQ} {image.size}")
    return image


if __name__ == "__main__":
    render_wide()
    render_square()
