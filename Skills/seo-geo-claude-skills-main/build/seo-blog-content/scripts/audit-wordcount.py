#!/usr/bin/env python3
"""Audit blog articles: word count 1900–2750 (soft), keyword density adaptive to keyword length.

Body = from ## TL;DR through end (excludes frontmatter + TOC).
Keyword = exact phrase from **Target keyword** in article.md (case-insensitive).

Density gate: **minimum 1.2%** preferred for Pillar 26–30 (audit floor remains 1.0%
for older pillars). Upper bound scales with keyword length to avoid stuffing.

  keyword words | acceptable density
  ------------- | ------------------
  1–3           | 1.0% – 1.8%
  4–5           | 1.0% – 1.5%
  6+            | 1.0% – 1.5%
"""
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from article_keyword_meta import target_keyword as resolve_keyword

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(
    p for p in BLOG.glob("pillar[0-9]*-*")
    if p.is_dir() and " copy" not in p.name
)


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
    # Hard floor: 1.0% — keyword density must exceed sub-1% values (see content-quality-gates.md).
    # 6+ word phrases share the 1.5% cap with 4–5 word phrases so dens > 1.2% remains achievable.
    n = len(keyword.split())
    if n <= 3:
        return (1.0, 1.8)
    return (1.0, 1.5)


def audit_pillar(pillar: Path) -> list[dict]:
    rows = []
    for article in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
        text = article.read_text(encoding="utf-8")
        keyword = resolve_keyword(article, text)
        if not keyword:
            continue
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
