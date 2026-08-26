#!/usr/bin/env python3
"""Fix internal links for Pillars 21-25 per Library Model + planned siblings."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

from url_config import blog_url_en

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
_spec = importlib.util.spec_from_file_location(
    "audit", Path(__file__).resolve().parent / "audit-internal-links-p21-25.py"
)
_audit = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_audit)

PILLARS = _audit.PILLARS
PLANNED_SIBLINGS = _audit.PLANNED_SIBLINGS


def h1_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            # concise anchor: drop trailing year parenthetical
            t = re.sub(r"\s*\(20\d{2}\)\s*$", "", t)
            t = re.sub(r":\s*A\s+.+$", "", t)
            t = re.sub(r":\s*The\s+.+$", "", t)
            if len(t) > 55:
                t = t[:52] + "..."
            return t
    return path.parent.name.replace("-", " ").title()


def slug_from_folder(pdir: Path, folder: str) -> str:
    art = pdir / folder / "article.md"
    m = re.search(
        r"\*\*Slug\*\*:\s*`?/blog/([a-z0-9-]+)`?",
        art.read_text(encoding="utf-8"),
    )
    if m:
        return m.group(1)
    return re.match(r"\d{3}-(.+)", folder).group(1)


def folder_for_num(pdir: Path, num: str) -> str | None:
    for d in pdir.iterdir():
        if d.is_dir() and d.name.startswith(f"{num}-"):
            return d.name
    return None


def internal_slugs(text: str) -> set[str]:
    slugs = set()
    for _, slug in re.findall(
        r"\[([^\]]+)\]\((?:https?://[^/]+)?(?:/[a-z]{2})?/blog/([^)/\s]+)", text
    ):
        slugs.add(slug.strip("/").split("/")[-1])
    return slugs


def link_phrase(title: str, slug: str) -> str:
    return f"[{title}]({blog_url_en(slug)})"


def build_missing_block(
    pdir: Path,
    hub_slug: str,
    hub_title: str,
    present: set[str],
    planned_nums: list[str],
) -> str | None:
    to_add: list[tuple[str, str]] = []

    if hub_slug not in present:
        to_add.append((hub_title, hub_slug))

    for num in planned_nums:
        folder = folder_for_num(pdir, num)
        if not folder:
            continue
        slug = slug_from_folder(pdir, folder)
        if slug not in present and not any(s == slug for _, s in to_add):
            title = h1_title(pdir / folder / "article.md")
            to_add.append((title, slug))

    if not to_add:
        return None

    hub_link = link_phrase(hub_title, hub_slug)
    sibling_links = [link_phrase(t, s) for t, s in to_add if s != hub_slug]

    if hub_slug not in present:
        if len(sibling_links) == 0:
            body = f"This guide is part of our {hub_link}."
        elif len(sibling_links) == 1:
            body = (
                f"This guide is part of our {hub_link}; "
                f"for related depth in this pillar, see {sibling_links[0]}."
            )
        else:
            body = (
                f"This guide is part of our {hub_link}; "
                f"for related depth in this pillar, see {sibling_links[0]} and {sibling_links[1]}."
            )
    else:
        if len(sibling_links) == 1:
            body = f"For related depth in this pillar, see {sibling_links[0]}."
        elif len(sibling_links) == 2:
            body = f"For related depth in this pillar, see {sibling_links[0]} and {sibling_links[1]}."
        else:
            body = (
                f"For related depth in this pillar, see {sibling_links[0]}, "
                f"{sibling_links[1]}, and {sibling_links[2]}."
            )
    return body


def insert_after_tldr(text: str, block: str) -> str:
    marker = "\n\n" + block + "\n"
    if block in text:
        return text
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    if not m:
        return text
    rest = text[m.end() :]
    nxt = re.search(r"^## [^#]", rest, re.M)
    if not nxt:
        return text
    insert_at = m.end() + nxt.start()
    return text[:insert_at] + marker + text[insert_at:]


def fix_pillar(pdir: Path, meta: dict) -> int:
    hub_folder = meta["hub"]
    hub_slug = meta["hub_slug"]
    hub_title = h1_title(pdir / hub_folder / "article.md")
    fixed = 0

    for art in sorted(pdir.glob("[0-9][0-9][0-9]-*/article.md")):
        folder = art.parent.name
        if folder == hub_folder:
            continue
        text = art.read_text(encoding="utf-8")
        present = internal_slugs(text)
        planned = PLANNED_SIBLINGS.get(folder, [])
        block = build_missing_block(pdir, hub_slug, hub_title, present, planned)
        if not block:
            # still fix if missing hub or <2 siblings
            cluster_folders = [
                d.name
                for d in pdir.iterdir()
                if re.match(r"\d{3}-", d.name)
                and d.name != hub_folder
                and (d / "article.md").is_file()
            ]
            sibling_slugs = {slug_from_folder(pdir, f) for f in cluster_folders}
            linked = present & sibling_slugs
            need_hub = hub_slug not in present
            need_sibs = len(linked) < 2
            if need_hub or need_sibs:
                extra_nums = []
                for f in cluster_folders:
                    if f == folder:
                        continue
                    s = slug_from_folder(pdir, f)
                    if s not in present:
                        extra_nums.append(f[:3])
                    if len(extra_nums) >= (2 - len(linked)) + (1 if need_hub else 0):
                        break
                block = build_missing_block(
                    pdir, hub_slug, hub_title, present, extra_nums
                )
        if not block:
            continue
        new_text = insert_after_tldr(text, block)
        if new_text != text:
            art.write_text(new_text, encoding="utf-8")
            fixed += 1
            print(f"  {folder}: +{block[:80]}...")
    return fixed


def main() -> int:
    total = 0
    for pname, meta in PILLARS.items():
        pdir = BLOG / pname
        print(f"\n{pname}")
        n = fix_pillar(pdir, meta)
        total += n
        print(f"  fixed {n} articles")
    print(f"\nTotal fixed: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
