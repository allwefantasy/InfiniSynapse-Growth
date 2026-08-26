#!/usr/bin/env python3
"""Fix remaining internal-link and high-DR audit gaps for vibe series."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hdr", SCRIPTS / "high-dr-authority-sources.py")
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

HUB_FOLDERS = {
    "203-api-integration-services": "pillar18-api-integration-vibe-built",
    "223-agentic-orchestration": "pillar19-tool-calling-agent-workflows",
    "243-professional-data-api": "pillar20-data-api-production-readiness",
    "263-vibe-coding-tools": "pillar17-vibe-coding-stack",
    "283-vibe-coding-best-practices": "pillar16-vibe-coding-workflow",
}

COMMA_CHAIN_FIXES = {
    "283-vibe-coding-best-practices": (
        "Pair these rituals with [Vibe Coding Checklist](/en/blog/vibe-coding-checklist-reddit), [Vibe Coding Security](/en/blog/vibe-coding-security-reddit), and [How to Vibe Code](/en/blog/how-to-vibe-code-reddit) for tactical depth.",
        "Pair these rituals with [Vibe Coding Checklist](/en/blog/vibe-coding-checklist-reddit). "
        "For security depth see [Vibe Coding Security](/en/blog/vibe-coding-security-reddit). "
        "For day-one workflow see [How to Vibe Code](/en/blog/how-to-vibe-code-reddit).",
    ),
    "263-vibe-coding-tools": (
        "Explore cluster depth in [Best Vibe Coding Tools](/en/blog/best-vibe-coding-tool-reddits-reddit), [Replit Vibe Coding](/en/blog/replit-vibe-coding-reddit), and [Lovable Vibe Coding](/en/blog/lovable-vibe-coding-reddit).",
        "Explore cluster depth in [Best Vibe Coding Tools](/en/blog/best-vibe-coding-tool-reddits-reddit). "
        "Compare [Replit Vibe Coding](/en/blog/replit-vibe-coding-reddit) for hosted stacks. "
        "See [Lovable Vibe Coding](/en/blog/lovable-vibe-coding-reddit) for rapid UI iteration.",
    ),
    "243-professional-data-api": (
        "For implementation depth see [Production Readiness Checklist](/en/blog/production-readiness-reddit-checklist), [API Data Governance](/en/blog/api-data-governance-reddit), and [Dataset API](/en/blog/dataset-api-reddit).",
        "For implementation depth see [Production Readiness Checklist](/en/blog/production-readiness-reddit-checklist). "
        "Governance patterns live in [API Data Governance](/en/blog/api-data-governance-reddit). "
        "Structured exports are covered in [Dataset API](/en/blog/dataset-api-reddit).",
    ),
}

HUB_CLUSTER_BLURBS = {}


def hub_cluster_blurb(pillar: str, hub_folder: str) -> str:
    reg = json.loads((BLOG / pillar / "articles_registry.json").read_text(encoding="utf-8"))
    lines = ["\n## Cluster Navigation\n"]
    for art in reg["articles"]:
        if art["folder"] == hub_folder:
            continue
        title = art["keyword"].title()
        lines.append(f"- [{title}](/en/blog/{art['slug']})")
    lines.append("")
    return "\n".join(lines)

HIGH_DR_EXTRA = {
    "204-integration-software": [0, 2, 3, 4, 6],
    "218-manage-multiple-api-integrations": [1, 3, 5, 7, 9],
    "221-api-integration-testing": [2, 4, 6, 8, 10],
    "223-agentic-orchestration": [0, 3, 5, 7, 9],
    "224-tool-calling": [1, 4, 6, 8, 11],
}


def add_high_dr(art: Path, indices: list[int]) -> None:
    text = art.read_text(encoding="utf-8")
    for j, idx in enumerate(indices):
        src = _hdr.HIGH_DR_SOURCES[idx % len(_hdr.HIGH_DR_SOURCES)]
        weave = src["weave"].format(url=src["url"])
        if src["url"] in text:
            continue
        anchor = "\n## Failure Modes\n" if j == 0 else "\n## Frequently Asked Questions\n"
        if anchor in text:
            text = text.replace(anchor, f"\n{weave}\n{anchor}", 1)
    art.write_text(text, encoding="utf-8")


def main() -> int:
    for folder, (old, new) in COMMA_CHAIN_FIXES.items():
        for art in BLOG.rglob(f"{folder}/article.md"):
            text = art.read_text(encoding="utf-8")
            if old in text:
                art.write_text(text.replace(old, new), encoding="utf-8")
                print(f"fixed comma chain {folder}")

    for folder, pillar in HUB_FOLDERS.items():
        art = BLOG / pillar / folder / "article.md"
        if not art.is_file():
            continue
        blurb = hub_cluster_blurb(pillar, folder)
        text = art.read_text(encoding="utf-8")
        if "## Cluster Navigation\n" in text:
            text = re.sub(r"\n## Cluster Navigation\n[\s\S]*?(?=\n## Frequently Asked Questions\n)", "\n", text)
        text = text.replace("\n## Frequently Asked Questions\n", blurb + "\n## Frequently Asked Questions\n", 1)
        art.write_text(text, encoding="utf-8")
        print(f"added hub cluster links {folder}")

    for folder, indices in HIGH_DR_EXTRA.items():
        art = next(BLOG.rglob(f"{folder}/article.md"), None)
        if art:
            add_high_dr(art, indices)
            print(f"added high-DR {folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
