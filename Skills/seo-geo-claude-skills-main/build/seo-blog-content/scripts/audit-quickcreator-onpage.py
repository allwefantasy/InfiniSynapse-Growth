#!/usr/bin/env python3
"""Audit the 4 QuickCreator / On-Page SEO issues on the DEPLOY pack.

1. Canonical URL present (meta-tags.html)
2. No H1 in the deploy body (article.md) — page <h1> is rendered from the title,
   so a body H1 would create a duplicate on the live page.
3. Meta description length 150-160 chars
4. Social media meta tags present (og:* + twitter:*)
5. Meta <title> length 40-60 chars (QuickCreator On-Page rule)

Default target = frontend-handoff/content (the body-only deploy copies). Pass a path to
override. NOTE: do not point this at the source SEO/Blog/pillar* tree for the H1 check —
source intentionally keeps its H1 for the authoring gates.

Usage:
  python3 audit-quickcreator-onpage.py                      # frontend-handoff/content
  python3 audit-quickcreator-onpage.py frontend-handoff/content
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
DEFAULT_TARGET = BLOG / "frontend-handoff" / "content"


def article_dirs(target: Path) -> list[Path]:
    return [md.parent for md in sorted(target.rglob("article.md"))]


def count_h1(md: str) -> int:
    # ATX H1: lines starting with single '# ' (not ## etc), outside code fences
    n = 0
    in_fence = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^#\s+\S", line):
            n += 1
    return n


def md_meta_desc(md: str) -> str | None:
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)", md)
    return m.group(1).strip() if m else None


def html_desc(html: str) -> str | None:
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    return m.group(1) if m else None


def html_title(html: str) -> str | None:
    m = re.search(r"<title>([^<]*)</title>", html)
    return m.group(1) if m else None


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TARGET
    if not target.is_dir():
        print(f"Target not found: {target}\nBuild it first: python3 build-frontend-handoff.py")
        raise SystemExit(1)
    arts = article_dirs(target)
    print(f"Target: {target}")
    issues = {"canonical": [], "multi_h1": [], "desc_len": [], "social": [], "title_len": []}
    desc_lengths = []
    title_lengths = []

    for art in arts:
        md = (art / "article.md").read_text(encoding="utf-8")
        meta = (art / "meta-tags.html")
        html = meta.read_text(encoding="utf-8") if meta.is_file() else ""
        aid = art.name[:3]

        # 1. canonical
        if 'rel="canonical"' not in html:
            issues["canonical"].append(aid)

        # 2. H1 — body must have 0 (page H1 is rendered by template from the title);
        #    any H1 in body would create a duplicate alongside the template H1.
        h1n = count_h1(md)
        if h1n != 0:
            issues["multi_h1"].append(f"{aid}({h1n})")

        # 3. meta desc length (use html meta description as source of truth)
        desc = html_desc(html) or md_meta_desc(md) or ""
        dlen = len(desc)
        desc_lengths.append((aid, dlen))
        if not (150 <= dlen <= 160):
            issues["desc_len"].append(f"{aid}({dlen})")

        # 4. social tags
        has_og = 'property="og:title"' in html and 'property="og:image"' in html
        has_tw = 'name="twitter:card"' in html
        if not (has_og and has_tw):
            issues["social"].append(aid)

        # 5. title length 40-60
        title = html_title(html) or ""
        tlen = len(title)
        title_lengths.append((aid, tlen))
        if not (40 <= tlen <= 60):
            issues["title_len"].append(f"{aid}({tlen})")

    print(f"Audited {len(arts)} articles\n")
    print(f"1. Missing canonical:        {len(issues['canonical'])}")
    if issues["canonical"]:
        print(f"   {', '.join(issues['canonical'])}")
    print(f"2. H1 in body (must be 0):   {len(issues['multi_h1'])}")
    if issues["multi_h1"]:
        print(f"   {', '.join(issues['multi_h1'])}")
    print(f"3. Meta desc NOT 150-160:    {len(issues['desc_len'])}")
    if issues["desc_len"]:
        print(f"   {', '.join(issues['desc_len'])}")
    print(f"4. Missing social tags:      {len(issues['social'])}")
    if issues["social"]:
        print(f"   {', '.join(issues['social'])}")
    print(f"5. Title NOT 40-60 chars:    {len(issues['title_len'])}")
    if issues["title_len"]:
        print(f"   {', '.join(issues['title_len'])}")

    too_short = [f"{a}({l})" for a, l in desc_lengths if l < 150]
    too_long = [f"{a}({l})" for a, l in desc_lengths if l > 160]
    print(f"\n   desc <150: {len(too_short)}  |  desc >160: {len(too_long)}")
    if desc_lengths:
        avg = sum(l for _, l in desc_lengths) / len(desc_lengths)
        print(f"   desc length min={min(l for _,l in desc_lengths)} "
              f"max={max(l for _,l in desc_lengths)} avg={avg:.0f}")
    t_short = [a for a, l in title_lengths if l < 40]
    t_long = [a for a, l in title_lengths if l > 60]
    print(f"   title <40: {len(t_short)}  |  title >60: {len(t_long)}")
    if title_lengths:
        print(f"   title length min={min(l for _,l in title_lengths)} "
              f"max={max(l for _,l in title_lengths)} avg={sum(l for _,l in title_lengths)/len(title_lengths):.0f}")


if __name__ == "__main__":
    main()
