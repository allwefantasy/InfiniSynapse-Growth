#!/usr/bin/env python3
"""Repair article:published_time / article:modified_time meta tags mangled by an
earlier batch date bump.

The bad script dropped the property name and the `20` century digits, leaving:

    <meta property="P26-07-20T00:00:00Z">

Two shapes exist in the repo:

* one broken line  -> only `article:modified_time` was hit; published_time survived
* two broken lines -> published_time and modified_time were both hit (Pillar 13)

Repair rules (in-place, never a full head.html rebuild):

* modified_time  = the timestamp preserved inside the broken tag
* published_time = the file's own JSON-LD `datePublished`, so the restored meta tag
  cannot claim a publish date the structured data disagrees with
* the embedded JSON-LD `dateModified` is refreshed only when the sibling
  `schema.json` already carries a newer value — never invented here

A full rebuild via generate-deploy-meta.py is deliberately avoided: Pillar 1-15
`head.html` files are hand-maintained (that glob does not reach them) and carry
CTR-tuned titles plus hreflang/Breadcrumb blocks their stale meta-tags.html lacks.

Usage:
  python3 repair-broken-modified-time-meta.py --dry-run
  python3 repair-broken-modified-time-meta.py
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SEO = ROOT / "SEO"

BROKEN = re.compile(r'<meta property="P(\d\d-\d\d-\d\dT[^">]*)">')
PUB = re.compile(r'<meta property="article:published_time" content="([^"]+)"\s*/?>')
MOD = re.compile(r'<meta property="article:modified_time" content="([^"]+)"\s*/?>')
JSON_PUB = re.compile(r'"datePublished":\s*"([^"]+)"')
JSON_MOD = re.compile(r'"dateModified":\s*"([^"]+)"')


def tag(prop: str, value: str) -> str:
    return f'<meta property="{prop}" content="{value}">'


def sibling_schema_modified(path: Path) -> str | None:
    schema = path.parent / "schema.json"
    if not schema.is_file():
        return None
    try:
        blocks = json.loads(schema.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if isinstance(blocks, dict):
        blocks = [blocks]
    for block in blocks:
        if isinstance(block, dict) and block.get("dateModified"):
            return block["dateModified"]
    return None


def repair(path: Path, text: str) -> tuple[str, list[str]]:
    matches = list(BROKEN.finditer(text))
    if not matches:
        return text, []

    has_pub = bool(PUB.search(text))
    json_pub = JSON_PUB.search(text)
    schema_mod = sibling_schema_modified(path)
    notes: list[str] = []

    parts, cursor = [], 0
    modified_value = None
    for idx, m in enumerate(matches):
        preserved = "20" + m.group(1)
        if len(matches) == 2 and idx == 0 and not has_pub:
            value = json_pub.group(1) if json_pub else preserved
            line = tag("article:published_time", value)
        else:
            # Same instant, but schema.json spells it in the repo's +08:00 style.
            same_day = schema_mod and schema_mod[:10] == preserved[:10]
            modified_value = schema_mod if same_day else preserved
            line = tag("article:modified_time", modified_value)
        notes.append(line)
        parts.append(text[cursor : m.start()])
        parts.append(line)
        cursor = m.end()
    parts.append(text[cursor:])
    out = "".join(parts)

    # Keep the embedded JSON-LD in step, but only on evidence from schema.json.
    embedded = JSON_MOD.search(out)
    if (
        modified_value
        and schema_mod
        and embedded
        and embedded.group(1) != schema_mod
        and schema_mod[:10] == modified_value[:10]
    ):
        out = JSON_MOD.sub(f'"dateModified": "{schema_mod}"', out, count=1)
        notes.append(f'JSON-LD dateModified {embedded.group(1)} -> {schema_mod}')

    return out, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = 0
    for path in sorted(SEO.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not BROKEN.search(text):
            continue
        fixed, notes = repair(path, text)
        assert not BROKEN.search(fixed), path
        assert len(MOD.findall(fixed)) == 1, f"duplicate modified_time in {path}"
        assert len(PUB.findall(fixed)) == 1, f"missing/duplicate published_time in {path}"
        files += 1
        print(f"{'would fix' if args.dry_run else 'fixed'} {path.relative_to(ROOT)}")
        for note in notes:
            print(f"    {note}")
        if not args.dry_run:
            path.write_text(fixed, encoding="utf-8")

    print(f"\n{files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
