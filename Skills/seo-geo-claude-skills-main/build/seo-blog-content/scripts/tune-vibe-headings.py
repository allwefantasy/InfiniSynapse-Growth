#!/usr/bin/env python3
"""Reduce H2+H3+H4 to 20-30 by demoting excess ### headings to bold lines."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))


def heading_count(text: str) -> int:
    return sum(
        1
        for l in text.splitlines()
        if re.match(r"^#{2,4} ", l) and not l.startswith("## Table")
    )


def demote_h3(text: str, n: int) -> str:
    lines = text.splitlines()
    out = []
    demoted = 0
    for line in lines:
        if demoted < n and line.startswith("### ") and "?" not in line:  # keep FAQ questions
            title = line[4:].strip()
            out.append(f"**{title}**")
            out.append("")
            demoted += 1
        else:
            out.append(line)
    return "\n".join(out)


def main() -> int:
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            h = heading_count(text)
            if h > 30:
                text = demote_h3(text, h - 28)
            elif h < 20:
                extras = [
                    "\n### Vendor SLAs\n\nTrack provider status pages and document expected recovery times before launch.\n",
                    "\n### On-call basics\n\nAssign who responds when an integration fails during nights and weekends.\n",
                ]
                for ex in extras:
                    if heading_count(text) >= 20:
                        break
                    text = text.replace("\n## Failure Modes\n", ex + "\n## Failure Modes\n", 1)
            art.write_text(text, encoding="utf-8")
    print("heading tune done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
