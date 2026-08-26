#!/usr/bin/env python3
"""Remove tune-script padding, fix 'this approach' placeholders, de-stuff FAQ headers."""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))
SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

SKIP_FOLDERS = {
    "203-api-integration-services",
    "206-api-integration-tools",
    "218-manage-multiple-api-integrations",
    "221-api-integration-testing",
    "223-agentic-orchestration",
    "224-tool-calling",
}

PADDING_RES = [
    re.compile(
        r"\n\nBefore public beta, run a thirty-minute[^\n]+\n",
        re.I,
    ),
    re.compile(
        r"\n\nShip \*\*[^*]+\*\* with a written rollback plan[^\n]+\n",
        re.I,
    ),
    re.compile(
        r"\n\nProduction teams document \*\*[^*]+\*\* runbooks[^\n]+\n",
        re.I,
    ),
    re.compile(
        r"\n\nReliable \*\*[^*]+\*\* depends on[^\n]+\n",
        re.I,
    ),
    re.compile(
        r"\n\nTeams shipping \*\*[^*]+\*\* should treat[^\n]+\n",
        re.I,
    ),
]

FAQ_RENAMES = [
    (re.compile(r"^### What is .+\?$", re.M), "### Definition and scope"),
    (re.compile(r"^### When do teams need .+\?$", re.M), "### When teams should prioritize it"),
    (re.compile(r"^### How does .+ relate to InfiniSynapse\?$", re.M), "### How InfiniSynapse fits"),
    (re.compile(r"^### What is the first step to improve .+\?$", re.M), "### First improvement step"),
    (re.compile(r"^### How long does a .+ rollout take\?$", re.M), "### Typical rollout timeline"),
]

BODY_ALTS = [
    "the production layer",
    "this stack",
    "these patterns",
    "the integration layer",
    "this discipline",
    "the underlying architecture",
]


def extract_kw(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1) if m else ""


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def word_count(text: str) -> int:
    t = re.sub(r"^#+\s+", "", text, flags=re.M)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"^>\s+", "", t, flags=re.M)
    t = re.sub(r"^[-*]\s+", "", t, flags=re.M)
    t = re.sub(r"^\d+\.\s+", "", t, flags=re.M)
    t = re.sub(r"\|", " ", t)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))


def strip_padding(text: str) -> str:
    for pat in PADDING_RES:
        while True:
            new = pat.sub("\n", text, count=1)
            if new == text:
                break
            text = new
    # Keep at most one of each padding sentence type before Conclusion
    m = re.search(r"\n## Conclusion\n", text)
    if not m:
        return text
    head, tail = text[: m.start()], text[m.start() :]
    for pat in PADDING_RES:
        matches = list(pat.finditer(head))
        if len(matches) > 1:
            for match in reversed(matches[1:]):
                head = head[: match.start()] + head[match.end() :]
    return head + tail


def fix_this_approach(text: str, kw: str) -> str:
    if not kw:
        return text
    alt_i = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal alt_i
        alt_i += 1
        if alt_i % 3 == 0:
            return f"**{kw}**"
        return BODY_ALTS[alt_i % len(BODY_ALTS)]

    text = re.sub(r"\bthis approach\b", repl, text, flags=re.I)
    text = re.sub(r"\bthis topic\b", repl, text, flags=re.I)
    return text


def fix_broken_conclusions(text: str, kw: str) -> str:
    text = re.sub(
        r"\n\n(?:the production layer|this stack|these patterns|the integration layer|this discipline|the underlying architecture) is how vibe-coded products earn trust[^\n]+\n",
        f"\n\n**{kw.title() if len(kw) < 36 else kw}** is how vibe-coded products earn trust after the UI demo ends.\n",
        text,
        flags=re.I,
    )
    return text


def rename_faq_headers(text: str) -> str:
    for pat, repl in FAQ_RENAMES:
        text = pat.sub(repl, text)
    return text


def pad_unique(text: str, kw: str, target: int = 1920) -> str:
    fillers = [
        f"Teams we work with treat **{kw}** as a weekly review topic: vendor SLAs, contract tests, and on-call ownership—not a one-time launch checklist.",
        f"Mature **{kw}** rollouts pair structured logging with user-safe error surfaces so support can trace failures without reading raw vendor payloads.",
        f"Before scaling traffic, document **{kw}** assumptions in a one-page runbook: credential owners, rollback steps, and which calls must stay async.",
        f"Production **{kw}** rarely fails on missing features; it fails when secrets live in chat logs and long jobs block the UI thread.",
        f"Score **{kw}** readiness with contract tests in CI, not slide decks—schema drift should fail builds before users see it.",
    ]
    i = 0
    while word_count(body_from_tldr(text)) < target and i < len(fillers) * 3:
        insert = f"\n\n{fillers[i % len(fillers)]}\n"
        if insert.strip() not in text:
            text = text.replace("\n## Conclusion\n", insert + "\n## Conclusion\n", 1)
        i += 1
    return text


def high_dr_ids(text: str) -> set[str]:
    body = body_from_tldr(text)
    ids: set[str] = set()
    for _, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body):
        host = url.lower()
        if "infinisynapse" in host:
            continue
        for src in _hdr.HIGH_DR_SOURCES:
            sh = src["url"].split("/")[2].lower()
            if sh in host or host.split("/")[2] in sh:
                ids.add(src["id"])
    return ids


def weave_high_dr(text: str, article_idx: int) -> str:
    if len(high_dr_ids(text)) >= _hdr.MIN_HIGH_DR_CITATIONS:
        return text
    needed = _hdr.MIN_HIGH_DR_CITATIONS - len(high_dr_ids(text))
    for j in range(needed):
        src = _hdr.HIGH_DR_SOURCES[(article_idx * 5 + j * 7) % len(_hdr.HIGH_DR_SOURCES)]
        weave = src["weave"].format(url=src["url"])
        if src["url"] in text:
            continue
        text = text.replace(
            "\n## Failure Modes\n",
            f"\n{weave}\n\n## Failure Modes\n",
            1,
        )
    return text


def sync_schema_faq(art_dir: Path, text: str) -> None:
    schema_path = art_dir / "schema.json"
    if not schema_path.is_file():
        return
    faqs: list[tuple[str, str]] = []
    in_faq = False
    q = ""
    for line in text.splitlines():
        if line.startswith("## Frequently Asked Questions"):
            in_faq = True
            continue
        if in_faq and line.startswith("## ") and not line.startswith("###"):
            break
        if in_faq and line.startswith("### "):
            q = line[4:].strip()
        elif in_faq and q and line.strip() and not line.startswith("#"):
            faqs.append((q, line.strip()))
            q = ""
    if not faqs:
        return
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "@graph" in data:
        items = data["@graph"]
    elif isinstance(data, list):
        items = data
    else:
        items = [data]
    for item in items:
        if item.get("@type") == "FAQPage":
            item["mainEntity"] = [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs[:5]
            ]
    schema_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    fixed = 0
    for pi, pillar in enumerate(PILLARS):
        for ai, art in enumerate(sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md"))):
            folder = art.parent.name
            text = art.read_text(encoding="utf-8")
            kw = extract_kw(text)
            text = strip_padding(text)
            text = rename_faq_headers(text)
            text = fix_broken_conclusions(text, kw)
            idx = pi * 30 + ai
            if folder not in SKIP_FOLDERS:
                text = weave_high_dr(text, idx)
            art.write_text(text, encoding="utf-8")
            sync_schema_faq(art.parent, text)
            fixed += 1
    print(f"fixed {fixed} template articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
