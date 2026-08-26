#!/usr/bin/env python3
"""Force-correct Pillar 16–20 slugs from plan + safe global relink for deploy."""
from __future__ import annotations

import csv
import importlib.util
import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
PLAN = BLOG / "blog-vibe-coding-topics-plan.csv"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

SKIP_REDDIT = {
    "prod system",
    "webhook relay service api data model",
    "database application programming interface",
}

_spec = importlib.util.spec_from_file_location(
    "upgrade", SCRIPTS / "upgrade-vibe-reddit-geo.py"
)
_upgrade = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_upgrade)
sync_meta = _upgrade.sync_meta
title_case_keyword = _upgrade.title_case_keyword

BAD = re.compile(r"reddit-reddit|reddits-reddit|(?:-reddit){3,}")


def load_plan() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    with PLAN.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            out[row["编号"].strip()] = row
    return out


def expected_slug(row: dict[str, str]) -> str:
    s = row["slug"].strip()
    kw = row["关键词"].strip().lower()
    if kw in SKIP_REDDIT:
        return s
    return s if s.endswith("-reddit") else f"{s}-reddit"


def repair_slug(slug: str, canonical: set[str]) -> str | None:
    if slug in canonical:
        return slug
    s = slug.replace("-reddits-reddit", "-reddit").replace("reddits-reddit", "reddit")
    while "-reddit-reddit" in s:
        s = s.replace("-reddit-reddit", "-reddit")
    s = re.sub(r"(?:-reddit)+$", "-reddit", s)
    if s in canonical:
        return s
    return None


def article_meta(art: Path) -> tuple[str, str, str, str]:
    text = art.read_text(encoding="utf-8")
    kw = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text).group(1).strip()
    h1 = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), "")
    title = h1 or title_case_keyword(kw)
    desc_m = re.search(r"\*\*Meta Description\*\*:\s*(.+)$", text, re.M)
    desc = desc_m.group(1).strip() if desc_m else title
    return kw, title, desc, text


def force_article_slug(text: str, slug: str) -> str:
    return re.sub(r"\*\*Slug\*\*:\s*`[^`]+`", f"**Slug**: `/blog/{slug}`", text, count=1)


def main() -> int:
    plan = load_plan()
    correct: dict[str, str] = {aid: expected_slug(row) for aid, row in plan.items()}
    canonical = set(correct.values())

    # 1) Force article.md + registry + meta from plan
    for pillar in PILLARS:
        reg_path = pillar / "articles_registry.json"
        if reg_path.is_file():
            data = json.loads(reg_path.read_text(encoding="utf-8"))
            for art in data.get("articles", []):
                if art["id"] in correct:
                    art["slug"] = correct[art["id"]]
            reg_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            aid = art.parent.name[:3]
            if aid not in correct:
                continue
            exp = correct[aid]
            kw, title, desc, text = article_meta(art)
            text = force_article_slug(text, exp)
            art.write_text(text, encoding="utf-8")
            sync_meta(art.parent, title, desc, exp, kw)

    # 2) Build replace map only for corrupted slugs
    slug_map: dict[str, str] = {}
    for path in BLOG.rglob("*"):
        if path.suffix not in {".md", ".html", ".json", ".csv", ".xml"}:
            continue
        if "vibe-coding-handoff-pack" in str(path) or "_archive" in str(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in re.finditer(r"/(?:en|zh)/blog/([a-z0-9-]+)", text):
            s = m.group(1)
            if s in canonical:
                continue
            fixed = repair_slug(s, canonical)
            if fixed and fixed != s:
                slug_map[s] = fixed
        for m in re.finditer(r'"/blog/([a-z0-9-]+)"', text):
            s = m.group(1)
            if s in canonical:
                continue
            fixed = repair_slug(s, canonical)
            if fixed and fixed != s:
                slug_map[s] = fixed

    pairs = sorted(slug_map.items(), key=lambda x: -len(x[0]))
    n_files = 0
    for path in BLOG.rglob("*"):
        if path.suffix not in {".md", ".html", ".json", ".csv", ".xml"}:
            continue
        if "vibe-coding-handoff-pack" in str(path) or "_archive" in str(path):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        orig = content
        for old, new in pairs:
            for prefix in ("/en/blog/", "/zh/blog/", "/blog/"):
                content = content.replace(f"{prefix}{old}", f"{prefix}{new}")
        if content != orig:
            path.write_text(content, encoding="utf-8")
            n_files += 1

    # 3) Re-force article slugs + meta (global replace may have touched Slug lines)
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            aid = art.parent.name[:3]
            if aid not in correct:
                continue
            exp = correct[aid]
            kw, title, desc, text = article_meta(art)
            text = force_article_slug(text, exp)
            art.write_text(text, encoding="utf-8")
            sync_meta(art.parent, title, desc, exp, kw)

    print(f"forced {len(correct)} slugs | bad->good pairs {len(pairs)} | relinked files {n_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
