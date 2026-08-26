#!/usr/bin/env python3
"""Prize card in the same editorial style as generate_final_announcement_v2.py."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ART = Path(__file__).resolve().parent
OUT = ART / "images" / "02-prizes.png"
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


def tw(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    return round(draw.textlength(text, font=fnt))


def draw_grid(draw: ImageDraw.ImageDraw, height: int):
    for x in range(90, W, 120):
        draw.line((x, 0, x, height), fill=(230, 226, 217), width=1)
    for y in range(0, height, 120):
        draw.line((0, y, W, y), fill=(230, 226, 217), width=1)


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


def render():
    h = 1680
    image = Image.new("RGB", (W, h), PAPER)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, h)
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

    draw.text((90, 196), "PRIZES & BENEFITS", font=font(19, 5), fill=BLUE)
    draw.text((90, 220), "奖金", font=font(110), fill=INK)
    draw.text((560, 220), "与权益", font=font(110), fill=CORAL)
    draw.rectangle((1260, 214, 1710, 430), fill=LIME, outline=INK, width=4)
    draw.text((1300, 232), "CASH", font=font(42), fill=INK)
    draw.text((1300, 288), "POOL", font=font(42), fill=INK)
    draw.text((1304, 360), "¥22,528", font=font(38), fill=INK)

    draw.text((98, 456), "现金奖金池  ¥22,528", font=font(48), fill=INK)
    draw.text((98, 528), "另附 InfiniSynapse Pro 会员 · 四档联名证书", font=font(28, 5), fill=BLUE)

    prizes = [
        ("01", "一等奖", "¥4,096", "2 席 · 年度 Pro", "FIRST PRIZE", CORAL),
        ("02", "二等奖", "¥2,048", "4 席 · 季度 Pro", "SECOND PRIZE", BLUE),
        ("03", "三等奖", "¥1,024", "6 席 · 月度 Pro", "THIRD PRIZE", LIME),
        ("04", "优秀奖", "月度Pro", "50 席 · 无现金", "EXCELLENCE", PINK),
    ]
    y = 600
    gap = 18
    card_w = (W - 180 - gap * 3) // 4
    card_h = 320
    for i, (num, title, money, meta, en, color) in enumerate(prizes):
        x = 90 + i * (card_w + gap)
        draw.rectangle((x, y, x + card_w, y + 72), fill=INK)
        draw.rectangle((x, y, x + 82, y + 72), fill=color)
        num_fill = INK if color == LIME else WHITE
        draw.text((x + 41, y + 36), num, font=font(28), fill=num_fill, anchor="mm")
        draw.text((x + 100, y + 16), title, font=font(28), fill=WHITE)
        en_font = font(14, 5)
        draw.text((x + 100, y + 48), en, font=en_font, fill=color)

        draw.rectangle((x, y + 72, x + card_w, y + card_h), fill=WHITE, outline=INK, width=3)
        money_fill = INK if color != LIME else INK
        draw.text((x + 28, y + 108), money, font=font(56), fill=money_fill)
        draw.rectangle((x + 28, y + 196, x + 28 + 72, y + 202), fill=color)
        draw.text((x + 28, y + 224), meta, font=font(24, 5), fill=INK)
        extra = {
            "01": "价值 ¥1,800",
            "02": "价值 ¥450",
            "03": "价值 ¥150",
            "04": "价值 ¥150",
        }[num]
        draw.text((x + 28, y + 266), extra, font=font(20, 5), fill=BLUE)

    y = 960
    draw.rectangle((90, y, W - 90, y + 148), fill=WHITE, outline=INK, width=3)
    draw.rectangle((90, y, 290, y + 148), fill=BLUE)
    draw.text((122, y + 28), "证书", font=font(42), fill=WHITE)
    draw.text((122, y + 90), "CERTIFICATE", font=font(18, 5), fill=WHITE)
    draw.text((330, y + 32), "InfiniSynapse × CSDN 联名获奖证书", font=font(40), fill=INK)
    draw.text((330, y + 96), "四档均可核验，写进简历与作品集都站得住", font=font(26, 5), fill=BLUE)

    y = 1148
    draw.rectangle((90, y, W - 90, y + 124), fill=INK)
    draw.text((122, y + 20), "PRIZES / 奖金与权益", font=font(28), fill=LIME)
    draw.text(
        (122, y + 70),
        "奖金、会员与证书发放通过官方渠道另行通知",
        font=font(24, 5),
        fill=WHITE,
    )
    note = "现金总额 ¥22,528"
    note_font = font(22, 5)
    draw.text((W - 120 - tw(draw, note, note_font), y + 76), note, font=note_font, fill=GRAY)

    final_h = y + 214
    image = image.crop((0, 0, W, final_h))
    # WeChat-friendly width
    out = image.resize((1080, round(image.height * 1080 / image.width)), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(exist_ok=True)
    out.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    render()
