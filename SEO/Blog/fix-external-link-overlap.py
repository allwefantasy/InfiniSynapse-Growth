#!/usr/bin/env python3
"""Diversify external citations so pairwise URL overlap stays <= 30%."""
from __future__ import annotations

import importlib.util
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

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

TARGET_LINKS = 10
MAX_OVERLAP = 0.30

_hdr_spec = importlib.util.spec_from_file_location("hdr", BLOG / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_hdr_spec)
assert _hdr_spec and _hdr_spec.loader
_hdr_spec.loader.exec_module(_hdr)

_ext_spec = importlib.util.spec_from_file_location("ext", BLOG / "audit-external-links.py")
_ext = importlib.util.module_from_spec(_ext_spec)
assert _ext_spec and _ext_spec.loader
_ext_spec.loader.exec_module(_ext)

_ov_spec = importlib.util.spec_from_file_location("ov", BLOG / "audit-external-link-overlap.py")
_ov = importlib.util.module_from_spec(_ov_spec)
assert _ov_spec and _ov_spec.loader
_ov_spec.loader.exec_module(_ov)

LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def max_allowed_shared(k: int) -> int:
    return int(MAX_OVERLAP * k)


def pick_trial(slug: str, pool: list[dict], k: int, seed: int) -> list[dict]:
    order = sorted(
        range(len(pool)),
        key=lambda i: hashlib.sha256(f"{slug}:{seed}:{i}".encode()).hexdigest(),
    )
    picks: list[dict] = []
    seen: set[str] = set()
    for i in order:
        src = pool[i]
        key = norm(src["url"])
        if key in seen:
            continue
        seen.add(key)
        picks.append(src)
        if len(picks) == k:
            break
    return picks


def greedy_assign(slugs: list[str], pool: list[dict], k: int) -> dict[str, list[dict]]:
    assignments: dict[str, set[str]] = {}
    out: dict[str, list[dict]] = {}
    usage: Counter[str] = Counter()
    max_shared = max_allowed_shared(k)

    for slug in slugs:
        best: list[dict] | None = None
        best_score = -10**12
        for seed in range(800):
            trial_sources = pick_trial(slug, pool, k, seed)
            trial = {norm(s["url"]) for s in trial_sources}
            ok = True
            worst = 0.0
            for other, urls in assignments.items():
                inter = len(trial & urls)
                if inter > max_shared:
                    ok = False
                    break
                rate = overlap_rate(trial, urls)
                worst = max(worst, rate)
            if not ok:
                continue
            score = -worst * 10_000 - sum(usage[u] for u in trial)
            if score > best_score:
                best_score = score
                best = trial_sources
        if not best:
            best = pick_trial(slug, pool, k, 999)
        out[slug] = best
        assignments[slug] = {norm(s["url"]) for s in best}
        for u in assignments[slug]:
            usage[u] += 1
    return out


def external_link_matches(text: str) -> list[re.Match[str]]:
    out = []
    for m in LINK_RE.finditer(text):
        if "infinisynapse" not in m.group(2).lower():
            out.append(m)
    return out


