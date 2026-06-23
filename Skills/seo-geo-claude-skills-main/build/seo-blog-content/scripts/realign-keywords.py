#!/usr/bin/env python3
"""Realign article Target keyword to the plan keyword via case-aware whole-phrase swap.

For each targeted article: replace EVERY occurrence of the current (wrong) keyword phrase
with the plan keyword, across article.md (body + **Target keyword** + **Meta Description** +
H1), meta-tags.html (title/desc/og/twitter), schema.json (headline/description/keywords/
about/FAQ). Case-aware: lower/Title/Cap-first preserved.

EXCLUDE set = brand/identity pages + connector action-phrases + odd long plan keywords;
those need manual rewriting and are reported, not auto-changed.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
RECONCILE = BLOG / "keyword-reconcile.csv"

# Do NOT auto-swap these (handle manually / decide separately):
EXCLUDE = {
    "002",  # manifesto identity
    "005",  # superset would over-stuff "agentic analytics"
    "037", "038", "039", "041", "043",  # brand / review identity + cannibalization
    "045", "046", "047", "048",  # connector action-phrase / odd long
    "061",  # plan kw off-topic vs benchmark article
    "062", "063", "068",  # 67-char odd plan keyword
    "072", "083",  # odd long plan keyword
    "098",  # structural: old phrase "how to evaluate ai data analyst" leaves "requirements Tools"
}

ACRO = {
    "ai": "AI", "sql": "SQL", "bi": "BI", "csv": "CSV", "saas": "SaaS",
    "chatgpt": "ChatGPT", "plg": "PLG", "kpi": "KPI", "roi": "ROI",
    "vlookup": "VLOOKUP", "nl2sql": "NL2SQL", "llm": "LLM", "faq": "FAQ",
}


def sentence_form(phrase: str) -> str:
    return " ".join(ACRO.get(w.lower(), w.lower()) for w in phrase.split())


def title_form(phrase: str) -> str:
    small = {"a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "vs", "with"}
    out = []
    for i, w in enumerate(phrase.split()):
        lw = w.lower()
        if lw in ACRO:
            out.append(ACRO[lw])
        elif i > 0 and lw in small:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:])
    return " ".join(out)


def cap_first(phrase: str) -> str:
    sf = sentence_form(phrase)
    # capitalize first alpha char (acronyms already correct)
    for i, ch in enumerate(sf):
        if ch.isalpha():
            if sf.split()[0].lower() in ACRO:
                return sf  # first token is acronym, leave as-is
            return sf[:i] + sf[i].upper() + sf[i + 1:]
    return sf


def case_like(sample: str, repl: str) -> str:
    words = sample.split()
    if len(words) > 1 and all(w[:1].isupper() for w in words if w and w[:1].isalpha()):
        return title_form(repl)
    if sample[:1].isupper():
        return cap_first(repl)
    return sentence_form(repl)


def swap(text: str, old: str, new: str) -> tuple[str, int]:
    pat = re.compile(re.escape(old), re.IGNORECASE)
    n = 0

    def _r(m: re.Match) -> str:
        nonlocal n
        n += 1
        return case_like(m.group(0), new)

    return pat.sub(_r, text), n


def swap_schema(path: Path, old: str, new: str) -> int:
    if not path.is_file():
        return 0
    raw = path.read_text(encoding="utf-8")
    new_raw, n = swap(raw, old, new)
    if n:
        # validate JSON still parses
        json.loads(new_raw)
        path.write_text(new_raw, encoding="utf-8")
    return n


def main() -> None:
    rows = [r for r in csv.DictReader(RECONCILE.open(encoding="utf-8-sig"))
            if r["是否一致"] == "否"]
    done, skipped = [], []
    for r in rows:
        aid = r["编号"]
        old = r["实际Target关键词"].strip()
        new = r["规划关键词(替换后)"].strip()
        if aid in EXCLUDE:
            skipped.append((aid, old, new))
            continue
        art = next(iter(BLOG.glob(f"pillar*/{aid}-*/")), None)
        if not art:
            continue
        total = 0
        for name in ("article.md", "meta-tags.html"):
            p = art / name
            if p.is_file():
                t, n = swap(p.read_text(encoding="utf-8"), old, new)
                if n:
                    p.write_text(t, encoding="utf-8")
                total += n
        total += swap_schema(art / "schema.json", old, new)
        done.append((aid, old, new, total))

    print(f"Realigned {len(done)} articles; skipped {len(skipped)} (manual).\n")
    print("=== 已对齐 ===")
    for aid, old, new, n in done:
        print(f"  {aid}: '{old}' -> '{new}'  ({n} 处)")
    print("\n=== 跳过（需人工/决策）===")
    for aid, old, new in skipped:
        print(f"  {aid}: '{old}'  (规划: '{new}')")


if __name__ == "__main__":
    main()
