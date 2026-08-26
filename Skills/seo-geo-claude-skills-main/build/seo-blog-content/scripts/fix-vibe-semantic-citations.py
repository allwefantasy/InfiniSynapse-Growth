#!/usr/bin/env python3
"""Replace semantically wrong citation reuse (same URL, wrong context) in Pillar 16–20."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

# When paragraph hints match, prefer these source ids (high DR)
HINT_SOURCES: list[tuple[str, str]] = [
    (r"api gateway|gateway pattern|entry point for all api", "owasp-api"),
    (r"proxy|authentication header|credential", "owasp-api"),
    (r"registry|integration registry|source of truth for your api", "ms-data-arch"),
    (r"secret|credential|rotation|vault", "nist-ai-rmf"),
    (r"security|governance|compliance", "owasp-llm"),
    (r"warehouse|sql|bigquery|snowflake", "google-bigquery-docs"),
    (r"stream|kafka|event", "apache-kafka-docs"),
    (r"kubernetes|deploy|container", "kubernetes-docs"),
    (r"monitor|observability|sre|postmortem", "google-sre"),
    (r"agent|tool calling|llm", "owasp-llm"),
    (r"eu|gdpr|regulation", "eu-ai-act"),
]

SOURCE_BY_ID = {s["id"]: s for s in _hdr.HIGH_DR_SOURCES}


def weave_for(sid: str) -> str:
    s = SOURCE_BY_ID[sid]
    return s["weave"].format(url=s["url"])


def pick_source(paragraph: str, exclude_urls: set[str]) -> dict | None:
    for pat, sid in HINT_SOURCES:
        if re.search(pat, paragraph, re.I) and sid in SOURCE_BY_ID:
            s = SOURCE_BY_ID[sid]
            if s["url"] not in exclude_urls:
                return s
    for s in _hdr.HIGH_DR_SOURCES:
        if s["url"] not in exclude_urls:
            return s
    return None


def fix_duplicates(text: str) -> tuple[str, int]:
    fixes = 0
    lines = text.splitlines(keepends=True)
    url_counts: dict[str, int] = {}
    for line in lines:
        for _, u in LINK_RE.findall(line):
            if u.startswith("http"):
                url_counts[u] = url_counts.get(u, 0) + 1

    overused = {u for u, n in url_counts.items() if n >= 2}
    if not overused:
        return text, 0

    seen_url: dict[str, int] = {}
    out: list[str] = []
    for line in lines:
        if not any(u in line for u in overused):
            out.append(line)
            continue

        def repl(m: re.Match[str]) -> str:
            nonlocal fixes
            anchor, url = m.group(1), m.group(2)
            if url not in overused:
                return m.group(0)
            seen_url[url] = seen_url.get(url, 0) + 1
            if seen_url[url] == 1:
                return m.group(0)
            src = pick_source(line, {url})
            if not src:
                return m.group(0)
            fixes += 1
            wm = re.search(r"\[([^\]]+)\]", src["weave"].format(url=src["url"]))
            return f"[{wm.group(1) if wm else src['label']}]({src['url']})"

        out.append(LINK_RE.sub(repl, line))
    return "".join(out), fixes


def fix_typos(text: str) -> str:
    return text.replace(
        "(manual sample, 2024–2026—not a formal crawl), ere is what",
        "(manual sample, 2024–2026—not a formal crawl), here is what",
    )


def main() -> int:
    total = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            fixed, n = fix_duplicates(text)
            fixed = fix_typos(fixed)
            if n or fixed != text:
                art.write_text(fixed, encoding="utf-8")
                total += n
                if n:
                    print(f"  {art.parent.name}: {n} semantic fixes")
    print(f"Semantic citation fixes: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
