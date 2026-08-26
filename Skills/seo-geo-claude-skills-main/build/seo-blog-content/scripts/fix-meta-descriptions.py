#!/usr/bin/env python3
"""Normalize all meta descriptions to 150-160 chars (complete words, no dangling fragments).

Syncs article.md (**Meta Description**), meta-tags.html (description/og/twitter), schema.json.
- In range: keep.
- Too long: trim at a word boundary <=160, drop trailing function words.
- Too short: append a complete, type-appropriate clause, stopping on a real word in [150,160].
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
LO, HI = 150, 160

FUNC = {
    "a", "an", "the", "and", "or", "with", "for", "to", "of", "in", "on", "at",
    "by", "plus", "&", "it", "is", "its", "each", "that", "this", "as", "from",
}

# Graded COMPLETE tail sentences (with leading space + trailing period).
# Pick the longest whose total lands in [LO, HI]; never truncated → no fragments.
TAILS_FAQ = [
    " Read on.",                                                       # 9
    " Learn more.",                                                    # 12
    " See the FAQ.",                                                   # 13
    " Includes a quick FAQ.",                                          # 22
    " Includes examples and a FAQ.",                                   # 29
    " Includes worked examples and a FAQ.",                            # 36
    " Includes worked examples, criteria, and a FAQ.",                 # 47
    " Includes worked examples, clear criteria, and a buyer FAQ.",     # 58
    " Includes worked examples, clear criteria, pricing, and a buyer FAQ.",  # 67
]
TAILS_NOFAQ = [
    " Read on.",                                                       # 9
    " Learn more.",                                                    # 12
    " See real examples.",                                             # 19
    " Includes worked examples.",                                      # 26
    " Includes worked examples and steps.",                            # 36
    " Includes worked examples, criteria, and steps.",                 # 47
    " Includes worked examples, clear criteria, and next steps.",      # 57
    " Includes worked examples, clear criteria, pricing, and next steps.",   # 66
]


def pillar_dirs() -> list[Path]:
    return sorted(
        p for p in BLOG.glob("pillar*")
        if p.is_dir() and re.match(r"pillar\d+", p.name) and " copy" not in p.name
    )


def load_content_types() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in ("blog-cms-import-202.csv", "blog-cms-import-100.csv"):
        csv_path = BLOG / name
        if not csv_path.is_file():
            continue
        with csv_path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                out[row["folder"]] = row["content_type"]
    return out


def strip_trailing_func(text: str) -> str:
    words = text.rstrip(" ,;:.—-").split()
    while words and words[-1].lower().strip(",;:") in FUNC:
        words.pop()
    return " ".join(words).rstrip(" ,;:—-")


def trim_long(base: str) -> str:
    words = base.split()
    acc = ""
    for w in words:
        cand = (acc + " " + w).strip()
        if len(cand) + 1 > HI:
            break
        acc = cand
    acc = strip_trailing_func(acc)
    return acc + "."


def extend_short(base: str, ctype: str) -> str:
    base = base.rstrip(" .") + "."
    tails = TAILS_NOFAQ if "faq" in base.lower() else TAILS_FAQ
    best = None
    for tail in tails:  # ascending length
        total = base + tail
        if LO <= len(total) <= HI:
            best = total  # keep longest that still fits
        elif len(total) > HI:
            break
    if best is None:
        # base extremely short/long edge: use the largest tail that keeps <=HI
        for tail in tails:
            if len(base + tail) <= HI:
                best = base + tail
        best = best or (base + tails[0])
    return best


def make_description(cur: str, ctype: str) -> str:
    n = len(cur)
    if LO <= n <= HI:
        return cur
    if n > HI:
        return trim_long(cur)
    return extend_short(cur, ctype)


def update_article_md(path: Path, new_desc: str) -> None:
    text = path.read_text(encoding="utf-8")
    new = re.sub(r"(\*\*Meta Description\*\*:\s*).+", lambda m: m.group(1) + new_desc, text, count=1)
    if new != text:
        path.write_text(new, encoding="utf-8")


def update_meta_html(path: Path, new_desc: str) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    esc = new_desc.replace('"', "&quot;")
    for attr in (
        '<meta name="description" content="',
        '<meta property="og:description" content="',
        '<meta name="twitter:description" content="',
    ):
        text = re.sub(re.escape(attr) + r'[^"]*"', attr + esc + '"', text, count=1)
    path.write_text(text, encoding="utf-8")


def update_schema(path: Path, new_desc: str) -> None:
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    changed = False
    for item in data:
        if item.get("@type") == "BlogPosting" and "description" in item:
            item["description"] = new_desc
            changed = True
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ctypes = load_content_types()
    fixed = 0
    descs: dict[str, str] = {}
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            md_path = art / "article.md"
            if not md_path.is_file():
                continue
            html_path = art / "meta-tags.html"
            html = html_path.read_text(encoding="utf-8") if html_path.is_file() else ""
            m = re.search(r'<meta name="description" content="([^"]*)"', html)
            md_text = md_path.read_text(encoding="utf-8")
            mm = re.search(r"\*\*Meta Description\*\*:\s*(.+)", md_text)
            cur = (m.group(1) if m else (mm.group(1).strip() if mm else "")).replace("&quot;", '"').strip()
            if not cur:
                continue
            ctype = ctypes.get(art.name, "guide")
            if LO <= len(cur) <= HI:
                descs[art.name] = cur
                continue
            new_desc = make_description(cur, ctype)
            update_article_md(md_path, new_desc)
            update_meta_html(html_path, new_desc)
            update_schema(art / "schema.json", new_desc)
            descs[art.name] = new_desc
            fixed += 1

    seen: dict[str, list[str]] = {}
    for folder, d in descs.items():
        seen.setdefault(d, []).append(folder)
    dups = {d: fs for d, fs in seen.items() if len(fs) > 1}
    out_of = [(f, len(d)) for f, d in descs.items() if not (LO <= len(d) <= HI)]

    print(f"Fixed {fixed} descriptions")
    print(f"Still out of range: {len(out_of)} {out_of}")
    print(f"Duplicate descriptions: {len(dups)}")
    for d, fs in dups.items():
        print(f"  {fs}: {d}")


if __name__ == "__main__":
    main()
