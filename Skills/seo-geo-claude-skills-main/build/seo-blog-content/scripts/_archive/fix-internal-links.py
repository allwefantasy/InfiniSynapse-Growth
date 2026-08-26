#!/usr/bin/env python3
"""Remove Related Reading / list-weave blocks; embed cluster links contextually."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

BLOG = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("reg", BLOG / "cluster-link-registry.py")
_reg = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_reg)

_weave_spec = importlib.util.spec_from_file_location("weave", BLOG / "contextual-internal-weave.py")
_weave = importlib.util.module_from_spec(_weave_spec)
assert _weave_spec and _weave_spec.loader
_weave_spec.loader.exec_module(_weave)


def remove_related_reading(text: str) -> str:
    text = re.sub(
        r"^## Conclusion \+ Related Reading\s*$",
        "## Conclusion",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^## Final Verdict \+ Related Reading\s*$",
        "## Final Verdict",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"\n## Related Reading\n.*?(?=\n---\s*\n|\Z)",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\n\*\*Pillar \d+ cluster — read next\*\*:\s*\n(?:- .+\n)+",
        "\n",
        text,
    )
    text = re.sub(
        r"^-\s+For related workflow depth, see \[[^\]]+\]\(/blog/[^)]+\)\.\s*\n",
        "",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^-\s+For (foundational context|workflow patterns|adjacent depth|connector setup|evaluation criteria|platform comparisons|tooling options|architecture and memory), (see|read|review|explore) \[[^\]]+\]\(/blog/[^)]+\)[^\n]*\n",
        "",
        text,
        flags=re.M,
    )
    text = re.sub(r"^\d+\. \[Related Reading\]\(#related-reading\)\s*\n", "", text, flags=re.M)
    text = re.sub(r"^\d+\. \[Related reading\]\(#related-reading\)\s*\n", "", text, flags=re.M)
    text = re.sub(
        r"^(\d+\. \[Conclusion) \+ Related Reading\]\(#conclusion--related-reading\)\s*$",
        r"\1](#conclusion)",
        text,
        flags=re.M,
    )
    text = re.sub(
        r"^(\d+\. \[Final Verdict) \+ Related Reading\]\(#final-verdict--related-reading\)\s*$",
        r"\1](#final-verdict)",
        text,
        flags=re.M,
    )
    return text


def internal_slugs_in_body(text: str) -> set[str]:
    slugs: set[str] = set()
    for m in re.finditer(r"\[([^\]]+)\]\(/blog/([^)]+)\)", text):
        slugs.add(m.group(2).strip("/"))
    return slugs


def process_article(path: Path, cluster: dict) -> bool:
    folder = path.parent.name
    original = path.read_text(encoding="utf-8")
    text = remove_related_reading(original)
    text = _weave.normalize_internal_prose(text)
    reqs = _reg.required_internal_urls(folder, cluster)
    seed_base = sum(ord(c) for c in folder) % 997
    used: set[int] = set()
    for i, (title, url) in enumerate(reqs):
        if url.replace("/blog/", "") not in internal_slugs_in_body(text):
            text, used = _weave.embed_link(text, title, url, seed_base + i, used)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    clusters = _reg.all_clusters()
    changed = 0
    for pillar_name, cluster in clusters.items():
        pillar_dir = BLOG / pillar_name
        for art in sorted(pillar_dir.glob("[0-9][0-9][0-9]-*/article.md")):
            if process_article(art, cluster):
                changed += 1
                print(f"fixed: {art.parent.name}")
    print(f"\nUpdated {changed} articles")


if __name__ == "__main__":
    main()
