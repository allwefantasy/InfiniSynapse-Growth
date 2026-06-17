#!/usr/bin/env python3
"""Remove exact duplicate standalone citation/sentence lines (keep first).

Targets the over-weaving artifact where the same one-line citation paragraph was
inserted multiple times. Only removes a line if:
  - its stripped text already appeared earlier in the file, AND
  - it is a 'sentence-like' standalone line (len > 40 and contains a markdown link)
This never touches headings, tables, lists, or the first occurrence.
"""
import re
from pathlib import Path

BLOG = Path(__file__).parent
PILLARS = sorted(p for p in BLOG.glob("pillar[0-9]*") if p.is_dir())
LINK = re.compile(r"\]\(https?://")


def clean(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    seen: set[str] = set()
    out = []
    removed = 0
    for ln in lines:
        s = ln.strip()
        sentence_like = len(s) > 40 and bool(LINK.search(s)) and not s.startswith(("#", "|", "-", ">", "*"))
        if sentence_like and s in seen:
            removed += 1
            continue
        if sentence_like:
            seen.add(s)
        out.append(ln)
    if removed:
        text = re.sub(r"\n{3,}", "\n\n", "".join(out))
        path.write_text(text, encoding="utf-8")
    return removed


def main() -> None:
    total = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            n = clean(art)
            if n:
                total += n
                print(f"  -{n:>2}  {art.parent.name}")
    print(f"\nRemoved {total} exact-duplicate standalone citation lines.")


if __name__ == "__main__":
    main()
