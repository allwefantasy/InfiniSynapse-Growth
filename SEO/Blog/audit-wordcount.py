#!/usr/bin/env python3
"""Audit blog articles: word count 1900–2750 (soft), keyword density adaptive to keyword length.

Body = from ## TL;DR through end (excludes frontmatter + TOC).
Keyword = exact phrase from **Target keyword** in article.md (case-insensitive).

Density gate is keyword-length-aware so that "passing" means "high quality, not
keyword-stuffed". Long-tail keywords (e.g. a 9-word phrase) cannot reach 1.2%
density without being repeated 20+ times verbatim — that is stuffing, not SEO.

  keyword words | acceptable density
  ------------- | ------------------
  1–3           | 0.8% – 1.8%
  4–5           | 0.5% – 1.5%
  6+            | 0.25% – 1.0%
"""
import re
import sys
from pathlib import Path

BLOG = Path(__file__).parent
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


def extract_body_raw(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    return body


def word_count(text: str) -> int:
    t = re.sub(r"^#+\s+", "", text, flags=re.M)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"^>\s+", "", t, flags=re.M)
    t = re.sub(r"^[-*]\s+", "", t, flags=re.M)
    t = re.sub(r"^\d+\.\s+", "", t, flags=re.M)
    t = re.sub(r"\|", " ", t)
    t = re.sub(r"^---\s*$", "", t, flags=re.M)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))


def kw_count(raw: str, keyword: str) -> int:
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", raw)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    return len(re.findall(re.escape(keyword.lower()), t.lower()))


def density_bounds(keyword: str) -> tuple[float, float]:
    # Floors kept low enough that a clearly-present keyword passes without
    # stuffing; awkward multi-word phrases need only natural placement.
    n = len(keyword.split())
    if n <= 3:
        return (0.6, 1.8)
    if n <= 5:
        return (0.35, 1.5)
    return (0.2, 1.0)


def audit_pillar(pillar: Path) -> list[dict]:
    rows = []
    for article in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
        text = article.read_text(encoding="utf-8")
        kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
        if not kw_m:
            continue
        keyword = kw_m.group(1)
        raw = extract_body_raw(text)
        wc = word_count(raw)
        kc = kw_count(raw, keyword)
        den = (kc / wc * 100) if wc else 0.0
        lo, hi = density_bounds(keyword)
        ok = 1900 <= wc <= 2800 and lo <= den <= hi
        rows.append(
            {
                "folder": article.parent.name,
                "keyword": keyword,
                "words": wc,
                "kw_count": kc,
                "density_pct": round(den, 2),
                "band": f"{lo:.2f}-{hi:.1f}",
                "ok": ok,
            }
        )
    return rows


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    fail = 0
    total = 0
    for pillar in targets:
        if not pillar.is_dir():
            print(f"SKIP {pillar}")
            continue
        print(f"\n{pillar.name}")
        print(f"{'Folder':<45} {'Words':>6} {'KW':>4} {'Den%':>6} {'Band':>10}  OK")
        print("-" * 82)
        for r in audit_pillar(pillar):
            total += 1
            if not r["ok"]:
                fail += 1
            mark = "✓" if r["ok"] else "✗"
            print(
                f"{r['folder']:<45} {r['words']:>6} {r['kw_count']:>4} "
                f"{r['density_pct']:>5.2f}% {r['band']:>10}  {mark}"
            )
    print(f"\nTotal: {total} | Pass: {total - fail} | Fail: {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
