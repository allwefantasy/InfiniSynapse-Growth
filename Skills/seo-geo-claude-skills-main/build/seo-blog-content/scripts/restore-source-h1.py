#!/usr/bin/env python3
"""Restore the leading H1 in each source article.md from git HEAD, keeping current body edits.

We strip the body H1 only in the DEPLOY copy (see build-frontend-handoff.py), not in source.
Source keeps its single H1 so the authoring gates (outline / keyword-in-title) still pass.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"


def pillar_dirs() -> list[Path]:
    return sorted(p for p in BLOG.glob("pillar[1-8]-*") if p.is_dir() and " copy" not in p.name)


def original_h1(rel: str) -> str | None:
    """Walk this file's git history; return the H1 from the most recent revision that has one."""
    try:
        revs = subprocess.run(
            ["git", "rev-list", "HEAD", "--", rel], cwd=REPO,
            capture_output=True, text=True, check=True,
        ).stdout.split()
    except subprocess.CalledProcessError:
        return None
    for rev in revs:
        try:
            content = subprocess.run(
                ["git", "show", f"{rev}:{rel}"], cwd=REPO,
                capture_output=True, text=True, check=True,
            ).stdout
        except subprocess.CalledProcessError:
            continue
        for line in content.splitlines():
            if re.match(r"^#\s+\S", line):
                return line.rstrip("\n")
    return None


def main() -> None:
    restored = skipped = 0
    for pillar in pillar_dirs():
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/")):
            md = art / "article.md"
            if not md.is_file():
                continue
            text = md.read_text(encoding="utf-8")
            # already has a leading H1?
            first_heading = next((l for l in text.splitlines() if re.match(r"^#{1,6}\s", l)), "")
            if re.match(r"^#\s+\S", first_heading):
                skipped += 1
                continue
            rel = str(md.relative_to(REPO))
            h1 = original_h1(rel)
            if not h1:
                skipped += 1
                continue
            md.write_text(f"{h1}\n\n{text}", encoding="utf-8")
            restored += 1
    print(f"Restored H1 to {restored} source article.md; skipped {skipped}")


if __name__ == "__main__":
    main()
