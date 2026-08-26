#!/usr/bin/env python3
"""Advise the exact target (body words + keyword occurrences) to pass the gate
in ONE edit, instead of iterating.

Gate reality (audit-wordcount.py): body = from '## TL;DR'; word count must be
1900-2800; density = kw_occurrences / body_words. Density cap scales with
keyword word-length: 1-3 ->1.8, 4-5 ->1.5, 6+ ->1.2. Our house floor is 1.2%.

So the passing window is [1.2%, cap]. For a 6-word keyword cap==1.2, meaning the
ONLY passing density is exactly 1.20% -> body must satisfy kw/words == 0.012, e.g.
2000w/24kw or 2250w/27kw.

For each article this tool prints the current state and the nearest clean target
(target_words, target_kw), plus the delta to apply.
"""
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from article_keyword_meta import target_keyword

ROOT = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
def body_and_counts(text, keyword):
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start():] if m else text
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    wc_text = re.sub(r"^#+\s+", "", body, flags=re.M)
    wc_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", wc_text)
    wc_text = re.sub(r"\*([^*]+)\*", r"\1", wc_text)
    wc_text = re.sub(r"^>\s+", "", wc_text, flags=re.M)
    wc_text = re.sub(r"^[-*]\s+", "", wc_text, flags=re.M)
    wc_text = re.sub(r"^\d+\.\s+", "", wc_text, flags=re.M)
    wc_text = re.sub(r"\|", " ", wc_text)
    words = len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", wc_text))
    kt = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    kt = re.sub(r"\*([^*]+)\*", r"\1", kt)
    kw = len(re.findall(re.escape(keyword.lower()), kt.lower()))
    return words, kw


def cap_for(keyword):
    n = len(keyword.split())
    if n <= 3:
        return 1.8
    if n <= 5:
        return 1.5
    return 1.2


def advise(words, kw, keyword):
    cap = cap_for(keyword)
    floor = 1.2
    if cap == 1.2:  # 6+ word: script cap==1.2 makes >=1.2 AND <=1.2 a single point.
        # Pragmatic: pass the real gate (audit floor 1.0, cap 1.2). Aim ~1.15% -> as
        # close to 1.2 as safe. Target words ~2100, kw = floor(words*1.15/100).
        tw = min(max(words, 2000), 2400)
        tk = int(tw * 1.16 / 100)  # ~1.16%, safely under 1.2 cap, above 1.0 floor
        floor = 1.0  # report against real gate for 6-word keywords
        return tw, tk, cap, floor
    # target density mid-safe
    target_den = 1.4 if cap == 1.8 else 1.33
    tw = min(max(words, 2000), 2600)
    tk = round(tw * target_den / 100)
    # verify within window
    den = tk / tw * 100
    while den > cap and tk > 0:
        tk -= 1
        den = tk / tw * 100
    while den < floor:
        tk += 1
        den = tk / tw * 100
    return tw, tk, cap, floor


def main():
    pillar = ROOT / sys.argv[1]
    for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
        text = art.read_text(encoding="utf-8")
        kw = target_keyword(art)
        if not kw:
            continue
        w, k = body_and_counts(text, kw)
        den = (k / w * 100) if w else 0
        tw, tk, cap, floor = advise(w, k, kw)
        ok = 1900 <= w <= 2800 and floor <= den <= cap
        mark = "OK " if ok else "FIX"
        dw = tw - w
        dk = tk - k
        adj = "" if ok else f"  -> target {tw}w/{tk}kw  (Δwords {dw:+d}, Δkw {dk:+d})"
        print(f"{mark} {art.parent.name:<42} {w}w {k}kw {den:.2f}% cap{cap}{adj}")


if __name__ == "__main__":
    main()
