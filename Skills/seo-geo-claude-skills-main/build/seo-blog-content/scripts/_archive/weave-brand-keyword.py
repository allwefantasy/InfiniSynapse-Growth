#!/usr/bin/env python3
"""Weave a brand-suffix Target keyword into body by extending brand mentions.

Replaces up to N standalone occurrences of BRAND (in body, TL;DR onward) with
"BRAND SUFFIX" so the exact Target keyword appears naturally. Skips:
  - "vs BRAND" / "BRAND vs" comparison phrases
  - BRAND already followed by the suffix
  - headings, the H1, Meta, Target-keyword line
Usage: python3 weave-brand-keyword.py <article.md> "<brand>" "<suffix>" <N>
"""
import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    brand = sys.argv[2]
    suffix = sys.argv[3]
    n_target = int(sys.argv[4])
    text = path.read_text(encoding="utf-8")
    tl = re.search(r"^## TL;DR\s*$", text, re.M)
    head, body = (text[: tl.start()], text[tl.start():]) if tl else ("", text)

    full = f"{brand} {suffix}"
    pat = re.compile(rf"(?<!vs ){re.escape(brand)}\b(?! {re.escape(suffix)})(?! vs)", )
    done = {"n": 0}

    def repl(m: re.Match) -> str:
        start = m.start()
        ls = body.rfind("\n", 0, start) + 1
        le = body.find("\n", start)
        line = body[ls: le if le != -1 else len(body)]
        if line.lstrip().startswith(("#", "|")):
            return m.group(0)
        if done["n"] >= n_target:
            return m.group(0)
        # avoid double "data analysis data analysis"
        after = body[m.end(): m.end() + 20]
        if after.lstrip().lower().startswith(suffix.lower()):
            return m.group(0)
        done["n"] += 1
        return full

    new_body = pat.sub(repl, body)
    path.write_text(head + new_body, encoding="utf-8")
    print(f"{path.parent.name}: wove '{full}' x{done['n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
