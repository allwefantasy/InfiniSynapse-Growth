#!/usr/bin/env python3
"""Official Vibe Coding award posters: vertical + two 16:9 landscape boards."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent / "images"
FONT = "/System/Library/Fonts/PingFang.ttc"

FIRST = [
    "SEO Health Checker",
    "AI智能售卖机商品推荐",
]
SECOND = [
    "仲裁小助手",
    "鼹鼠",
    "司南 SINAN · 多智能体证据研判引擎",
    "SafeX",
]
THIRD = [
    "LifeFlow Agent——本地生活数据决策分析管家",
    "Offer 雷达｜入职前公司尽调助手",
    "医数智析",
    "DataForNGO Lab — Insight Engine",
    "FORGE·X 智造洞察 —— 面向 3D 打印（增材制造）工厂的生产数据分析应用",
    "提前退休研究所",
]
EXCELLENT = [
    "退货雷达",
    "装明白｜装修报价与合同风险联审 AI",
    "数鉴交易市场",
    "跨境智选 SuperSignal｜基于供需信号的跨境优选决策平台",
    "Evidence Desk 专家发现台",
    "mynx",
    "城市值得去工作吗（city_worth）",
    "面试模拟器",
    "住哪儿｜租房通勤决策器",
    "AI 装修报价审计员",
    "语感工坊 YuGan",
    "琢玉轩",
    "Real Raise：涨薪真实购买力计算器",
    "先鉴",
    "OPC Gate｜一人公司政策与落地路线诊断",
    "拾余",
    "合同明镜 · AI 合同风险助手",
    "掌柜参谋",
    "北京摆摊点位分析",
    "小红书种草甄别",
    "客满满",
    "Token体检",
    "逆向罗盘（Return Compass）",
    "赛场扫描仪",
    "凤栖梧",
    "Retro/Radar · 项目复盘雷达",
    "电商经营分析助手",
    "帅治星球-职场情绪分析平台",
    "智能掌柜",
    "学情罗盘 EduCompass",
    "资析智策（资产分析与智能决策 Asset Intelligence & Decision Analytics System）",
    "职牌",
    "RepoPulse｜开源项目运营体检",
    "智管进销存",
    "智析账本 BillLens",
    "家居供应链协同平台",
    "财格-AI犀利点评你的理财性格",
    "统计分析系统（Statistical Analysis System）",
    "泡泡看市｜小白的股市翻译官",
    "智行路线 RouteWise",
    "SEO数据分析",
    "ProjectValueLab",
    "选题雷达 Topic Radar",
    "学习计划助手",
    "CET-4 Vocab Lab 四级单词学习舱",
    "竞品对标分析器",
    "产品经理数据汇报工作台",
    "簿言",
    "明日足球",
    "人生模拟器",
]

NAVY = (8, 16, 36)
NAVY_MID = (14, 28, 58)
GOLD = (232, 196, 122)
GOLD_DEEP = (196, 154, 72)
SILVER = (210, 220, 232)
BRONZE = (214, 158, 106)
TEAL = (92, 214, 196)
WHITE = (246, 248, 252)
MUTED = (168, 180, 204)
CARD = (18, 32, 64)
LINE = (36, 56, 96)
SOFT = (120, 136, 164)


def font(size: int, index: int = 4) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size, index=index)


def text_w(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    return int(draw.textlength(text, font=fnt))


def wrap_name(draw, name: str, fnt, max_w: float, max_lines: int = 2) -> list[str]:
    if text_w(draw, name, fnt) <= max_w:
        return [name]
    breaks = ("——", " — ", "｜", "|", "·", "：", "（", "(", " ")
    for sep in breaks:
        if sep in name:
            left, right = name.split(sep, 1)
            right = sep + right if sep in ("（", "(") else right
            if sep in ("——", " — ", "｜", "|", "·", "："):
                left = left + sep.rstrip()
            if text_w(draw, left, fnt) <= max_w and text_w(draw, right, fnt) <= max_w:
                return [left, right]
    lines, cur = [], ""
    for ch in name:
        trial = cur + ch
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
            if len(lines) >= max_lines - 1:
                # last line: shrink by cutting with ellipsis only if truly overflow
                rest = ch + name[name.find(ch) + 1 :] if False else name[len("".join(lines)) :]
                while text_w(draw, rest, fnt) > max_w and len(rest) > 2:
                    rest = rest[:-1]
                return lines + [rest]
    if cur:
        lines.append(cur)
    return lines[:max_lines]


def center_text(draw, y, text, fnt, fill, width):
    draw.text(((width - text_w(draw, text, fnt)) / 2, y), text, font=fnt, fill=fill)


def make_bg(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), NAVY)
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(NAVY[0] + (NAVY_MID[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (22 - NAVY[1]) * t * 0.35)
        b = int(NAVY[2] + (NAVY_MID[2] - NAVY[2]) * t * 0.55)
        for x in range(w):
            dx = abs(x - w / 2) / (w / 2)
            shade = 1 - 0.12 * dx
            px[x, y] = (int(r * shade), int(g * shade), int(b * shade))
    glow = Image.new("RGB", (w, h), NAVY)
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((int(w * 0.26), -int(h * 0.08), int(w * 0.74), int(h * 0.16)), fill=(28, 48, 92))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    return Image.blend(img, glow, 0.38)


def diamond_rule(draw, y, width, color=GOLD):
    cx = width / 2
    draw.polygon([(cx, y - 7), (cx + 7, y), (cx, y + 7), (cx - 7, y)], fill=color)
    draw.line((cx - 240, y, cx - 20, y), fill=GOLD_DEEP, width=2)
    draw.line((cx + 20, y, cx + 240, y), fill=GOLD_DEEP, width=2)


def section_label(draw, y, title, count, color, width):
    f_title = font(32, 5)
    f_sub = font(18, 0)
    center_text(draw, y, title, f_title, color, width)
    tw = text_w(draw, title, f_title)
    left = (width - tw) / 2
    draw.line((left - 120, y + 18, left - 20, y + 18), fill=color, width=2)
    draw.line((left + tw + 20, y + 18, left + tw + 120, y + 18), fill=color, width=2)
    center_text(draw, y + 42, count, f_sub, MUTED, width)
    return y + 78


def draw_cards(draw, box_w, y, names, color, cols, card_h, gap_x, gap_y, pad_x, name_size, idx_size=16, start_idx=1):
    usable = box_w - pad_x * 2
    card_w = (usable - gap_x * (cols - 1)) / cols
    f_idx = font(idx_size, 0)
    for i, name in enumerate(names):
        col = i % cols
        row = i // cols
        x0 = pad_x + col * (card_w + gap_x)
        y0 = y + row * (card_h + gap_y)
        x1 = x0 + card_w
        y1 = y0 + card_h
        draw.rounded_rectangle((x0, y0, x1, y1), radius=14, fill=CARD, outline=LINE, width=2)
        draw.rounded_rectangle((x0, y0, x0 + 7, y1), radius=7, fill=color)
        idx = f"{i + start_idx:02d}"
        draw.text((x0 + 20, y0 + (card_h - idx_size - 4) / 2), idx, font=f_idx, fill=color)
        size = name_size
        nf = font(size, 5)
        max_w = card_w - 78
        lines = wrap_name(draw, name, nf, max_w, 2)
        while (any(text_w(draw, ln, nf) > max_w for ln in lines) or len(lines) > 2) and size > 13:
            size -= 1
            nf = font(size, 5)
            lines = wrap_name(draw, name, nf, max_w, 2)
        line_h = size + 4
        block_h = line_h * len(lines)
        ty = y0 + (card_h - block_h) / 2
        for li, ln in enumerate(lines):
            draw.text((x0 + 58, ty + li * line_h), ln, font=nf, fill=WHITE)
    rows = (len(names) + cols - 1) // cols
    return y + rows * (card_h + gap_y) - gap_y


def header(draw, width, y, subtitle: str):
    center_text(draw, y, "INFINISYNAPSE  ×  CSDN", font(20, 0), GOLD, width)
    y += 34
    center_text(draw, y, "VIBE CODING 大赛", font(18, 0), MUTED, width)
    y += 40
    center_text(draw, y, "获奖名单公告", font(56, 5), WHITE, width)
    y += 76
    diamond_rule(draw, y, width)
    y += 28
    center_text(draw, y, subtitle, font(18, 0), MUTED, width)
    y += 30
    center_text(draw, y, "评选维度：场景价值 40%  ·  技术完成度 35%  ·  创新性 25%", font(16, 0), SOFT, width)
    return y + 40


def footer(draw, width, y, extra=""):
    draw.line((80, y, width - 80, y), fill=LINE, width=1)
    y += 18
    center_text(draw, y, "以上名单为 InfiniSynapse × CSDN Vibe Coding 大赛最终获奖结果", font(16, 0), MUTED, width)
    y += 26
    line = "排名按奖项档位公布，优秀奖排名不分先后"
    if extra:
        line = extra
    center_text(draw, y, line, font(15, 0), (110, 124, 150), width)


def save(img: Image.Image, name: str):
    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / name
    img.save(path, "PNG", optimize=True)
    print(f"saved {path}  {img.size[0]}x{img.size[1]}")


def render_vertical():
    w, h = 1600, 4280
    img = make_bg(w, h)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 8), fill=GOLD)
    y = header(draw, w, 48, "共 62 席   ·   2 一等奖   ·   4 二等奖   ·   6 三等奖   ·   50 优秀奖")
    y = section_label(draw, y, "一等奖", "FIRST PRIZE  ·  2 席", GOLD, w)
    y = draw_cards(draw, w, y, FIRST, GOLD, 2, 92, 18, 14, 56, 26)
    y += 36
    y = section_label(draw, y, "二等奖", "SECOND PRIZE  ·  4 席", SILVER, w)
    y = draw_cards(draw, w, y, SECOND, SILVER, 1, 78, 18, 12, 56, 24)
    y += 36
    y = section_label(draw, y, "三等奖", "THIRD PRIZE  ·  6 席", BRONZE, w)
    y = draw_cards(draw, w, y, THIRD, BRONZE, 1, 78, 18, 12, 56, 22)
    y += 36
    y = section_label(draw, y, "优秀奖", "EXCELLENCE AWARD  ·  50 席", TEAL, w)
    y = draw_cards(draw, w, y, EXCELLENT, TEAL, 2, 70, 14, 8, 48, 17)
    y += 36
    footer(draw, w, y)
    draw.rectangle((0, h - 8, w, h), fill=GOLD)
    save(img, "award-announcement.png")


def render_landscape_prizes():
    w, h = 3840, 2160
    img = make_bg(w, h)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 10), fill=GOLD)
    y = 40
    center_text(draw, y, "INFINISYNAPSE  ×  CSDN    ·    VIBE CODING 大赛", font(24, 0), GOLD, w)
    y += 46
    center_text(draw, y, "获奖名单公告", font(64, 5), WHITE, w)
    y += 82
    diamond_rule(draw, y, w)
    y += 26
    center_text(draw, y, "一 / 二 / 三等奖   ·   共 12 席", font(22, 0), MUTED, w)
    y += 44

    # 一等奖
    center_text(draw, y, "一等奖", font(30, 5), GOLD, w)
    y += 48
    y = draw_cards(draw, w, y, FIRST, GOLD, 2, 100, 24, 16, 120, 30, 20)
    y += 36
    center_text(draw, y, "二等奖", font(28, 5), SILVER, w)
    y += 44
    y = draw_cards(draw, w, y, SECOND, SILVER, 2, 92, 20, 14, 120, 24, 18)
    y += 32
    center_text(draw, y, "三等奖", font(28, 5), BRONZE, w)
    y += 44
    y = draw_cards(draw, w, y, THIRD, BRONZE, 2, 96, 20, 12, 120, 22, 18)
    y += 40
    footer(draw, w, y, "横版 1 / 3    ·    后两张为优秀奖 50 席")
    draw.rectangle((0, h - 10, w, h), fill=GOLD)
    save(img, "award-announcement-landscape-1.png")


def render_landscape_excellent(names, page: int, pages: int, filename: str, range_label: str, start_idx: int):
    w, h = 3840, 2160
    img = make_bg(w, h)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w, 10), fill=GOLD)
    y = 28
    center_text(draw, y, "INFINISYNAPSE  ×  CSDN    ·    VIBE CODING 大赛", font(22, 0), GOLD, w)
    y += 38
    center_text(draw, y, "优秀奖 · 50 席", font(50, 5), WHITE, w)
    y += 64
    diamond_rule(draw, y, w)
    y += 20
    center_text(draw, y, f"排名不分先后    ·    {range_label}    ·    横版 {page} / {pages}", font(20, 0), MUTED, w)
    y += 32
    y = draw_cards(draw, w, y, names, TEAL, 2, 112, 20, 10, 80, 24, 18, start_idx=start_idx)
    y += 24
    footer(draw, w, y, "以上为 InfiniSynapse × CSDN Vibe Coding 大赛最终优秀奖名单")
    draw.rectangle((0, h - 10, w, h), fill=GOLD)
    save(img, filename)


def main():
    render_vertical()
    render_landscape_prizes()
    render_landscape_excellent(
        EXCELLENT[:25], 2, 3, "award-announcement-landscape-2.png", "01 — 25", 1
    )
    render_landscape_excellent(
        EXCELLENT[25:], 3, 3, "award-announcement-landscape-3.png", "26 — 50", 26
    )


if __name__ == "__main__":
    main()
