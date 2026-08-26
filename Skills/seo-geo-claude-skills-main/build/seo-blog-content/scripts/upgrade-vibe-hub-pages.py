#!/usr/bin/env python3
"""Upgrade template hub pages 243, 263, 283 to ultimate-guide depth."""
from __future__ import annotations

import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[5] / "SEO" / "Blog"
HUB_EXPANSIONS = {
    "243-professional-data-api": """
## What Buyers Mean by a Professional Data API

A **professional data API** is not a public REST endpoint with a Swagger file. Buyers evaluate whether your product can expose structured business data—accounts, transactions, documents, enrichment fields—with the same rigor they expect from a SaaS vendor: versioning, auth scopes, rate limits, audit logs, and SLAs.

Three signals separate demo-grade data access from a professional data API:

| Signal | Demo API | Professional data API |
|--------|----------|------------------------|
| Auth | Single bearer token | Scoped keys, rotation, per-tenant isolation |
| Schema | Ad hoc JSON | Versioned contracts + backward compatibility |
| Operations | Best-effort uptime | Error budgets, status page, incident runbooks |
| Governance | None | Row-level rules, export controls, retention policy |
| Observability | Console logs | Per-tenant usage metrics and anomaly alerts |

The [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) is a practical baseline when credentials and regulated data cross your API boundary—especially for vibe-coded products that added a `/api` route in one afternoon.

---

## Architecture Layers for Vibe-Coded Data Products

### Layer 1: Ingestion and normalization

Vibe-coded teams often start with CSV uploads or a single Postgres table. A professional data API requires normalized entities before exposure: stable IDs, typed fields, and explicit null semantics. Map messy source payloads at the boundary—never in the UI.

### Layer 2: Access control and tenancy

Every read and write must resolve **who** is calling and **which tenant** they belong to. Row-level security patterns in [Supabase documentation](https://supabase.com/docs) translate well to API gateways: the token carries tenant context; the database enforces it.

### Layer 3: Contract and compatibility

Publish OpenAPI or JSON Schema for every public surface. Treat breaking changes as product releases with migration notes. Contract tests in CI catch vendor drift before customers do.

### Layer 4: Async extraction and enrichment

Contact enrichment, document parsing, and multi-source joins exceed serverless timeouts. Route them to async jobs with task IDs, webhooks, or SSE progress—patterns InfiniSynapse Server API uses for long-running data agent work.

### Layer 5: Observability and commercial readiness

Log tenant ID, endpoint, latency, and payload size per call. Buyers will ask for usage dashboards, export audit trails, and proof you can throttle abusive clients without taking honest users offline.

---

## 30-Day Professional Data API Rollout

**Week 1 — Inventory and classify data assets.** List every table, file bucket, and external enrichment source. Mark PII, payment data, and cross-border fields.

**Week 2 — Auth and secrets.** Move keys to a secret manager; implement scoped tokens; ban client-side vendor keys entirely.

**Week 3 — Contracts and validation.** Add Zod/Pydantic validation on every response; ship OpenAPI; wire contract tests.

**Week 4 — Async paths and monitoring.** Classify sync vs async endpoints; add structured logging; define error budgets and on-call rotation.

For implementation depth see [Production Readiness Checklist](/en/blog/production-readiness-reddit-checklist), [API Data Governance](/en/blog/api-data-governance-reddit), and [Dataset API](/en/blog/dataset-api-reddit).

---
""",
    "263-vibe-coding-tools": """
## The Vibe Coding Tool Landscape in 2026

**Vibe coding tools** span four categories that solve different parts of the stack:

| Category | Examples | Gets you to… | Breaks when… |
|----------|----------|--------------|--------------|
| IDE copilots | Cursor, Claude Code, Copilot | Fast UI + routes | You need governed data access |
| UI generators | v0, Figma AI | Polished frontends | Backend auth is undefined |
| App builders | Replit, Bolt, Lovable | End-to-end demos | Long jobs hit serverless limits |
| Agent backends | InfiniSynapse Server API | Data + file workflows | You skip proxy discipline |

The [Stanford HAI AI Index](https://hai.stanford.edu/ai-index) tracks the same shift: builders ship interfaces faster than they ship dependable infrastructure underneath.

---

## Selection Framework: Match Tool to Job

### Prototype velocity (days 1–7)

Optimize for iteration loops: chat-driven edits, instant preview, component libraries. Cursor and v0 excel here. Do not over-invest in custom backend until user value is proven.

### Integration velocity (weeks 2–4)

Once Stripe, OAuth, or warehouse data appears, prioritize tools that respect secret boundaries and async UX. App builders that hide backend complexity often hide **where** keys live—audit before beta.

### Production velocity (week 5+)

You need contract tests, structured logging, and a data API that survives real traffic. Compare [Cursor AI for vibe coding](/en/blog/cursor-ai-for-vibe-coding-reddit) for frontend speed with [API integration tools](/en/blog/api-integration-tools-reddit) for backend depth.

---

## Tool Stack Scorecard for Small Teams

Score 1 point per Yes before calling your stack "production-ready":

| Check | Pass? |
|-------|-------|
| Secrets never committed to git | |
| One command reproduces local dev environment | |
| Long LLM/data jobs run async with progress UI | |
| External API responses validated at boundary | |
| Staging uses production-like auth scopes | |
| On-call knows which tool generated which layer | |

**7+**: ready for closed beta. **5–6**: demo-plus. **Below 5**: stay in prototype mode.

Explore cluster depth in [Best Vibe Coding Tools](/en/blog/best-vibe-coding-tool-reddits-reddit), [Replit Vibe Coding](/en/blog/replit-vibe-coding-reddit), and [Lovable Vibe Coding](/en/blog/lovable-vibe-coding-reddit).

---
""",
    "283-vibe-coding-best-practices": """
## Vibe Coding Best Practices: The Production Mindset

**Vibe coding best practices** are not about prettier prompts—they are about habits that keep AI-generated code safe once real users, real money, and real data show up.

### Practice 1: Spec before codegen

Write a one-page spec: inputs, outputs, auth model, failure behavior, and success metrics. Paste it into every Cursor session. Models hallucinate less when constraints are explicit.

### Practice 2: Thin UI, thick boundaries

Keep React components dumb. Validate every external payload in one backend module. The [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) applies the moment your app calls tools or third-party APIs.

### Practice 3: Async by default for intelligence

Anything involving LLM chains, PDF parsing, or multi-step analysis belongs off the request thread. Show progress; never block the main UI for six minutes.

### Practice 4: Review diffs like a senior engineer

AI speed is worthless if nobody reads the diff. Focus reviews on auth, SQL, credential handling, and error surfaces—not spacing.

### Practice 5: Ship observability with the feature

Structured logs per external call beat post-mortem Slack threads. Define error budgets before marketing launch.

---

## Weekly Rituals That Scale

| Ritual | Owner | Outcome |
|--------|-------|---------|
| Integration inventory | Founder | No surprise vendor dependencies |
| Secret rotation drill | Backend | Keys rotatable in < 30 minutes |
| Contract test on CI | Any dev | Schema drift fails builds |
| Demo vs prod checklist | PM | No mock data in production paths |

Pair these rituals with [Vibe Coding Checklist](/en/blog/vibe-coding-checklist-reddit), [Vibe Coding Security](/en/blog/vibe-coding-security-reddit), and [How to Vibe Code](/en/blog/how-to-vibe-code-reddit) for tactical depth.

Microsoft's [Azure architecture guidance](https://learn.microsoft.com/en-us/azure/architecture/) reinforces the same pattern: isolate domains, validate at boundaries, and design for failure from day one—not after the first outage.

---
""",
}


