#!/usr/bin/env python3
"""Remove duplicate external-link lines from blog articles."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for pillar in ["pillar10-mcp-data-access", "pillar11-agentic-analytics"]:
    for art in Path(ROOT / f"SEO/Blog/{pillar}").glob("[0-9][0-9][0-9]-*/article.md"):
        text = art.read_text(encoding="utf-8")
        seen_urls: set[str] = set()
        out = []
        for line in text.splitlines():
            m = re.search(r"\((https?://[^)]+)\)", line)
            if m and "infinisynapse" not in m.group(1):
                u = m.group(1).rstrip("/").lower()
                if u in seen_urls:
                    continue
                seen_urls.add(u)
            out.append(line)
        art.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(art.parent.name, len(seen_urls))
