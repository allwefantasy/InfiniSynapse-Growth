#!/usr/bin/env python3
"""
inject-styles.py — 给 md2html.py 输出的 HTML 注入行内样式, 配合 wechat-mp-draft-skill 使用.

为什么需要这步:
公众号 ProseMirror 编辑器只接受**行内样式 (inline style)**. CSS 类名 / <style> 块都会被
编辑器粘贴时丢弃. 所以必须给每个 HTML 标签预先打上 style="..." 才能在公众号里呈现出
设计感(字号 / 颜色 / 行距 / 对齐 / 边框 等).

设计要点:
1. 用负向先行断言 `(?![^>]*style=)` 跳过已经有 style 属性的标签
   —— 这样图片占位符 <p data-image-placeholder="..." style="..."> 不会被覆盖.
2. 默认是 InfiniSynapse 蓝主色调 + 15px 正文 + 1.75 行高的"产品文风".
   要改换主题, 直接编辑 TAG_STYLES 字典即可.
3. 同时输出 .html 和 .b64 两个文件, 后者用于通过 agent-browser eval 注入到公众号编辑器.

用法:
    python3 inject-styles.py --in article.html --out-html article.html --out-b64 article.html.b64

流水线 (与 md2html.py 串起来):
    python3 md2html.py --in article.md --out-html article.html --out-b64 article.html.b64
    python3 inject-styles.py --in article.html --out-html article.html --out-b64 article.html.b64
"""
import argparse
import base64
import re
import sys


# ---------- 样式预设 ----------
# 改换设计风格 = 改这个字典. 键是 HTML 标签名, 值是 inline style 字符串.
# 默认主题: 蓝色品牌主色, 适合数据/AI 类技术品牌的官方文章.
TAG_STYLES_DEFAULT = {
    "h1": (
        "font-size:20px;color:#1e6fff;line-height:1.75;text-align:left;"
        "font-weight:bold;margin:1.4em 0 0.8em;"
    ),
    "h2": (
        "font-size:18px;color:#1e6fff;line-height:4;text-align:left;"
        "font-weight:bold;margin:1.2em 0 0.6em;"
    ),
    "h3": (
        "font-size:16px;color:#333;line-height:4;text-align:left;"
        "font-weight:bold;margin:1em 0 0.5em;"
    ),
    "p": (
        "font-size:15px;line-height:1.75;text-align:left;letter-spacing:0.5px;"
    ),
    "li": (
        "font-size:15px;line-height:1.75;text-align:left;"
    ),
    "blockquote": (
        "font-size:14px;line-height:1.75;color:#666;"
        "border-left:3px solid #1e6fff;padding-left:12px;margin:1em 0;"
    ),
    "table": (
        "font-size:14px;line-height:1.75;border-collapse:collapse;"
        "width:100%;margin:1em 0;"
    ),
    "th": (
        "font-size:14px;line-height:1.75;padding:6px 8px;"
        "font-weight:bold;background:#f5f8ff;"
    ),
    "td": (
        "font-size:14px;line-height:1.75;padding:6px 8px;"
    ),
}


def inject(html: str, tag_styles: dict) -> str:
    """对每个标签, 在没有 style 属性时注入默认样式."""
    for tag, style in tag_styles.items():
        # 负向先行断言: 跳过已经有 style="..." 的标签
        # 这样 md2html.py 生成的图片占位符 <p ... style="..."> 不会被覆盖
        html = re.sub(
            r"<" + tag + r"(?![^>]*style=)([^>]*)>",
            f'<{tag} style="{style}"\\1>',
            html,
        )
    return html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inject inline styles into HTML for WeChat MP editor"
    )
    parser.add_argument(
        "--in", dest="input_file",
        default="article.html",
        help="Input HTML file (default: article.html in cwd)",
    )
    parser.add_argument(
        "--out-html", dest="out_html",
        default=None,
        help="Output HTML file (default: overwrite input)",
    )
    parser.add_argument(
        "--out-b64", dest="out_b64",
        default=None,
        help="Output base64 file (default: <out-html>.b64)",
    )
    args = parser.parse_args()

    out_html = args.out_html or args.input_file
    out_b64 = args.out_b64 or (out_html + ".b64")

    with open(args.input_file, "r", encoding="utf-8") as f:
        html = f.read()
    before_len = len(html)

    html = inject(html, TAG_STYLES_DEFAULT)

    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
    with open(out_b64, "w", encoding="utf-8") as f:
        f.write(b64)

    print(f"Input HTML:  {args.input_file} ({before_len} chars)")
    print(f"Styled HTML: {out_html} ({len(html)} chars)")
    print(f"Base64:      {out_b64} ({len(b64)} chars)")
    print()
    print("Next: paste base64 into ProseMirror via agent-browser (see SKILL.md §5).")


if __name__ == "__main__":
    main()
