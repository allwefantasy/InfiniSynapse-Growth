#!/usr/bin/env python3
"""Move Slug / Target keyword / Secondary out of article.md into article-meta.json."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from article_keyword_meta import _from_article_md

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR_GLOB = "pillar2[1-5]-*"

STRIP_LINES = re.compile(
    r"^\*\*(?:Slug|Target keyword|Secondary)\*\*:.*\n?",
    re.M,
)


def strip_article(text: str) -> tuple[str, bool]:
    if not re.search(r"\*\*(?:Slug|Target keyword)\*\*:", text):
        return text, False
    new = STRIP_LINES.sub("", text)
    # collapse extra blank lines before ---
    new = re.sub(r"\n{3,}(---)", r"\n\n\1", new)
    return new, new != text


def main() -> int:
    written = stripped = 0
    for pillar in sorted(BLOG.glob(PILLAR_GLOB)):
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            meta = _from_article_md(text)
            if not meta.get("target_keyword"):
                continue

            sidecar = art.parent / "article-meta.json"
            payload = {
                "slug": meta.get("slug", ""),
                "target_keyword": meta["target_keyword"],
                "secondary": meta.get("secondary", []),
            }
            sidecar.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            written += 1

            new_text, changed = strip_article(text)
            if changed:
                art.write_text(new_text, encoding="utf-8")
                stripped += 1

    print(f"article-meta.json written: {written}")
    print(f"article.md stripped: {stripped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
