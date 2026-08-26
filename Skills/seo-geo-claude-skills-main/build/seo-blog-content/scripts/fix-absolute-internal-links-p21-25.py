#!/usr/bin/env python3
"""Convert relative internal blog links to absolute production URLs (P21-25).

QuickCreator flags chrome-extension:// when relative /en/blog/ links are
resolved inside the browser extension context. Absolute https://infinisynapse.com
links avoid that mis-resolution after CMS redeploy.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from url_config import blog_url_en

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[1-5]-*"))

# [text](/en/blog/slug) or [text](/blog/slug) — skip if already absolute
REL_INTERNAL = re.compile(
    r"\[([^\]]+)\]\((?!https?://)(?:/[a-z]{2})?/blog/([^)/\s#]+)([^)]*)\)"
)


def fix_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        anchor, slug, suffix = m.group(1), m.group(2).strip("/"), m.group(3)
        count += 1
        return f"[{anchor}]({blog_url_en(slug)}{suffix})"

    return REL_INTERNAL.sub(repl, text), count


def main() -> int:
    total_links = 0
    files_touched = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            new_text, n = fix_text(text)
            if new_text != text:
                art.write_text(new_text, encoding="utf-8")
                files_touched += 1
                total_links += n
                print(f"  {art.parent.name}: {n} links")
    print(f"\nFixed {total_links} internal links in {files_touched} articles")
    if files_touched:
        gen = Path(__file__).resolve().parent / "gen-meta-schema-p21-25.py"
        subprocess.run([sys.executable, str(gen)], check=True)
        deploy = Path(__file__).resolve().parent / "generate-deploy-meta.py"
        subprocess.run([sys.executable, str(deploy)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
