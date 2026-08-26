#!/usr/bin/env python3
"""Add high-DR citations and inline links to hand-polished articles still failing audit."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

PATCHES = {
    "204-integration-software": [
        _hdr.HIGH_DR_SOURCES[2]["weave"].format(url=_hdr.HIGH_DR_SOURCES[2]["url"]),
        _hdr.HIGH_DR_SOURCES[4]["weave"].format(url=_hdr.HIGH_DR_SOURCES[4]["url"]),
        _hdr.HIGH_DR_SOURCES[6]["weave"].format(url=_hdr.HIGH_DR_SOURCES[6]["url"]),
        _hdr.HIGH_DR_SOURCES[7]["weave"].format(url=_hdr.HIGH_DR_SOURCES[7]["url"]),
    ],
    "218-manage-multiple-api-integrations": [
        _hdr.HIGH_DR_SOURCES[3]["weave"].format(url=_hdr.HIGH_DR_SOURCES[3]["url"]),
        _hdr.HIGH_DR_SOURCES[5]["weave"].format(url=_hdr.HIGH_DR_SOURCES[5]["url"]),
        _hdr.HIGH_DR_SOURCES[8]["weave"].format(url=_hdr.HIGH_DR_SOURCES[8]["url"]),
    ],
    "221-api-integration-testing": [
        _hdr.HIGH_DR_SOURCES[1]["weave"].format(url=_hdr.HIGH_DR_SOURCES[1]["url"]),
    ],
    "223-agentic-orchestration": [
        _hdr.HIGH_DR_SOURCES[0]["weave"].format(url=_hdr.HIGH_DR_SOURCES[0]["url"]),
        _hdr.HIGH_DR_SOURCES[9]["weave"].format(url=_hdr.HIGH_DR_SOURCES[9]["url"]),
    ],
    "224-tool-calling": [
        _hdr.HIGH_DR_SOURCES[4]["weave"].format(url=_hdr.HIGH_DR_SOURCES[4]["url"]),
        _hdr.HIGH_DR_SOURCES[10]["weave"].format(url=_hdr.HIGH_DR_SOURCES[10]["url"]),
    ],
}


def main() -> int:
    for folder, weaves in PATCHES.items():
        art = next(BLOG.rglob(f"{folder}/article.md"), None)
        if not art:
            continue
        text = art.read_text(encoding="utf-8")
        for w in weaves:
            if w.split("](")[1].split(")")[0] in text:
                continue
            text = text.replace("\n## Failure Modes\n", f"\n{w}\n\n## Failure Modes\n", 1)
        art.write_text(text, encoding="utf-8")
        print(f"patched {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
