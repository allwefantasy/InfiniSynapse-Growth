#!/usr/bin/env python3
"""Write prompts/cover.prompt for each P26-30 article (English, no-text rule)."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR_PALETTE = {
    "pillar26": "deep teal (#0e1e26) and aqua (#2dd4bf) accents — data governance and quality",
    "pillar27": "deep violet (#1a1230) and orchid (#a855f7) accents — master data and metadata",
    "pillar28": "midnight navy (#0a182c) and cobalt (#3b82f6) accents — data engineering and pipelines",
    "pillar29": "dark cyan (#082028) and sky (#22d3ee) accents — warehouse, lake, and lakehouse",
    "pillar30": "deep magenta (#220818) and rose (#f472b6) accents — analytics and visualization",
}

NO_TEXT = """Strict no-text rule: ABSOLUTELY no text, no letters, no numbers, no digits, no year stamps, no glyphs, no symbols, no characters, no logos, no watermarks, no UI labels, no captions, no scribbles, no faux handwriting, no Chinese/Japanese/Korean characters, no document panels, no browser windows, no speech bubbles, no title bars, no fake paragraphs, no dashboard mockups, no step labels, no flowchart words, no title banners, no blog headers. Pure abstract visual illustration only — charts as wordless geometric shapes (bars, dots, lines) with no axis labels, never readable content."""

STYLE = (
    "Style: modern editorial vector illustration for a professional tech blog hero, "
    "soft gradients, clean infographic aesthetic, subtle glow, slight depth, "
    "16:9 composition with breathing room, no photorealistic faces, no stock-photo cliches."
)


def subject_from_alt(alt: str) -> str:
    alt = re.sub(
        r"\b(20\d{2}|snowflake|databricks|azure|tableau|microsoft|aws|"
        r"dashboard|template|certificate|bootcamp|course|courses|salary|"
        r"software|platform|toolpak)\b",
        "",
        alt,
        flags=re.I,
    )
    alt = re.sub(r"\s+", " ", alt).strip()
    return (
        "Minimal wordless abstract composition: soft gradient background, "
        "glowing geometric primitives only (circles, bars, curves, dots, nodes, flows), "
        "faceless silhouettes at most — absolutely no screens, panels, or interfaces. "
        "Mood: "
        + (alt[:100] or "enterprise data")
    )


def build_prompt(alt: str, pillar_key: str) -> str:
    palette = PILLAR_PALETTE.get(pillar_key[:8], PILLAR_PALETTE["pillar26"])
    subject = subject_from_alt(alt)
    return f"""# Auto-generated hero prompt for OpenOctopus imagen-4
# Regenerate: python3 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/gen-hero-prompts-p26-30.py

A cinematic editorial blog hero illustration about enterprise data and analytics.

Subject: {subject}

{NO_TEXT}

Color palette: {palette}.

{STYLE}
"""


def main() -> int:
    n = 0
    pillars = sorted(BLOG.glob("pillar2[6-9]-*")) + sorted(BLOG.glob("pillar30-*"))
    for pillar in pillars:
        key = pillar.name[:8]
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            m = re.search(r"!\[([^\]]*)\]\(\./images/([^)]+)\)", text)
            if not m:
                continue
            alt = m.group(1)
            prompt_dir = art.parent / "prompts"
            prompt_dir.mkdir(parents=True, exist_ok=True)
            (prompt_dir / "cover.prompt").write_text(
                build_prompt(alt, key), encoding="utf-8"
            )
            n += 1
    print(f"Wrote {n} prompts/cover.prompt files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
