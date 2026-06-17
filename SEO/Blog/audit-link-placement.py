#!/usr/bin/env python3
"""Detect external links clustered at article tail instead of narrative body."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

BLOG = Path(__file__).parent
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

TAIL_MARKERS = re.compile(
    r"^##\s+(Sources|Reference|References|Further reading|Bibliography|Citations)\s*$",
    re.I,
)
BARE_BULLET = re.compile(
    r"^-\s+\*\*([^*]+)\*\*:\s+(https?://\S+|\[https?://)",
    re.I,
)


def is_external(url: str) -> bool:
    return "infinisynapse" not in urlparse(url).netloc.lower()


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def link_lines(text: str) -> list[tuple[int, str, str]]:
    """Return (line_no, url, line) for external links."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for _, url in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", line):
            if is_external(url):
                out.append((i, url, line.strip()))
        for url in re.findall(r"(?<!\()https?://[^\s)>]+", line):
            if is_external(url):
                out.append((i, url, line.strip()))
    return out


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails: list[str] = []
    lines = text.splitlines()
    total = len(lines)

    if TAIL_MARKERS.search(text, re.M):
        fails.append("standalone tail section (Sources/References)")

    for i, line in enumerate(lines, 1):
        if BARE_BULLET.match(line.strip()):
            fails.append(f"L{i}: bare label:URL bullet")

    body = body_from_tldr(text)
    body_lines = body.splitlines()
    body_total = len(body_lines)

    # Links only in last 15% of body (after conclusion/related reading)
    ext_links = link_lines(body)
    if not ext_links:
        return fails

    tail_start = int(body_total * 0.85)
    tail_links = [x for x in ext_links if x[0] >= tail_start]
    head_links = [x for x in ext_links if x[0] < tail_start]

    unique_tail = {u for _, u, _ in tail_links}
    unique_head = {u for _, u, _ in head_links}
    tail_only = unique_tail - unique_head

    if len(tail_only) >= 2:
        fails.append(f"{len(tail_only)} external URLs appear only in last 15% of body")

    # Block: 3+ external links in last 30 lines with <2 in first half
    last_30 = {u for ln, u, _ in ext_links if ln > total - 30}
    first_half = {u for ln, u, _ in ext_links if ln < total // 2}
    if len(last_30) >= 3 and len(first_half) < 2:
        fails.append(f"{len(last_30)} external links in final 30 lines, sparse in first half")

    # Evaluation basis only pattern
    narrative = "\n".join(
        ln
        for ln in body_lines
        if not ln.strip().startswith("> **Evaluation basis**")
    )
    narr_urls = {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", narrative) if is_external(u)}
    eval_urls = set()
    for ln in body_lines:
        if ln.strip().startswith("> **Evaluation"):
            for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", ln):
                if is_external(u):
                    eval_urls.add(u)
    if eval_urls and len(narr_urls - eval_urls) < 3:
        fails.append("most external links only in Evaluation basis block")

    return fails


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = fail_n = 0
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            fails = audit(art)
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
