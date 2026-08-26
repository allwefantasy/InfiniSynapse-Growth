#!/usr/bin/env python3
"""Reduce over-stuffed primary-keyword density to a target band.

For an over-optimized article, keeps the first `keep` occurrences of the Target
keyword in the body (TL;DR onward) and replaces the rest with natural variants,
de-bolding them. Never touches the H1, Meta Description, Target-keyword line, or
the Key Definition blockquote (so title/desc audits stay green). Prints a diff
summary; review output for grammar afterward.

Usage: python3 reduce-keyword-density.py <article.md> [keep]
"""
import re
import sys
from pathlib import Path

VARIANTS = [
    "the workflow",
    "this practice",
    "the analysis workflow",
    "this approach",
    "SQL-based analysis",
    "the process",
    "this capability",
]


def main() -> int:
    path = Path(sys.argv[1])
    keep = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    text = path.read_text(encoding="utf-8")
    kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    if not kw_m:
        print("no target keyword")
        return 1
    kw = kw_m.group(1)

    tl = re.search(r"^## TL;DR\s*$", text, re.M)
    head, body = (text[: tl.start()], text[tl.start():]) if tl else ("", text)

    # protect Key Definition blockquote lines and any heading lines
    pat = re.compile(re.escape(kw), re.I)
    count = {"n": 0, "rep": 0, "vi": 0}

    def repl(m: re.Match) -> str:
        # find the line this match is on
        start = m.start()
        line_start = body.rfind("\n", 0, start) + 1
        line_end = body.find("\n", start)
        line = body[line_start: line_end if line_end != -1 else len(body)]
        protected = line.lstrip().startswith(("#", ">", "|")) or "Target keyword" in line
        count["n"] += 1
        if protected or count["n"] <= keep:
            return m.group(0)
        # replace with a variant (de-bold by consuming surrounding ** if present)
        v = VARIANTS[count["vi"] % len(VARIANTS)]
        count["vi"] += 1
        count["rep"] += 1
        # capitalize if at sentence start
        before = body[max(0, m.start() - 2): m.start()]
        if before.strip().endswith((".", "!", "?")) or m.start() == 0:
            v = v[0].upper() + v[1:]
        return v

    new_body = pat.sub(repl, body)
    # strip bold markers that now wrap a variant artifact: **the workflow** -> the workflow
    for v in VARIANTS:
        new_body = new_body.replace(f"**{v}**", v)
        new_body = new_body.replace(f"**{v[0].upper()+v[1:]}**", v[0].upper()+v[1:])
    path.write_text(head + new_body, encoding="utf-8")
    print(f"{path.parent.name}: total={count['n']} kept~{keep} replaced={count['rep']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
