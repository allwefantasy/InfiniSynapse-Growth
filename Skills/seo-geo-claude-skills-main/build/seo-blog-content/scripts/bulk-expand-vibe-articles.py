#!/usr/bin/env python3
"""Bulk-expand vibe articles to 1950-2750 words; tune keyword density."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))

EXTRA_SECTIONS = """
## Operating Model for Small Teams

### Who owns integrations

Assign one integration owner—even in a solo project—to maintain the API registry, rotate keys, and approve new vendors. Without ownership, vibe-coded repos accumulate duplicate clients and conflicting error handling.

### Weekly integration review

Spend thirty minutes each week reviewing: new endpoints added, failed contract tests, p95 latency spikes, and vendor changelog emails. This cadence prevents the slow drift that causes month-two outages.

### Documentation minimum

Each external dependency needs a one-page note: auth method, rate limits, sandbox vs production URLs, example success payload, and on-call runbook link. Future you (or Cursor) will need it at 2 a.m.

## Security and Compliance Baseline

### Client-side boundaries

No vendor secrets in front-end bundles, environment variables prefixed for client exposure, or API keys in screenshot-ready demo videos. Treat the browser as hostile.

### Least privilege

OAuth scopes and API keys should allow only what the current feature needs. Expand scopes when requirements expand—not preemptively.

### Agent-specific risks

When LLMs choose tools dynamically, validate tool inputs server-side and cap outbound destinations. Prompt injection often targets integration layers first.

## Case Study: Rent-vs-Commute Analyzer

A builder shipped a polished form in Cursor over a weekend. Users entered budget, office location, and max commute time; the UI promised a PDF neighborhood report. Behind the scenes, nothing called geocoding, transit data, or document generation yet.

The fix was not more prompts—it was a backend proxy plus InfiniSynapse Server API: SSE progress, a single `newTask` with structured instructions, workspace download for the PDF. The UI stayed unchanged; the integration layer became real. Time to first working end-to-end path: three days after the UI was already "done."

## Buyer Questions Before You Commit

| Question | Pass answer |
|----------|-------------|
| Can we rotate keys without redeploying the UI? | Yes, via secret manager |
| Do we have contract tests in CI? | Yes, per vendor |
| Are long jobs async with user-visible progress? | Yes |
| Can we trace which provider failed? | Yes, structured logs |
| Is there an approval gate for risky actions? | Yes, for payments and writes |

## Rollout Timeline (Typical)

| Week | Focus |
|------|-------|
| 1 | Inventory + secret store + proxy skeleton |
| 2 | First vendor integrated with contract test |
| 3 | Async path + monitoring + error UX |
| 4 | Beta users + runbook + on-call rotation |

## Tooling Shortlist

- **Secret store**: hosting provider env + vault for production
- **Contract tests**: Postman, Pact, or schema assertions in CI
- **Workflow/async**: Inngest, Temporal, or InfiniSynapse for agent jobs
- **Gateway** (optional): Kong, AWS API Gateway when surface area grows
- **Observability**: structured logs + alert on integration error rate
"""


def body_stats(text: str, kw: str) -> tuple[int, int]:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    t = re.sub(r"^#+\s+", "", body, flags=re.M)
    wc = len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))
    kc = len(re.findall(re.escape(kw.lower()), body.lower()))
    return wc, kc


def kw_band(kw: str) -> tuple[int, int]:
    n = len(kw.split())
    if n <= 3:
        return (12, 28)
    if n <= 5:
        return (7, 18)
    return (4, 12)


def trim_keywords(text: str, kw: str, max_k: int) -> str:
    wc, kc = body_stats(text, kw)
    if kc <= max_k:
        return text
    # Remove repetitive expansion sentences
    text = re.sub(
        r"\n\nMature \*\*" + re.escape(kw) + r"\*\* programs run weekly integration reviews:.*?\n",
        "\n",
        text,
    )
    text = re.sub(
        r"\n\nTeams shipping \*\*" + re.escape(kw) + r"\*\* should treat observability.*?\n",
        "\n",
        text,
    )
    while body_stats(text, kw)[1] > max_k:
        text = re.sub(
            r"\*\*" + re.escape(kw) + r"\*\*",
            "this approach",
            text,
            count=1,
            flags=re.I,
        )
    return text


def add_keywords(text: str, kw: str, min_k: int) -> str:
    while body_stats(text, kw)[1] < min_k:
        text = text.replace(
            "\n## Conclusion\n",
            f"\n\nProduction teams treat **{kw}** as an operating discipline—not a one-time integration ticket.\n\n## Conclusion\n",
            1,
        )
        if body_stats(text, kw)[1] >= min_k:
            break
        min_k -= 1
    return text


def trim_length(text: str, max_wc: int = 2790) -> str:
    while body_stats(text, "")[0] > max_wc:
        text = re.sub(r"\n### Rollout detail \d+\n\n.*?(?=\n### |\n## )", "\n", text, count=1, flags=re.S)
        if "## Production Rollout Notes" in text and body_stats(text, "")[0] > max_wc:
            text = re.sub(r"\n## Production Rollout Notes\n.*?(?=\n## Evaluation Metrics)", "\n", text, count=1, flags=re.S)
        if body_stats(text, "")[0] > max_wc:
            break
    return text


def main() -> int:
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
            if not m:
                continue
            kw = m.group(1)
            wc, _ = body_stats(text, kw)
            if wc < 1900 and "## Operating Model for Small Teams" not in text:
                anchor = "\n## Frequently Asked Questions\n"
                if anchor not in text:
                    anchor = "\n## Conclusion\n"
                # inject keyword once in extra block intro
                block = EXTRA_SECTIONS.replace(
                    "A builder shipped",
                    f"Teams implementing **{kw}** often ship",
                    1,
                )
                text = text.replace(anchor, "\n" + block + "\n" + anchor, 1)

            wc, kc = body_stats(text, kw)
            lo, hi = kw_band(kw)
            if kc > hi:
                text = trim_keywords(text, kw, hi)
            elif kc < lo:
                text = add_keywords(text, kw, lo)

            text = trim_length(text)
            art.write_text(text, encoding="utf-8")
    print("bulk expand complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
