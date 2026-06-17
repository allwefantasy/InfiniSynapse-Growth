#!/usr/bin/env python3
"""Sync cover.prompt subject + v5 suffix across all 13 articles."""
from pathlib import Path

PILLAR = Path(__file__).resolve().parent
SUFFIX = (PILLAR / "_prompt-style-suffix.txt").read_text().strip()

SUBJECTS = {
    "001-ai-for-data-analysis": (
        "Flowing connected nodes and smooth arcs in soft blue-purple gradient, "
        "dual paths converging toward a single glowing focal point, right-weighted cluster."
    ),
    "002-data-agent-manifesto": (
        "Ascending geometric arrow built from triangles and circles, soft blue-to-purple "
        "gradient trail, sparse constellation nodes, upward momentum on the right."
    ),
    "003-what-is-a-data-agent": (
        "Layered rounded rectangles and thin connecting curves in blue-purple gradient, "
        "pipeline flow metaphor using pure shapes only, focal cluster on the right."
    ),
    "004-ai-native-data-platform": (
        "Five vertical translucent pillars on a floating platform layer, soft isometric "
        "depth, blue and violet accent edges, generous empty area on the left."
    ),
    "005-best-agentic-analytics": (
        "Six vertical translucent prisms of varying heights in two loose clusters, "
        "soft perspective grid, blue-purple gradient on the taller cluster, right side."
    ),
    "006-autonomous-data-agent": (
        "Circular lifecycle ring of geometric arc segments with a small purple feedback "
        "loop, soft central orb, empty calm area on the left third."
    ),
    "007-ai-data-analyst": (
        "Abstract split: pale gray geometric circle zone left, flowing agent pipeline "
        "nodes in blue-purple right, thin luminous vertical divider — no human figure."
    ),
    "008-ai-data-analyst-job-description": (
        "Overlapping translucent disks and diamond facets in a loose lattice pattern, "
        "blue-purple accent glow on three focal shapes, calm empty area on the left."
    ),
    "009-data-agent-memory": (
        "Left: fading ghost layers of translucent rounded squares. Right: single glowing "
        "structured card silhouette with five empty geometric field slots, no writing."
    ),
    "010-fabric-data-agent-vs-copilot": (
        "Two parallel translucent platform stacks, left shorter cool gray-blue, right "
        "taller with purple accent layers, minimal abstract geometry without brand marks."
    ),
    "011-ai-native-vs-augmented-analytics": (
        "Soft Venn diagram: large pale blue circle with smaller nested purple-teal circle "
        "and five inner pillar dots, airy white background, empty left area."
    ),
    "012-ai-data-analysis": (
        "Seven connected hexagon nodes in horizontal pipeline, gradient brightness "
        "increasing rightward, thin blue-purple connecting lines, right-weighted."
    ),
    "013-data-agent-glossary": (
        "Hub-and-spoke constellation: central glowing node with two rings of smaller "
        "orbiting circles, thin connection lines, blue-purple on white, right cluster."
    ),
}

for slug, subject in SUBJECTS.items():
    prompt_path = PILLAR / slug / "prompts" / "cover.prompt"
    num = slug.split("-")[0]
    title = slug.replace(f"{num}-", "").replace("-", " ")
    body = f"{subject}\n\n{SUFFIX}\n"
    content = f"# {num} {title} — abstract geometric cover v5\n\n{body}"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(content)
    print(f"✓ {prompt_path.relative_to(PILLAR)}")
