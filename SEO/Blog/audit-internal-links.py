#!/usr/bin/env python3
"""Audit cluster internal links by page role (Pillar Page vs Cluster Page)."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

BLOG = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("reg", BLOG / "cluster-link-registry.py")
_reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_reg)

RELATED_PAT = re.compile(
    r"## Related Reading|## Conclusion \+ Related Reading|## Final Verdict \+ Related Reading|"
    r"For related workflow depth, see|\*\*Pillar \d+ cluster — read next\*\*|"
    r"Within this topic cluster|To continue in this cluster|For adjacent depth in the same cluster|"
    r"as you operationalize this workflow|when you extend this workflow across the cluster|"
    r"for the surrounding workflow context",
    re.I,
)

COMMA_BLOG_CHAIN = re.compile(
    r"\[[^\]]+\]\(/blog/[^)]+\),\s*(?:\[[^\]]+\]\(/blog/[^)]+\),?\s*)+(?:and\s+)?\[[^\]]+\]\(/blog/",
    re.I,
)


def slugs_in_prose(text: str) -> set[str]:
    slugs: set[str] = set()
    for _, slug in re.findall(r"\[([^\]]+)\]\(/blog/([^)]+)\)", text):
        slugs.add(slug.strip("/"))
    return slugs


def audit(path: Path, cluster: dict) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails: list[str] = []
    folder = path.parent.name

    if RELATED_PAT.search(text):
        fails.append("Related Reading block or template bullets still present")

    for line in text.splitlines():
        if COMMA_BLOG_CHAIN.search(line):
            fails.append("comma-chained internal link list in one clause")
            break

    present = slugs_in_prose(text)
    reqs = _reg.required_internal_urls(folder, cluster)
    missing = [u for _, u in reqs if u.replace("/blog/", "") not in present]
    role = _reg.page_role(folder, cluster)

    if role == "pillar_page":
        other_hubs = [pf for pf in cluster["pillar_pages"] if pf != folder]
        for pf in other_hubs:
            slug = cluster["articles"][pf]["slug"]
            if slug not in present:
                fails.append(f"missing pillar-page link: /blog/{slug}")
        if len(cluster["pillar_pages"]) == 1:
            need = len(cluster["folders"]) - 1
            have = len(present & {cluster["articles"][f]["slug"] for f in cluster["folders"] if f != folder})
            if have < need:
                fails.append(f"hub missing cluster links ({have}/{need})")
    else:
        hub_slug = cluster["articles"][cluster["primary_hub"]]["slug"]
        if hub_slug not in present:
            fails.append(f"missing primary hub link: /blog/{hub_slug}")
        cluster_slugs = {
            cluster["articles"][f]["slug"]
            for f in cluster["folders"]
            if f not in cluster["pillar_pages"] and f != folder
        }
        linked_cluster = len(present & cluster_slugs)
        if linked_cluster < 2:
            fails.append(f"cluster page needs >=2 sibling links (has {linked_cluster})")

    for _, u in reqs:
        if u.replace("/blog/", "") not in present:
            fails.append(f"missing required link: {u}")

    return fails


def main() -> int:
    clusters = _reg.all_clusters()
    total = fail_n = 0
    for pillar_name, cluster in clusters.items():
        print(f"\n{pillar_name}")
        for art in sorted((BLOG / pillar_name).glob("[0-9][0-9][0-9]-*/article.md")):
            fails = audit(art, cluster)
            total += 1
            ok = not fails
            if not ok:
                fail_n += 1
            print(f"  {art.parent.name:<45} {'✓' if ok else '✗'}")
            for f in fails[:4]:
                print(f"      · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
