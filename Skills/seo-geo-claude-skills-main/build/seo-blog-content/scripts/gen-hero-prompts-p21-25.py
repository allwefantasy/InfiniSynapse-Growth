#!/usr/bin/env python3
"""Write prompts/cover.prompt for each P21-25 article (English, no-text rule)."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLAR_PALETTE = {
    "pillar21": "deep navy (#0c1117) and sky blue (#38bdf8) accents — data analysis fundamentals",
    "pillar22": "deep indigo (#1e1b4b) and violet (#a78bfa) accents — advanced analysis methods",
    "pillar23": "dark teal (#0f2e2a) and emerald (#34d399) accents — analytics tools and software",
    "pillar24": "charcoal (#1c1917) and amber (#f59e0b) accents — data analyst careers",
    "pillar25": "midnight blue (#1e1b4b) and periwinkle (#818cf8) accents — learning and certification",
}

NO_TEXT = """Strict no-text rule: ABSOLUTELY no text, no letters, no numbers, no digits, no year stamps, no glyphs, no symbols, no characters, no logos, no watermarks, no UI labels, no captions, no scribbles, no faux handwriting, no Chinese/Japanese/Korean characters, no document panels, no browser windows, no speech bubbles, no title bars, no fake paragraphs, no dashboard mockups, no step labels, no flowchart words, no title banners, no blog headers. Pure abstract visual illustration only — charts as wordless geometric shapes (bars, dots, lines) with no axis labels, never readable content."""

STYLE = (
    "Style: modern editorial vector illustration for a professional tech blog hero, "
    "soft gradients, clean infographic aesthetic, subtle glow, slight depth, "
    "16:9 composition with breathing room, no photorealistic faces, no stock-photo cliches."
)


def subject_from_alt(alt: str) -> str:
    # Strip title-like / UI-inviting phrases from alt text.
    alt = re.sub(
        r"\b(20\d{2}|excel|tableau|microsoft|toolpak|dialog|dashboard|"
        r"template|certificate|bootcamp|course|courses|salary|resume|"
        r"interview|software|platform|toolpak)\b",
        "",
        alt,
        flags=re.I,
    )
    alt = re.sub(r"\s+", " ", alt).strip()
    return (
        "Minimal wordless abstract composition: soft gradient background, "
        "glowing geometric primitives only (circles, bars, curves, dots), "
        "faceless silhouettes at most — absolutely no screens, panels, or interfaces. "
        "Mood: "
        + (alt[:80] or "data analytics")
    )


def build_prompt(alt: str, pillar_key: str) -> str:
    palette = PILLAR_PALETTE.get(pillar_key[:8], PILLAR_PALETTE["pillar21"])
    subject = subject_from_alt(alt)
    return f"""# Auto-generated hero prompt for OpenOctopus imagen-4
# Regenerate: python3 Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/gen-hero-prompts-p21-25.py

A cinematic editorial blog hero illustration about data analytics.

Subject: {subject}

{NO_TEXT}

Color palette: {palette}.

{STYLE}
"""


def main() -> int:
    n = 0
    for pillar in sorted(BLOG.glob("pillar2[1-5]-*")):
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
