#!/usr/bin/env python3
"""Strict external-link audit: every outbound link must use descriptive anchor text in prose."""
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

BAD_ANCHOR = re.compile(
    r"^https?://|^www\.|\.(com|cn|org|io|edu|gov)/?$|^[a-z0-9.-]+\.(com|cn|io|org)$",
    re.I,
)


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def is_external(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return bool(host) and "infinisynapse" not in host


def audit_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails: list[str] = []

    if re.search(r"^## Sources\s*$", text, re.M):
        fails.append("standalone ## Sources section")

    body = body_from_tldr(text)
    links = re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", text)

    for anchor, url in links:
        if not is_external(url):
            continue
        a = anchor.strip()
        if BAD_ANCHOR.search(a) or a.lower() == url.lower():
            fails.append(f"naked/URL anchor: [{a[:40]}]({url[:50]})")
        if a.lower().startswith("http"):
            fails.append(f"URL used as anchor: {url[:60]}")

    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^-\s+[^:]+:\s+\[https?://", s):
            fails.append("bullet exposes external URL")
        if re.match(r"^-\s+\[https?://", s):
            fails.append("bullet is bare external URL")
        if re.match(r"^\*\*Product entry\*\*:\s+\[", s):
            fails.append("standalone Product entry link line")

    # External link must appear inside a sentence (>= 8 words on line, or blockquote)
    for anchor, url in links:
        if not is_external(url):
            continue
        found_prose = False
        for line in body.splitlines():
            if url not in line and anchor not in line:
                continue
            if line.strip().startswith("|") or line.strip().startswith("!["):
                continue
            if line.strip().startswith("#"):
                continue
            words = len(re.findall(r"[a-zA-Z0-9]+", line))
            if words >= 8 or line.strip().startswith(">"):
                found_prose = True
                break
        if not found_prose:
            fails.append(f"link not in prose sentence: [{anchor[:30]}]({url[:40]})")

    return fails


def eval_only_urls(text: str) -> set[str]:
    body = body_from_tldr(text)
    narrative = "\n".join(
        ln
        for ln in body.splitlines()
        if not ln.strip().startswith("> **Evaluation basis**")
    )
    in_narr = {u for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", narrative) if is_external(u)}
    eval_text = "\n".join(
        ln for ln in body.splitlines() if ln.strip().startswith("> **Evaluation")
    )
    return {
        u
        for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", eval_text)
        if is_external(u) and u not in in_narr
    }


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
            text = art.read_text(encoding="utf-8")
            fails = audit_file(art)
            orphan = eval_only_urls(text)
            if orphan:
                fails.append(f"{len(orphan)} external link(s) only in Evaluation basis block")
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails[:5]:
                print(f"      · {f}")
            if len(fails) > 5:
                print(f"      · ... +{len(fails)-5} more")
    print(f"\nTotal: {total} | Pass: {total-fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
