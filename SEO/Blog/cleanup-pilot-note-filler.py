#!/usr/bin/env python3
"""Surgical removal of templated 'Pilot note N:' density-booster filler.

Only deletes standalone lines matching `^Pilot note \\d+:` that contain NO
markdown link (link-bearing lines are left for manual rewrite so internal links
are never dropped). Collapses the blank line left behind. Reports every change.
"""
import re
from pathlib import Path

BLOG = Path(__file__).parent
PILLARS = sorted(
    p for p in BLOG.glob("pillar[0-9]*") if p.is_dir()
)

FILLER = re.compile(r"^(Pilot note \d+|Operational note|Field note|Practitioner note):")
LINK = re.compile(r"\]\(")


def clean(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    removed = 0
    for ln in lines:
        if FILLER.match(ln) and not LINK.search(ln):
            removed += 1
            continue
        out.append(ln)
    if not removed:
        return 0
    text = "".join(out)
    # collapse 3+ blank lines created by deletions down to a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)
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
    print(f"\nRemoved {total} linkless 'Pilot note' filler lines.")


if __name__ == "__main__":
    main()
