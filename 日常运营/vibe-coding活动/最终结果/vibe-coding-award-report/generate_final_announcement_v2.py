#!/usr/bin/env python3
"""Generate a radically redesigned vertical final-results announcement."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from generate_announcement import EXCELLENT, FIRST, SECOND, THIRD


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "final-award-announcement-v2.png"
XHS_OUT = ROOT / "final-award-xhs-cover-v2.png"
FONT = "/System/Library/Fonts/PingFang.ttc"
BRAND_ROOT = Path(
    "/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/"
    "日常运营/vibe-coding活动/收官公示-公众号/visuals/samples/brands"
)
INFINISYNAPSE_LOGO = BRAND_ROOT / "cert-logo-infinisynapse.png"
CSDN_LOGO = BRAND_ROOT / "cert-logo-csdn.png"

W = 1800
PAPER = (245, 242, 234)
INK = (20, 20, 18)
BLUE = (42, 83, 255)
CORAL = (255, 91, 55)
LIME = (184, 242, 54)
PINK = (255, 79, 168)
WHITE = (255, 255, 252)
GRAY = (218, 215, 207)


def font(size: int, index: int = 8) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=index)


def width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    return round(draw.textlength(text, font=fnt))


def split_text(draw, text: str, fnt, max_width: int, max_lines: int = 2) -> list[str]:
    if width(draw, text, fnt) <= max_width:
        return [text]
    lines, current = [], ""
    preferred = set("｜|·—：:（(")
    last_break = -1
    for char in text:
        candidate = current + char
        if width(draw, candidate, fnt) <= max_width:
            current = candidate
            if char in preferred or char == " ":
                last_break = len(current)
            continue
        if last_break > 0:
            lines.append(current[:last_break].rstrip())
            current = current[last_break:].lstrip() + char
        else:
            lines.append(current)
            current = char
        last_break = -1
        if len(lines) == max_lines - 1:
            break
    consumed = "".join(lines) + current
    if len(consumed) < len(text):
        current += text[len(consumed) :]
    if current:
        lines.append(current)
    return lines[:max_lines]


def fit_lines(draw, text: str, max_width: int, start_size: int, min_size: int = 22):
    size = start_size
    while size >= min_size:
        fnt = font(size)
        lines = split_text(draw, text, fnt, max_width, 2)
        if all(width(draw, line, fnt) <= max_width for line in lines):
            return lines, fnt
        size -= 1
    return split_text(draw, text, font(min_size), max_width, 2), font(min_size)


def draw_grid(draw: ImageDraw.ImageDraw, height: int):
    for x in range(90, W, 120):
        draw.line((x, 0, x, height), fill=(230, 226, 217), width=1)
    for y in range(0, height, 120):
        draw.line((0, y, W, y), fill=(230, 226, 217), width=1)


def logo_with_transparency(path: Path, max_width: int, max_height: int) -> Image.Image:
    """Remove the certificate-paper background and fit the official logo."""
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


def section_head(draw, y: int, number: str, title: str, count: str, color):
    draw.rectangle((90, y, W - 90, y + 118), fill=INK)
    draw.rectangle((90, y, 290, y + 118), fill=color)
    draw.text((122, y + 12), number, font=font(70), fill=INK if color == LIME else WHITE)
    draw.text((330, y + 22), title, font=font(52), fill=WHITE)
    count_font = font(24, 5)
    draw.text((W - 120 - width(draw, count, count_font), y + 42), count, font=count_font, fill=color)
    return y + 150


def award_cards(draw, y: int, names: list[str], color, columns: int, start_index: int = 1):
    gap = 18
    x0 = 90
    usable = W - 180
    card_w = (usable - gap * (columns - 1)) // columns
    card_h = 132 if columns == 2 else 116
    rows = (len(names) + columns - 1) // columns
    for idx, name in enumerate(names):
        col = idx % columns
        row = idx // columns
        x = x0 + col * (card_w + gap)
        top = y + row * (card_h + gap)
        draw.rectangle((x, top, x + card_w, top + card_h), fill=WHITE, outline=INK, width=3)
        draw.rectangle((x, top, x + 82, top + card_h), fill=color)
        index = f"{idx + start_index:02d}"
        idx_font = font(28)
        idx_fill = INK if color == LIME else WHITE
        draw.text((x + 41, top + card_h / 2), index, font=idx_font, fill=idx_fill, anchor="mm")
        lines, name_font = fit_lines(draw, name, card_w - 130, 34 if columns == 2 else 31)
        line_h = name_font.size + 7
        block_h = line_h * len(lines)
        ty = top + (card_h - block_h) / 2
        for line in lines:
            draw.text((x + 108, ty), line, font=name_font, fill=INK)
            ty += line_h
    return y + rows * (card_h + gap) - gap


def excellence_rows(draw, y: int):
    gap_x = 18
    col_w = (W - 180 - gap_x) // 2
    row_h = 86
    gap_y = 8
    rows = 25
    for i, name in enumerate(EXCELLENT):
        col = i // rows
        row = i % rows
        x = 90 + col * (col_w + gap_x)
        top = y + row * (row_h + gap_y)
        fill = WHITE if row % 2 == 0 else (239, 236, 228)
        draw.rectangle((x, top, x + col_w, top + row_h), fill=fill)
        draw.rectangle((x, top, x + 9, top + row_h), fill=PINK if col == 0 else BLUE)
        idx = f"{i + 1:02d}"
        draw.text((x + 30, top + 26), idx, font=font(22), fill=PINK if col == 0 else BLUE)
        lines, name_font = fit_lines(draw, name, col_w - 110, 25, 18)
        if len(lines) == 1:
            draw.text((x + 86, top + 26), lines[0], font=name_font, fill=INK)
        else:
            draw.text((x + 86, top + 9), lines[0], font=name_font, fill=INK)
            draw.text((x + 86, top + 45), lines[1], font=name_font, fill=INK)
    return y + rows * (row_h + gap_y) - gap_y


def render():
    h = 4920
    image = Image.new("RGB", (W, h), PAPER)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, h)

    # Asymmetric editorial header with the official organizer logos.
    draw.rectangle((0, 0, 56, h), fill=INK)
    draw.rectangle((90, 48, W - 90, 168), fill=WHITE, outline=INK, width=3)
    draw.rectangle((90, 48, 310, 168), fill=BLUE)
    draw.text((114, 70), "主办方", font=font(25), fill=WHITE)
    draw.text((114, 112), "HOSTED BY", font=font(17, 5), fill=WHITE)
    infini_logo = logo_with_transparency(INFINISYNAPSE_LOGO, 440, 82)
    csdn_logo = logo_with_transparency(CSDN_LOGO, 250, 78)
    image.paste(infini_logo, (350, 67), infini_logo)
    draw.text((830, 106), "×", font=font(42, 5), fill=INK, anchor="mm")
    image.paste(csdn_logo, (900, 70), csdn_logo)
    draw.text((1198, 76), "首届 Vibe Coding", font=font(28), fill=INK)
    draw.text((1198, 119), "泛数据分析应用开发大赛", font=font(24, 5), fill=BLUE)
    draw.text((90, 184), "PAN-DATA ANALYSIS APPLICATION CONTEST", font=font(19, 5), fill=BLUE)
    draw.text((90, 208), "VIBE", font=font(146), fill=INK)
    draw.text((540, 208), "CODING", font=font(146), fill=CORAL)
    draw.text((98, 384), "大赛最终获奖名单", font=font(76), fill=INK)
    draw.rectangle((1260, 212, 1710, 488), fill=LIME, outline=INK, width=4)
    draw.text((1300, 234), "FINAL", font=font(62), fill=INK)
    draw.text((1300, 318), "RESULTS", font=font(62), fill=INK)
    draw.text((1304, 420), "62 WINNERS", font=font(26), fill=INK)

    # Statistics strip.
    stats = [("02", "一等奖", CORAL), ("04", "二等奖", BLUE), ("06", "三等奖", LIME), ("50", "优秀奖", PINK)]
    stat_y = 540
    stat_w = (W - 180 - 18 * 3) // 4
    for i, (value, label, color) in enumerate(stats):
        x = 90 + i * (stat_w + 18)
        draw.rectangle((x, stat_y, x + stat_w, stat_y + 138), fill=color, outline=INK, width=3)
        value_fill = INK if color == LIME else WHITE
        draw.text((x + 24, stat_y + 10), value, font=font(64), fill=value_fill)
        draw.text((x + 25, stat_y + 92), label, font=font(25), fill=value_fill)

    y = 748
    y = section_head(draw, y, "01", "一等奖", "FIRST PRIZE · 2 席", CORAL)
    y = award_cards(draw, y, FIRST, CORAL, 2)
    y += 46

    y = section_head(draw, y, "02", "二等奖", "SECOND PRIZE · 4 席", BLUE)
    y = award_cards(draw, y, SECOND, BLUE, 2)
    y += 46

    y = section_head(draw, y, "03", "三等奖", "THIRD PRIZE · 6 席", LIME)
    y = award_cards(draw, y, THIRD, LIME, 2)
    y += 46

    y = section_head(draw, y, "04", "优秀奖", "EXCELLENCE AWARD · 50 席", PINK)
    y = excellence_rows(draw, y)

    footer_y = y + 58
    draw.rectangle((90, footer_y, W - 90, footer_y + 124), fill=INK)
    draw.text((122, footer_y + 20), "FINAL RESULT / 最终结果", font=font(28), fill=LIME)
    draw.text(
        (122, footer_y + 70),
        "以上名单为 InfiniSynapse × CSDN Vibe Coding 大赛最终获奖结果",
        font=font(24, 5),
        fill=WHITE,
    )
    note = "优秀奖排名不分先后"
    note_font = font(22, 5)
    draw.text((W - 120 - width(draw, note, note_font), footer_y + 76), note, font=note_font, fill=GRAY)

    # Crop unused bottom space without changing the designed footer margin.
    final_h = footer_y + 214
    image = image.crop((0, 0, W, final_h))
    image.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {image.size[0]}x{image.size[1]}")


def render_xhs_cover():
    # Xiaohongshu full-screen cover: 9:16 @ 1080×1920
    width_px, height_px = 1080, 1920
    image = Image.new("RGB", (width_px, height_px), PAPER)
    draw = ImageDraw.Draw(image)

    # Editorial grid, inset so the left edge stays paper-colored.
    for x in range(72, width_px, 72):
        draw.line((x, 0, x, height_px), fill=(230, 226, 217), width=1)
    for y in range(0, height_px, 72):
        draw.line((0, y, width_px, y), fill=(230, 226, 217), width=1)

    # Official organizer strip.
    draw.rectangle((58, 56, 1022, 168), fill=WHITE, outline=INK, width=3)
    draw.rectangle((58, 56, 190, 168), fill=BLUE)
    draw.text((78, 78), "主办方", font=font(26), fill=WHITE)
    draw.text((78, 122), "HOST", font=font(16, 5), fill=WHITE)
    infini_logo = logo_with_transparency(INFINISYNAPSE_LOGO, 300, 60)
    csdn_logo = logo_with_transparency(CSDN_LOGO, 170, 58)
    image.paste(infini_logo, (218, 82), infini_logo)
    draw.text((550, 112), "×", font=font(32, 5), fill=INK, anchor="mm")
    image.paste(csdn_logo, (590, 84), csdn_logo)
    draw.text((806, 82), "VIBE CODING", font=font(23), fill=INK)
    draw.text((806, 122), "FINAL RESULTS", font=font(18, 5), fill=BLUE)

    draw.text((58, 200), "首届 Vibe Coding", font=font(26), fill=BLUE)
    draw.text((58, 244), "泛数据分析应用开发大赛", font=font(30), fill=INK)

    # Main cover statement.
    draw.rectangle((58, 312, 1022, 640), fill=INK)
    draw.text((94, 352), "获奖名单", font=font(92), fill=WHITE)
    draw.text((94, 472), "正式公布", font=font(92), fill=CORAL)
    draw.rectangle((778, 348, 982, 604), fill=LIME)
    draw.text((812, 384), "62", font=font(112), fill=INK)
    draw.text((808, 526), "获奖席位", font=font(26), fill=INK)

    # Prize statistics.
    stats = [("02", "一等奖", CORAL), ("04", "二等奖", BLUE), ("06", "三等奖", LIME), ("50", "优秀奖", PINK)]
    card_width = 230
    for idx, (value, label, color) in enumerate(stats):
        x = 58 + idx * 242
        draw.rectangle((x, 676, x + card_width, 850), fill=color, outline=INK, width=3)
        text_fill = INK if color == LIME else WHITE
        draw.text((x + 22, 692), value, font=font(68), fill=text_fill)
        draw.text((x + 24, 790), label, font=font(24), fill=text_fill)

    # First-prize reveal used as the visual hook.
    draw.rectangle((58, 890, 1022, 1220), fill=WHITE, outline=INK, width=3)
    draw.rectangle((58, 890, 238, 1220), fill=CORAL)
    draw.text((90, 940), "一等奖", font=font(36), fill=WHITE)
    draw.text((90, 1018), "FIRST", font=font(24), fill=WHITE)
    draw.text((90, 1062), "PRIZE", font=font(24), fill=WHITE)
    draw.text((278, 930), "01", font=font(26), fill=CORAL)
    draw.text((338, 926), FIRST[0], font=font(36), fill=INK)
    draw.line((278, 1014, 974, 1014), fill=GRAY, width=2)
    draw.text((278, 1048), "02", font=font(26), fill=CORAL)
    draw.text((338, 1044), FIRST[1], font=font(34), fill=INK)
    draw.text((278, 1140), "另有 4 个二等奖 · 6 个三等奖 · 50 个优秀奖", font=font(23, 5), fill=BLUE)

    # Bottom information band. Keep clear of Xiaohongshu UI chrome.
    draw.rectangle((58, 1260, 1022, 1548), fill=BLUE)
    draw.text((94, 1310), "FINAL", font=font(56), fill=WHITE)
    draw.text((94, 1384), "RESULTS", font=font(56), fill=LIME)
    draw.text((94, 1480), "62 件获奖作品 · 完整名单现已公布", font=font(28), fill=WHITE)

    draw.rectangle((58, 1588, 1022, 1768), fill=INK)
    draw.text((94, 1624), "INFINISYNAPSE × CSDN", font=font(28), fill=LIME)
    draw.text((94, 1688), "VIBE CODING CONTEST", font=font(26, 5), fill=WHITE)

    draw.text((58, 1816), "首届 Vibe Coding 泛数据分析应用开发大赛 · 最终结果", font=font(18, 5), fill=INK)

    image.save(XHS_OUT, "PNG", optimize=True)
    print(f"saved {XHS_OUT} {image.size[0]}x{image.size[1]}")


if __name__ == "__main__":
    render()
    render_xhs_cover()
