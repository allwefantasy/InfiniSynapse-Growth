#!/usr/bin/env python3
"""Repair triple -reddit-reddit-reddit slug corruption from global replace."""
from __future__ import annotations

import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))


def normalize_slug(slug: str) -> str:
    s = slug.strip().strip("/").removeprefix("blog/")
    base = re.sub(r"(?:-reddit)+$", "", s)
    if base != s:
        return f"{base}-reddit"
    return s


def normalize_keyword(kw: str) -> str:
    k = re.sub(r"(?:\s+reddit)+$", " reddit", kw.strip(), flags=re.I)
    return k


def title_case_keyword(kw: str) -> str:
    return " ".join(w.capitalize() if w.lower() != "vs" else "vs" for w in kw.split())


def fix_h1_for_reddit(text: str, kw: str) -> str:
    if not kw.lower().endswith(" reddit"):
        return text
    tc = title_case_keyword(kw)
    h1_m = re.match(r"^(# .+)$", text, re.M)
    if not h1_m or tc.lower() in h1_m.group(1).lower():
        return text
    body = h1_m.group(1)[2:].strip()
    base_kw = kw.rsplit(" reddit", 1)[0]
    base_tc = title_case_keyword(base_kw)
    if body.lower().startswith(base_tc.lower()):
        new_h1 = f"# {tc}{body[len(base_tc):]}"
    elif ":" in body:
        _, rest = body.split(":", 1)
        new_h1 = f"# {tc}: {rest.strip()}"
    else:
        new_h1 = f"# {tc}: {body}"
    return text.replace(h1_m.group(1), new_h1, 1)


def fix_meta_desc(text: str, kw: str) -> str:
    if not kw.lower().endswith(" reddit"):
        return text
    tc = title_case_keyword(kw)
    m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    if not m:
        return text
    desc = m.group(1).strip()
    # remove duplicate title prefix
    desc = re.sub(rf"^{re.escape(tc)}:\s*", "", desc, flags=re.I)
    base_tc = title_case_keyword(kw.rsplit(" reddit", 1)[0])
    desc = re.sub(rf"^{re.escape(base_tc)}:\s*", "", desc, flags=re.I)
    new_desc = f"{tc}: {desc}"[:155]
    return text.replace(f"**Meta Description**: {m.group(1).strip()}", f"**Meta Description**: {new_desc}", 1)


def main() -> int:
    slug_map: dict[str, str] = {}
    for pillar in PILLARS:
        reg = pillar / "articles_registry.json"
        if reg.is_file():
            data = json.loads(reg.read_text(encoding="utf-8"))
            for art in data.get("articles", []):
                old = art["slug"]
                new = normalize_slug(old)
                if old != new:
                    slug_map[old] = new
                art["slug"] = new
                art["keyword"] = normalize_keyword(art.get("keyword", ""))
            reg.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for path in BLOG.rglob("*"):
        if path.suffix not in {".md", ".html", ".json", ".csv", ".xml"}:
            continue
        if "handoff-pack" in str(path) or "_archive" in str(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in re.finditer(r"/(?:en|zh)/blog/([a-z0-9-]+)", text):
            old = m.group(1)
            new = normalize_slug(old)
            if old != new:
                slug_map[old] = new

    pairs = sorted(slug_map.items(), key=lambda x: -len(x[0]))
    n_files = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            content = art.read_text(encoding="utf-8")
            orig = content
            for old, new in pairs:
                for prefix in ("/en/blog/", "/zh/blog/", "/blog/"):
                    content = content.replace(f"{prefix}{old}", f"{prefix}{new}")
            content = re.sub(
                r"(\*\*Target keyword\*\*:\s*`)([^`]+)(`)",
                lambda m: m.group(1) + normalize_keyword(m.group(2)) + m.group(3),
                content,
                count=1,
            )
            content = re.sub(
                r"\*\*Slug\*\*:\s*`(/blog/)?([^`]+)`",
                lambda m: f"**Slug**: `/blog/{normalize_slug(m.group(2))}`",
                content,
                count=1,
            )
            kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", content)
            if kw_m:
                kw = kw_m.group(1)
                content = fix_h1_for_reddit(content, kw)
                content = fix_meta_desc(content, kw)
            if content != orig:
                art.write_text(content, encoding="utf-8")
                n_files += 1

    print(f"repaired slugs {len(slug_map)} | polished {n_files} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
