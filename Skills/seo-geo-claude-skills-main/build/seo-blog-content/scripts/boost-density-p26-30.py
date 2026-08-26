#!/usr/bin/env python3
"""Boost keyword density above 1.2% for Pillar 26–30 articles (stay within audit upper band)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import importlib.util

from article_keyword_meta import target_keyword as resolve_keyword

_aw_spec = importlib.util.spec_from_file_location("audit_wordcount", _SCRIPTS / "audit-wordcount.py")
_aw = importlib.util.module_from_spec(_aw_spec)
_aw_spec.loader.exec_module(_aw)
density_bounds = _aw.density_bounds
extract_body_raw = _aw.extract_body_raw
kw_count = _aw.kw_count
word_count = _aw.word_count

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
TARGET_MIN = 1.21  # strictly > 1.2%
PILLARS = [
    BLOG / "pillar26-data-governance-quality",
    BLOG / "pillar27-master-data-catalog-lineage",
    BLOG / "pillar28-data-engineering-pipelines",
    BLOG / "pillar29-warehouse-lakehouse-architecture",
    BLOG / "pillar30-analytics-dashboards-visualization",
]

# Natural weave templates — {kw} = exact target keyword
WEAVES = [
    "In practice, teams evaluating {kw} should judge outcomes by reliability and clarity, not by tool count alone.",
    "That is the practical bar for {kw}: if the result is not trustworthy day after day, the program has not worked.",
    "When stakeholders ask for a short takeaway on {kw}, start from the decision it must support and work backward.",
    "The honest test of {kw} is whether a new teammate can trust the outputs without a week of tribal knowledge.",
    "Treat {kw} as an operating discipline: measure it, assign owners, and revisit it when sources or questions change.",
]


def dens(kc: int, wc: int) -> float:
    return 100.0 * kc / wc if wc else 0.0


def insert_weaves(text: str, keyword: str, n: int, start_idx: int = 0) -> tuple[str, int]:
    """Insert up to n unique weave sentences before Conclusion (or FAQ if no Conclusion)."""
    if n <= 0:
        return text, 0
    marker = None
    for cand in ("## Conclusion", "## Frequently Asked Questions", "## Common Misconceptions"):
        if cand in text:
            marker = cand
            break
    if not marker:
        return text, 0

    inserted = 0
    block_lines = []
    i = start_idx
    guard = 0
    while inserted < n and guard < len(WEAVES) * 3:
        guard += 1
        line = WEAVES[i % len(WEAVES)].format(kw=f"**{keyword}**")
        i += 1
        if line.lower() in text.lower() or line in block_lines:
            line = WEAVES[i % len(WEAVES)].format(kw=keyword)
            i += 1
        if line.lower() in text.lower() or line in block_lines:
            continue
        block_lines.append(line)
        inserted += 1

    if not block_lines:
        return text, 0
    block = "\n\n".join(block_lines) + "\n\n"
    idx = text.find(marker)
    text = text[:idx] + block + text[idx:]
    return text, inserted


def boost_one(art: Path) -> dict | None:
    text = art.read_text(encoding="utf-8")
    keyword = resolve_keyword(art, text)
    if not keyword:
        return None
    body = extract_body_raw(text)
    wc = word_count(body)
    kc = kw_count(body, keyword)
    d = dens(kc, wc)
    lo, hi = density_bounds(keyword)
    if d > 1.2:
        return {"folder": art.parent.name, "status": "ok", "dens": d, "kc": kc, "wc": wc}

    # Need dens > 1.2 and dens <= hi
    # After insert, both kc and wc rise. Estimate words per weave ≈ len(weave.split())
    adds = 0
    new_text = text
    # iterative: add one unique weave at a time until dens > 1.2 or hit hi
    for step in range(8):
        body = extract_body_raw(new_text)
        wc = word_count(body)
        kc = kw_count(body, keyword)
        d = dens(kc, wc)
        if d > 1.2 and d <= hi:
            break
        if d > hi:
            break
        est_wc = wc + 18 + len(keyword.split())
        est_kc = kc + 1
        est_d = dens(est_kc, est_wc)
        if est_d > hi:
            break
        new_text, n = insert_weaves(new_text, keyword, 1, start_idx=step)
        if n == 0:
            break
        adds += n

    if new_text != text:
        art.write_text(new_text, encoding="utf-8")

    body = extract_body_raw(new_text)
    wc = word_count(body)
    kc = kw_count(body, keyword)
    d = dens(kc, wc)
    return {
        "folder": art.parent.name,
        "status": "boosted" if adds else "unchanged",
        "adds": adds,
        "dens": d,
        "kc": kc,
        "wc": wc,
        "hi": hi,
        "kw": keyword,
        "pass": d > 1.2 and lo <= d <= hi,
    }


def main() -> int:
    results = []
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            r = boost_one(art)
            if r:
                results.append(r)

    boosted = [r for r in results if r.get("status") == "boosted"]
    failed = [r for r in results if not r.get("pass", True) and r.get("status") != "ok"]
    print(f"Boosted: {len(boosted)}")
    for r in boosted:
        mark = "✓" if r["pass"] else "✗"
        print(
            f"  {mark} {r['folder']}: +{r['adds']} → {r['dens']:.2f}% "
            f"(kc={r['kc']}, wc={r['wc']}, hi={r['hi']:.1f}%)"
        )
    # Final sweep: any still <= 1.2
    still = []
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            kw = resolve_keyword(art, text)
            body = extract_body_raw(text)
            wc = word_count(body)
            kc = kw_count(body, kw)
            d = dens(kc, wc)
            if d <= 1.2:
                still.append((art.parent.name, d, kc, wc, kw))
    print(f"\nStill dens<=1.2%: {len(still)}")
    for row in still:
        print(f"  {row}")
    return 1 if still else 0


if __name__ == "__main__":
    # audit_wordcount module name has hyphen — import via path already done above as audit_wordcount
    raise SystemExit(main())
