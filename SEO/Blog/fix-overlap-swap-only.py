#!/usr/bin/env python3
"""Swap-only external link overlap fix — replaces existing links, never inserts weave blocks."""
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

LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")


def external_link_matches(text: str) -> list[re.Match[str]]:
    out = []
    for m in LINK_RE.finditer(text):
        if "infinisynapse" not in m.group(2).lower():
            out.append(m)
    return out


def enforce_swap_only(text: str, target_sources: list[dict]) -> str:
    if not target_sources:
        return text
    target_by_norm = {_fix.norm(s["url"]): s for s in target_sources}
    target_keys = [_fix.norm(s["url"]) for s in target_sources]
    matches = external_link_matches(text)
    if not matches:
        return text
    # Replace from the end; assign targets in order, cycling if fewer targets than links.
    queue = list(target_keys)
    for m in reversed(matches):
        pick = queue.pop(0) if queue else target_keys[len(matches) % len(target_keys)]
        src = target_by_norm[pick]
        repl = f"[{src['label']}]({src['url']})"
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

    for round_i in range(12):
        assignments = _fix.greedy_assign(slugs, pool, k)
        assignments = _fix.repair_assignments(slugs, assignments, pool, k)
        round_changed = 0
        for art, slug in articles:
            text = art.read_text(encoding="utf-8")
            new_text = enforce_swap_only(text, assignments[slug])
            if new_text != text:
                art.write_text(new_text, encoding="utf-8")
                round_changed += 1
        violations = _ov.audit_pairs(_ov.collect_articles(_fix.PILLARS))
        print(f"Round {round_i + 1}: changed {round_changed}, violations {len(violations)}")
        if not violations:
            print("All pairs <= 30% overlap")
            return 0

    violations = _ov.audit_pairs(_ov.collect_articles(_fix.PILLARS))
    print(f"\nRemaining violations: {len(violations)}")
    for rate, a, b, inter, denom in violations[:15]:
        print(f"  {rate:.0%} {a} vs {b} ({inter}/{denom})")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
