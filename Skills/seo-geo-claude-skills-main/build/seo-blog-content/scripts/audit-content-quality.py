#!/usr/bin/env python3
"""Content quality gate: EEAT signals, keyword stuffing heuristics, inline link rules."""
import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = [
    BLOG / "pillar1-ai-native-data-analysis",
    BLOG / "pillar2-data-agent-vs-alternatives",
    BLOG / "pillar3-ai-analyst-tools",
    BLOG / "pillar4-data-source-connectors",
    BLOG / "pillar5-nl2sql-text-to-sql",
    BLOG / "pillar6-ai-excel-csv-spreadsheet",
    BLOG / "pillar7-use-cases-role-industry",
    BLOG / "pillar8-skills-templates-glossary",
]

AI_TEMPLATE_PHRASES = [
    "is most valuable when it is implemented as a recurring operating system",
    "performs best when teams prioritize repeatability over one-off demos",
    "The common thread is not intelligence; it is orchestration",
    "Teams get better outcomes when they pair AI speed with metric contracts",
]

EXPERIENCE_PAT = re.compile(
    r"We (build|evaluate|evaluated|work|maintain|apply|tested|run)|hands-on|Evaluation basis|In our (tests|pilots|rollouts)",
    re.I,
)
ORIGINALITY_PAT = re.compile(
    r"scorecard|framework|30.day|playbook|case study|first-party|\d+%|\d+ minutes|April baseline|lobster",
    re.I,
)
ACCURACY_PAT = re.compile(r"Sources|NIST|Stanford|IBM|Microsoft Learn|verify|audit trail", re.I)


def body_from_tldr(text: str) -> str:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    return text[m.start() :] if m else text


def extract_keyword(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1).lower() if m else ""


def audit(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body = body_from_tldr(text)
    kw = extract_keyword(text)
    fails = []

    # Trust / Experience / Expertise
    if not EXPERIENCE_PAT.search(text):
        fails.append("Experience: missing first-person / hands-on signal")
    if "InfiniSynapse Data Team" not in text and "InfiniSynapse Team" not in text:
        fails.append("Trust: missing byline")
    if "Last updated: 2026" not in text:
        fails.append("Trust: missing freshness date")

    # Originality / Effort
    if not ORIGINALITY_PAT.search(body):
        fails.append("Originality: weak framework/scorecard/original signal")

    # Standalone external link blocks
    if re.search(r"^## Sources\s*$", text, re.M):
        fails.append("Links: standalone ## Sources section (must embed in body prose)")

    # Naked URL anchors
    if re.search(r"\[(https?://[^\]]+)\]\(\1\)", text):
        fails.append("Links: naked URL used as anchor text")

    # Bullet external links outside Sources
    for line in body.splitlines():
        if re.match(r"^-\s+[^:]+:\s+\[https?://", line):
            fails.append("Links: bullet list exposes external URL")
            break

    # Generic keyword placeholder (batch template artifact)
    generic_wf = len(re.findall(r"\bthis (?:connector )?workflow\b", body, re.I))
    if kw and generic_wf > 1:
        fails.append(
            f"Keyword: generic 'this workflow' ×{generic_wf} — use Target keyword `{kw}` in body"
        )

    # Keyword stuffing heuristics
    if kw:
        # keyword in 3+ consecutive section headers
        headers = re.findall(r"^#{2,3}\s+(.+)$", body, re.M)
        kw_headers = sum(1 for h in headers if kw in h.lower())
        if kw_headers >= 3:
            fails.append(f"Keyword: phrase in {kw_headers} H2/H3 headers (stuffing risk)")
        # same sentence repeated (mask URLs so path segments are not treated as sentences)
        masked = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1", body)
        sents = re.findall(r"[^.!?]+[.!?]", masked)
        from collections import Counter

        c = Counter(s.strip().lower() for s in sents if len(s.strip()) > 40)
        dup = [s for s, n in c.items() if n >= 2]
        if dup:
            fails.append("AI pattern: duplicate sentence detected")

    # AI template phrases (pillar7-style)
    for p in AI_TEMPLATE_PHRASES:
        if p.lower() in body.lower():
            fails.append(f"AI template: '{p[:50]}...'")
            break

    # Inline external links in body (not only at end)
    ext_inline = len(
        set(
            u
            for _, u in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body)
            if "infinisynapse" not in u.lower()
        )
    )
    if ext_inline < 5:
        fails.append(f"Links: only {ext_inline} inline external links in body (need >=5)")

    # Related reading bare link table
    if re.search(r"\|\s*\[/blog/", body):
        fails.append("Links: bare /blog/ URL in Related Reading table")

    return {
        "folder": path.parent.name,
        "pass": len(fails) == 0,
        "fails": fails,
        "inline_ext": ext_inline,
    }


def main() -> int:
    targets = PILLARS
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]
    total = fail_n = 0
    issue_counts: dict[str, int] = {}
    for pillar in targets:
        if not pillar.is_dir():
            continue
        print(f"\n{pillar.name}")
        print(f"{'Folder':<45} {'OK':>4}")
        print("-" * 52)
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            r = audit(art)
            total += 1
            if not r["pass"]:
                fail_n += 1
            print(f"{r['folder']:<45} {'✓' if r['pass'] else '✗':>4}")
            for f in r["fails"]:
                issue_counts[f.split(":")[0]] = issue_counts.get(f.split(":")[0], 0) + 1
                print(f"    · {f}")
    print(f"\nTotal: {total} | Pass: {total - fail_n} | Fail: {fail_n}")
    if issue_counts:
        print("\nIssue frequency:")
        for k, v in sorted(issue_counts.items(), key=lambda x: -x[1]):
            print(f"  {k}: {v}")
    return 1 if fail_n else 0


if __name__ == "__main__":
    raise SystemExit(main())
