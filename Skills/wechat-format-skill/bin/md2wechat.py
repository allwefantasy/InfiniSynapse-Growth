#!/usr/bin/env python3
"""
md2wechat.py — Markdown → 微信公众号兼容的样式化 HTML

配套 `wechat-format-skill`。和姊妹脚本 `wechat-mp-draft-skill/bin/md2html.py` 的区别：

| 维度 | md2html.py（draft skill） | md2wechat.py（本脚本） |
|---|---|---|
| 目的 | 占位符化、base64 化，方便 agent-browser 注入 | **视觉排版**——主题、内联样式、组件 |
| 样式 | 几乎不加 | 8 套主题，每标签全内联 style |
| 兼容性处理 | 仅去 H1 | CJK 间距、加粗标点、外链转脚注、ul→flex |
| 自定义容器 | 无 | :::dialogue / :::gallery / :::longimage / [!tip] 等 |

典型用法：

    python3 md2wechat.py --input article.md --theme newspaper --output article.html
    python3 md2wechat.py --input article.md --theme terracotta --output article.html --open
    python3 md2wechat.py --list-themes

依赖：
    pip3 install markdown beautifulsoup4 pygments

输出：
    article.html          —— 直接复制粘贴到公众号编辑器的 HTML
    article.preview.html  —— 带浏览器壳的预览页（标题 + 模拟微信宽度的 wrapper）
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import webbrowser
from pathlib import Path
from typing import Any

try:
    import markdown
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    sys.stderr.write(
        "Missing deps. Install:  pip3 install markdown beautifulsoup4 pygments\n"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

THEMES: dict[str, dict[str, Any]] = {
    "newspaper": {
        "name": "报纸 / 纽约时报",
        "primary": "#326891",
        "text": "#111111",
        "muted": "#666666",
        "bg": "#ffffff",
        "code_bg": "#f0ede8",
        "blockquote_bg": "#f7f3ee",
        "font_family": "Georgia, 'Source Han Serif SC', 'Noto Serif CJK SC', serif",
        "h1": "font-size:29px;font-weight:700;color:#111;line-height:1.3;letter-spacing:-0.015em;padding:10px 0 9px;border-top:2px solid #111;border-bottom:1px solid #111;text-align:left;margin:38px 0 16px;",
        "h2": "font-size:19px;font-weight:700;color:#111;line-height:1.5;text-transform:uppercase;letter-spacing:0.12em;text-align:center;padding:10px 0;border-top:1px solid rgba(17,17,17,0.85);border-bottom:1px solid rgba(17,17,17,0.85);margin:38px 0 18px;",
        "h3": "font-size:17px;font-weight:700;color:#111;line-height:1.45;letter-spacing:0.04em;padding-bottom:6px;margin:28px 0 14px;",
        "p": "font-size:15px;color:#000;line-height:1.7;margin:0 0 18px 0;letter-spacing:0.5px;text-align:left;",
        "strong": "font-weight:700;color:#111;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 62%,rgba(50,104,145,0.1) 62%,rgba(50,104,145,0.1) 100%);display:inline;",
        "em": "font-style:italic;color:#666;",
        "blockquote": "border-top:1px solid #d5cfc5;border-bottom:1px solid #d5cfc5;background:#f7f3ee;padding:18px 20px;margin:24px 0;border-radius:0;font-size:16px;color:#555;line-height:1.7;font-style:italic;",
        "hr": "margin:40px auto;height:1px;background:linear-gradient(90deg,rgba(213,207,197,0) 0%,rgba(17,17,17,0.9) 26%,rgba(17,17,17,0.9) 74%,rgba(213,207,197,0) 100%);border:none;width:38%;",
        "li_bullet_color": "#326891",
    },
    "terracotta": {
        "name": "赤陶 / 暖橙圆角",
        "primary": "#C56C3F",
        "text": "#3a2e26",
        "muted": "#8B5E3C",
        "bg": "#fffaf3",
        "code_bg": "#f5ede0",
        "blockquote_bg": "#fff3e6",
        "font_family": "'Source Han Serif SC', 'Noto Serif CJK SC', Georgia, serif",
        "h1": "font-size:24px;font-weight:700;color:#fff;background:linear-gradient(135deg,#C56C3F 0%,#A55530 100%);padding:14px 18px;border-radius:8px;text-align:center;margin:32px 0 20px;",
        "h2": "font-size:20px;font-weight:700;color:#C56C3F;border-left:5px solid #C56C3F;padding:4px 0 4px 14px;background:linear-gradient(to right,rgba(197,108,63,0.08),transparent);margin:30px 0 16px;",
        "h3": "font-size:17px;font-weight:700;color:#C56C3F;margin:24px 0 12px;",
        "p": "font-size:15px;color:#3a2e26;line-height:1.75;margin:0 0 18px 0;letter-spacing:0.3px;",
        "strong": "font-weight:700;color:#C56C3F;",
        "em": "font-style:italic;color:#8B5E3C;",
        "blockquote": "background:#fff3e6;border-left:4px solid #C56C3F;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0;font-size:15px;color:#5a3e2e;line-height:1.75;",
        "hr": "margin:32px auto;height:2px;background:linear-gradient(90deg,transparent,#C56C3F,transparent);border:none;width:50%;",
        "li_bullet_color": "#C56C3F",
    },
    "ink": {
        "name": "墨韵 / 极简纯黑",
        "primary": "#000000",
        "text": "#000000",
        "muted": "#666666",
        "bg": "#ffffff",
        "code_bg": "#f5f5f5",
        "blockquote_bg": "#ffffff",
        "font_family": "'Source Han Serif SC', 'Noto Serif CJK SC', Georgia, serif",
        "h1": "font-size:26px;font-weight:700;color:#000;line-height:1.4;text-align:left;margin:32px 0 16px;",
        "h2": "font-size:18px;font-weight:700;color:#000;line-height:1.5;margin:28px 0 14px;",
        "h3": "font-size:16px;font-weight:700;color:#000;margin:22px 0 12px;",
        "p": "font-size:15px;color:#000;line-height:1.8;margin:0 0 18px 0;letter-spacing:0.6px;",
        "strong": "font-weight:700;color:#000;",
        "em": "font-style:italic;color:#666;",
        "blockquote": "border-left:2px solid #000;padding:6px 0 6px 18px;margin:22px 0;font-size:15px;color:#333;line-height:1.8;font-style:italic;",
        "hr": "margin:36px auto;height:1px;background:#000;border:none;width:30%;",
        "li_bullet_color": "#000000",
    },
    "github": {
        "name": "GitHub / 开发者风",
        "primary": "#0969da",
        "text": "#1f2328",
        "muted": "#656d76",
        "bg": "#ffffff",
        "code_bg": "#f6f8fa",
        "blockquote_bg": "#f6f8fa",
        "font_family": "-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif",
        "h1": "font-size:24px;font-weight:700;color:#1f2328;border-bottom:2px solid #d1d9e0;padding-bottom:8px;margin:30px 0 16px;",
        "h2": "font-size:20px;font-weight:700;color:#1f2328;border-bottom:1px solid #d1d9e0;padding-bottom:6px;margin:26px 0 14px;",
        "h3": "font-size:17px;font-weight:700;color:#1f2328;margin:22px 0 12px;",
        "p": "font-size:14px;color:#1f2328;line-height:1.6;margin:0 0 16px 0;",
        "strong": "font-weight:700;color:#1f2328;",
        "em": "font-style:italic;color:#656d76;",
        "blockquote": "border-left:4px solid #d1d9e0;background:#f6f8fa;padding:10px 14px;margin:18px 0;font-size:14px;color:#656d76;line-height:1.6;",
        "hr": "margin:24px 0;height:1px;background:#d1d9e0;border:none;",
        "li_bullet_color": "#0969da",
    },
    "chinese": {
        "name": "中国风 / 朱砂红",
        "primary": "#9F2A2A",
        "text": "#3a2818",
        "muted": "#704214",
        "bg": "#fdf6e3",
        "code_bg": "#f5ecd0",
        "blockquote_bg": "#faf0d8",
        "font_family": "'Source Han Serif SC','STKaiti','KaiTi','Noto Serif CJK SC',serif",
        "h1": "font-size:26px;font-weight:700;color:#9F2A2A;text-align:center;padding:14px 0;border-top:2px double #9F2A2A;border-bottom:2px double #9F2A2A;margin:32px 0 20px;",
        "h2": "font-size:20px;font-weight:700;color:#9F2A2A;border-bottom:1px dashed #9F2A2A;padding-bottom:6px;margin:28px 0 16px;",
        "h3": "font-size:17px;font-weight:700;color:#704214;margin:24px 0 12px;",
        "p": "font-size:15px;color:#3a2818;line-height:2.0;margin:0 0 18px 0;letter-spacing:0.5px;",
        "strong": "font-weight:700;color:#9F2A2A;",
        "em": "font-style:italic;color:#704214;",
        "blockquote": "background:#faf0d8;border-left:4px solid #9F2A2A;padding:14px 18px;margin:20px 0;font-size:15px;color:#5a3e1e;line-height:1.85;font-style:italic;",
        "hr": "margin:32px auto;height:0;border:none;border-top:1px dashed #9F2A2A;width:50%;",
        "li_bullet_color": "#9F2A2A",
    },
    "midnight": {
        "name": "暗夜 / 赛博朋克",
        "primary": "#00ffaa",
        "text": "#e8e8f0",
        "muted": "#a0a0b0",
        "bg": "#0a0a0f",
        "code_bg": "#1a1a25",
        "blockquote_bg": "#15151f",
        "font_family": "-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif",
        "h1": "font-size:28px;font-weight:700;color:#00ffaa;text-shadow:0 0 12px rgba(0,255,170,0.4);margin:32px 0 18px;",
        "h2": "font-size:20px;font-weight:700;color:#ff3399;border-left:4px solid #ff3399;padding-left:14px;margin:28px 0 16px;",
        "h3": "font-size:17px;font-weight:700;color:#e8e8f0;margin:24px 0 12px;",
        "p": "font-size:15px;color:#e8e8f0;line-height:1.7;margin:0 0 18px 0;",
        "strong": "font-weight:700;color:#ff3399;",
        "em": "font-style:italic;color:#a0a0b0;",
        "blockquote": "background:#15151f;border-left:3px solid #00ffaa;padding:14px 18px;margin:20px 0;font-size:15px;color:#c0c0d0;line-height:1.7;",
        "hr": "margin:32px 0;height:1px;background:linear-gradient(90deg,transparent,#00ffaa 50%,transparent);border:none;",
        "li_bullet_color": "#00ffaa",
    },
    "sunset-amber": {
        "name": "日落 / 琥珀暖调",
        "primary": "#D97706",
        "text": "#3a2e1e",
        "muted": "#92400E",
        "bg": "#FFFBF5",
        "code_bg": "#fdf3e2",
        "blockquote_bg": "#fff3dc",
        "font_family": "Georgia, 'Source Han Serif SC', serif",
        "h1": "font-size:24px;font-weight:700;color:#D97706;margin:32px 0 16px;",
        "h2": "font-size:20px;font-weight:700;color:#92400E;padding-bottom:6px;border-bottom:1px solid;border-image:linear-gradient(90deg,#D97706,transparent) 1;margin:28px 0 14px;",
        "h3": "font-size:17px;font-weight:700;color:#92400E;margin:24px 0 12px;",
        "p": "font-size:15px;color:#3a2e1e;line-height:1.75;margin:0 0 18px 0;letter-spacing:0.3px;",
        "strong": "font-weight:700;color:#D97706;",
        "em": "font-style:italic;color:#92400E;",
        "blockquote": "background:#fff3dc;border-left:4px solid;border-image:linear-gradient(180deg,#D97706,#92400E) 1;padding:14px 18px;margin:20px 0;font-size:15px;color:#5a4830;line-height:1.75;",
        "hr": "margin:32px auto;height:1px;background:linear-gradient(90deg,transparent,#D97706,transparent);border:none;width:50%;",
        "li_bullet_color": "#D97706",
    },
    "magazine": {
        "name": "杂志 / 超大留白",
        "primary": "#1a1a1a",
        "text": "#1a1a1a",
        "muted": "#737373",
        "bg": "#ffffff",
        "code_bg": "#f5f5f5",
        "blockquote_bg": "#ffffff",
        "font_family": "'Playfair Display','Source Han Serif SC',Georgia,serif",
        "h1": "font-size:32px;font-weight:700;color:#1a1a1a;line-height:1.2;text-align:center;margin:36px 0 20px;",
        "h2": "font-size:22px;font-weight:700;color:#1a1a1a;margin:32px 0 16px;",
        "h3": "font-size:18px;font-weight:700;color:#1a1a1a;margin:26px 0 12px;",
        "p": "font-size:16px;color:#1a1a1a;line-height:1.85;margin:0 0 24px 0;letter-spacing:0.3px;",
        "strong": "font-weight:700;color:#1a1a1a;",
        "em": "font-style:italic;color:#737373;font-size:1.05em;",
        "blockquote": "padding:8px 0 8px 22px;margin:28px 0;border-left:3px solid #1a1a1a;font-size:18px;color:#1a1a1a;line-height:1.7;font-style:italic;",
        "hr": "margin:40px auto;height:1px;background:#1a1a1a;border:none;width:20%;",
        "li_bullet_color": "#1a1a1a",
    },
}


# ---------------------------------------------------------------------------
# Pre-processing: text-level fixes
# ---------------------------------------------------------------------------

CJK = r"\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef"


def fix_cjk_spacing(text: str) -> str:
    """中英文/中数字之间补半角空格。在 markdown 阶段就处理掉。"""
    text = re.sub(rf"([{CJK}])([a-zA-Z0-9])", r"\1 \2", text)
    text = re.sub(rf"([a-zA-Z0-9])([{CJK}])", r"\1 \2", text)
    return text


def fix_bold_punctuation(text: str) -> str:
    """`**文字，**` → `**文字**，` —— 把中文标点移出加粗。"""
    return re.sub(
        r"\*\*([^*]+?)([，。！？：；、])\*\*",
        r"**\1**\2",
        text,
    )


def strip_first_h1(text: str) -> str:
    """公众号顶部已有标题输入框，正文首个 H1 重复。"""
    return re.sub(r"^# .*?\n+", "", text, count=1, flags=re.MULTILINE)


def extract_external_links(text: str) -> tuple[str, list[tuple[str, str]]]:
    """正文外链 → 角标 + 文末脚注。返回 (新文本, [(label, url)])。

    保留公众号自家链接（`mp.weixin.qq.com`）和锚点链接。
    """
    footnotes: list[tuple[str, str]] = []

    def _replace(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        if (
            url.startswith("#")
            or "mp.weixin.qq.com" in url
            or url.startswith("mailto:")
        ):
            return match.group(0)
        footnotes.append((label, url))
        n = len(footnotes)
        return f'{label}<sup style="color:#326891;">[{n}]</sup>'

    new_text = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", _replace, text)
    return new_text, footnotes


# ---------------------------------------------------------------------------
# Custom container parsing: :::dialogue, :::gallery, :::longimage
# ---------------------------------------------------------------------------

CONTAINER_RE = re.compile(
    r"^:::(dialogue|gallery|longimage)(?:\[([^\]]*)\])?\s*\n(.*?)\n:::\s*$",
    re.DOTALL | re.MULTILINE,
)


def render_dialogue(title: str, body: str, theme: dict[str, Any]) -> str:
    """`:::dialogue[标题]\n张三: 你好\n李四: 你也好\n:::` → 气泡布局"""
    primary = theme["primary"]
    accent = theme.get("muted", "#888")
    lines = [ln.strip() for ln in body.strip().split("\n") if ln.strip()]
    bubbles = []
    speakers: dict[str, int] = {}
    for line in lines:
        m = re.match(r"^([^:：]+)[:：]\s*(.*)$", line)
        if not m:
            continue
        speaker, content = m.group(1).strip(), m.group(2).strip()
        idx = speakers.setdefault(speaker, len(speakers))
        is_left = idx % 2 == 0
        speaker_color = primary if is_left else accent
        bubble_bg = "#ffffff" if is_left else "rgba(0,0,0,0.04)"
        radius = "12px 12px 12px 0" if is_left else "12px 12px 0 12px"
        direction = "" if is_left else "flex-direction:row-reverse;"
        margin = (
            "margin-right:10px"
            if is_left
            else "margin-left:10px"
        )
        bubbles.append(
            f'<section style="display:flex;align-items:flex-start;margin-bottom:12px;{direction}">'
            f'<span style="font-size:13px;font-weight:700;color:{speaker_color};{margin};flex-shrink:0;">{speaker}:</span>'
            f'<section style="flex:1;background:{bubble_bg};padding:10px 14px;border-radius:{radius};font-size:14px;line-height:1.65;color:#333;">{content}</section>'
            f"</section>"
        )
    title_html = (
        f'<p style="font-size:12px;color:#888;margin:0 0 12px 0;font-weight:700;letter-spacing:0.5px;">💬 {title}</p>'
        if title
        else ""
    )
    return (
        f'<section style="margin:20px 0;padding:16px;background:rgba(0,0,0,0.02);border-radius:8px;">'
        f"{title_html}{''.join(bubbles)}</section>"
    )


def render_gallery(title: str, body: str, theme: dict[str, Any]) -> str:
    """`:::gallery[标题]\n![](a.png)\n![](b.png)\n:::` → 横向滚动多图"""
    img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    images = img_pattern.findall(body)
    imgs = "".join(
        f'<img src="{src}" alt="{alt}" style="flex-shrink:0;max-width:80%;border-radius:6px;display:block;" />'
        for alt, src in images
    )
    title_html = (
        f'<p style="font-size:12px;color:#888;margin:0 0 8px 0;font-weight:700;">🖼️ {title}</p>'
        if title
        else ""
    )
    return (
        f'<section style="margin:20px 0;">'
        f"{title_html}"
        f'<section style="display:flex;gap:12px;overflow-x:auto;padding-bottom:8px;">{imgs}</section>'
        f"</section>"
    )


def render_longimage(title: str, body: str, theme: dict[str, Any]) -> str:
    """`:::longimage[标题]\n![](long.png)\n:::` → 固定高度纵向滚动"""
    img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    m = img_pattern.search(body)
    if not m:
        return ""
    alt, src = m.group(1), m.group(2)
    title_html = (
        f'<p style="font-size:12px;color:#888;margin:0 0 8px 0;font-weight:700;">📜 {title}</p>'
        if title
        else ""
    )
    return (
        f'<section style="margin:20px 0;">'
        f"{title_html}"
        f'<section style="max-height:600px;overflow-y:auto;border:1px solid #e0e0e0;border-radius:4px;">'
        f'<img src="{src}" alt="{alt}" style="width:100%;display:block;" />'
        f"</section></section>"
    )


def render_callout(kind: str, title: str, body_html: str, theme: dict[str, Any]) -> str:
    """`> [!tip] 标题\n内容` → 不同色块。"""
    spec = {
        "important": ("⚡", "#326891", "rgba(50,104,145,0.08)"),
        "note":      ("📝", "#326891", "rgba(50,104,145,0.06)"),
        "tip":       ("💡", "#22c55e", "rgba(34,197,94,0.06)"),
        "warning":   ("⚠️", "#f59e0b", "rgba(245,158,11,0.06)"),
        "caution":   ("🚨", "#ef4444", "rgba(239,68,68,0.06)"),
        "callout":   ("✦",  theme["primary"], "rgba(0,0,0,0.04)"),
    }
    icon, color, bg = spec.get(kind.lower(), spec["callout"])
    title_html = (
        f'<p style="font-size:13px;font-weight:700;color:{color};margin:0 0 6px 0;letter-spacing:0.5px;">{icon} {title}</p>'
        if title
        else ""
    )
    return (
        f'<section style="background:{bg};border-left:4px solid {color};padding:12px 16px;margin:20px 0;border-radius:0 4px 4px 0;">'
        f"{title_html}{body_html}</section>"
    )


def preprocess_containers(md: str, theme: dict[str, Any]) -> str:
    """先把 :::xxx::: 容器替换成预渲染的 HTML（用 placeholder 保留，避免被 markdown 二次解析）。"""
    rendered: list[str] = []

    def _replace(match: re.Match) -> str:
        kind = match.group(1)
        title = match.group(2) or ""
        body = match.group(3)
        if kind == "dialogue":
            html = render_dialogue(title, body, theme)
        elif kind == "gallery":
            html = render_gallery(title, body, theme)
        elif kind == "longimage":
            html = render_longimage(title, body, theme)
        else:
            html = ""
        idx = len(rendered)
        rendered.append(html)
        return f"\n\n@@CONTAINER_{idx}@@\n\n"

    md = CONTAINER_RE.sub(_replace, md)
    return md, rendered


CALLOUT_RE = re.compile(
    r"^> \[!(important|note|tip|warning|caution|callout)\](?:\s+(.+))?\n((?:^>.*\n?)+)",
    re.MULTILINE | re.IGNORECASE,
)


def preprocess_callouts(md: str, theme: dict[str, Any]) -> tuple[str, list[str]]:
    rendered: list[str] = []

    def _replace(match: re.Match) -> str:
        kind = match.group(1)
        title = (match.group(2) or "").strip()
        body_lines = match.group(3).splitlines()
        body_md = "\n".join(re.sub(r"^>\s?", "", ln) for ln in body_lines)
        body_html = markdown.markdown(body_md, extensions=["extra"])
        html = render_callout(kind, title, body_html, theme)
        idx = len(rendered)
        rendered.append(html)
        return f"\n\n@@CALLOUT_{idx}@@\n\n"

    md = CALLOUT_RE.sub(_replace, md)
    return md, rendered


# ---------------------------------------------------------------------------
# Post-processing: DOM-level inline styling
# ---------------------------------------------------------------------------

def style_dom(html: str, theme: dict[str, Any]) -> str:
    soup = BeautifulSoup(html, "html.parser")

    def apply(selector: str, css: str) -> None:
        for el in soup.select(selector):
            existing = el.get("style", "")
            el["style"] = (existing + ";" + css).strip(";")

    apply("h1", theme["h1"])
    apply("h2", theme["h2"])
    apply("h3", theme["h3"])
    apply("h4", "font-size:15px;font-weight:700;color:" + theme["text"] + ";margin:20px 0 10px;")
    apply("h5", "font-size:14px;font-weight:700;color:" + theme["text"] + ";margin:18px 0 8px;")
    apply("h6", "font-size:13px;font-weight:700;color:" + theme["muted"] + ";margin:16px 0 6px;")
    apply("p", theme["p"])
    apply("strong", theme["strong"])
    apply("b",      theme["strong"])
    apply("em",     theme["em"])
    apply("i",      theme["em"])
    apply("hr",     theme["hr"])

    for bq in soup.select("blockquote"):
        bq["style"] = (bq.get("style", "") + ";" + theme["blockquote"]).strip(";")
        for p in bq.select("p"):
            p["style"] = "margin:0;font-size:inherit;color:inherit;line-height:inherit;"

    for code in soup.select("code"):
        if code.parent and code.parent.name == "pre":
            continue
        code["style"] = (
            f"background:{theme['code_bg']};padding:2px 6px;border-radius:3px;"
            f"font-family:Consolas,Menlo,'SF Mono',monospace;font-size:0.9em;color:#d6336c;"
        )

    for pre in soup.select("pre"):
        pre["style"] = (
            f"background:{theme['code_bg']};border-radius:6px;padding:14px 16px;margin:16px 0;"
            f"overflow-x:auto;font-family:Consolas,Menlo,'SF Mono',monospace;"
            f"font-size:13px;line-height:1.5;color:#24292e;white-space:pre;"
        )
        for code in pre.select("code"):
            code["style"] = "background:transparent;padding:0;color:inherit;"

    for table in soup.select("table"):
        table["style"] = "width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;"
        for th in table.select("th"):
            th["style"] = (
                f"padding:10px;text-align:left;border-bottom:2px solid {theme['primary']};"
                f"color:{theme['primary']};background:rgba(0,0,0,0.03);"
            )
        for td in table.select("td"):
            td["style"] = "padding:10px;border-bottom:1px solid #e0e0e0;"

    for img in soup.select("img"):
        wrapper = soup.new_tag(
            "section",
            style="text-align:center;margin:16px 0;",
        )
        img["style"] = (
            "max-width:100%;border-radius:4px;display:block;margin:0 auto;"
            "box-shadow:0 2px 8px rgba(0,0,0,0.08);"
        )
        img.replace_with(wrapper)
        wrapper.append(img)

    convert_lists(soup, theme)

    for el in soup.find_all(True):
        if "class" in el.attrs:
            del el["class"]
        if "id" in el.attrs:
            del el["id"]

    return str(soup)


def convert_lists(soup: BeautifulSoup, theme: dict[str, Any]) -> None:
    """微信会抹平 ul/ol 样式，转为 section + flex 模拟。"""
    bullet_color = theme["li_bullet_color"]

    for ul in soup.select("ul"):
        if ul.find_parent(["ul", "ol"]):
            continue
        _convert_list(ul, soup, bullet_color, ordered=False)

    for ol in soup.select("ol"):
        if ol.find_parent(["ul", "ol"]):
            continue
        _convert_list(ol, soup, bullet_color, ordered=True)


def _convert_list(
    list_el: Tag,
    soup: BeautifulSoup,
    bullet_color: str,
    ordered: bool,
    depth: int = 0,
) -> None:
    new_section = soup.new_tag("section", style="margin:14px 0;")
    items = list_el.find_all("li", recursive=False)

    for idx, li in enumerate(items, 1):
        nested_lists = li.find_all(["ul", "ol"], recursive=False)
        for nl in nested_lists:
            nl.extract()

        item_section = soup.new_tag(
            "section",
            style="display:flex;align-items:flex-start;margin-bottom:8px;"
            f"margin-left:{depth * 20}px;",
        )
        if ordered:
            marker = soup.new_tag(
                "span",
                style=(
                    f"display:inline-block;min-width:22px;font-weight:700;"
                    f"color:{bullet_color};margin-right:8px;flex-shrink:0;"
                ),
            )
            marker.string = f"{idx}."
        else:
            marker = soup.new_tag(
                "span",
                style=(
                    f"display:inline-block;width:6px;height:6px;border-radius:50%;"
                    f"background:{bullet_color};margin:9px 12px 0 0;flex-shrink:0;"
                ),
            )
        content = soup.new_tag(
            "section",
            style=f"flex:1;font-size:15px;line-height:1.7;color:{theme_text};",
        )
        for child in list(li.children):
            if isinstance(child, NavigableString):
                content.append(NavigableString(str(child)))
            else:
                content.append(child)
        item_section.append(marker)
        item_section.append(content)
        new_section.append(item_section)

        for nl in nested_lists:
            nested_section = soup.new_tag("section")
            new_section.append(nested_section)
            _convert_list(
                nl, soup, bullet_color, ordered=(nl.name == "ol"), depth=depth + 1
            )
            nested_section.replace_with(nl)

    list_el.replace_with(new_section)


theme_text = "#333"

# ---------------------------------------------------------------------------
# Footnotes
# ---------------------------------------------------------------------------

def render_footnotes(footnotes: list[tuple[str, str]], theme: dict[str, Any]) -> str:
    if not footnotes:
        return ""
    lines = "".join(
        f'<p style="font-size:13px;color:{theme["muted"]};margin:0 0 6px 0;line-height:1.6;">'
        f"[{i}] {label}: {url}</p>"
        for i, (label, url) in enumerate(footnotes, 1)
    )
    return (
        f'<section style="margin-top:32px;padding-top:16px;border-top:1px solid #e0e0e0;">'
        f'<p style="font-size:13px;color:{theme["muted"]};margin:0 0 10px 0;font-weight:700;">参考链接</p>'
        f"{lines}</section>"
    )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def convert(md_text: str, theme_id: str) -> str:
    if theme_id not in THEMES:
        raise ValueError(
            f"Unknown theme: {theme_id}. Available: {', '.join(THEMES.keys())}"
        )
    theme = THEMES[theme_id]

    global theme_text
    theme_text = theme["text"]

    md_text = strip_first_h1(md_text)
    md_text = fix_cjk_spacing(md_text)
    md_text = fix_bold_punctuation(md_text)
    md_text, footnotes = extract_external_links(md_text)
    md_text, container_html = preprocess_containers(md_text, theme)
    md_text, callout_html = preprocess_callouts(md_text, theme)

    html = markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "fenced_code", "tables"],
    )

    for i, h in enumerate(container_html):
        for variant in (
            f"<p>@@CONTAINER_{i}@@</p>",
            f'<p style="font-size:15px;color:#000;line-height:1.7;margin:0 0 18px 0;letter-spacing:0.5px;text-align:left">@@CONTAINER_{i}@@</p>',
            f"@@CONTAINER_{i}@@",
        ):
            html = html.replace(variant, h)
    for i, h in enumerate(callout_html):
        for variant in (
            f"<p>@@CALLOUT_{i}@@</p>",
            f'<p style="font-size:15px;color:#000;line-height:1.7;margin:0 0 18px 0;letter-spacing:0.5px;text-align:left">@@CALLOUT_{i}@@</p>',
            f"@@CALLOUT_{i}@@",
        ):
            html = html.replace(variant, h)
    html = re.sub(r"<p[^>]*>(\s*<section[^>]*>.*?</section>\s*)</p>", r"\1", html, flags=re.DOTALL)

    html = style_dom(html, theme)

    html += render_footnotes(footnotes, theme)

    body_wrapper = (
        f'<section style="font-family:{theme["font_family"]};color:{theme["text"]};'
        f'background:{theme["bg"]};padding:16px;line-height:1.7;">'
        f"{html}"
        f"</section>"
    )
    return body_wrapper


def make_preview(article_html: str, title: str, theme_id: str) -> str:
    """带浏览器壳的预览页（模拟微信宽度 + 显示主题名）。"""
    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>预览：{title}（主题：{THEMES[theme_id]["name"]}）</title>
<style>
body {{ background:#f3f3f3; margin:0; padding:24px; font-family:-apple-system,BlinkMacSystemFont,sans-serif; }}
.toolbar {{ max-width:677px; margin:0 auto 12px auto; padding:8px 14px; background:#fff; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.06); font-size:13px; color:#666; display:flex; gap:16px; align-items:center; }}
.toolbar strong {{ color:#326891; }}
.wechat-frame {{ max-width:677px; margin:0 auto; background:#fff; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.08); overflow:hidden; }}
.wechat-frame > section {{ padding:24px !important; }}
.tip {{ max-width:677px; margin:12px auto 0 auto; padding:12px; background:#fff8e1; border:1px solid #ffe082; border-radius:4px; font-size:12px; color:#5d4037; }}
</style>
</head>
<body>
<div class="toolbar">
  <span>📝 <strong>{title}</strong></span>
  <span>🎨 主题：<strong>{THEMES[theme_id]["name"]}</strong></span>
  <span>📐 宽度模拟：677px（微信编辑器）</span>
</div>
<div class="wechat-frame">{article_html}</div>
<div class="tip">💡 复制方法：在此预览页 Cmd+A 全选 → Cmd+C 复制 → 公众号编辑器 Cmd+V 粘贴。直接复制 .html 文件不行，必须从浏览器复制。</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Markdown → 微信公众号兼容的样式化 HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
EXAMPLES:
    %(prog)s --input article.md --theme newspaper --output article.html
    %(prog)s --list-themes

预览方式（重要）：
    脚本会在末尾打印一个 file:// 开头的 URL。
    复制这个 URL → 粘贴到浏览器地址栏（Chrome/Edge/Safari 都行）→ 回车。
    不要用 open / 双击 / 默认应用等方式打开 —— 那些方式复制出来粘到公众号会丢样式。
""",
    )
    parser.add_argument("--input", "-i", help="Markdown 文件路径")
    parser.add_argument("--output", "-o", help="HTML 输出路径（默认 <input>.html）")
    parser.add_argument(
        "--theme", "-t", default="newspaper",
        help=f"主题（默认 newspaper）。可选：{', '.join(THEMES.keys())}",
    )
    parser.add_argument(
        "--open", action="store_true",
        help="（已废弃）通过 webbrowser 打开预览。建议改为复制脚本输出的 file:// URL 粘到浏览器地址栏。"
    )
    parser.add_argument("--list-themes", action="store_true", help="列出所有主题")
    args = parser.parse_args()

    if args.list_themes:
        print(f"\n可用主题（{len(THEMES)} 个）：\n")
        for tid, t in THEMES.items():
            print(f"  {tid:18s}  {t['name']}")
        print()
        return 0

    if not args.input:
        parser.error("--input is required (or use --list-themes)")

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        print(f"❌ Input not found: {in_path}", file=sys.stderr)
        return 2

    out_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else in_path.with_suffix(".html")
    )
    preview_path = out_path.with_suffix(".preview.html")

    md_text = in_path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+?)\s*$", md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else in_path.stem

    article_html = convert(md_text, args.theme)
    out_path.write_text(article_html, encoding="utf-8")

    preview_html = make_preview(article_html, title, args.theme)
    preview_path.write_text(preview_html, encoding="utf-8")

    print(f"✅ HTML:    {out_path}")
    print(f"✅ Preview: {preview_path}")
    print(f"🎨 Theme:   {args.theme} ({THEMES[args.theme]['name']})")

    print()
    print("📋 复制下面这一行 URL，粘贴到浏览器地址栏（Chrome/Edge/Safari 都行）→ 回车：")
    print()
    print(f"   file://{preview_path}")
    print()
    print("⚠️  不要用 open / 双击 / 默认应用打开——那些方式复制粘贴到公众号会丢样式。")

    if args.open:
        print()
        print("⚠️  --open 选项已废弃，调用 webbrowser 打开仅作兼容。强烈建议手动复制上面的 URL 到浏览器地址栏。")
        webbrowser.open(f"file://{preview_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
