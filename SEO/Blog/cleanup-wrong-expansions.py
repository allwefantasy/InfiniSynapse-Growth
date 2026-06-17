#!/usr/bin/env python3
"""Remove misplaced expansion blocks and duplicate density-booster paragraphs."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).parent

BLOCKS_TO_STRIP = [
    r"## Troubleshooting Connector Rollouts\n\n.*?(?=\n---\n\n## |\n## )",
    r"## Production Debugging Notes\n\n.*?(?=\n---\n\n## |\n## )",
]

BOOSTER_LINES = [
    r"Teams evaluating \*\*[^*]+\*\* should score repeatability before demo sparkle\.",
    r"In our rollouts, \*\*[^*]+\*\* wins when metric contracts precede connector sprawl\.",
    r"Reviewers trust \*\*[^*]+\*\* outputs when assumptions are versioned, not retyped\.",
    r"We benchmark \*\*[^*]+\*\* on the tenth run, not the first—schema drift is the real test\.",
]

PILLAR4 = BLOG / "pillar4-data-source-connectors"
PILLAR5 = BLOG / "pillar5-nl2sql-text-to-sql"


def cleanup(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    folder = path.parent.name
    art_id = int(folder[:3])

    for pat in BLOCKS_TO_STRIP:
        if pat.startswith("## Troubleshooting") and path.parent.parent == PILLAR4:
            continue
        if pat.startswith("## Production Debugging") and path.parent.parent == PILLAR5:
            continue
        text = re.sub(pat, "", text, flags=re.S)

    for line_pat in BOOSTER_LINES:
        text = re.sub(r"\n*" + line_pat + r"\n*", "\n", text)

    text = re.sub(r"\n---\n\n---\n", "\n---\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for pillar in BLOG.glob("pillar*"):
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            if cleanup(art):
                changed += 1
                print(f"cleaned: {art.parent.name}")
    print(f"Cleaned {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
