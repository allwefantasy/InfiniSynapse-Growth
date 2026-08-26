#!/usr/bin/env python3
"""Insert Practical Next Steps into TOC before FAQ for P21-25 articles."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[1-5]-*"))
ENTRY = "11. [Practical Next Steps](#practical-next-steps)\n"


def fix_toc(text: str) -> str:
    if "## Practical Next Steps" not in text:
        return text
    if "Practical Next Steps](#practical-next-steps)" in text:
        return text
    m = re.search(
        r"(?P<header>## Table of Contents\s*\n)(?P<body>.*?)(?=\n---)",
        text,
        re.S,
    )
    if not m:
        return text
    body = m.group("body")
    faq_line = re.search(r"^(\d+)\. \[Frequently Asked Questions\]", body, re.M)
    if not faq_line:
        return text
    n = int(faq_line.group(1))
    lines = body.splitlines(keepends=True)
    new_lines = []
    inserted = False
    for line in lines:
        mm = re.match(r"^(\d+)\. \[", line)
        if mm and not inserted and int(mm.group(1)) == n:
            new_lines.append(ENTRY)
            inserted = True
        if mm and inserted:
            new_lines.append(f"{int(mm.group(1))+1}. [{line.split('. [',1)[1]}")
        else:
            new_lines.append(line)
    new_body = "".join(new_lines)
    return text[: m.start()] + m.group("header") + new_body + text[m.end() :]


def main() -> int:
    n = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            new = fix_toc(text)
            if new != text:
                art.write_text(new, encoding="utf-8")
                n += 1
                print(f"  {art.parent.name}")
    print(f"TOC updates: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
