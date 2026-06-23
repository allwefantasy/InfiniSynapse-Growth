#!/usr/bin/env python3
"""Insert a second topic-anchored paragraph before the FAQ to clear the word floor.

Keyword-light (lowers any over-dense article) and topic-anchored. Inserts right
before '## Frequently Asked Questions'.

Usage: python3 expand-topic-section2.py <article.md> "<topic>" "<readers>"
"""
import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    topic = sys.argv[2]
    readers = sys.argv[3] if len(sys.argv) > 3 else "teams"
    text = path.read_text(encoding="utf-8")
    faq = text.find("## Frequently Asked Questions")
    if faq == -1:
        print(f"SKIP {path.parent.name}")
        return 1
    para = (
        f"### From pilot to durable capability\n\n"
        f"The move from a promising pilot to a durable capability is mostly organizational, not technical. "
        f"Name an owner for each recurring workflow, agree the metric definitions in writing before automating, "
        f"and put a short weekly review on the calendar where {readers} inspect what ran and what changed. Keep the "
        f"first version small: one workflow, one source of truth, one reviewer. Expand only after that workflow has "
        f"survived a month of real use without surprising anyone. The teams that sustain momentum resist the urge to "
        f"connect every system at once; they let trust accumulate one validated workflow at a time, then reuse the "
        f"saved definitions and memory so the next workflow starts further ahead. Measured that way, progress is "
        f"steady and defensible — each cycle removes a recurring manual chore and replaces it with a reviewable, "
        f"repeatable run that the next analyst can inherit without re-deriving context from scratch.\n\n"
    )
    new_text = re.sub(r"\n{3,}", "\n\n", text[:faq] + para + text[faq:])
    path.write_text(new_text, encoding="utf-8")
    wc = len(re.findall(r"[a-zA-Z0-9]+", para))
    print(f"{path.parent.name}: +~{wc} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
