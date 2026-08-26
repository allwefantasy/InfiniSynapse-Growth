#!/usr/bin/env python3
"""Report external links that appear only in TL;DR evaluation blocks, not narrative sections."""
import re
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]


def is_external(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return bool(host) and "infinisynapse" not in host


def main() -> None:
    weak = []
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            m = re.search(r"^## TL;DR\s*$", text, re.M)
            body = text[m.start() :] if m else text
            narrative_lines = []
            eval_only_lines = []
            for line in body.splitlines():
                if line.strip().startswith("> **Evaluation basis**"):
                    eval_only_lines.append(line)
                    continue
                if line.strip().startswith("#") or line.strip().startswith("|"):
                    continue
                narrative_lines.append(line)
            narrative = "\n".join(narrative_lines)
            eval_block = "\n".join(eval_only_lines)
            urls = {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body) if is_external(u)}
            in_narr = {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", narrative) if is_external(u)}
            only_eval = urls - in_narr
            if only_eval:
                weak.append((art.parent.name, len(only_eval), list(only_eval)[:2]))
    if not weak:
        print("All external links appear in narrative prose (outside Evaluation basis block).")
        return
    print(f"Weak placement: {len(weak)} articles")
    for name, n, urls in weak[:20]:
        print(f"  {name}: {n} link(s) only in eval block — e.g. {urls[0][:50]}")


if __name__ == "__main__":
    main()
