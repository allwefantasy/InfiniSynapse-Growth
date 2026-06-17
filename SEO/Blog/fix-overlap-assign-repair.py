#!/usr/bin/env python3
"""Repair greedy URL assignments to 0 pairwise violations, then apply URL-only swaps."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

BLOG = Path(__file__).parent

_fix_spec = importlib.util.spec_from_file_location("fix_ov", BLOG / "fix-external-link-overlap.py")
_fix = importlib.util.module_from_spec(_fix_spec)
assert _fix_spec and _fix_spec.loader
_fix_spec.loader.exec_module(_fix)

_ov_spec = importlib.util.spec_from_file_location("ov", BLOG / "audit-external-link-overlap.py")
_ov = importlib.util.module_from_spec(_ov_spec)
assert _ov_spec and _ov_spec.loader
_ov_spec.loader.exec_module(_ov)

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def external_matches(text: str) -> list[re.Match[str]]:
    out = []
    for m in LINK_RE.finditer(text):
        if "infinisynapse" not in m.group(2).lower():
            out.append(m)
    return out


def apply_url_only(text: str, sources: list[dict]) -> str:
    if not sources:
        return text
    urls = [s["url"] for s in sources]
    matches = sorted(external_matches(text), key=lambda m: m.start())
    if not matches:
        return text
    pairs = list(zip(matches, urls[: len(matches)]))
    for m, url in reversed(pairs):
        label = m.group(1)
        repl = f"[{label}]({url})"
        text = text[: m.start()] + repl + text[m.end() :]
    return text


MAX_OVERLAP = 0.30
K = 10


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def assignment_sets(assign: dict[str, list[dict]]) -> dict[str, set[str]]:
    return {s: {norm(x["url"]) for x in assign[s]} for s in assign}


def worst_pair(sets: dict[str, set[str]]) -> tuple[float, str, str] | None:
    slugs = list(sets.keys())
    worst = None
    for i, a in enumerate(slugs):
        for b in slugs[i + 1 :]:
            rate = overlap_rate(sets[a], sets[b])
            if rate > MAX_OVERLAP and (worst is None or rate > worst[0]):
                worst = (rate, a, b)
    return worst


def pool_by_norm(pool: list[dict]) -> dict[str, dict]:
    return {norm(s["url"]): s for s in pool}


def repair_assignments_hard(
    slugs: list[str],
    assign: dict[str, list[dict]],
    pool: list[dict],
    max_iter: int = 5000,
) -> dict[str, list[dict]]:
    pbn = pool_by_norm(pool)
    sets = assignment_sets(assign)

    for _ in range(max_iter):
        wp = worst_pair(sets)
        if not wp:
            return assign
        rate, a, b = wp
        shared = list(sets[a] & sets[b])
        if not shared:
            continue
        old = shared[0]
        target_slug = a if len(sets[a]) >= len(sets[b]) else b
        partner = b if target_slug == a else a
        partner_set = sets[partner]
        target_set = sets[target_slug]

        replacement = None
        for src in pool:
            u = norm(src["url"])
            if u in target_set or u in partner_set:
                continue
            trial = (target_set - {old}) | {u}
            ok = True
            for other, oset in sets.items():
                if other == target_slug:
                    continue
                if overlap_rate(trial, oset) > MAX_OVERLAP:
                    ok = False
                    break
            if ok:
                replacement = src
                break
        if not replacement:
            continue

        new_list = []
        replaced = False
        for src in assign[target_slug]:
            if norm(src["url"]) == old and not replaced:
                new_list.append(replacement)
                replaced = True
            else:
                new_list.append(src)
        assign[target_slug] = new_list
        sets = assignment_sets(assign)

    return assign


def main() -> int:
    articles: list[tuple[Path, str]] = []
    for pillar in _fix.PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            articles.append((art, art.parent.name))

    slugs = [s for _, s in articles]
    pool = _fix._hdr.HIGH_DR_SOURCES

    before = len(_ov.audit_pairs(_ov.collect_articles(_fix.PILLARS)))
    print(f"Article violations before: {before}")

    assign = _fix.greedy_assign(slugs, pool, K)
    assign = _fix.repair_assignments(slugs, assign, pool, K)
    av = worst_pair(assignment_sets(assign))
    print(f"Assignment violations after greedy+repair: {av[0] if av else 0:.0%}")

    assign = repair_assignments_hard(slugs, assign, pool)
    av2 = worst_pair(assignment_sets(assign))
    print(f"Assignment violations after hard repair: {av2[0] if av2 else 0:.0%}")

    changed = 0
    for art, slug in articles:
        text = art.read_text(encoding="utf-8")
        new = apply_url_only(text, assign[slug])
        if new != text:
            art.write_text(new, encoding="utf-8")
            changed += 1

    after = len(_ov.audit_pairs(_ov.collect_articles(_fix.PILLARS)))
    print(f"Applied to {changed} articles | Article violations after: {after}")

    if after:
        import subprocess

        subprocess.run([sys.executable, str(BLOG / "fix-overlap-surgical.py"), "500"], check=False)
        after = len(_ov.audit_pairs(_ov.collect_articles(_fix.PILLARS)))
        print(f"After surgical: {after}")

    return 0 if after == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
