#!/usr/bin/env python3
"""Diversify external citations for Pillars 26–30: ≥5 high-DR hosts, ≤30% URL overlap.

Target: 10 unique high-DR URLs per article, ≥5 distinct hosts, pairwise overlap ≤30%.
Updates anchors to match assigned sources and weaves any missing citations into the body.
"""
from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

SCRIPTS = Path(__file__).resolve().parent
BLOG = SCRIPTS.parents[4] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))

TARGET_LINKS = 10
MAX_OVERLAP = 0.30
MIN_HOSTS = 5

LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")


def norm(url: str) -> str:
    return url.rstrip("/").lower()


def host_of(url: str) -> str:
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def safe_weave(src: dict) -> str:
    """Neutral weaves — avoid agent/NL2SQL jargon that mismatches governance/viz topics."""
    url = src["url"]
    label = src["label"]
    host = host_of(url)
    if "wikipedia.org" in host:
        return (
            f"Core definitions remain usefully summarized in [{label}]({url}) "
            "for shared vocabulary across stakeholders."
        )
    if any(x in host for x in ("nist.gov", "iso.org", "cisa.gov", "ncsc.gov", "ftc.gov", "europa.eu", "oecd.ai")):
        return (
            f"Governance and risk expectations are framed by [{label}]({url}) "
            "when programs need an external control reference."
        )
    if any(
        x in host
        for x in ("docs.", "learn.microsoft", "cloud.google", "aws.amazon", "apache.org", "kubernetes.io")
    ):
        return (
            f"Implementation details are commonly grounded in [{label}]({url}) "
            "when teams translate concepts into production practice."
        )
    if any(x in host for x in ("ibm.com", "databricks.com", "snowflake.com", "microsoft.com")):
        return (
            f"Architecture choices are often checked against [{label}]({url}) "
            "so boundaries, ownership, and scale patterns stay explicit."
        )
    return (
        f"Teams evaluating this topic often cross-check [{label}]({url}) "
        "for a durable, vendor-neutral reference point."
    )


def hint_score(src: dict, article_text_lower: str) -> int:
    """article_text_lower must already be lowercased."""
    score = 0
    for hint in src.get("hints") or []:
        # hints are simple regex fragments; prefer substring for speed
        token = hint.replace(r"\b", "").replace(".", " ").strip().lower()
        if token and token in article_text_lower:
            score += 2
    for token in re.findall(r"[a-z]{4,}", src.get("label", "").lower()):
        if token in article_text_lower:
            score += 1
    return score


def precompute_scores(pool: list[dict], article_text: str) -> list[tuple[int, dict]]:
    low = article_text.lower()
    return [(hint_score(s, low), s) for s in pool]


def strip_prior_weaves(text: str, pool: list[dict]) -> str:
    """Remove previously injected weave paragraphs so re-assignment can re-weave cleanly."""
    markers = []
    for s in pool:
        w = s.get("weave", "")
        # first ~40 chars of weave without the link are distinctive
        head = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", w.split("{url}")[0])
        head = head.strip()[:48]
        if len(head) >= 24:
            markers.append(head)
    # Also strip our SAFE_WEAVE openings
    markers.extend(
        [
            "Teams evaluating this topic often cross-check",
            "Implementation details are commonly grounded in",
            "Core definitions remain usefully summarized in",
            "Governance and risk expectations are framed by",
            "Architecture choices are often checked against",
            "Operational security reviews should cross-check",
            "Secure AI rollouts should reference the",
            "EU-facing teams map control expectations using the",
            "Warehouse vendors describe governed NL2SQL",
            "Adoption benchmarks in the",
            "The move from dashboard-first BI to augmented",
            "Production rollouts should align access",
            "Multi-source connector design should follow",
            "LLM-backed analytics should account for",
            "Enterprise AI adoption guidance in",
            "Operational maturity for analytics agents aligns",
            "Regulated rollouts often anchor access reviews",
            "Analytics uptime improves when teams borrow",
            "Leaderboard scores on the",
            "The BIRD benchmark adds dirty-schema",
        ]
    )
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        drop = False
        if stripped and any(stripped.startswith(m) for m in markers):
            # only drop if the line contains an external http link
            if "http" in stripped and "infinisynapse" not in stripped.lower():
                drop = True
        if drop:
            i += 1
            # skip following blank
            if i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1
    # collapse 3+ blanks
    text2 = "\n".join(out)
    text2 = re.sub(r"\n{4,}", "\n\n\n", text2)
    return text2 if text2.endswith("\n") else text2 + "\n"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


