#!/usr/bin/env python3
"""Boost body keyword density using planning-table core keyword (Pillar 16–20).

Reddit GEO keeps `{core} reddit` in H1 / meta / slug / Direct answer.
Body prose should weave **{core}** at ~1.0–1.35% (minimum **1.0%** per audit gate).
"""
from __future__ import annotations

import csv
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

_gate = SCRIPTS / "tune-vibe-audit-gates.py"
exec(compile(_gate.read_text(encoding="utf-8").split("def main")[0], str(_gate), "exec"))

WEAVES = [
    "Teams evaluating **{core}** should score auth hygiene, schema validation, and observability before feature checklists.",
    "Production **{core}** rollouts start by inventorying external dependencies—not by polishing UI copy alone.",
    "Most month-two incidents trace back to skipped **{core}** basics: secret storage, contract tests, and async routing.",
    "Buyers comparing vendors on **{core}** should ask for audit trails and failure replay—not demo latency alone.",
    "A focused **{core}** pilot—one workflow, structured logging, contract tests—beats a broad rewrite.",
    "Document **{core}** ownership in the runbook: who rotates credentials and who watches vendor status pages.",
    "Treat **{core}** contract tests as release gates—schema drift should fail CI before users see it.",
    "Assign an on-call owner for **{core}** vendor failures before you invite beta traffic.",
]


def load_plan() -> dict[str, str]:
    out: dict[str, str] = {}
    with PLAN.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            out[row["编号"].strip()] = row["关键词"].strip().lower()
    return out


PLAN_KW = load_plan()


def article_id(art_path: Path) -> str:
    return art_path.parent.name[:3]


def core_keyword(aid: str, full_kw: str) -> str:
    core = PLAN_KW.get(aid, "")
    if not core:
        return full_kw
    if core in SKIP_REDDIT or full_kw.lower() == core:
        return full_kw
    if full_kw.lower() == f"{core} reddit":
        return core
    return full_kw


def target_core_count(wc: int, core: str) -> int:
    lo, hi = density_bounds(core)
    # Aim mid-high healthy band (~1.05–1.25%), never below floor.
    aim = min(hi - 0.08, max(1.05, (lo + hi) / 2 + 0.15))
    return max(int(wc * aim / 100), int(wc * lo / 100) + 1)


def split_direct_answer(body: str) -> tuple[str, str, str]:
    """Return (prefix, direct_answer_block, rest)."""
    m = re.search(
        r"(^> \*\*Direct answer:\*\*.*?)(?=\n(?!>)|\Z)",
        body,
        re.M | re.S,
    )
    if not m:
        return body, "", ""
    start, end = m.start(), m.end()
    return body[:start], body[start:end], body[end:]


def replace_full_with_core(text: str, full: str, core: str) -> str:
    if full.lower() == core.lower():
        return text

    def repl_bold(m: re.Match[str]) -> str:
        return f"**{core}**"

    text = re.sub(
        r"\*\*" + re.escape(full) + r"\*\*",
        repl_bold,
        text,
        flags=re.I,
    )
    # Case-insensitive plain phrase (longest first).
    pat = re.compile(re.escape(full), re.I)
    return pat.sub(core, text)


def insert_weaves(text: str, core: str, need: int, aid: str) -> str:
    if need <= 0:
        return text
    anchor = "\n## Conclusion\n"
    if anchor not in text:
        anchor = "\n## Frequently Asked Questions\n"
    if anchor not in text:
        return text
    chunks: list[str] = []
    idx = int(aid) if aid.isdigit() else 0
    for i in range(need):
        wc = word_count(extract_body_raw(text))
        if wc >= 2760:
            break
        tpl = WEAVES[(idx + i) % len(WEAVES)]
        line = tpl.format(core=core)
        if line in text:
            continue
        chunks.append(f"\n\n{line}\n")
    if not chunks:
        return text
    return text.replace(anchor, "".join(chunks) + anchor, 1)


def should_boost(aid: str, full: str, text: str) -> bool:
    core = core_keyword(aid, full)
    if core == full:
        return False
    raw = extract_body_raw(text)
    wc = word_count(raw)
    kc = kw_count(raw, core)
    den = kc / wc * 100 if wc else 0
    full_den = kw_count(raw, full) / wc * 100 if wc else 0
    tgt = target_core_count(wc, core)
    lo, hi = density_bounds(core)
    # User-requested band on full phrase, or core below healthy target.
    if 0.6 <= full_den < 1.0:
        return True
    if kc < tgt or den < lo:
        return True
    # 4–5 word cores: nudge if stuck below 1.0% when full phrase was the metric.
    if len(core.split()) >= 4 and full_den < 1.0 and den < 1.0:
        return True
    return False


def boost_article(text: str, aid: str, full: str) -> str:
    core = core_keyword(aid, full)
    if core == full:
        return text

    body_m = re.search(r"^## TL;DR\s*$", text, re.M)
    if not body_m:
        return text
    head = text[: body_m.start()]
    body = text[body_m.start() :]

    prefix, direct, rest = split_direct_answer(body)
    rest = replace_full_with_core(rest, full, core)
    body = prefix + direct + rest

    weaves_added = False
    for _ in range(40):
        raw = extract_body_raw(head + body)
        wc = word_count(raw)
        kc = kw_count(raw, core)
        tgt = target_core_count(wc, core)
        lo, hi = density_bounds(core)
        den = kc / wc * 100 if wc else 0
        if lo <= den <= hi and kc >= min(tgt, int(wc * 1.0 / 100)):
            break
        if wc > 2800:
            body = re.sub(
                r"\n\n(?:Teams evaluating|Mature|Production|Most month-two|Buyers comparing|A focused|Document|Treat|Assign) \*\*[^*]+\*\*[^\n]+\n",
                "\n",
                body,
                count=1,
            )
            continue
        if kc < tgt and not weaves_added and wc < 2760:
            body = insert_weaves(body, core, min(tgt - kc, 8), aid)
            weaves_added = True
            continue
        if den > hi:
            body = re.sub(
                r"\*\*" + re.escape(core) + r"\*\*",
                "this stack",
                body,
                count=1,
                flags=re.I,
            )
            continue
        break

    return head + body


def main() -> int:
    touched = boosted = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            aid = article_id(art)
            text = art.read_text(encoding="utf-8")
            m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
            if not m:
                continue
            full = m.group(1).strip()
            if not should_boost(aid, full, text):
                continue
            new = boost_article(text, aid, full)
            if new != text:
                art.write_text(new, encoding="utf-8")
                touched += 1
            core = core_keyword(aid, full)
            raw = extract_body_raw(new)
            wc = word_count(raw)
            kc = kw_count(raw, core)
            den = kc / wc * 100 if wc else 0
            lo, hi = density_bounds(core)
            ok = lo <= den <= hi
            if ok:
                boosted += 1
            print(
                f"[{aid}] {art.parent.name}: core `{core}` "
                f"{kc}x {den:.2f}% (band {lo}-{hi}%) {'OK' if ok else 'CHECK'}"
            )
    print(f"\nboosted {boosted}/{touched} articles to core density band")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
