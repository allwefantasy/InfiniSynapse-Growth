#!/usr/bin/env python3
"""Scan P21-25 hero PNGs for readable text artifacts (Tesseract + heuristics)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
TESSERACT = "/opt/homebrew/bin/tesseract"

# Domain + common imagen text leakage patterns.
KEYWORDS = {
    "data", "analysis", "analytics", "analyst", "analy", "analytic", "analyist",
    "analyics", "analysics", "analysics", "excel", "tableau", "python", "sql",
    "bootcamp", "certification", "certificate", "course", "courses", "salary",
    "resume", "interview", "career", "blog", "hero", "guide", "process", "method",
    "methods", "technique", "techniques", "diagnostic", "predictive", "prescriptive",
    "descriptive", "exploratory", "qualitative", "quantitative", "survey", "spatial",
    "bayesian", "financial", "software", "platform", "tool", "tools", "microsoft",
    "office", "toolpak", "toolpak", "internship", "junior", "senior", "entry",
    "remote", "jobs", "market", "training", "learning", "online", "free", "define",
    "collect", "clean", "interpret", "communicate", "research", "question",
}

# Phrases that indicate real UI/title text even when OCR is garbled.
PHRASE_PATTERNS = [
    r"data\s+anal",
    r"blog\s+hero",
    r"no\s*text",
    r"strict",
    r"absol",
    r"pure\s+no",
    r"in\s+2026",
    r"for\s+2026",
    r"what\s+is",
    r"how\s+to",
    r"job\s+desc",
    r"salary",
    r"certif",
    r"bootcamp",
    r"tableau",
    r"microsoft\s+excel",
    r"toolpak",
]


def ocr_image(path: Path) -> str:
    try:
        out = subprocess.run(
            [TESSERACT, str(path), "stdout", "-l", "eng", "--psm", "6"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        sys.exit("tesseract not found — brew install tesseract")
    if out.returncode != 0:
        return ""
    return out.stdout.strip()


def score_text(text: str) -> tuple[int, list[str]]:
    """Return (score, reasons). Higher = more likely real readable text."""
    reasons: list[str] = []
    score = 0
    lower = text.lower()

    for pat in PHRASE_PATTERNS:
        if re.search(pat, lower):
            score += 3
            reasons.append(f"phrase:{pat}")

    words = re.findall(r"[a-zA-Z]{3,}", lower)
    kw_hits = [w for w in words if any(k in w for k in KEYWORDS)]
    if kw_hits:
        score += min(len(set(kw_hits)), 5)
        reasons.append(f"keywords:{','.join(sorted(set(kw_hits))[:6])}")

    for line in text.splitlines():
        line = line.strip()
        if len(line) < 8:
            continue
        alpha = sum(c.isalpha() for c in line)
        ratio = alpha / max(len(line), 1)
        # Long, mostly-alphabetic line — likely a title or label.
        if len(line) >= 18 and ratio >= 0.55:
            score += 2
            reasons.append(f"long_line:{line[:50]}")
        # Year stamps imagen often adds.
        if re.search(r"\b20[12][0-9]\b", line):
            score += 2
            reasons.append("year_stamp")

    # Multiple distinct word-like tokens on one line.
    for line in text.splitlines():
        tokens = re.findall(r"[a-zA-Z]{4,}", line)
        if len(tokens) >= 3:
            score += 2
            reasons.append(f"multi_word:{line[:50]}")
            break

    return score, reasons


def main() -> int:
    threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    flagged: list[dict] = []
    clean = 0
    missing = 0

    for art in sorted(BLOG.glob("pillar2[1-5]-*/[0-9][0-9][0-9]-*/article.md")):
        text = art.read_text(encoding="utf-8")
        m = re.search(r"!\[[^\]]*\]\(\./images/([^)]+)\)", text)
        if not m:
            continue
        img = art.parent / "images" / m.group(1)
        name = art.parent.name
        if not img.is_file():
            missing += 1
            print(f"MISSING {name}")
            continue

        raw = ocr_image(img)
        score, reasons = score_text(raw)
        if score >= threshold:
            flagged.append({
                "name": name,
                "score": score,
                "reasons": reasons,
                "ocr_sample": " | ".join(
                    ln.strip() for ln in raw.splitlines() if ln.strip()
                )[:200],
            })
            print(f"FLAG {name} score={score}")
            for r in reasons[:4]:
                print(f"  {r}")
        else:
            clean += 1

    print(f"\nSummary: clean={clean} flagged={len(flagged)} missing={missing} threshold={threshold}")

    out = Path(__file__).resolve().parent / "_archive/p21-25/hero-text-flags.json"
    out.write_text(json.dumps(flagged, indent=2), encoding="utf-8")
    print(f"Wrote {out}")

    txt = BLOG / "hero-text-flags.txt"
    txt.write_text(
        "\n".join(f"{f['name']}\tscore={f['score']}\t{f['ocr_sample']}" for f in flagged),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
