#!/usr/bin/env python3
"""Convert 90-day playbook Markdown → HTML with week jump navigation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import markdown
from markdown.extensions.tables import TableExtension


def slugify(text: str) -> str:
    text = re.sub(r"[`*]", "", text)
    text = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", text.strip().lower())
    return re.sub(r"-+", "-", text).strip("-") or "section"


def extract_week_links(html: str) -> list[tuple[str, str]]:
    """Find h3 headings like '第 N 周' and return (label, id)."""
    links: list[tuple[str, str]] = []
    for m in re.finditer(r'<h3 id="([^"]+)">([^<]+)</h3>', html):
        hid, title = m.group(1), m.group(2).strip()
        if re.search(r"第\s*\d+", title) or "10–12" in title or "10-12" in title:
            short = re.sub(r"\s*·.*", "", title)
            links.append((short, hid))
    return links


def add_heading_ids(html: str) -> str:
    counters: dict[int, int] = {}

    def repl(m: re.Match) -> str:
        level = int(m.group(1))
        inner = m.group(2)
        counters[level] = counters.get(level, 0) + 1
        for l in list(counters):
            if l > level:
                counters[l] = 0
        hid = slugify(re.sub(r"<[^>]+>", "", inner))
        if level == 3 and re.search(r"第\s*\d+", inner):
            w = re.search(r"第\s*(\d+)", inner)
            if w:
                hid = f"week-{w.group(1)}"
        elif "10" in inner and ("12" in inner or "–" in inner):
            hid = "week-10-12"
        return f'<h{level} id="{hid}">{inner}</h{level}>'

    return re.sub(r"<h([2-4])>(.*?)</h\1>", repl, html, flags=re.DOTALL)


def build_week_jump(links: list[tuple[str, str]]) -> str:
    if not links:
        return ""
    pills = "".join(
        f'<a href="#{hid}">{label}</a>' for label, hid in links
    )
    sections = "".join(
        f'<a href="#appendix-{chr(65 + i)}">附录 {chr(65 + i)}</a>'
        for i in range(5)
    )
    return f"""
<div class="week-jump-wrap">
  <div class="week-jump-label">按周跳转</div>
  <nav class="week-jump">{pills}</nav>
  <nav class="week-jump week-jump-appendix">{sections}</nav>
</div>"""


def wrap_page(
    *,
    title: str,
    subtitle: str,
    css_href: str,
    index_href: str,
    index_anchor: str,
    seo_href: str,
    reddit_href: str,
    body_html: str,
    week_links: list[tuple[str, str]],
) -> str:
    jump = build_week_jump(week_links)
    # Tag appendix h2 for jump
    for i, letter in enumerate("ABCDE"):
        body_html = body_html.replace(
            f"<h2>附录 {letter}",
            f'<h2 id="appendix-{letter}">附录 {letter}',
            1,
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="{css_href}" />
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <div class="topbar-brand">InfiniSynapse · 90 天执行手册</div>
    <nav class="topbar-nav">
      <a href="{index_href}">← 返回总报告</a>
      <a href="{index_href}{index_anchor}">周历摘要</a>
      <a href="{seo_href}">SEO 手册</a>
      <a href="{reddit_href}">Reddit 手册</a>
    </nav>
  </div>
</header>
<div class="page playbook-page">
  <p class="breadcrumb"><a href="{index_href}">增长调研报告</a> / {subtitle}</p>
  {jump}
  <article class="playbook-content">
{body_html}
  </article>
  <footer class="footer">
    {title} · 源文件 Markdown 同步更新后请运行 <code>python3 build-playbook-html.py</code>
  </footer>
</div>
</body>
</html>
"""


def convert(md_path: Path, out_path: Path, *, css_href: str, index_href: str, index_anchor: str, seo_href: str, reddit_href: str, title: str, subtitle: str) -> None:
    text = md_path.read_text(encoding="utf-8")
    # Strip YAML-style title blockquote metadata stays; markdown handles it
    html = markdown.markdown(
        text,
        extensions=[
            TableExtension(),
            "fenced_code",
            "nl2br",
            "sane_lists",
        ],
    )
    html = add_heading_ids(html)
    week_links = extract_week_links(html)
    page = wrap_page(
        title=title,
        subtitle=subtitle,
        css_href=css_href,
        index_href=index_href,
        index_anchor=index_anchor,
        seo_href=seo_href,
        reddit_href=reddit_href,
        body_html=html,
        week_links=week_links,
    )
    out_path.write_text(page, encoding="utf-8")
    print(f"Wrote {out_path} ({len(week_links)} week anchors)")


def main() -> int:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Build SEO + Reddit HTML")
    args = parser.parse_args()

    growth = base
    growth_idx = "index.html"
    jobs = [
        (
            base / "SEO-90天可执行操作手册.md",
            base / "SEO-90天可执行操作手册.html",
            "assets/report.css",
            growth_idx,
            "#seo-weekly",
            "SEO-90天可执行操作手册.html",
            "Reddit-90天可执行操作手册.html",
            "SEO 90 天可执行操作手册",
            "SEO · Google 搜索",
        ),
        (
            base / "Reddit-90天可执行操作手册.md",
            base / "Reddit-90天可执行操作手册.html",
            "assets/report.css",
            growth_idx,
            "#reddit-weekly",
            "SEO-90天可执行操作手册.html",
            "Reddit-90天可执行操作手册.html",
            "Reddit 90 天可执行操作手册",
            "Reddit · 社区运营",
        ),
    ]

    reddit_src = Path(__file__).resolve().parents[2] / "Reddit运营" / "Reddit-InfiniSynapse-90天可执行操作手册.md"
    reddit_out = reddit_src.parent / "Reddit-InfiniSynapse-90天可执行操作手册.html"
    rel_growth = "../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析"
    if reddit_src.exists():
        jobs.append(
            (
                reddit_src,
                reddit_out,
                f"{rel_growth}/assets/report.css",
                f"{rel_growth}/index.html",
                "#reddit-weekly",
                f"{rel_growth}/SEO-90天可执行操作手册.html",
                "Reddit-InfiniSynapse-90天可执行操作手册.html",
                "Reddit 90 天可执行操作手册",
                "Reddit · 社区运营",
            )
        )

    for md, out, css, idx, anchor, seo_h, red_h, title, sub in jobs:
        if not md.exists():
            print(f"Skip missing {md}", file=sys.stderr)
            continue
        convert(md, out, css_href=css, index_href=idx, index_anchor=anchor, seo_href=seo_h, reddit_href=red_h, title=title, subtitle=sub)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
