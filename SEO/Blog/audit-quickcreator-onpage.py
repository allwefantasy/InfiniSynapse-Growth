#!/usr/bin/env python3
"""Audit the 4 QuickCreator On-Page SEO issues across all 100 articles.

1. Canonical URL present (meta-tags.html)
2. Single H1 (article.md should have exactly one leading '# ')
3. Meta description length 150-160 chars
4. Social media meta tags present (og:* + twitter:*)
"""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).parent


def pillar_dirs() -> list[Path]:
    return sorted(
        p for p in BLOG.glob("pillar[1-8]-*")
        if p.is_dir() and " copy" not in p.name
    )


def article_dirs() -> list[Path]:
    out = []
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            if (art / "article.md").is_file():
                out.append(art)
    return out


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


def main() -> None:
    arts = article_dirs()
    issues = {"canonical": [], "multi_h1": [], "desc_len": [], "social": []}
    desc_lengths = []

    for art in arts:
        md = (art / "article.md").read_text(encoding="utf-8")
        meta = (art / "meta-tags.html")
        html = meta.read_text(encoding="utf-8") if meta.is_file() else ""
        aid = art.name[:3]

        # 1. canonical
        if 'rel="canonical"' not in html:
            issues["canonical"].append(aid)

        # 2. H1
        h1n = count_h1(md)
        if h1n != 1:
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

    print(f"Audited {len(arts)} articles\n")
    print(f"1. Missing canonical:        {len(issues['canonical'])}")
    if issues["canonical"]:
        print(f"   {', '.join(issues['canonical'])}")
    print(f"2. H1 count != 1 (in body):  {len(issues['multi_h1'])}")
    if issues["multi_h1"]:
        print(f"   {', '.join(issues['multi_h1'])}")
    print(f"3. Meta desc NOT 150-160:    {len(issues['desc_len'])}")
    if issues["desc_len"]:
        print(f"   {', '.join(issues['desc_len'])}")
    print(f"4. Missing social tags:      {len(issues['social'])}")
    if issues["social"]:
        print(f"   {', '.join(issues['social'])}")

    too_short = [f"{a}({l})" for a, l in desc_lengths if l < 150]
    too_long = [f"{a}({l})" for a, l in desc_lengths if l > 160]
    print(f"\n   desc <150: {len(too_short)}  |  desc >160: {len(too_long)}")
    if desc_lengths:
        avg = sum(l for _, l in desc_lengths) / len(desc_lengths)
        print(f"   desc length min={min(l for _,l in desc_lengths)} "
              f"max={max(l for _,l in desc_lengths)} avg={avg:.0f}")


if __name__ == "__main__":
    main()
