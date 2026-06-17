#!/usr/bin/env python3
"""Remove repeated slug-specific density booster paragraphs before Conclusion."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).parent

PATTERNS = [
    r"\nIn our `[^`]+` pilots, mature \*\*[^*]+\*\* workflows reduced rework once metric contracts were signed\.\n?",
    r"\nReviewers accepted \*\*[^*]+\*\* outputs faster when `[^`]+` runbooks listed owners, sources, and escalation paths\.\n?",
    r"\nWe stress-test \*\*[^*]+\*\* on schema drift—not demo day—before expanding `[^`]+` scope\.\n?",
    r"\nStakeholders trusted \*\*[^*]+\*\* memos when `[^`]+` teams attached query fingerprints to every chart\.\n?",
    r"\nThe `[^`]+` rollout improved when \*\*[^*]+\*\* memory cards captured exception fixes weekly\.\n?",
    r"\nFor `[^`]+` buyers, \*\*[^*]+\*\* ROI showed up in cycle-time minutes, not slide polish\.\n?",
    r"\nGovernance expectations for production analytics align with the \[NIST AI Risk Management Framework\]\([^)]+\), which we reference when designing reviewer checkpoints\.\n?",
]


def cleanup(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for pat in PATTERNS:
        text = re.sub(pat, "\n", text, flags=re.I)
    # Catch-all for slug booster family
    text = re.sub(
        r"\n(?:In our|Reviewers accepted|We stress-test|Stakeholders trusted|The `[^`]+` rollout improved|For `[^`]+` buyers),[^\n]+\n",
        "\n",
        text,
        flags=re.I,
    )
    # Remove duplicate pilot-note density lines (keep first of each id)
    seen_notes: set[str] = set()
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        m = re.match(r"^Pilot note (\d+):", line)
        if m:
            if m.group(1) in seen_notes:
                continue
            seen_notes.add(m.group(1))
        out.append(line)
    text = "\n".join(out)
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
    print(f"Cleaned boosters in {changed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
