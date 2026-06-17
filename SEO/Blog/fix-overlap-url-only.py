#!/usr/bin/env python3
"""Greedy overlap reassignment — swap external URLs only, preserve anchor text. No weave inserts."""
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


def main() -> int:
    articles: list[tuple[Path, str]] = []
    for pillar in _fix.PILLARS:
        if not pillar.is_dir():
            continue
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            articles.append((art, art.parent.name))

    slugs = [s for _, s in articles]
    pool = _fix._hdr.HIGH_DR_SOURCES
    k = _fix.TARGET_LINKS

    before = len(_ov.audit_pairs(_ov.collect_articles(_fix.PILLARS)))
    print(f"Violations before: {before}")

    violations: list = []
    total_changed = 0
    for round_i in range(12):
        assignments = _fix.greedy_assign(slugs, pool, k)
        assignments = _fix.repair_assignments(slugs, assignments, pool, k)
        round_changed = 0
        for art, slug in articles:
            text = art.read_text(encoding="utf-8")
            new_text = apply_url_only(text, assignments[slug])
            if new_text != text:
                art.write_text(new_text, encoding="utf-8")
                round_changed += 1
        total_changed += round_changed
        violations = _ov.audit_pairs(_ov.collect_articles(_fix.PILLARS))
        print(f"Round {round_i + 1}: changed {round_changed}, violations {len(violations)}")
        if not violations:
            break

    if violations:
        print("Running surgical cleanup...")
        import subprocess

        subprocess.run([sys.executable, str(BLOG / "fix-overlap-surgical.py"), "400"], check=False)
        violations = _ov.audit_pairs(_ov.collect_articles(_fix.PILLARS))

    print(f"\nTotal writes: {total_changed} | Final violations: {len(violations)}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