def word_count(text: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start() :] if m else text
    t = re.sub(r"^#+\s+", "", body, flags=re.M)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t))


def upgrade_hub(folder: str, expansion: str) -> None:
    for pillar in BLOG.glob("pillar*"):
        art = pillar / folder / "article.md"
        if not art.is_file():
            continue
        text = art.read_text(encoding="utf-8")
        if expansion.strip() in text:
            print(f"skip {folder} (already upgraded)")
            return
        # Replace template TL;DR blockquote with bullet TL;DR
        kw_m = re.search(r"\*\*Target keyword\*\*:\s*`([^`]+)`", text)
        kw = kw_m.group(1) if kw_m else ""
        if kw and "> this approach is" in text.lower():
            bullets = (
                f"- **{kw.title()}** bridge the gap between AI-generated UI and production backends—auth, data APIs, async jobs, and observability.\n"
                f"- Vibe-coded teams hit the wall at credentials, schema validation, and long-running workflows—not at component styling.\n"
                f"- This hub maps the full cluster: definitions, scorecards, failure modes, and InfiniSynapse Server API patterns.\n"
                f"- Treat integration and data access as product features, not post-launch chores.\n"
            )
            text = re.sub(
                r"> this approach is[^\n]+\n",
                bullets,
                text,
                count=1,
                flags=re.I,
            )
        anchor = "## Scorecard\n"
        if anchor not in text:
            anchor = "## Core Framework\n"
        text = text.replace(anchor, expansion.strip() + "\n\n" + anchor, 1)
        art.write_text(text, encoding="utf-8")
        print(f"upgraded {folder} -> {word_count(text)} words")


def main() -> int:
    for folder, block in HUB_EXPANSIONS.items():
        upgrade_hub(folder, block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
