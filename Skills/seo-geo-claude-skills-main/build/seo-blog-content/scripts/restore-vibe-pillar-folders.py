#!/usr/bin/env python3
"""Copy Pillar 16–20 article folders from handoff pack back to SEO/Blog/."""
from __future__ import annotations

import shutil
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SRC = BLOG / "vibe-coding-handoff-pack" / "articles"


def main() -> int:
    if not SRC.is_dir():
        print(f"Missing {SRC}")
        return 1
    n = 0
    for pillar in sorted(SRC.glob("pillar*")):
        dest = BLOG / pillar.name
        dest.mkdir(parents=True, exist_ok=True)
        for art in pillar.glob("[0-9][0-9][0-9]-*"):
            target = dest / art.name
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(art, target)
            n += 1
    print(f"Restored {n} articles to SEO/Blog/pillar16–20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
