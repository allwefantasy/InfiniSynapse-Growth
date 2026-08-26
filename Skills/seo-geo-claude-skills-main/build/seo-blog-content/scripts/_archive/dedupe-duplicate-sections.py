#!/usr/bin/env python3
"""Remove duplicate ## sections and repeated paragraphs introduced by batch expansion."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).parent


def split_sections(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?=^## )", text, flags=re.M)
    out: list[tuple[str, str]] = []
    for p in parts:
        if not p.startswith("## "):
            if p.strip():
                out.append(("", p))
            continue
        lines = p.split("\n", 1)
        title = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""
        out.append((title, body))
    return out


def dedupe_paragraphs(block: str) -> str:
    paras = re.split(r"\n\n+", block.strip())
    seen: set[str] = set()
    kept: list[str] = []
    for para in paras:
        norm = re.sub(r"\s+", " ", para.strip()).lower()
        if not norm:
            continue
        if norm in seen:
            continue
        seen.add(norm)
        kept.append(para)
    return "\n\n".join(kept) + ("\n" if block.endswith("\n") else "")


def dedupe_article(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    if not sections:
        return False

    prefix = sections[0][1] if sections[0][0] == "" else ""
    seen_titles: set[str] = set()
    rebuilt: list[str] = []
    if prefix:
        rebuilt.append(prefix.rstrip("\n"))

    for title, body in sections:
        if not title:
            continue
        if title in seen_titles:
            continue
        seen_titles.add(title)
        body = dedupe_paragraphs(body)
        rebuilt.append(f"{title}\n\n{body}".rstrip())

    new_text = "\n\n".join(rebuilt) + "\n"
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for pillar in BLOG.glob("pillar*"):
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if dedupe_article(art):
                changed += 1
    print(f"Deduped {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
