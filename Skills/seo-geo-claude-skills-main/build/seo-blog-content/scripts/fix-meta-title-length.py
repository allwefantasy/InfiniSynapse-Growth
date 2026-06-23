#!/usr/bin/env python3
"""Make meta <title> 40-60 chars while keeping the Target keyword.

QuickCreator On-Page rule: <title> 40-60 chars. Our H1/display titles are often >60
(keyword + framing + year). We keep:
  - article.md H1  (display, full)          -> authoring gates unchanged
  - schema headline (full)                  -> matches H1
and only rewrite the meta <title> (+ og:title, twitter:title) to a 40-60 SEO title
that still contains the keyword.

Exception: if the keyword itself is too long to fit a <=60 title, we keep the full
keyword and accept >60 (skill rule: keyword completeness > length). These are logged.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
LO, HI, SWEET = 40, 60, 54

YEAR = "(2026)"
FUNC_TAIL = {
    "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "at", "by",
    "with", "vs", "&", "is", "are", "that", "this", "from", "as",
}

# Type-aware subtitles appended after "Keyword: " (varied length for 40-60 landing).
TYPE_SUBTITLES: dict[str, list[str]] = {
    "versus": ["Comparison (2026)", "Neutral Comparison (2026)", "Head-to-Head Guide (2026)"],
    "comparison": ["Comparison (2026)", "Neutral Comparison (2026)", "Head-to-Head Guide (2026)"],
    "alternatives": ["Top Alternatives (2026)", "Best Alternatives Compared (2026)"],
    "listicle": ["Top Tools (2026)", "Top Tools Compared (2026)", "Best Tools Ranked (2026)"],
    "how-to": ["Setup Guide (2026)", "Step-by-Step Guide (2026)", "Practical Setup Guide (2026)"],
    "guide": ["2026 Guide", "Complete 2026 Guide", "Practical 2026 Guide"],
    "buyer-guide": ["Buyer Guide (2026)", "2026 Buyer Guide", "Buyer Guide and Checklist (2026)"],
    "role-guide": ["Role Guide (2026)", "Role and Workflow Guide (2026)"],
    "what-is": ["Definition and Guide (2026)", "Definition, Examples, and Guide (2026)"],
    "deep-dive": ["Deep Dive (2026)", "Architecture Deep Dive (2026)"],
    "manifesto": ["Vision and Principles (2026)", "A 2026 Manifesto"],
    "review": ["Honest Review (2026)", "Hands-On Review (2026)"],
    "use-case": ["Practical Workflows (2026)", "Use Cases and Workflows (2026)"],
    "glossary": ["Key Terms Explained (2026)", "Essential Terms (2026)"],
    "faq": ["Key Questions Answered (2026)", "Common Questions Answered (2026)"],
    "prompt-resource": ["Ready-to-Use Prompts (2026)", "Prompt Templates (2026)"],
    "job-template": ["Template and Skills (2026)", "JD Template and Skills Matrix (2026)"],
    "deployment-guide": ["Deployment Guide (2026)", "Self-Hosting Guide (2026)"],
}
DEFAULT_SUBS = ["2026 Guide", "Complete 2026 Guide", "Practical 2026 Guide"]


def load_content_types() -> dict[str, str]:
    out: dict[str, str] = {}
    p = BLOG / "blog-cms-import-100.csv"
    if p.is_file():
        for row in csv.DictReader(p.open(encoding="utf-8-sig")):
            out[row["folder"]] = row.get("content_type", "")
    return out


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def title_case_kw(kw: str) -> str:
    small = {"a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "vs", "with"}
    words = kw.split()
    out = []
    for i, w in enumerate(words):
        if w.lower() == "ai":
            out.append("AI")
        elif w.lower() == "sql":
            out.append("SQL")
        elif w.lower() == "bi":
            out.append("BI")
        elif w.lower() in ("nl2sql", "llm", "csv", "roi", "kpi", "saas", "fp&a"):
            out.append(w.upper())
        elif i > 0 and w.lower() in small:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def has_kw(title: str, kw: str) -> bool:
    return kw.lower() in title.lower()


def strip_func_tail(s: str) -> str:
    s = s.strip(" -:—,;")
    words = s.split()
    while words and words[-1].lower().strip(",;:") in FUNC_TAIL:
        words.pop()
    return " ".join(words).strip(" -:—,;")


def candidates(h1: str, kw: str, ctype: str) -> list[str]:
    cands: list[str] = []

    def add(s: str) -> None:
        s = re.sub(r"\s+", " ", s).strip(" -:—")
        if s and s not in cands:
            cands.append(s)

    # 1. original and original minus year
    add(h1)
    add(re.sub(r"\s*\(20\d\d\)\s*$", "", h1))
    # 2. original before-colon (display lead, usually has keyword) + type subtitle
    subs = TYPE_SUBTITLES.get(ctype, DEFAULT_SUBS)
    lead = h1.split(":", 1)[0].strip() if ":" in h1 else ""
    kwt = title_case_kw(kw)
    for base in ([lead] if lead and has_kw(lead, kw) else []) + [kwt]:
        add(base)
        add(f"{base} {YEAR}")
        for sub in subs:
            add(f"{base}: {sub}")
    return cands


def make_title(h1: str, kw: str, ctype: str) -> tuple[str, bool]:
    """Return (title, exception). exception=True means keyword too long to fit 40-60."""
    if LO <= len(h1) <= HI and has_kw(h1, kw):
        return h1, False

    fitting = [
        c for c in candidates(h1, kw, ctype)
        if LO <= len(c) <= HI and has_kw(c, kw) and c.split()[-1].lower() not in FUNC_TAIL
    ]
    if fitting:
        fitting.sort(key=lambda s: abs(len(s) - SWEET))
        return fitting[0], False

    # keyword too long to fit: keep full keyword (skill rule: completeness > length)
    if len(kw) > HI - 2:
        kwt = title_case_kw(kw)
        return (kwt if has_kw(kwt, kw) else h1), True

    # last resort: truncate h1 at word boundary <=60, drop trailing function words
    words = h1.split()
    acc = ""
    for w in words:
        if len(acc + " " + w) > HI:
            break
        acc = (acc + " " + w).strip()
    acc = strip_func_tail(acc)
    if LO <= len(acc) <= HI and has_kw(acc, kw):
        return acc, False
    return h1, True  # give up, keep original (logged)


def update_meta(path: Path, new_title: str) -> None:
    text = path.read_text(encoding="utf-8")
    esc = new_title.replace('"', "&quot;")
    text = re.sub(r"<title>[^<]*</title>", f"<title>{esc}</title>", text, count=1)
    text = re.sub(
        r'(<meta property="og:title" content=")[^"]*(")', rf"\1{esc}\2", text, count=1
    )
    text = re.sub(
        r'(<meta name="twitter:title" content=")[^"]*(")', rf"\1{esc}\2", text, count=1
    )
    path.write_text(text, encoding="utf-8")


def read_h1(md: str) -> str:
    return next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "")


def read_kw(md: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", md)
    return m.group(1).strip() if m else ""


def main() -> None:
    ctypes = load_content_types()
    fixed = exceptions = unchanged = 0
    exc_list = []
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            meta = art / "meta-tags.html"
            md_path = art / "article.md"
            if not meta.is_file() or not md_path.is_file():
                continue
            html = meta.read_text(encoding="utf-8")
            cur = re.search(r"<title>([^<]*)</title>", html)
            cur_title = cur.group(1) if cur else ""
            md = md_path.read_text(encoding="utf-8")
            h1 = read_h1(md)
            kw = read_kw(md)
            source = h1 or cur_title
            new_title, exc = make_title(source, kw, ctypes.get(art.name, "guide"))
            if new_title == cur_title:
                unchanged += 1
                if exc and not (LO <= len(cur_title) <= HI):
                    exceptions += 1
                    exc_list.append(f"{art.name[:3]}({len(cur_title)}) kw={len(kw)}")
                continue
            update_meta(meta, new_title)
            if exc:
                exceptions += 1
                exc_list.append(f"{art.name[:3]}({len(new_title)}) kw={len(kw)}")
            else:
                fixed += 1
    print(f"Fixed titles to 40-60: {fixed}")
    print(f"Unchanged: {unchanged}")
    print(f"Exceptions (keyword too long, kept >60): {exceptions}")
    for e in exc_list:
        print(f"   {e}")


if __name__ == "__main__":
    main()