def _line_at(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def _body_tail_start(text: str, ratio: float = 0.85) -> tuple[int, int]:
    """Return (body_start_line_1based, tail_start_line_1based within body)."""
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body_start_line = _line_at(text, m.start()) if m else 1
    body_lines = text[m.start() :].splitlines() if m else text.splitlines()
    return body_start_line, int(len(body_lines) * ratio)


def _weave_insert_points(text: str, count: int) -> list[int]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body_start = m.start() if m else 0
    body_lines = text[body_start:].splitlines()
    tail_line = int(len(body_lines) * 0.75)
    headings: list[int] = []
    char_pos = body_start
    for i, line in enumerate(body_lines):
        if i <= tail_line and line.startswith("## ") and not line.startswith("## TL;DR"):
            headings.append(char_pos + len(line) + 1)
        char_pos += len(line) + 1
    if not headings:
        return [body_start] * count
    if len(headings) >= count:
        step = max(1, len(headings) // count)
        return [headings[i * step] for i in range(count)]
    out = headings[:]
    while len(out) < count:
        out.append(headings[len(out) % len(headings)])
    return out


def _head_tail_url_sets(text: str) -> tuple[set[str], set[str]]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    body_start = _line_at(text, m.start()) if m else 1
    body_lines = body.splitlines()
    tail_start = int(len(body_lines) * 0.85)
    head: set[str] = set()
    tail: set[str] = set()
    for i, line in enumerate(body_lines):
        zone = tail if (i + 1) >= tail_start else head
        for _, url in LINK_RE.findall(line):
            if "infinisynapse" in url.lower():
                continue
            zone.add(norm(url))
    return head, tail


def _ensure_head_coverage(text: str, target_by_norm: dict[str, dict]) -> str:
    head, tail = _head_tail_url_sets(text)
    tail_only = tail - head
    if len(tail_only) < 2:
        return text
    pool_by_norm = {norm(s["url"]): s for s in _hdr.HIGH_DR_SOURCES}
    to_mirror = sorted(tail_only)
    for src_key, pos in zip(to_mirror, reversed(_weave_insert_points(text, len(to_mirror)))):
        src = target_by_norm.get(src_key) or pool_by_norm.get(src_key)
        if not src:
            continue
        block = src["weave"].format(url=src["url"]) + "\n\n"
        text = text[:pos] + block + text[pos:]
    return text


def enforce_target_set_url_only(text: str, target_sources: list[dict]) -> str:
    """Replace external link URLs to match assignment; keep anchor labels."""
    if not target_sources:
        return text
    urls = [s["url"] for s in target_sources]
    matches = sorted(external_link_matches(text), key=lambda m: m.start())
    if not matches:
        return text
    for m, url in reversed(list(zip(matches, urls[: len(matches)]))):
        label = m.group(1)
        repl = f"[{label}]({url})"
        text = text[: m.start()] + repl + text[m.end() :]
    return text


def enforce_target_set(text: str, target_sources: list[dict]) -> str:
    if not target_sources:
        return text
    target_by_norm = {norm(s["url"]): s for s in target_sources}
    target_keys = [norm(s["url"]) for s in target_sources]
    matches = external_link_matches(text)
    body_start_line, tail_start = _body_tail_start(text)

    head_matches = sorted(
        [
            m
            for m in matches
            if (_line_at(text, m.start()) - body_start_line + 1) < tail_start
        ],
        key=lambda m: m.start(),
    )
    tail_matches = sorted(
        [m for m in matches if m not in head_matches],
        key=lambda m: m.start(),
    )
    ordered = head_matches + tail_matches

    queue = list(target_keys)
    for m in reversed(ordered):
        pick = queue.pop(0) if queue else target_keys[0]
        src = target_by_norm[pick]
        repl = f"[{src['label']}]({src['url']})"
        text = text[: m.start()] + repl + text[m.end() :]

    present = {norm(u) for u in _ext.external_links(text)}
    missing = [target_by_norm[k] for k in target_keys if k not in present]
    if missing:
        for src, pos in zip(missing, reversed(_weave_insert_points(text, len(missing)))):
            block = src["weave"].format(url=src["url"]) + "\n\n"
            text = text[:pos] + block + text[pos:]

    return _ensure_head_coverage(text, target_by_norm)


def repair_assignments(slugs: list[str], assignments: dict[str, list[dict]], pool: list[dict], k: int) -> dict[str, list[dict]]:
    max_shared = max_allowed_shared(k)
    for _ in range(80):
        sets = {s: {norm(x["url"]) for x in assignments[s]} for s in slugs}
        worst = None
        for i, a in enumerate(slugs):
            for b in slugs[i + 1 :]:
                inter = len(sets[a] & sets[b])
                if inter > max_shared or overlap_rate(sets[a], sets[b]) > MAX_OVERLAP:
                    rate = overlap_rate(sets[a], sets[b])
                    if not worst or rate > worst[0]:
                        worst = (rate, a, b, inter)
        if not worst:
            break
        _, a, b, _ = worst
        # Re-roll assignment for slug `b`
        forbidden = sets[a]
        for seed in range(1000):
            trial = pick_trial(b, pool, k, 10_000 + seed)
            trial_set = {norm(s["url"]) for s in trial}
            if len(trial_set & forbidden) > max_shared:
                continue
            ok = True
            for other in slugs:
                if other == b:
                    continue
                if len(trial_set & sets[other]) > max_shared:
                    ok = False
                    break
            if ok:
                assignments[b] = trial
                break
    return assignments


def main() -> int:
    url_only = "--url-only" in sys.argv
    articles: list[tuple[Path, str]] = []
    for pillar in PILLARS:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            articles.append((art, art.parent.name))

    slugs = [s for _, s in articles]
    pool = _hdr.HIGH_DR_SOURCES
    changed = 0
    violations: list = []
    for round_i in range(20):
        assignments = greedy_assign(slugs, pool, TARGET_LINKS)
        assignments = repair_assignments(slugs, assignments, pool, TARGET_LINKS)
        round_changed = 0
        for art, slug in articles:
            text = art.read_text(encoding="utf-8")
            if url_only:
                new_text = enforce_target_set_url_only(text, assignments[slug])
            else:
                new_text = enforce_target_set(text, assignments[slug])
                target_by_norm = {norm(s["url"]): s for s in assignments[slug]}
                new_text = _ensure_head_coverage(new_text, target_by_norm)
            if new_text != text:
                art.write_text(new_text, encoding="utf-8")
                round_changed += 1
        changed += round_changed
        violations = _ov.audit_pairs(_ov.collect_articles(PILLARS))
        print(f"Round {round_i + 1}: changed {round_changed}, violations {len(violations)}")
        if not violations:
            break

    print(f"\nUpdated {changed} article writes total")
    print(f"Remaining overlap violations: {len(violations)}")
    if violations:
        for rate, a, b, inter, denom in violations[:15]:
            print(f"  {rate:.0%} {a} vs {b} ({inter}/{denom})")
        return 1
    print("All pairs <= 30% overlap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
