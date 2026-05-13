#!/usr/bin/env python3
"""
md2html.py — 把 Markdown 转成适合 **微信公众号 ProseMirror 编辑器**粘贴的 HTML。

配套 `wechat-mp-draft-skill`。脚本做 3 件事：

1. 删掉文件开头的第一个 `# 一级标题`（因为公众号编辑器顶部已经有独立的"标题"输入框，
   正文再来一个 H1 会重复显示）。
2. 把 `![alt](images/XX.png)` 转成带 `data-image-placeholder` 属性的醒目占位段落，
   方便后续在浏览器端用 JS 定位并替换为真正上传到 mmbiz CDN 的图片。
3. 输出 base64 版本，便于通过 `agent-browser eval` 传递长 HTML 字符串而不被
   shell 的引号/反斜杠转义吃掉。

用法:
    python3 md2html.py --in draft.md --out-html draft.html --out-b64 draft.html.b64

或使用默认路径 (当前目录):
    python3 md2html.py
"""
import argparse
import base64
import re
import sys
from typing import List, Tuple

try:
    import markdown
except ImportError:
    sys.stderr.write(
        "Missing `markdown` package.\n"
        "Install:  pip3 install markdown\n"
    )
    sys.exit(1)


def convert(md_text: str) -> Tuple[str, List[str]]:
    """Return (styled_html, list_of_image_paths)."""

    md_text = re.sub(r'^# .*?\n\n', '', md_text, count=1, flags=re.MULTILINE)

    images = re.findall(r'!\[.*?\]\((images/[^)]+)\)', md_text)

    md_no_images = re.sub(
        r'!\[(.*?)\]\((images/[^)]+)\)',
        lambda m: f'\n\n@@IMAGE_PLACEHOLDER::{m.group(2)}::{m.group(1)}@@\n\n',
        md_text,
    )

    html = markdown.markdown(
        md_no_images,
        extensions=["extra", "sane_lists"],
    )

    html = re.sub(
        r'<p>@@IMAGE_PLACEHOLDER::(.*?)::(.*?)@@</p>',
        lambda m: (
            f'<p data-image-placeholder="{m.group(1)}" '
            f'style="text-align:center;color:#999;background:#f7f7f7;padding:10px;">'
            f'【待上传图片：{m.group(2) or m.group(1)}】</p>'
        ),
        html,
    )

    styled_html = f'<section>\n{html}\n</section>'
    return styled_html, images


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markdown → HTML for wechat-mp-draft-skill",
    )
    parser.add_argument(
        "--in", dest="input_file",
        default="draft.md",
        help="Input Markdown file (default: draft.md in cwd)",
    )
    parser.add_argument(
        "--out-html", dest="out_html",
        default="draft.html",
        help="Output HTML file (default: draft.html)",
    )
    parser.add_argument(
        "--out-b64", dest="out_b64",
        default="draft.html.b64",
        help="Output base64 file for eval transfer (default: draft.html.b64)",
    )
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    html, images = convert(md_text)

    with open(args.out_html, "w", encoding="utf-8") as f:
        f.write(html)

    b64 = base64.b64encode(html.encode("utf-8")).decode("ascii")
    with open(args.out_b64, "w", encoding="utf-8") as f:
        f.write(b64)

    print(f"Markdown source: {args.input_file} ({len(md_text)} chars)")
    print(f"HTML output:     {args.out_html} ({len(html)} chars)")
    print(f"Base64 output:   {args.out_b64} ({len(b64)} chars)")
    print(f"Images found ({len(images)}):")
    for img in images:
        print(f"  - {img}")

    print()
    print("Next step — paste this HTML into ProseMirror editor. In agent-browser:")
    print()
    print(f'  B64=$(cat {args.out_b64})')
    print('  ~/.auto-coder/.autocodertools/agent-browser eval "(() => {')
    print("    const b64 = '${B64}';")
    print('    window.__article_html = decodeURIComponent(escape(atob(b64)));')
    print('    return \'html_len=\' + window.__article_html.length;')
    print('  })()"')


if __name__ == "__main__":
    main()
