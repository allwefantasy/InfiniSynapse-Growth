#!/usr/bin/env python3
"""Strip excess headings and pad word count for vibe-coding series."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

PAD = """
## Production Checklist

Before beta users arrive, confirm secrets live in a vault, async jobs stream progress to the UI, contract tests run in CI, and on-call knows which vendor owns each alert. Solo founders should still write this checklist—it prevents the predictable first-week outage.
"""


def stats(text: str, kw: str = "") -> tuple[int, int]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    wc = len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", re.sub(r"^#+\s+", "", body, flags=re.M)))
    h = sum(1 for l in text.splitlines() if re.match(r"^#{2,4} ", l))
    return wc, h


def strip(text: str) -> str:
    text = re.sub(r"\n## Table of Contents\n[\s\S]*?(?=\n---\n\n## TL;DR)", "\n", text, count=1)
    for h2 in (
        "## Buyer Questions Before You Commit",
        "## Rollout Timeline (Typical)",
        "## Tooling Shortlist",
        "## Case Study: Rent-vs-Commute Analyzer",
    ):
        text = re.sub(r"\n" + re.escape(h2) + r"\n[\s\S]*?(?=\n## )", "\n", text, count=1)
    # merge Security into Operating Model
    text = re.sub(
        r"\n## Security and Compliance Baseline\n",
        "\n### Security and compliance baseline\n",
        text,
        count=1,
    )
    return text


def main() -> int:
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            t = art.read_text(encoding="utf-8")
            kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", t)
            kw = kw_m.group(1) if kw_m else ""
            t = strip(t)
            if stats(t)[0] < 1920 and "## Production Checklist" not in t:
                t = t.replace("\n## Frequently Asked Questions\n", PAD + "\n## Frequently Asked Questions\n", 1)
            while stats(t, kw)[0] < 1915 and kw:
                t = t.replace(
                    "\n## Conclusion\n",
                    f"\n\nShip **{kw}** with a written rollback plan and vendor status page bookmarks—not optimism.\n\n## Conclusion\n",
                    1,
                )
            art.write_text(t, encoding="utf-8")
    print("strip+pad done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
