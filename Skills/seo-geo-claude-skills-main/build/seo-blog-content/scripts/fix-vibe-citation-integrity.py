#!/usr/bin/env python3
"""Repair mismatched external citation anchor↔URL pairs in Pillar 16–20 articles."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
HANDOFF = BLOG / "vibe-coding-handoff-pack" / "articles"

_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)
SOURCES: list[dict] = _hdr.HIGH_DR_SOURCES

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
WIKI_ANCHOR_RE = re.compile(r"wikipedia", re.I)

# Anchor keyword → source id (longest match wins)
ANCHOR_TO_ID: list[tuple[str, str]] = []
for s in SOURCES:
    sid = s["id"]
    label = s["label"].lower()
    ANCHOR_TO_ID.append((label, sid))
    m = re.search(r"\[([^\]]+)\]", s.get("weave", ""))
    if m:
        ANCHOR_TO_ID.append((m.group(1).lower(), sid))
    # Extra aliases from label tokens
    for token in re.split(r"[\s'/-]+", label):
        if len(token) >= 5:
            ANCHOR_TO_ID.append((token, sid))
ANCHOR_TO_ID.sort(key=lambda x: len(x[0]), reverse=True)

URL_TO_SOURCE: dict[str, dict] = {}
for s in SOURCES:
    u = s["url"].rstrip("/")
    URL_TO_SOURCE[u] = s
    host = urlparse(u).netloc.lower()
    URL_TO_SOURCE[host] = s


def article_roots() -> list[Path]:
    roots: list[Path] = []
    for p in sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*")):
        roots.append(p)
    if HANDOFF.is_dir():
        for p in sorted(HANDOFF.glob("pillar*")):
            if p not in roots:
                roots.append(p)
    return roots


def source_for_url(url: str) -> dict | None:
    url = url.rstrip("/.,)")
    if url in URL_TO_SOURCE:
        return URL_TO_SOURCE[url]
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    best: dict | None = None
    best_len = 0
    for s in SOURCES:
        su = s["url"].rstrip("/")
        sh = urlparse(su).netloc.lower()
        sp = urlparse(su).path.lower().rstrip("/")
        if host == sh and (not sp or path.startswith(sp) or sp.startswith(path[: max(len(sp), 1)])):
            if len(sp) > best_len:
                best, best_len = s, len(sp)
    return best


def source_for_anchor(anchor: str) -> dict | None:
    al = anchor.lower()
    for key, sid in ANCHOR_TO_ID:
        if key in al:
            return _hdr.source_by_id(sid)
    return None


def canonical_anchor(source: dict) -> str:
    m = re.search(r"\[([^\]]+)\]", source.get("weave", ""))
    if m:
        return m.group(1)
    return source["label"]


def url_matches_anchor(source: dict | None, anchor: str) -> bool:
    if not source:
        return False
    al = anchor.lower()
    label = source["label"].lower()
    host = urlparse(source["url"]).netloc.lower().split(".")
    tokens = set(re.split(r"[\s'/-]+", label)) | {host[0]}
    tokens = {t for t in tokens if len(t) >= 4}
    return any(t in al for t in tokens)


LOW_DR_HOSTS = {"swagger.io", "12factor.net", "localhost"}

def is_low_dr(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    if any(h in host for h in LOW_DR_HOSTS):
        return True
    return not _hdr.is_high_dr_url(url)


def fix_link(anchor: str, url: str) -> tuple[str, str, str]:
    """Return (new_anchor, new_url, reason)."""
    if is_low_dr(url):
        src = source_for_anchor(anchor)
        if src:
            return canonical_anchor(src), src["url"], "low_dr"
    src_url = source_for_url(url)
    src_anchor = source_for_anchor(anchor)

    # Wikipedia anchors must point to wikipedia.org
    if WIKI_ANCHOR_RE.search(anchor) and "wikipedia.org" not in url.lower():
        if src_anchor and "wikipedia" in src_anchor["label"].lower():
            return canonical_anchor(src_anchor), src_anchor["url"], "wiki_anchor"
        # generic wiki fix from anchor
        wiki_map = {
            "business intelligence": "https://en.wikipedia.org/wiki/Business_intelligence",
            "data warehouse": "https://en.wikipedia.org/wiki/Data_warehouse",
            "machine learning": "https://en.wikipedia.org/wiki/Machine_learning",
            "natural language": "https://en.wikipedia.org/wiki/Natural_language_processing",
            "statistics": "https://en.wikipedia.org/wiki/Statistics",
            "etl": "https://en.wikipedia.org/wiki/Extract,_transform,_load",
            "sql": "https://en.wikipedia.org/wiki/SQL",
        }
        al = anchor.lower()
        for k, wu in wiki_map.items():
            if k in al:
                return anchor, wu, "wiki_url"
        return anchor, "https://en.wikipedia.org/wiki/Business_intelligence", "wiki_fallback"

    if src_anchor and src_url and src_anchor["id"] != src_url["id"]:
        # URL and anchor disagree — trust anchor (reader-visible label)
        return canonical_anchor(src_anchor), src_anchor["url"], "anchor_wins"

    if src_anchor and not url_matches_anchor(src_url, anchor):
        return canonical_anchor(src_anchor), src_anchor["url"], "anchor_wins"

    if src_url and not url_matches_anchor(src_url, anchor):
        return canonical_anchor(src_url), src_url["url"], "url_wins"

    return anchor, url, "ok"


REDDIT_HOOK_PAT = re.compile(
    r"(After skimming |I read |I pulled |From )(\d{2,4})\+?\s*Reddit[^,\n]{0,80}",
    re.I,
)
REDDIT_METHODOLOGY = (
    "After reviewing recurring build-log threads in r/vibecoding, r/Cursor, and r/webdev "
    "(manual sample, 2024–2026—not a formal crawl), "
)


def soften_reddit_hooks(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return REDDIT_METHODOLOGY

    return REDDIT_HOOK_PAT.sub(repl, text, count=1)


def fix_article(text: str) -> tuple[str, int]:
    fixes = 0

    def sub_link(m: re.Match[str]) -> str:
        nonlocal fixes
        anchor, url = m.group(1), m.group(2)
        if "infinisynapse" in url.lower():
            return m.group(0)
        na, nu, reason = fix_link(anchor, url)
        if reason != "ok" and (na != anchor or nu != url):
            fixes += 1
            return f"[{na}]({nu})"
        return m.group(0)

    text = LINK_RE.sub(sub_link, text)
    new_text = soften_reddit_hooks(text)
    if new_text != text:
        fixes += 1
        text = new_text
    return text, fixes


def main() -> int:
    total_fixes = 0
    files = 0
    for root in article_roots():
        for art in sorted(root.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            fixed, n = fix_article(text)
            if n:
                art.write_text(fixed, encoding="utf-8")
                total_fixes += n
                files += 1
                print(f"  {art.parent.name}: {n} fixes")
    print(f"Fixed {total_fixes} issues in {files} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
