#!/usr/bin/env python3
"""Audit: Target keyword must appear in title (H1 + meta <title>) and description."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from article_keyword_meta import target_keyword as resolve_keyword

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]


def extract_keyword(article_path: Path, text: str) -> str:
    kw = resolve_keyword(article_path, text)
    if kw:
        return kw.lower()
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).strip().lower() if m else ""


def extract_h1(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_article_desc(text: str) -> str:
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    if not m:
        return ""
    desc = m.group(1).strip()
    return re.sub(r"\s*\(\d+\s*chars\)\s*$", "", desc, flags=re.I)


def meta_fields(meta_path: Path) -> tuple[str, str]:
    if not meta_path.is_file():
        return "", ""
    mt = meta_path.read_text(encoding="utf-8")
    title = re.search(r"<title>([^<]+)</title>", mt, re.I)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', mt, re.I)
    return (
        title.group(1).strip() if title else "",
        desc.group(1).strip() if desc else "",
    )


def audit(article_path: Path) -> list[str]:
    text = article_path.read_text(encoding="utf-8")
    kw = extract_keyword(article_path, text)
    if not kw:
        return ["missing target keyword (article-meta.json)"]

    fails: list[str] = []
    h1 = extract_h1(text)
    art_desc = extract_article_desc(text)
    meta_title, meta_desc = meta_fields(article_path.parent / "meta-tags.html")

    if not h1:
        fails.append("missing H1 (# title)")
    elif kw not in h1.lower():
        fails.append(f"H1 missing keyword: {h1[:50]}")

    if not art_desc:
        fails.append("missing **Meta Description** in article.md")
    elif kw not in art_desc.lower():
        fails.append("article Meta Description missing keyword")

    if not (article_path.parent / "meta-tags.html").is_file():
        fails.append("missing meta-tags.html")
    else:
        if not meta_title:
            fails.append("missing <title> in meta-tags.html")
        elif kw not in meta_title.lower():
            fails.append("meta-tags <title> missing keyword")
        if not meta_desc:
            fails.append("missing meta description tag")
        elif kw not in meta_desc.lower():
            fails.append("meta-tags description missing keyword")

    return fails


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = fail_n = 0
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            fails = audit(art)
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails[:3]:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
