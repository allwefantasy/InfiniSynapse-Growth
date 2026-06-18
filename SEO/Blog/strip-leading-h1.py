#!/usr/bin/env python3
"""Remove the leading H1 from each article.md body.

Rationale: the page <h1> must be rendered by the template from the post title
(meta-tags <title> / blog-index title). Keeping a '# ...' in the body produces a
duplicate H1 on platforms that already render the title as H1 (e.g. QuickCreator).

Idempotent: only strips when the FIRST heading in the file is an H1 ('# ').
The title text is preserved in meta-tags.html, schema.json, and the blog index.
"""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).parent


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def strip_h1(text: str) -> tuple[str, str | None]:
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
            return text, None  # first heading is H2+ -> already stripped
        m = re.match(r"^#\s+(\S.*)$", line)
        if m:
            title = m.group(1).strip()
            del lines[i]
            # remove a single following blank line, if present
            if i < len(lines) and lines[i].strip() == "":
                del lines[i]
            return "".join(lines), title
    return text, None


def main() -> None:
    stripped, skipped = 0, 0
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            md = art / "article.md"
            if not md.is_file():
                continue
            text = md.read_text(encoding="utf-8")
            new, title = strip_h1(text)
            if title is None:
                skipped += 1
                continue
            md.write_text(new, encoding="utf-8")
            stripped += 1
    print(f"Stripped H1 from {stripped} articles; skipped {skipped} (already no leading H1)")


if __name__ == "__main__":
    main()
