#!/usr/bin/env python3
"""De-stuff H2/H3 keyword headers and trim excess internal links (P21-25)."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
_spec = importlib.util.spec_from_file_location("audit_il", Path(__file__).resolve().parent / "audit-internal-links-p21-25.py")
_il = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_il)

PILLARS = _il.PILLARS
PLANNED_SIBLINGS = _il.PLANNED_SIBLINGS

MAX_CLUSTER_INTERNAL = 7
HUB_FOLDERS = {meta["hub"] for meta in PILLARS.values()}

INTERNAL_LINK = re.compile(r"\[([^\]]+)\]\((?:/[a-z]{2})?/blog/([^)/\s#]+)")


from article_keyword_meta import target_keyword as meta_target_keyword


def extract_keyword(text: str, article_path: Path | None = None) -> str:
    if article_path is not None:
        kw = meta_target_keyword(article_path)
        if kw:
            return kw.lower()
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).lower() if m else ""


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def slugify_header(title: str) -> str:
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
    t = re.sub(r"[*_`]", "", t).lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def dekeyword_title(title: str, kw: str) -> str:
    if not kw or kw not in title.lower():
        return title

    esc = re.escape(kw)
    faq_rules: list[tuple[str, str]] = [
        (rf"^What is {esc}\?$", "What is the core idea?"),
        (rf"^What is {esc} used for\?$", "What is it used for?"),
        (rf"^What is the {esc}\?$", "What is the core idea?"),
        (rf"^What is the intuition behind {esc}\?$", "What is the core intuition?"),
        (rf"^What does {esc} mean\?$", "What does certification mean here?"),
        (rf"^What are the (.+)?{esc}(.*)\?$", r"What are the \1options\2?"),
        (rf"^What are some (.+)?{esc}(.*)\?$", r"What are some \1examples\2?"),
        (rf"^What should (.+)?{esc}(.*)\?$", r"What should \1you include\2?"),
        (rf"^What makes (.+)?{esc}(.*)\?$", r"What makes \1a strong fit\2?"),
        (rf"^What is the best (.+)?{esc}(.*)\?$", r"What is the best \1path\2?"),
        (rf"^What is the difference between (.+) and {esc}(.*)\?$", r"What is the difference between \1 approaches\2?"),
        (rf"^How do you do {esc}\?$", "How do you run the workflow?"),
        (rf"^How do I (.+)?{esc}(.*)\?$", r"How do I \1get started\2?"),
        (rf"^How do (.+)?{esc}(.*)\?$", r"How do \1teams proceed\2?"),
        (rf"^How does (.+)?{esc}(.*)\?$", r"How does \1it help\2?"),
        (rf"^How is (.+)?{esc}(.*)\?$", r"How is \1the role changing\2?"),
        (rf"^How long does (.+)?{esc}(.*)\?$", r"How long does \1training take\2?"),
        (rf"^How much does (.+)?{esc}(.*)\?$", r"How much does \1it cost\2?"),
        (rf"^How can I (.+)?{esc}(.*)\?$", r"How can I \1improve outcomes\2?"),
        (rf"^Why is {esc} important\?$", "Why is exploration important?"),
        (rf"^Why does {esc}(.*)\?$", r"Why does rigor matter\1?"),
        (rf"^When should you use {esc}\?$", "When should you use this approach?"),
        (rf"^Where can I find (.+)?{esc}(.*)\?$", r"Where can I \1find openings\2?"),
        (rf"^Do (.+)?{esc}(.*)\?$", r"Do \1employers require proof\2?"),
        (rf"^Does {esc}(.*)\?$", r"Does completion guarantee results\1?"),
        (rf"^Can (.+)?{esc}(.*)\?$", r"Can \1AI assist\2?"),
        (rf"^Is {esc}(.*)\?$", r"Is formal training worth it\1?"),
        (rf"^Are (.+)?{esc}(.*)\?$", r"Are \1programs still in demand\2?"),
        (rf"^Will (.+)?{esc}(.*)\?$", r"Will \1automation reduce demand\2?"),
        (rf"^Which (.+)?{esc}(.*)\?$", r"Which \1options fit beginners\2?"),
    ]
    for pat, repl in faq_rules:
        m = re.match(pat, title, re.I)
        if m:
            out = re.sub(r"\s{2,}", " ", repl).strip()
            out = re.sub(r"\s+\?", "?", out)
            out = re.sub(r"\(\s*\)", "", out)
            if len(out) >= 8:
                return out

    new = re.sub(esc, "", title, flags=re.I)
    new = re.sub(r"\bfor\b", "", new, flags=re.I)
    new = re.sub(r"\s{2,}", " ", new).strip(" :-")
    new = re.sub(r"^What\s+", "What ", new)
    if len(new) < 10:
        words = [w for w in kw.split() if w not in ("data", "analysis", "the", "a", "of")]
        if words:
            new = f"{words[0].title()} essentials"
        else:
            new = "Practical overview"
    return new


def trim_keyword_headers(text: str, kw: str) -> tuple[str, int]:
    if not kw:
        return text, 0
    kw_l = kw.lower()
    matches = list(re.finditer(r"^(#{2,3})\s+(.+)$", text, re.M))
    skip = {"table of contents", "tldr", "frequently asked questions", "conclusion", "scorecard"}
    kw_matches = [
        m for m in matches if kw_l in m.group(2).lower() and m.group(2).lower() not in skip
    ]
    if len(kw_matches) < 3:
        return text, 0

    keep_pos = {kw_matches[0].start(), kw_matches[1].start()}
    changed = 0
    for m in reversed(kw_matches):
        if m.start() in keep_pos:
            continue
        level, title = m.group(1), m.group(2)
        new_title = dekeyword_title(title, kw)
        if new_title != title:
            text = text[: m.start()] + f"{level} {new_title}" + text[m.end() :]
            changed += 1
    return text, changed


def rebuild_toc(text: str) -> str:
    m = re.search(r"^## Table of Contents\s*\n", text, re.M)
    if not m:
        return text
    rest = text[m.end() :]
    sep = re.search(r"^---\s*$", rest, re.M)
    if not sep:
        return text
    toc_block_end = m.end() + sep.end()
    after = text[toc_block_end:]

    h2s: list[str] = []
    for line in after.splitlines():
        hm = re.match(r"^## (.+)$", line)
        if hm and hm.group(1) != "Table of Contents":
            h2s.append(hm.group(1))

    lines = ["## Table of Contents", ""]
    for i, h in enumerate(h2s, 1):
        lines.append(f"{i}. [{h}](#{slugify_header(h)})")
    lines.append("")
    new_toc = "\n".join(lines)
    return text[: m.start()] + new_toc + "\n---\n" + after.lstrip()


def faq_pairs(text: str) -> list[tuple[str, str]]:
    m = re.search(r"^## Frequently Asked Questions\s*\n", text, re.M)
    if not m:
        return []
    rest = text[m.end() :]
    end = re.search(r"^## ", rest, re.M)
    block = rest[: end.start()] if end else rest
    pairs = []
    for qm in re.finditer(r"^### (.+)$\n(.+?)(?=\n### |\Z)", block, re.S | re.M):
        pairs.append((qm.group(1).strip(), re.sub(r"\s+", " ", qm.group(2).strip())))
    return pairs


def sync_schema_faq(schema_path: Path, pairs: list[tuple[str, str]]) -> bool:
    if not schema_path.is_file() or not pairs:
        return False
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    changed = False
    for block in data:
        if block.get("@type") != "FAQPage":
            continue
        entities = [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ]
        if block.get("mainEntity") != entities:
            block["mainEntity"] = entities
            changed = True
    if changed:
        schema_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def folder_to_slug_map(pdir: Path) -> dict[str, str]:
    out = {}
    for art in pdir.glob("[0-9][0-9][0-9]-*/article.md"):
        text = art.read_text(encoding="utf-8")
        m = re.search(r"\*\*Slug\*\*:\s*`?/blog/([a-z0-9-]+)`?", text)
        slug = m.group(1) if m else art.parent.name.split("-", 1)[1]
        out[art.parent.name] = slug
    return out


def required_internal_slugs(folder: str, pdir: Path, hub_slug: str) -> set[str]:
    req = {hub_slug}
    f2s = folder_to_slug_map(pdir)
    for num in PLANNED_SIBLINGS.get(folder, []):
        for f, s in f2s.items():
            if f.startswith(f"{num}-"):
                req.add(s)
                break
    return req


def trim_internal_links(text: str, folder: str, pdir: Path, hub_slug: str) -> tuple[str, int]:
    if folder in HUB_FOLDERS:
        return text, 0

    req = required_internal_slugs(folder, pdir, hub_slug)
    matches = list(INTERNAL_LINK.finditer(text))
    if len(matches) <= MAX_CLUSTER_INTERNAL:
        return text, 0

    keep_starts: set[int] = set()
    kept_slugs: set[str] = set()

    for m in matches:
        slug = m.group(2).strip("/").split("/")[-1]
        if slug in req and slug not in kept_slugs:
            keep_starts.add(m.start())
            kept_slugs.add(slug)

    for m in matches:
        if len(keep_starts) >= MAX_CLUSTER_INTERNAL:
            break
        slug = m.group(2).strip("/").split("/")[-1]
        if m.start() not in keep_starts:
            keep_starts.add(m.start())
            kept_slugs.add(slug)

    removed = 0
    for m in reversed(matches):
        if m.start() in keep_starts:
            continue
        text = text[: m.start()] + m.group(1) + text[m.end() :]
        removed += 1
    return text, removed


def dedupe_tldr_hub_lines(text: str) -> str:
    """Collapse extra TL;DR cross-link clauses; keep hub + sibling block."""
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    if not m:
        return text
    rest = text[m.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    if not nxt:
        return text
    tldr = rest[: nxt.start()]
    if tldr.count("/blog/") <= 4:
        return text

    lines = tldr.splitlines()
    kept: list[str] = []
    link_lines = 0
    for ln in lines:
        if "/blog/" in ln:
            link_lines += 1
            if link_lines > 2:
                # strip internal links from overflow lines, keep prose
                ln = INTERNAL_LINK.sub(lambda mm: mm.group(1), ln)
            if ln.strip():
                kept.append(ln)
        else:
            kept.append(ln)
    new_tldr = "\n".join(kept)
    return text[: m.end()] + new_tldr + rest[nxt.start() :]


def process_article(article: Path, pname: str, meta: dict, *, links_only: bool = False) -> dict:
    folder = article.parent.name
    text = article.read_text(encoding="utf-8")
    kw = extract_keyword(text, article)
    stats = {"headers": 0, "links": 0, "toc": False, "schema": False}

    if not links_only:
        trimmed, n = trim_keyword_headers(text, kw)
        if n:
            text = trimmed
            stats["headers"] = n

        new_toc = rebuild_toc(text)
        if new_toc != text:
            text = new_toc
            stats["toc"] = True

    deduped = dedupe_tldr_hub_lines(text)
    if deduped != text:
        text = deduped

    pdir = BLOG / pname
    trimmed_links, ln = trim_internal_links(text, folder, pdir, meta["hub_slug"])
    if ln:
        text = trimmed_links
        stats["links"] = ln

    if text != article.read_text(encoding="utf-8"):
        article.write_text(text, encoding="utf-8")
        if not links_only:
            pairs = faq_pairs(text)
            if pairs:
                stats["schema"] = sync_schema_faq(article.parent / "schema.json", pairs)
    return stats


def main() -> int:
    links_only = "--links-only" in sys.argv
    total_h = total_l = articles = 0
    for pname, meta in PILLARS.items():
        pdir = BLOG / pname
        print(f"\n{pname}")
        for art in sorted(pdir.glob("[0-9][0-9][0-9]-*/article.md")):
            st = process_article(art, pname, meta, links_only=links_only)
            if any(st.values()):
                articles += 1
                print(
                    f"  {art.parent.name}: headers={st['headers']} "
                    f"links={st['links']} toc={st['toc']}"
                )
                total_h += st["headers"]
                total_l += st["links"]
    mode = "link trim" if links_only else "headers+links"
    print(f"\n[{mode}] Updated {articles} articles | headers: {total_h} | links trimmed: {total_l}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
