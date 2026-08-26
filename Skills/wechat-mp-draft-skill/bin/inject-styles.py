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

# 插图注解(图注)专属样式: 所有整段被 * 包裹的斜体段 (md 里的 `*图 N：...*`,
# 渲染后是 <p><em>...</em></p>) 统一 13 号 / 斜体 / 居中.
# color 是保守的图注灰, 只为观感; 三条硬要求是 font-size:13px / font-style:italic / text-align:center.
CAPTION_STYLE = (
    "font-size:13px;font-style:italic;text-align:center;"
    "color:#888;line-height:1.75;margin:0.4em 0 1em;"
)

# 网址 / 超链接文字统一品牌蓝. 注意: 公众号正文会**剥离外部 <a> 超链接**(外链在正文不可点),
# 只保留纯文字, 连 <a> 上的 inline color 也一起丢. 所以不能靠给 <a> 打 style, 必须在 paste 前
# 把 <a>...</a> 整个换成 <span style="蓝色">...</span> —— span 会被编辑器保留, 文字才真的变蓝.
LINK_SPAN_STYLE = "color:#1e6fff;word-break:break-all;"


def style_links(html: str) -> str:
    """把所有 <a ...>text</a> 转成蓝色 <span>text</span>.

    为什么不直接给 <a> 打 style: 公众号 ProseMirror 粘贴时会把外部链接的 <a> 拆掉(href 不
    允许跳转), 文字并回段落, inline color 也丢. 换成 <span> 后没有 href, 编辑器当普通带色文字
    保留, 链接文字就能稳定显示为品牌蓝. (内部 #话题# 标签由公众号自动生成并强制 #576B95, 不归此处管.)
    """
    return re.sub(
        r"<a\b[^>]*>(.*?)</a>",
        lambda m: f'<span style="{LINK_SPAN_STYLE}">{m.group(1)}</span>',
        html,
        flags=re.DOTALL,
    )


def style_captions(html: str) -> str:
    """给图注段落打专属样式.

    图注 = 整个段落只有一个 <em> 子节点 (即 md 里 `*...*` 单独成段). 必须在通用
    <p> 注入**之前**跑 —— 这样后续 `(?![^>]*style=)` 会自动跳过已打样式的图注段,
    图注就不会被 15px 左对齐的默认 <p> 样式覆盖.
    """
    return re.sub(
        r"<p(?![^>]*style=)([^>]*)>(\s*<em>.*?</em>\s*)</p>",
        f'<p style="{CAPTION_STYLE}"\\1>\\2</p>',
        html,
        flags=re.DOTALL,
    )


def inject(html: str, tag_styles: dict) -> str:
    """对每个标签, 在没有 style 属性时注入默认样式."""
    # 链接先转成蓝色 span (公众号会剥离 <a>, 见 style_links docstring)
    html = style_links(html)
    # 图注要先于通用 <p> 处理, 否则会被默认段落样式吃掉
    html = style_captions(html)
    for tag, style in tag_styles.items():
        # `(?=[\s/>])` 加标签名边界: 防止 <a> 误伤 <abbr>/<article>, <p> 误伤 <pre> 等.
        # 负向先行断言 `(?![^>]*style=)`: 跳过已经有 style="..." 的标签,
        # 这样 md2html.py 生成的图片占位符 <p ... style="..."> 不会被覆盖.
        html = re.sub(
            r"<" + tag + r"(?=[\s/>])(?![^>]*style=)([^>]*)>",
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
