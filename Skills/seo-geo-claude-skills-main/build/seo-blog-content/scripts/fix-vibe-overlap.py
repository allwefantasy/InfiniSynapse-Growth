#!/usr/bin/env python3
"""Rotate external URLs per article to reduce in-pillar link overlap."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

HAND_POLISHED = {
    "203-api-integration-services",
    "204-integration-software",
    "206-api-integration-tools",
    "218-manage-multiple-api-integrations",
    "221-api-integration-testing",
    "223-agentic-orchestration",
    "224-tool-calling",
}

_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

URL_POOL = list(dict.fromkeys(s["url"] for s in _hdr.HIGH_DR_SOURCES))


def rotate_links(text: str, article_num: int) -> str:
    if not URL_POOL:
        return text
    targets = [URL_POOL[(article_num * 7 + i * 13) % len(URL_POOL)] for i in range(14)]
    targets = list(dict.fromkeys(targets))

    body_start = re.search(r"^## TL;DR\s*$", text, re.M)
    if not body_start:
        return text
    head, body = text[: body_start.start()], text[body_start.start() :]

    idx = 0
    for m in list(re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", body)):
        url = m.group(2)
        if "infinisynapse" in urlparse(url).netloc.lower():
            continue
        new_url = targets[idx % len(targets)]
        idx += 1
        body = body.replace(m.group(0), f"[{m.group(1)}]({new_url})", 1)
    return head + body


def main() -> int:
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            folder = art.parent.name
            if folder in HAND_POLISHED:
                continue
            num = int(folder[:3])
            text = rotate_links(art.read_text(encoding="utf-8"), num)
            art.write_text(text, encoding="utf-8")
    print("rotated external URLs for template articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
