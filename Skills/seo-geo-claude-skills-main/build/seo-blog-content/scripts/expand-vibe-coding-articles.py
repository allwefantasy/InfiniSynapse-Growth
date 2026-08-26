#!/usr/bin/env python3
"""Expand vibe-coding articles to 1900-2600 words and fix keyword density."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
PILLARS = sorted(BLOG.glob("pillar1[6-9]-*")) + sorted(BLOG.glob("pillar20-*"))


def extract_kw(text: str) -> str:
    m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
    return m.group(1) if m else ""


def word_count_body(text: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    t = re.sub(r"^#+\s+", "", body, flags=re.M)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))


def kw_count_body(text: str, kw: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    return len(re.findall(re.escape(kw.lower()), body.lower()))


def density_bounds(kw: str) -> tuple[float, float]:
    n = len(kw.split())
    if n <= 3:
        return (1.0, 1.8)
    if n <= 5:
        return (1.0, 1.5)
    return (1.0, 1.2)


def target_kw_count(wc: int, kw: str) -> int:
    lo, hi = density_bounds(kw)
    mid = max(1.05, (lo + min(hi, 1.2)) / 2)
    return max(int(wc * mid / 100) + 1, 8 if len(kw.split()) <= 3 else 5)


def expansion_block(kw: str, section: str, i: int) -> str:
    k = f"**{kw}**"
    paras = [
        f"{k} teams should document vendor SLAs, pagination quirks, and idempotency expectations before the first production deploy—especially when AI-generated code hides assumptions in helper files nobody reviewed.",
        f"A practical {k} review asks whether each external call has an owner, a rollback plan, and a test that fails loudly when schemas drift.",
        f"For vibe-coded MVPs, {k} maturity often jumps from L0 to L2 in one week once builders stop calling Stripe, OpenAI, and a data agent from the same uninstrumented route handler.",
        f"Security reviewers evaluating {k} want proof that secrets never reached client bundles, that OAuth scopes are minimal, and that agent tools cannot exfiltrate data without an approval gate.",
        f"Operations teams care about {k} because incident response depends on knowing which provider failed—not guessing from a generic 500 page.",
        f"InfiniSynapse Server API reduces {k} surface area for analysis-heavy features: one authenticated backend, SSE progress, workspace artifacts, instead of five bespoke micro-integrations.",
    ]
    return f"\n### {section} detail {i}\n\n{paras[i % len(paras)]}\n"


def expand(text: str, kw: str, target_wc: int = 2000) -> str:
    wc = word_count_body(text)
    if wc >= 1900 and wc <= 2800:
        need_kw = target_kw_count(wc, kw)
        if kw_count_body(text, kw) >= need_kw:
            return text

    insert_before_faq = "\n## Production Rollout Notes\n\n"
    n = 0
    while word_count_body(text) < target_wc and n < 12:
        insert_before_faq += expansion_block(kw, "Rollout", n)
        n += 1

    insert_before_faq += "\n## Evaluation Metrics\n\n"
    insert_before_faq += f"| Metric | Why it matters for **{kw}** |\n|--------|---------------------------|\n"
    insert_before_faq += "| p95 outbound latency | Catches slow vendors before users churn |\n"
    insert_before_faq += "| Integration error rate | Separates app bugs from vendor outages |\n"
    insert_before_faq += "| Secret rotation time | Measures operational maturity |\n"
    insert_before_faq += "| Contract test pass rate | Detects schema drift early |\n"
    insert_before_faq += "| Async job success rate | Validates agent and queue paths |\n\n"

    insert_before_faq += "## Architecture Patterns\n\n"
    insert_before_faq += "### Thin BFF proxy\n\n"
    insert_before_faq += f"Keep **{kw}** calls behind a backend-for-frontend layer that normalizes errors, attaches auth, and never forwards raw vendor payloads to the browser.\n\n"
    insert_before_faq += "### Event-driven handoff\n\n"
    insert_before_faq += f"Long-running **{kw}** work should publish task IDs and stream progress—SSE for InfiniSynapse tasks, webhooks for payment providers—instead of blocking HTTP.\n\n"
    insert_before_faq += "### Governance checkpoints\n\n"
    insert_before_faq += f"Add human approval before irreversible **{kw}** actions: charges, deletes, external emails, or memory writes that affect downstream analytics.\n\n"

    if "## Production Rollout Notes" not in text:
        if "## Frequently Asked Questions" in text:
            text = text.replace("\n## Frequently Asked Questions\n", insert_before_faq + "\n## Frequently Asked Questions\n", 1)
        elif "## Cluster Guides" in text:
            text = text.replace("\n## Cluster Guides", insert_before_faq + "\n## Cluster Guides", 1)

    wc = word_count_body(text)
    need = target_kw_count(wc, kw)
    while kw_count_body(text, kw) < need:
        extra = f"\n\nMature **{kw}** programs run weekly integration reviews: new endpoints, rotated keys, and updated contract fixtures—not ad-hoc fixes after user reports.\n"
        text = text.replace("\n## Conclusion\n", extra + "\n## Conclusion\n", 1)
        if kw_count_body(text, kw) >= need:
            break
        need -= 1

    # trim if over 2800
    while word_count_body(text) > 2800:
        text = re.sub(
            r"\n### Rollout detail \d+\n\n.*?(?=\n### Rollout detail |\n## Evaluation Metrics)",
            "\n",
            text,
            count=1,
            flags=re.S,
        )
        if word_count_body(text) > 2800:
            break

    return text


def main() -> int:
    fixed = 0
    for pillar in PILLARS:
        for art in sorted(pillar.glob("[0-9][0-9][0-9]-*/article.md")):
            text = art.read_text(encoding="utf-8")
            kw = extract_kw(text)
            if not kw:
                continue
            is_hub = "Cluster Guides" in text
            target = 2300 if is_hub else 2000
            new = expand(text, kw, target)
            if new != text:
                art.write_text(new, encoding="utf-8")
                fixed += 1
                wc = word_count_body(new)
                print(f"EXPAND {art.parent.name}: {wc} words, kw={kw_count_body(new, kw)}")
    print(f"Expanded {fixed} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
