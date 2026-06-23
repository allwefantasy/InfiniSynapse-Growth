#!/usr/bin/env python3
"""Strip the leading H1 from article.md copies in a DEPLOY directory (publish layer).

DO NOT run this on the source SEO/Blog/pillar*/ tree — source keeps its single H1 so the
authoring gates (audit-outline-structure / audit-keyword-in-title-desc) still pass.
This is for the body-only copies shipped to a CMS/template that renders the page <h1>
from the title (e.g. QuickCreator, or a headless frontend).

Usage:
  python3 strip-leading-h1.py                       # default: frontend-handoff/content
  python3 strip-leading-h1.py path/to/deploy/content
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
DEFAULT_TARGET = BLOG / "frontend-handoff" / "content"


def strip_h1(text: str) -> tuple[str, bool]:
    lines = text.splitlines(keepends=True)
    in_fence = False
    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^#{2,6}\s", line):
            return text, False  # already body-only
        if re.match(r"^#\s+\S", line):
            del lines[i]
            if i < len(lines) and lines[i].strip() == "":
                del lines[i]
            return "".join(lines), True
    return text, False


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TARGET
    if not target.is_dir():
        print(f"Target not found: {target}")
        raise SystemExit(1)
    stripped = skipped = 0
    for md in sorted(target.rglob("article.md")):
        new, did = strip_h1(md.read_text(encoding="utf-8"))
        if did:
            md.write_text(new, encoding="utf-8")
            stripped += 1
        else:
            skipped += 1
    print(f"Stripped H1 from {stripped} files under {target}; skipped {skipped} (already body-only)")


if __name__ == "__main__":
    main()