_hdr = _load("hdr", SCRIPTS / "high-dr-authority-sources.py")
_ext = _load("ext", SCRIPTS / "audit-external-links.py")
_ov = _load("ov", SCRIPTS / "audit-external-link-overlap.py")
_hdr_audit = _load("hdr_audit", SCRIPTS / "audit-high-dr-links.py")


def overlap_rate(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def max_allowed_shared(k: int) -> int:
    return int(MAX_OVERLAP * k)


def dedupe_pool(sources: list[dict]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for s in sources:
        key = norm(s["url"])
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def pick_trial(slug: str, pool: list[dict], k: int, seed: int) -> list[dict]:
    """Hash-shuffled pick with host diversity. Overlap constraints applied by caller."""
    order = sorted(
        range(len(pool)),
        key=lambda i: hashlib.sha256(f"{slug}:{seed}:{i}".encode()).hexdigest(),
    )
    picks: list[dict] = []
    hosts: set[str] = set()
    urls: set[str] = set()
    for prefer_new_host in (True, False):
        for i in order:
            src = pool[i]
            u = norm(src["url"])
            h = host_of(src["url"])
            if u in urls:
                continue
            if prefer_new_host and h in hosts and len(hosts) < MIN_HOSTS:
                continue
            picks.append(src)
            hosts.add(h)
            urls.add(u)
            if len(picks) == k:
                return picks
    return picks


def greedy_assign(slugs: list[str], pool: list[dict], k: int) -> dict[str, list[dict]]:
    assignments: dict[str, set[str]] = {}
    out: dict[str, list[dict]] = {}
    usage: Counter[str] = Counter()
    max_shared = max_allowed_shared(k)

    for idx, slug in enumerate(slugs):
        if idx % 25 == 0:
            print(f"  assigning {idx + 1}/{len(slugs)}...", flush=True)
        best: list[dict] | None = None
        best_score = -10**12
        for seed in range(2000):
            trial_sources = pick_trial(slug, pool, k, seed)
            if len(trial_sources) < k:
                continue
            if len({host_of(s["url"]) for s in trial_sources}) < MIN_HOSTS:
                continue
            trial = {norm(s["url"]) for s in trial_sources}
            ok = True
            worst = 0.0
            for urls in assignments.values():
                inter = len(trial & urls)
                if inter > max_shared:
                    ok = False
                    break
                worst = max(worst, overlap_rate(trial, urls))
            if not ok:
                continue
            score = -worst * 10_000 - sum(usage[u] for u in trial)
            if score > best_score:
                best_score = score
                best = trial_sources
        if not best:
            best = pick_trial(slug, pool, k, 0)
        out[slug] = best
        assignments[slug] = {norm(s["url"]) for s in best}
        for u in assignments[slug]:
            usage[u] += 1
    return out


def repair_assignments(
    slugs: list[str], assignments: dict[str, list[dict]], pool: list[dict], k: int
) -> dict[str, list[dict]]:
    max_shared = max_allowed_shared(k)
    sets = {s: {norm(x["url"]) for x in assignments[s]} for s in slugs}
    for _ in range(300):
        worst = None
        for i, a in enumerate(slugs):
            for b in slugs[i + 1 :]:
                inter = len(sets[a] & sets[b])
                rate = overlap_rate(sets[a], sets[b])
                if inter > max_shared or rate > MAX_OVERLAP:
                    if not worst or rate > worst[0]:
                        worst = (rate, a, b)
        if not worst:
            break
        _, a, b = worst
        forbidden = sets[a]
        found = False
        for seed in range(4000):
            trial = pick_trial(b, pool, k, 50_000 + seed)
            if len(trial) < k or len({host_of(s["url"]) for s in trial}) < MIN_HOSTS:
                continue
            trial_set = {norm(s["url"]) for s in trial}
            if len(trial_set & forbidden) > max_shared:
                continue
            if all(len(trial_set & sets[o]) <= max_shared for o in slugs if o != b):
                assignments[b] = trial
                sets[b] = trial_set
                found = True
                break
        if not found:
            common = list(sets[a] & sets[b])
            if not common:
                break
            drop = common[0]
            candidates = [
                s
                for s in pool
                if norm(s["url"]) not in sets[b] and norm(s["url"]) not in forbidden
            ]
            candidates.sort(key=lambda s: sum(1 for o in slugs if norm(s["url"]) in sets[o]))
            for s in candidates:
                newset = (sets[b] - {drop}) | {norm(s["url"])}
                if len(newset) < k:
                    continue
                if all(len(newset & sets[o]) <= max_shared for o in slugs if o != b):
                    news = []
                    for x in assignments[b]:
                        if norm(x["url"]) == drop:
                            news.append(s)
                        else:
                            news.append(x)
                    seen: set[str] = set()
                    news2: list[dict] = []
                    for x in news:
                        u = norm(x["url"])
                        if u in seen:
                            continue
                        seen.add(u)
                        news2.append(x)
                    assignments[b] = news2[:k]
                    sets[b] = {norm(x["url"]) for x in assignments[b]}
                    found = True
                    break
            if not found:
                break
    return assignments


def _line_at(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def _body_tail_start(text: str, ratio: float = 0.85) -> tuple[int, int]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body_start_line = _line_at(text, m.start()) if m else 1
    body_lines = text[m.start() :].splitlines() if m else text.splitlines()
    return body_start_line, int(len(body_lines) * ratio)


def _weave_insert_points(text: str, count: int) -> list[int]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body_start = m.start() if m else 0
    body_lines = text[body_start:].splitlines()
    # Stay in first 75% of body; skip Conclusion/FAQ
    cutoff_markers = ("## Conclusion", "## Frequently Asked Questions", "## FAQ")
    cutoff_line = int(len(body_lines) * 0.75)
    for i, line in enumerate(body_lines):
        if any(line.startswith(m) for m in cutoff_markers):
            cutoff_line = min(cutoff_line, i)
            break
    headings: list[int] = []
    char_pos = body_start
    for i, line in enumerate(body_lines):
        if i < cutoff_line and line.startswith("## ") and not line.startswith("## TL;DR"):
            headings.append(char_pos + len(line) + 1)
        char_pos += len(line) + 1
    if not headings:
        return [body_start] * count
    if len(headings) >= count:
        step = max(1, len(headings) // count)
        return [headings[min(i * step, len(headings) - 1)] for i in range(count)]
    out = headings[:]
    while len(out) < count:
        out.append(headings[len(out) % len(headings)])
    return out


def external_link_matches(text: str) -> list[re.Match[str]]:
    out = []
    for m in LINK_RE.finditer(text):
        if "infinisynapse" not in m.group(2).lower():
            out.append(m)
    return out


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
            block = safe_weave(src) + "\n\n"
            text = text[:pos] + block + text[pos:]
    return text


def main() -> int:
    dry = "--dry-run" in sys.argv
    articles: list[tuple[Path, str]] = []
    for pillar in PILLARS:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            articles.append((art, art.parent.name))

    slugs = [s for _, s in articles]
    pool = dedupe_pool(_hdr.HIGH_DR_SOURCES)
    print(f"Articles: {len(slugs)} | Pool URLs: {len(pool)} | Target links: {TARGET_LINKS}")

    # Strip prior auto-weaves so we can re-embed cleanly
    for art, slug in articles:
        raw = art.read_text(encoding="utf-8")
        cleaned = strip_prior_weaves(raw, pool)
        if not dry and cleaned != raw:
            art.write_text(cleaned, encoding="utf-8")

    assignments = greedy_assign(slugs, pool, TARGET_LINKS)
    assignments = repair_assignments(slugs, assignments, pool, TARGET_LINKS)

    # Pre-check overlap on assignments
    sets = {s: {norm(x["url"]) for x in assignments[s]} for s in slugs}
    viol = 0
    for i, a in enumerate(slugs):
        for b in slugs[i + 1 :]:
            if overlap_rate(sets[a], sets[b]) > MAX_OVERLAP:
                viol += 1
    print(f"Assignment overlap violations: {viol}")

    changed = 0
    if not dry:
        for art, slug in articles:
            text = art.read_text(encoding="utf-8")
            new_text = enforce_target_set(text, assignments[slug])
            if new_text != text:
                art.write_text(new_text, encoding="utf-8")
                changed += 1
        print(f"Wrote {changed} articles")

    # Post-audit
    targets = [p for p in PILLARS if p.is_dir()]
    articles_map = _ov.collect_articles(targets)
    violations = _ov.audit_pairs(articles_map)
    print(f"Overlap violations after write: {len(violations)}")
    if violations:
        for rate, a, b, inter, denom in violations[:15]:
            print(f"  {rate:.0%} {a} vs {b} ({inter}/{denom})")

    hdr_fail = 0
    for art, slug in articles:
        fails = _hdr_audit.audit_file(art)
        if fails:
            hdr_fail += 1
            if hdr_fail <= 10:
                print(f"  high-DR fail {slug}: {fails[:3]}")
    print(f"High-DR audit fails: {hdr_fail}/{len(articles)}")

    # Quantity
    qty_fail = 0
    for art, slug in articles:
        n = len(_ext.external_links(art.read_text(encoding="utf-8")))
        if n < 5:
            qty_fail += 1
            print(f"  qty fail {slug}: {n}")
    print(f"Quantity <5 fails: {qty_fail}/{len(articles)}")

    return 1 if violations or hdr_fail or qty_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
