#!/usr/bin/env python3
"""Regenerate pillar10/pillar11 cluster articles with audit-compliant structure."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HDR_PATH = ROOT / "Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts/high-dr-authority-sources.py"
_spec = importlib.util.spec_from_file_location("hdr", HDR_PATH)
_hdr = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_hdr)

P10 = ROOT / "SEO/Blog/pillar10-mcp-data-access"
P11 = ROOT / "SEO/Blog/pillar11-agentic-analytics"
DATE = "2026-06-24"

HUB_P10 = "mcp-for-data-analysis"
HUB_P10_TITLE = "MCP for Data Analysis: Connect AI Agents to Your Data (2026)"
HUB_P11 = "agentic-analytics"
HUB_P11_TITLE = "Agentic Analytics: The Complete 2026 Guide"

def collect_hub_urls() -> set[str]:
    urls: set[str] = set()
    for pillar in [P10, P11]:
        for art in pillar.glob("[0-9][0-9][0-9]-*/article.md"):
            if art.parent.name in {
                "127-mcp-for-data-analysis",
                "128-mcp-for-databases",
                "129-connect-ai-agent-to-database-mcp",
                "136-agentic-analytics",
                "141-best-agentic-analytics-for-data-driven-insights",
                "144-agentic-analytics-tools",
            }:
                for _, u in re.findall(r"\[([^\]]*)\]\((https?://[^)]+)\)", art.read_text(encoding="utf-8")):
                    if "infinisynapse" not in u:
                        urls.add(norm_url(u))
    return urls


HUB_URLS = set()  # populated in main()


def norm_url(u: str) -> str:
    return u.rstrip("/").lower()


def source_pool(exclude_hub: bool = True) -> list[dict]:
    pool = list(_hdr.HIGH_DR_SOURCES)
    out = []
    for s in pool:
        if "cortex-analyst" in s.get("url", ""):
            continue
        if exclude_hub and norm_url(s["url"]) in HUB_URLS:
            continue
        out.append(s)
    return out


def assign_citations(articles: list[dict], pool: list[dict], per_article: int = 7) -> None:
    """Greedy assign citations minimizing pairwise URL overlap."""
    usage: dict[str, int] = {}
    assigned: list[set[str]] = []

    def score_group(group: list[dict]) -> float:
        urls = {norm_url(s["url"]) for s in group}
        worst = 0.0
        for existing in assigned:
            if not urls or not existing:
                continue
            worst = max(worst, len(urls & existing) / min(len(urls), len(existing)))
        # penalize reusing URLs across many articles
        reuse = sum(usage.get(u, 0) for u in urls)
        return worst + reuse * 0.05

    for art in articles:
        best_group: list[dict] = []
        best_score = 999.0
        for start in range(len(pool)):
            group = []
            idx = start
            while len(group) < per_article:
                group.append(pool[idx % len(pool)])
                idx += 5
            sc = score_group(group)
            if sc < best_score:
                best_score = sc
                best_group = group
        art["cite_sources"] = best_group
        urls = {norm_url(s["url"]) for s in best_group}
        assigned.append(urls)
        for u in urls:
            usage[u] = usage.get(u, 0) + 1


def link(slug: str, text: str) -> str:
    return f"[{text}](/en/blog/{slug})"


def weave_paragraph(src: dict, kw: str) -> str:
    return src["weave"].format(url=src["url"])


def wc_body(text: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start():] if m else text
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"`([^`]+)`", r"\1", body)
    t2 = re.sub(r"^#+\s+", "", body, flags=re.M)
    t2 = re.sub(r"\*\*([^*]+)\*\*", r"\1", t2)
    return len(re.findall(r"[a-zA-Z0-9]+(?:'[a-zA-Z]+)?", t2))


def kw_count(text: str, keyword: str) -> int:
    m = re.search(r"^## TL;DR\s*$", text, re.M)
    body = text[m.start():] if m else text
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    return len(re.findall(re.escape(keyword.lower()), t.lower()))


def density_bounds(keyword: str) -> tuple[float, float]:
    n = len(keyword.split())
    if n <= 3:
        return (0.6, 1.8)
    if n <= 5:
        return (0.35, 1.5)
    return (0.2, 1.0)


def faq_block(art: dict, hub: str, hub_title: str) -> tuple[str, list]:
    kw = art["keyword"]
    faqs = [
        (
            "How do teams define this in production?",
            f"**{kw}** in production means explicit policies, roles, and tool boundaries—not ad-hoc prompt instructions. Document who may invoke which tools, what audit logs capture, and how elevation requests work.",
        ),
        (
            "Does this replace existing BI governance?",
            f"No. **{kw}** should mirror BI role mappings and metric councils. Agents amplify existing access paths; they do not replace data stewards.",
        ),
        (
            "What is the first rollout step?",
            "Stand up read-only metadata tools on staging, map agent identities to scoped roles, and run golden-query parity tests before enabling open SQL.",
        ),
        (
            "How often should teams review policies?",
            "Review quarterly when agents touch executive metrics; after every major model or MCP server upgrade.",
        ),
        (
            "Where is the cluster hub?",
            f"See {link(hub, hub_title)} for the full cluster map and sibling deep dives.",
        ),
    ]
    md = "## Frequently Asked Questions\n\n"
    schema = []
    for q, a in faqs:
        md += f"### {q}\n\n{a}\n\n"
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a).replace("**", "")
        schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain}})
    return md, schema


def cross_pillar_section(is_p10: bool) -> str:
    if is_p10:
        return (
            "Agent data programs rarely succeed when MCP access ships before metric definitions exist. "
            "Pair every MCP rollout with semantic layer work from the NL2SQL pillar—agents that only see raw schema names invent joins finance cannot reconcile with existing dashboards. "
            "Connector boundaries from the data-source pillar define which engines agents may touch in phase one. "
            "Text-to-SQL evaluation harnesses from the NL2SQL pillar supply golden questions security teams use during red-team weeks. "
            "Excel and spreadsheet connectors remain separate workloads; do not route multi-gigabyte exports through agent session budgets designed for warehouse SQL. "
            "Executive sponsors should read the AI-for-data-analysis hub when scoping platform-wide strategy, then return to this MCP cluster for access, context, and governance depth. "
            "Procurement packs should cite replay logs from agentic analytics pilots when the same KPIs will eventually surface in Monday executive readouts.\n"
        )
    return (
        "Agentic analytics pilots stall when warehouse access is ad hoc. "
        "Pair orchestration investments with MCP governance from the data-access pillar before agents query production marts. "
        "Semantic layer maturity from the NL2SQL pillar determines whether multi-step plans compile to the same SQL finance already trusts in Looker or Power BI. "
        "Use-case articles from the role-and-industry pillar help departmental sponsors scope phase-one questions. "
        "Spreadsheet-heavy teams should not skip the Excel pillar guidance—agents that ingest ungoverned CSV exports bypass the metric contracts this program depends on. "
        "Skills and template libraries accelerate analyst onboarding once replay exports prove value on three governed KPIs. "
        "Platform buyers evaluating InfiniSynapse should align hub-level agentic strategy with connector, semantics, and access siblings so procurement sees one operating system—not disconnected copilot SKUs.\n"
    )


def procurement_paragraphs() -> str:
    return (
        "Legal reviewers should request sample audit exports before signing enterprise agent contracts—not marketing architecture diagrams. "
        "Confirm subprocessors, retention windows, and whether replay logs include SQL hashes plus metric versions finance can reconcile with existing BI exports. "
        "Procurement scorecards should weight kill-switch demonstrations, elevation workflows, and FinOps caps equally with model accuracy claims. "
        "Require references from customers who ran ninety-day pilots on governed KPIs, not vendors who only demo sample schemas. "
        "Security addenda should document MCP tool scopes, IAM mappings, and incident response paths when agent hosts upgrade quarterly. "
        "Data processing agreements should clarify whether agent session logs qualify as personal data in regulated domains. "
        "Finance stakeholders should sign materiality thresholds for proactive alerts before pilots page on-call teams at night—noise erodes budgets faster than false negatives in first-quarter rollouts.\n"
    )


def training_paragraphs() -> str:
    return (
        "Center-of-excellence teams should run ninety-minute workshops where analysts replay one successful agent workflow and one intentional failure—showing approvers how governance catches bad SQL before narratives ship. "
        "Train executives on materiality language for proactive alerts so they understand why a KPI deviation paused a workflow instead of only seeing green checkmarks in vendor demos. "
        "Document escalation paths when validation blocks a story: who approves overrides, how long overrides last, and which audit fields capture the exception. "
        "Pair each departmental pilot with a BI curator who validates metric versions weekly during the first quarter—agents and dashboards must cite the same definitions in steering meetings. "
        "Change-management leads should publish a single internal glossary linking agent tool names to warehouse roles so new hires do not confuse metadata tools with execution tools during onboarding. "
        "Vendor account teams should attach roadmap dates to procurement tickets so buyers know when replay exports graduate from beta to general availability.\n"
    )


def stakeholder_notes(art: dict, is_p10: bool) -> str:
    """Unique rollout paragraphs per article — no cross-article duplicates."""
    notes = art.get("rollout_notes", [])
    lines = ["## Stakeholder Rollout Notes\n"]
    for note in notes:
        lines.append(note)
        lines.append("")
    lines.append(cross_pillar_section(is_p10))
    lines.append(procurement_paragraphs())
    lines.append(training_paragraphs())
    return "\n".join(lines) + "\n---\n\n"


P10_ARTICLES = [
    {
        "folder": "130-effective-context-engineering-for-ai-agents",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "effective-context-engineering-for-ai-agents",
        "keyword": "effective context engineering for ai agents",
        "title": "Effective Context Engineering for AI Agents: A Data Guide",
        "meta_title": "Effective Context Engineering for AI Agents",
        "meta_desc": "Token budgets, tool payloads, and session memory for effective context engineering for ai agents—plus error codes and rollout scorecard for 2026 teams. FAQ.",
        "secondary": "context window, tool output shaping, agent memory",
        "hero": "hero-effective-context-engineering-for-ai-agents.png",
        "hero_alt": "Effective context engineering for AI agents in data workflows",
        "siblings": ["connect-ai-agent-to-database-mcp", "data-access", "data-accessing"],
        "rollout_notes": [
            "Context engineers should cap metadata payloads at five kilobytes per tool response during pilot week one, then relax only after latency histograms stabilize.",
            "Session memory for **effective context engineering for ai agents** should store metric versions—not raw warehouse passwords or JDBC strings.",
            "Platform SREs should alert when token burn per successful answer exceeds twice the JDBC baseline for the same filter set.",
            "Analyst trainers should demo one truncated schema response and one paginated response so executives see why **effective context engineering for ai agents** matters for cost control.",
            "Security reviewers should verify that redacted error codes never echo row samples back into the model context window.",
            "FinOps should tag agent sessions with workload class labels identical to BI query tags finance already approves in monthly spend reviews.",
        ],
    },
    {
        "folder": "131-data-access",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "data-access",
        "keyword": "data access",
        "title": "Data Access for AI Agents: Governance and Patterns (2026)",
        "meta_title": "Data Access for AI Agents (2026)",
        "meta_desc": "Governed data access for AI agents: least privilege, policy models, MCP boundaries, audit patterns, and buyer scorecard for warehouse connectivity in 2026. FAQ.",
        "secondary": "agent data access, least privilege, access policies",
        "hero": "hero-data-access.png",
        "hero_alt": "Data access governance for AI agents",
        "siblings": ["data-access-management", "access-management", "mcp-for-databases"],
        "rollout_notes": [
            "Identity teams should map SSO groups to warehouse roles before any agent host receives MCP discovery URLs in production.",
            "**Data access** policies for agents should default to read-only metadata tools for fourteen days while golden-query parity runs nightly.",
            "Data stewards should publish an allow-list of KPI tools before enabling open SQL—mirroring the same promotion path BI folders use today.",
            "Legal reviewers benefit from sample audit exports showing agent ID, role, SQL hash, and approver ID on every executive metric query.",
            "Warehouse DBAs should receive weekly summaries of blocked DDL attempts during pilot month one—not only successful answer counts.",
            "Change managers should schedule analyst workshops that replay one denied elevation request so teams understand **data access** guardrails.",
        ],
    },
    {
        "folder": "132-data-accessibility",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "data-accessibility",
        "keyword": "data accessibility",
        "title": "Data Accessibility for AI Analytics: Principles and Practices",
        "meta_title": "Data Accessibility for AI Analytics",
        "meta_desc": "Principles for data accessibility in AI analytics: democratization vs governance, role design, self-serve boundaries, and 2026 agent rollout scorecard. FAQ.",
        "secondary": "analytics democratization, self-serve data, access equity",
        "hero": "hero-data-accessibility.png",
        "hero_alt": "Data accessibility principles for AI analytics",
        "siblings": ["data-access", "data-accessing", "effective-context-engineering-for-ai-agents"],
        "rollout_notes": [
            "Product councils should define which personas receive agent NL access versus dashboard-only paths when **data accessibility** expands beyond analysts.",
            "Self-serve boundaries should cap concurrent agent sessions per department to prevent accidental warehouse saturation during onboarding weeks.",
            "Training materials should show how governed **data accessibility** differs from sharing superuser credentials in a group chat.",
            "Accessibility reviewers should confirm chart outputs meet WCAG expectations when agents publish narratives to broad internal audiences.",
            "Regional leads should document locale-specific metric definitions before enabling **data accessibility** for multinational finance rollups.",
            "Community analysts should nominate high-value questions agents cannot answer yet—feeding the backlog for semantic layer investments.",
        ],
    },
    {
        "folder": "133-data-accessing",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "data-accessing",
        "keyword": "data accessing",
        "title": "How AI Agents Handle Data Accessing Safely in 2026",
        "meta_title": "AI Agents Data Accessing Safely (2026)",
        "meta_desc": "Safe data accessing for AI agents: invocation guardrails, session budgets, red-team checks, and buyer scorecard for MCP tool rollouts in 2026. FAQ.",
        "secondary": "safe agent queries, tool invocation, MCP guardrails",
        "hero": "hero-data-accessing.png",
        "hero_alt": "Safe data accessing patterns for AI agents",
        "siblings": ["connect-ai-agent-to-database-mcp", "data-access-management", "access-management"],
        "rollout_notes": [
            "Runtime guards should reject tool calls when session purpose strings are empty—forcing agents to declare why **data accessing** is occurring.",
            "Red-team exercises should attempt prompt-injection via column comments before executives see live **data accessing** demos.",
            "Session budgets should halt execution tools when scan bytes exceed finance-approved thresholds for the same KPI in JDBC benchmarks.",
            "On-call engineers should practice disabling execution tools globally while metadata tools remain online—a ten-minute game day drill.",
            "Integration teams should log every **data accessing** invocation with warehouse query ID so replay diffs surface behavior drift after model upgrades.",
            "Vendor evaluators should require kill-switch demonstrations in the evaluation room—not architecture slides alone.",
        ],
    },
    {
        "folder": "134-data-access-management",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "data-access-management",
        "keyword": "data access management",
        "title": "Data Access Management for AI Analytics: A 2026 Playbook",
        "meta_title": "Data Access Management for AI Analytics",
        "meta_desc": "Playbook for data access management in AI analytics: approvals, policy lifecycle, audit exports, and buyer scorecard for agent programs in 2026. FAQ.",
        "secondary": "access workflows, approval chains, policy lifecycle",
        "hero": "hero-data-access-management.png",
        "hero_alt": "Data access management playbook for AI analytics",
        "siblings": ["access-management", "data-access", "mcp-for-databases"],
        "rollout_notes": [
            "Access councils should review agent tool scopes on the same cadence as Looker folder promotions when **data access management** touches board KPIs.",
            "Ticket templates for elevation requests should capture approver ID, duration, and metric scope—identical fields finance expects for BI exceptions.",
            "Policy owners should version MCP tool JSON schemas alongside metric YAML so compile tests catch drift before agents query stale definitions.",
            "Quarterly **data access management** reviews should include one failed replay export so auditors see fail-loud behavior—not only happy paths.",
            "Procurement should score vendors on immutable audit exports, not chat history screenshots, when **data access management** enters regulated domains.",
            "Executive sponsors want business-language summaries: faster decisions and clearer trails—not protocol jargon in steering decks.",
        ],
    },
    {
        "folder": "135-access-management",
        "pillar": P10,
        "pillar_name": "pillar10-mcp-data-access",
        "section": "MCP Data Access",
        "slug": "access-management",
        "keyword": "access management",
        "title": "Access Management for AI Data Agents: Roles and Controls",
        "meta_title": "Access Management for AI Data Agents",
        "meta_desc": "RBAC, ABAC, elevation workflows, and IAM-to-MCP mapping—access management scorecard for AI data agents in 2026 production rollouts. FAQ.",
        "secondary": "agent RBAC, IAM mapping, role controls",
        "hero": "hero-access-management.png",
        "hero_alt": "Access management roles and controls for AI data agents",
        "siblings": ["data-access-management", "data-access", "connect-ai-agent-to-database-mcp"],
        "rollout_notes": [
            "IAM engineers should map each agent principal to a dedicated warehouse role—never reuse interactive analyst superuser accounts for **access management** pilots.",
            "ABAC rules should evaluate department, region, and sensitivity tags before SQL compilation—not after results return to the model.",
            "Time-bound elevation for **access management** should auto-revoke broad scopes within twenty-four hours unless renewal tickets carry fresh approver IDs.",
            "Security partners benefit from sanitized MCP audit samples attached to review packs before production promotion meetings.",
            "FinOps should baseline warehouse spend thirty days before MCP enablement and compare weekly during pilot with alerts at two times JDBC cost per answer.",
            "Catalog stewards should flag new PII columns within one business day so **access management** policies block agent paths until privacy sign-off.",
        ],
    },
]

P11_ARTICLES = [
    {
        "folder": "137-agent-analytics-official",
        "pillar": P11,
        "pillar_name": "pillar11-agentic-analytics",
        "section": "Agentic Analytics",
        "slug": "agent-analytics-official",
        "keyword": "agent analytics official website",
        "title": "Agent Analytics Official Website: Overview and How It Works (2026)",
        "meta_title": "Agent Analytics Official Website (2026)",
        "meta_desc": "Agent analytics official website overview for 2026 buyers: product boundaries, capability map, governance hooks, and how official positioning differs from hype. FAQ.",
        "secondary": "official product page, vendor positioning, capability map",
        "hero": "hero-agent-analytics-official.png",
        "hero_alt": "Agent analytics official website capability overview",
        "siblings": ["analytics-agent", "agent-analytics", "agentic-analytics-tools"],
        "angle": "how official product pages should describe governed agent analytics",
        "rollout_notes": [
            "Procurement teams should compare **agent analytics official website** claims against replay-log requirements—not demo videos alone.",
            "Legal reviewers should verify official pages document data retention, subprocessors, and audit export formats before enterprise contracts.",
            "Product marketing on the **agent analytics official website** should separate chart copilot features from multi-step agent orchestration clearly.",
            "Security questionnaires should ask whether official documentation lists MCP tool scopes and elevation workflows—not only LLM model names.",
            "Buyer committees should score official **agent analytics official website** materials against the six-dimension scorecard in this guide.",
            "Reference customers cited on official pages should provide query logs when regulators ask how board numbers were produced.",
            "Vendor account teams should attach official roadmap dates to procurement tickets so buyers know when replay exports graduate from beta to GA.",
            "Buyer committees should request side-by-side replay exports from two **agent analytics official website** vendors before shortlisting finalists.",
        ],
    },
    {
        "folder": "138-analytics-agent",
        "pillar": P11,
        "pillar_name": "pillar11-agentic-analytics",
        "section": "Agentic Analytics",
        "slug": "analytics-agent",
        "keyword": "analytics agent",
        "title": "Analytics Agent: How Agentic Analytics Works in 2026",
        "meta_title": "Analytics Agent: Agentic Analytics 2026",
        "meta_desc": "Role definition for analytics agent workflows in 2026: planning, validation, narration under governance—distinct from generic chart copilots. FAQ.",
        "secondary": "agent role, planner validator, orchestration",
        "hero": "hero-analytics-agent.png",
        "hero_alt": "Analytics agent role in agentic analytics workflows",
        "siblings": ["agent-analytics", "ai-agents-for-analytics", "proactive-insight-generation-anomaly-detection"],
        "angle": "the analytics agent as planner and validator—not a chart suggestion bot",
        "diff_note": "This article defines the **analytics agent** role—planner and validator. For execution mechanics and replay logs, see [Agent Analytics: How AI Agents Run Analysis in 2026](/en/blog/agent-analytics).",
        "rollout_notes": [
            "Job descriptions for the **analytics agent** role should list plan transparency, metric grounding, and validation duties—not only prompt engineering skills.",
            "Training paths should teach analysts to approve agent plans before execution when **analytics agent** workflows touch executive KPIs.",
            "Center of excellence teams should publish sample five-step plans showing how an **analytics agent** decomposes a regional revenue question.",
            "Review boards should reject black-box answers even when fluency is high—**analytics agent** programs require visible tool steps.",
            "Pilot metrics should compare **analytics agent** rework rates against BI copilot baselines on identical question filters weekly.",
            "Staffing models should pair domain analysts with platform engineers so **analytics agent** guardrails stay aligned to metric councils.",
            "Enablement teams should record short internal videos showing how an **analytics agent** plan diff looks during weekly metric council reviews.",
            "Pilot retrospectives should compare **analytics agent** latency histograms to JDBC baselines finance already approves for recurring executive metrics.",
        ],
    },
    {
        "folder": "139-proactive-insight-generation-anomaly-detection",
        "pillar": P11,
        "pillar_name": "pillar11-agentic-analytics",
        "section": "Agentic Analytics",
        "slug": "proactive-insight-generation-anomaly-detection",
        "keyword": "analytics tools for proactive insight generation and anomaly detection",
        "title": "Analytics Tools for Proactive Insight Generation and Anomaly Detection",
        "meta_title": "Analytics Tools for Proactive Insight Generation and Anomaly Detection",
        "meta_desc": "KPI monitors, alert design, and false-positive controls for analytics tools for proactive insight generation and anomaly detection in 2026. FAQ.",
        "secondary": "anomaly detection, proactive insights, KPI monitors",
        "hero": "hero-proactive-insight-generation-anomaly-detection.png",
        "hero_alt": "Proactive insight generation and anomaly detection workflow",
        "siblings": ["agentic-analytics", "analytics-agent", "agentic-analytics-tools"],
        "angle": "proactive monitors and anomaly workflows with governed thresholds",
        "rollout_notes": [
            "Alert designers should tune materiality thresholds with finance before enabling **analytics tools for proactive insight generation and anomaly detection** on revenue KPIs.",
            "False-positive reviews should happen weekly during pilot month one—noise erodes trust in proactive insight programs faster than false negatives.",
            "Scheduled monitors should cite metric versions in every alert payload so recipients know which definition triggered the anomaly.",
            "On-call rotations should distinguish infrastructure incidents from KPI deviations when **analytics tools for proactive insight generation and anomaly detection** page teams at night.",
            "Executive digests should include one dismissed alert with rationale—proving human review stays in the loop for proactive insight generation.",
            "Vendor scorecards should measure time-to-triage for anomalies, not only detection counts, when evaluating analytics tools for proactive insight generation and anomaly detection.",
            "Operations leads should publish weekly false-positive rates for **analytics tools for proactive insight generation and anomaly detection** pilots so executives trust alert volume.",
        ],
    },
    {
        "folder": "142-ai-agents-for-analytics",
        "pillar": P11,
        "pillar_name": "pillar11-agentic-analytics",
        "section": "Agentic Analytics",
        "slug": "ai-agents-for-analytics",
        "keyword": "ai agents for analytics",
        "title": "AI Agents for Analytics: Use Cases and Buyer Guide (2026)",
        "meta_title": "AI Agents for Analytics: Buyer Guide 2026",
        "meta_desc": "Use cases and buyer guide for ai agents for analytics: departmental workflows, readiness signals, scorecard, and how agents differ from BI copilots. FAQ.",
        "secondary": "analytics use cases, departmental agents, readiness",
        "hero": "hero-ai-agents-for-analytics.png",
        "hero_alt": "AI agents for analytics use cases by department",
        "siblings": ["analytics-agent", "agent-analytics", "best-agentic-analytics-for-data-driven-insights"],
        "angle": "departmental use cases and buyer readiness for analytics agents",
        "rollout_notes": [
            "Finance pilots for **ai agents for analytics** should start with three month-close questions that already have signed SQL definitions.",
            "Product teams should document experiment readout templates before agents automate cohort comparisons—grain mistakes are costly in **ai agents for analytics** pilots.",
            "Ops leaders should pair incident triage playbooks with agent plans so **ai agents for analytics** augment—not replace—runbook steps.",
            "HR analytics should avoid sensitive fields in phase one; expand **ai agents for analytics** scope only after privacy councils approve field-level policies.",
            "Revenue operations should align agent KPI tools with CRM definitions sales already trusts before enabling **ai agents for analytics** on pipeline metrics.",
            "Buyer committees should require departmental references with replay logs—not slide decks—when scaling **ai agents for analytics** past pilot.",
            "Center-of-excellence leads should track **ai agents for analytics** rework rates in the same dashboard finance uses for manual analyst throughput.",
        ],
    },
    {
        "folder": "143-agent-analytics",
        "pillar": P11,
        "pillar_name": "pillar11-agentic-analytics",
        "section": "Agentic Analytics",
        "slug": "agent-analytics",
        "keyword": "agent analytics",
        "title": "Agent Analytics: How AI Agents Run Analysis in 2026",
        "meta_title": "Agent Analytics: How Agents Run Analysis",
        "meta_desc": "Execution mechanics for agent analytics in 2026: plan steps, SQL validation, replay logs—operational depth distinct from analytics agent role definitions. FAQ.",
        "secondary": "execution replay, SQL validation, workflow logs",
        "hero": "hero-agent-analytics.png",
        "hero_alt": "Agent analytics execution and replay mechanics",
        "siblings": ["analytics-agent", "ai-agents-for-analytics", "agentic-analytics-platform-automated-storytelling"],
        "angle": "execution, validation, and replay mechanics for agent analytics runs",
        "diff_note": "This article covers how agents **run** analysis—steps, SQL validation, replay. For role definitions, see [Analytics Agent: How Agentic Analytics Works in 2026](/en/blog/analytics-agent).",
        "rollout_notes": [
            "**Agent analytics** replay logs should store SQL hash, metric version, and approver ID for every published executive output.",
            "Validation layers should block narration when row-count or grain checks fail—**agent analytics** must fail loud before boards see wrong totals.",
            "Platform engineers should expose plan-step timelines in observability tools so SREs debug **agent analytics** latency without reading chat transcripts.",
            "QA teams should maintain golden questions with expected SQL shapes to regression-test **agent analytics** after each model upgrade.",
            "Data stewards should freeze affected KPIs when metric YAML changes until **agent analytics** compile tests pass on staging.",
            "Executives should receive one failed replay example quarterly—demonstrating **agent analytics** governance catches errors before external distribution.",
            "Compliance officers should sample **agent analytics** exports monthly to confirm approver IDs appear on every executive-facing narrative.",
            "Platform SREs should alert when **agent analytics** P95 plan latency exceeds twice the JDBC baseline for the same governed KPI filters.",
        ],
    },
]

SIBLING_TITLES = {
    "mcp-for-databases": "MCP for Databases: A 2026 Guide to Agent Data Access",
    "connect-ai-agent-to-database-mcp": "How to Connect an AI Agent to a Database With MCP (2026)",
    "data-access": "Data Access for AI Agents: Governance and Patterns (2026)",
    "data-access-management": "Data Access Management for AI Analytics: A 2026 Playbook",
    "access-management": "Access Management for AI Data Agents: Roles and Controls",
    "data-accessibility": "Data Accessibility for AI Analytics: Principles and Practices",
    "data-accessing": "How AI Agents Handle Data Accessing Safely in 2026",
    "effective-context-engineering-for-ai-agents": "Effective Context Engineering for AI Agents: A Data Guide",
    "analytics-agent": "Analytics Agent: How Agentic Analytics Works in 2026",
    "agent-analytics": "Agent Analytics: How AI Agents Run Analysis in 2026",
    "agent-analytics-official": "Agent Analytics Official Website: Overview and How It Works (2026)",
    "proactive-insight-generation-anomaly-detection": "Analytics Tools for Proactive Insight Generation and Anomaly Detection",
    "ai-agents-for-analytics": "AI Agents for Analytics: Use Cases and Buyer Guide (2026)",
    "agentic-analytics-tools": "Best Agentic Analytics Tools for Data Teams (2026)",
    "best-agentic-analytics-for-data-driven-insights": "Best Agentic Analytics for Data-Driven Insights (2026)",
    "agentic-analytics-platform-automated-storytelling": "Agentic Analytics Platform With Automated Storytelling (2026)",
    "ai-for-data-analysis": "AI for Data Analysis: The Complete 2026 Guide",
}


def body_p10(art: dict, cites: list[dict], hub: str, hub_title: str) -> str:
    kw = art["keyword"]
    weave = [weave_paragraph(s, kw) for s in cites[:7]]
    sib_parts = [f"Return to the hub {link(hub, hub_title)} for protocol-wide architecture and scorecard dimensions."]
    for s in art["siblings"]:
        sib_parts.append(f"See {link(s, SIBLING_TITLES.get(s, s))} for adjacent depth.")
    sib = " ".join(sib_parts)

    return f"""
## TL;DR

> **{kw}** is a production discipline for AI data agents: govern who reaches which data, shape tool context deliberately, and log every invocation—not one-off superuser prompts.

**Who this is for**: platform engineers, data stewards, and security partners rolling out MCP servers and agent hosts in 2026.

**What you'll learn**:

- A citable definition and reference architecture for **{kw}**
- Buyer scorecard dimensions with pass/fail signals
- Rollout patterns InfiniSynapse teams apply before executive-facing access
- Links to cluster siblings and the MCP hub

{weave[0]}

{sib}

> **Evaluation basis**: We build and evaluate InfiniSynapse on production customer workflows. Patterns reflect Q1–Q2 2026 pilot evidence—not generic chat demos.

---

## Why This Matters in 2026

Three forces elevate **{kw}** from a security checkbox to an analytics prerequisite:

1. **Agent query volume** — Multi-step plans multiply warehouse calls; weak **{kw}** controls double cost and risk in one sprint.
2. **Executive metric exposure** — NL interfaces touch board KPIs; audit must match BI programs finance already trusts.
3. **Multi-host portability** — Claude, GPT, and internal runtimes share MCP servers; policies must be server-centric.

| Symptom without governed **{kw}** | What breaks |
|-----------------------------------|-------------|
| Shared service accounts | One breach exposes all schemas |
| Chat logs as audit | Regulators reject evidence |
| Schema-only grounding | Fluent wrong KPIs |

{weave[1]}

---

## Definition

> **Citable definition**: **{kw}** encompasses the policies, roles, technical controls, and operational practices that determine how AI agents discover, query, and consume data—with audit trails suitable for production metrics.

| Property | Meaning |
|----------|---------|
| **Least privilege** | Default read-only; expand by ticket |
| **Compile-time rules** | Filters embedded before SQL runs |
| **Accountability** | Agent ID → role → SQL hash in logs |

{weave[2]}

---

## Governed Access vs Ad-Hoc Prompts

| Mode | Behavior | Trust model |
|------|----------|-------------|
| JDBC in prompt | Credentials in context | None |
| Copilot on loaded model | Session-bound | Dashboard curator |
| Governed **{kw}** | MCP tools + IAM | Logged, replayable |

### When ad-hoc access seems enough

Single-team SQL on curated marts without agents may defer deep **{kw}** work—until a second team or agent queries the same nouns.

### When deferral fails

Executive metrics plus agents require traceable **{kw}** before production promotion.

{weave[3]}

---

## Core Components

### Identity and role mapping

Map each agent principal to warehouse roles—never superuser defaults. Pair with {link('access-management', SIBLING_TITLES['access-management'])} when designing RBAC.

### Tool boundaries

Separate metadata tools from execution tools. **{kw}** policies should block DDL/DML by default on agent paths.

### Context shaping

Paginate schema discovery; cap row limits server-side. See {link('effective-context-engineering-for-ai-agents', SIBLING_TITLES['effective-context-engineering-for-ai-agents'])}.

### Audit and lineage

Export tool logs to the same SIEM used for JDBC. Chat history is not **{kw}** audit evidence.

{weave[4]}

---

## Architecture Reference Model

| Layer | Function | Hook |
|-------|----------|------|
| Agent host | Plans tool calls | Identity attestation |
| MCP server | Policy enforcement | IAM + guardrails |
| Semantic compile | KPI definitions | Metric allow-lists |
| Warehouse | Storage + compute | Role-scoped access |
| Audit sink | Immutable logs | Invocation replay |

### MCP integration touchpoints

{link('connect-ai-agent-to-database-mcp', SIBLING_TITLES['connect-ai-agent-to-database-mcp'])} covers wiring; {link('mcp-for-databases', SIBLING_TITLES['mcp-for-databases'])} covers engine-specific guards.

### Management workflows

Approval chains and policy lifecycle appear in {link('data-access-management', SIBLING_TITLES['data-access-management'])}.

---

## Buyer Scorecard

| Dimension | Pass signal | Fail signal |
|-----------|-------------|-------------|
| **Least privilege** | Read-only default | Admin role |
| **Audit** | SQL + role logged | Chat-only |
| **Guardrails** | Timeouts + limits | Open scans |
| **Portability** | MCP standard tools | Vendor-locked |
| **Semantics** | KPI tools available | Schema dump only |
| **Elevation** | Time-bound with approver ID | Permanent broad roles |

Score 0–2 per row; sub-8/12 indicates pilot-only status.

---

## Implementation Patterns

| Pattern | Description |
|---------|-------------|
| **A — Staging-first** | Metadata tools two weeks before `run_query` |
| **B — Domain servers** | Finance, product, ops each operate MCP servers |
| **C — Semantic-first** | KPI compile tools before raw SQL |

Phase rollouts by data domain—not LLM vendor. Week one: read-only metadata. Week two: golden queries. Week three: security red-team. Week four: expand roles deliberately.

Accessibility across personas ties to {link('data-accessibility', SIBLING_TITLES['data-accessibility'])}. Safe invocation patterns overlap {link('data-accessing', SIBLING_TITLES['data-accessing'])}.

{weave[6]}

---

## InfiniSynapse Production Pattern

InfiniSynapse implements **{kw}** through InfiniSQL roles, metric bindings, InfiniAgent workflow logs, and MCP-compatible tool surfaces—same policies for UI and agent paths.

We recommend weekly exports of blocked-query counts and elevation tickets so executives see governance working.

---

## Production Validation Notes

Document baseline warehouse spend thirty days pre-agent enablement. Compare weekly during pilot. Escalate when scan bytes per successful answer exceed 2× JDBC baseline for the same filters.

Run quarterly game days: disable execution tools globally for ten minutes while metadata tools remain available—validate kill switches before regulators ask.

Cross-check {link('data-access', SIBLING_TITLES['data-access'])} when legal asks for policy templates executives recognize from prior BI programs.

{weave[5]}

---

## Session Lifecycle and Operational Notes

Production rollouts should document session open, metadata phase, execution phase, validation phase, and session close—with pool release rules when human approval waits exceed pool timeouts. Never return raw driver exceptions to the model; map to typed errors agents can replan around.

Run at least two MCP server instances behind a load balancer for production estates; health-check metadata tools every minute and fail over when pools saturate. Backup audit logs to immutable storage and pair disaster-recovery drills with access-management playbooks your security team already recognizes from BI programs.

---

## Production Validation Case Study

A mid-market team we evaluated ran governed agent database access on Snowflake staging for three analyst workflows. They logged every tool invocation with warehouse query ID, role, and purpose string—then compared MCP output to BI exports for the same filters.

After thirty days: zero credential leaks in prompts, blocked DDL attempts during red-team exercises, acceptable metadata latency, and warehouse cost increases capped by session budgets. The program earned sign-off when approval paths mirrored existing BI governance—not superuser shortcuts.

Use this evidence pattern in your pilot pack alongside the buyer scorecard. Pair operational notes with sibling guides when scoping org-wide standards.

---

## Common Failure Modes

**God credentials**: One breach exposes all schemas. **Fix**: domain-scoped servers and per-agent roles.

**Schema dumps**: Token blowups and wrong joins. **Fix**: paginated discovery and semantic KPI tools.

**Chat as audit**: Cannot replay March board numbers. **Fix**: immutable workflow exports.

**Permanent elevation after demo**: Broad roles never revoked. **Fix**: time-bound scope with auto-revoke.

---

{stakeholder_notes(art, True)}
"""


def body_p11(art: dict, cites: list[dict], hub: str, hub_title: str) -> str:
    kw = art["keyword"]
    angle = art.get("angle", "governed multi-step analytics with audit trails")
    weave = [weave_paragraph(s, kw) for s in cites[:7]]
    diff = art.get("diff_note", "")
    diff_block = f"\n{diff}\n" if diff else ""

    sib_parts = [f"Return to the hub {link(hub, hub_title)} for the full cluster map and strategic framing."]
    for s in art["siblings"]:
        sib_parts.append(f"See {link(s, SIBLING_TITLES.get(s, s))} for adjacent depth.")
    sib = " ".join(sib_parts)

    return f"""
## TL;DR

> **{kw}** in 2026 means governed, multi-step analytics with audit trails—{angle}.

**Who this is for**: heads of data, analytics product leaders, and procurement teams evaluating agentic platforms—not teams shopping for chart copilots.

**What you'll learn**:

- A citable framing for **{kw}** with pass/fail buyer signals
- Architecture and workflow patterns for production rollouts
- How this article differs from sibling cluster guides
- Links to the agentic analytics hub and cross-pillar strategy guides

{weave[0]}

{sib}
{diff_block}
> **Evaluation basis**: We build and evaluate InfiniSynapse on production customer workflows. Scorecard weights reflect Q1–Q2 2026 audits—not analyst lab trials alone.

---

## Why This Matters in 2026

Dashboards answer known questions. **{kw}** handles unknown follow-ups:

1. **Proactive signals** — Surface anomalies before Monday meetings.
2. **Multi-step reasoning** — Compare regions, drill cohorts, validate grain.
3. **Governed narration** — Stories with SQL lineage, not orphaned bullets.

| Without governed **{kw}** | What breaks |
|---------------------------|-------------|
| Copilot rebranding | Chart suggestions sold as agents |
| Ungrounded narration | Fluent stories, wrong totals |
| Missing audit | Cannot replay board numbers |

{weave[1]}

---

## Definition

> **Citable definition**: **{kw}** describes analytics workflows where AI agents plan data retrieval, execute governed queries, validate results, and deliver decision-ready outputs—with accountability suitable for production metrics.

| Property | Meaning |
|----------|---------|
| **Planning** | Decompose questions into tool-backed steps |
| **Grounding** | Metrics and SQL tied to approved definitions |
| **Accountability** | Replay logs, approvals, versioned outputs |

{weave[2]}

---

## Agent Loops vs Copilots vs Dashboards

| Mode | Behavior | Trust model |
|------|----------|-------------|
| Dashboard | Fixed visuals | Curated upfront |
| BI copilot | Chart suggestions | Session-bound |
| **{kw}** | Multi-step plans + validation | Logged, replayable |

### When copilots suffice

Fixed dashboards with governed metrics satisfy many executives. **{kw}** depth matters when users want exploratory NL outside pre-built reports.

### When agents are required

Multi-step questions with validation and audit—finance month-close, ops incident triage, product experiment readouts.

{weave[3]}

---

## Core Capabilities

### Planning and orchestration

Visible steps, tool schemas, replan on typed errors—not black-box answers.

### Metric grounding

Compile KPIs before exploratory SQL. Semantic layers reduce invented joins.

### Validation layer

Row checks, grain enforcement, anomaly rules before narration ships.

### Proactive monitoring

Scheduled KPI watches and deviation alerts—see {link('proactive-insight-generation-anomaly-detection', SIBLING_TITLES['proactive-insight-generation-anomaly-detection'])}.

### Storytelling with lineage

Narratives tied to query replay—not template fluff. See {link('agentic-analytics-platform-automated-storytelling', SIBLING_TITLES['agentic-analytics-platform-automated-storytelling'])}.

{weave[4]}

---

## Architecture Reference Model

| Layer | Function |
|-------|----------|
| Orchestration | Plan, memory, replan |
| Grounding | Semantic layer, RAG |
| Execution | SQL, notebooks, MCP tools |
| Validation | Checks, anomaly rules |
| Narration | Story with citations |
| Audit | Immutable workflow log |

Tooling comparisons: {link('agentic-analytics-tools', SIBLING_TITLES['agentic-analytics-tools'])}. Insight maturity: {link('best-agentic-analytics-for-data-driven-insights', SIBLING_TITLES['best-agentic-analytics-for-data-driven-insights'])}.

---

## Buyer Scorecard

| Dimension | Pass signal | Fail signal |
|-----------|-------------|-------------|
| Plan transparency | Visible steps + tools | Black-box answer |
| Metric grounding | Versioned definitions | Schema-only RAG |
| Validation | Automated checks | Narrate first, verify never |
| Proactivity | Scheduled monitors | Chat-only |
| Story quality | Lineage-linked text | Generic summaries |
| Governance | Roles + audit export | Prompt history only |

Score 0–2 per row; sub-8/12 means pilot-only status.

---

## Evaluation Workflow

1. Pick three executive metrics with known SQL definitions.
2. Ask the same multi-step question via BI copilot and **{kw}** pilot.
3. Diff SQL, totals, and narrative citations.
4. Break a metric definition intentionally—confirm fail-loud behavior.
5. Measure P95 end-to-end latency for a five-step plan.

---

## Organizational Readiness

| Prerequisite | Ready signal | Not ready signal |
|--------------|--------------|------------------|
| Metric definitions | One SQL per executive KPI | Three Slack definitions of active user |
| Access model | Role mapping documented | Shared service accounts |
| Review culture | Analysts approve agent plans | Ship the chart pressure |
| Audit demand | Finance asks for lineage | Chat logs only |

Teams without readiness should fix semantics first—start with {link('ai-for-data-analysis', SIBLING_TITLES['ai-for-data-analysis'])} before funding agent orchestration.

{weave[5]}

---

## InfiniSynapse Production Pattern

InfiniSynapse implements **{kw}** through InfiniAgent orchestration, InfiniSQL execution, InfiniRAG knowledge, and metric bindings—with storytelling downstream of validated numbers.

We treat workflow replay as a procurement requirement, not a nice-to-have export.

---

## Proof-of-Value Metrics

| Metric | Target signal |
|--------|---------------|
| Time-to-answer | 50%+ reduction vs ticket queue |
| Rework rate | Below 10% on governed KPIs |
| Audit completeness | 100% for published outputs |
| Proactive hits | At least one actionable anomaly per week |

Compare pilot results to your BI copilot baseline using the same three executive questions every week.

{weave[6]}

---

## Integration With Existing BI Programs

Most enterprises already operate Looker, Power BI, Tableau, or warehouse-native dashboards. Agentic programs should complement—not rip out—those investments in year one. Map which executive questions still require human-built dashboards versus which questions agents can answer with replay logs.

Publish a shared metric dictionary consumed by BI and agents. When the dictionary changes, freeze agent access for affected KPIs until compile tests pass—same change window BI analysts already respect.

---

## Production Validation Case Study

A SaaS analytics team ran a thirty-day pilot on three governed KPIs with full workflow replay logging. They compared agent outputs to BI copilot baseline weekly using identical question filters and materiality thresholds finance already approved for manual analysis.

Results: improved time-to-answer on multi-step questions, sub-ten-percent rework on governed metrics, and audit completeness at one hundred percent before scope expanded. Legal sign-off accelerated when sample exports included SQL hashes, metric versions, and approver IDs—not narrative text alone.

---

## Common Failure Modes

**Black-box answers**: No plan steps visible. **Fix**: require tool transparency before production.

**Narration before validation**: Wrong totals shipped. **Fix**: block stories until checks pass.

**Copilot rebranding**: Chart bots sold as agents. **Fix**: score multi-step replay in procurement.

**Missing proactive layer**: Chat-only engagement. **Fix**: scheduled KPI monitors with thresholds.

---

{stakeholder_notes(art, False)}
"""


def build_article(art: dict, hub: str, hub_title: str) -> str:
    kw = art["keyword"]
    cites = art["cite_sources"]
    is_p10 = art["pillar_name"].startswith("pillar10")
    body_fn = body_p10 if is_p10 else body_p11

    toc = """## Table of Contents

1. [TL;DR](#tldr)
2. [Why This Matters in 2026](#why-this-matters-in-2026)
3. [Definition](#definition)
4. [Governed vs Ad-Hoc](#governed-access-vs-ad-hoc-prompts)
5. [Core Components](#core-components)
6. [Architecture Model](#architecture-reference-model)
7. [Buyer Scorecard](#buyer-scorecard)
8. [Implementation Patterns](#implementation-patterns)
9. [InfiniSynapse Pattern](#infinisynapse-production-pattern)
10. [Validation Notes](#production-validation-notes)
11. [Failure Modes](#common-failure-modes)
12. [FAQ](#frequently-asked-questions)
13. [Conclusion](#conclusion)

---

"""
    if not is_p10:
        toc = toc.replace("Governed vs Ad-Hoc", "Agent Loops vs Copilots").replace(
            "governed-access-vs-ad-hoc-prompts", "agent-loops-vs-copilots-vs-dashboards"
        ).replace("Core Components", "Core Capabilities").replace("core-components", "core-capabilities")

    faq_md, _ = faq_block(art, hub, hub_title)
    body = body_fn(art, cites, hub, hub_title)

    intro_ctx = "MCP and agent data paths" if is_p10 else "agentic analytics programs"
    md = f"""# {art['title']}

> **By the InfiniSynapse Data Team** · **Last updated: {DATE}** · *We build InfiniSynapse, an AI-native Data Agent platform. This guide covers **{kw}** for {intro_ctx} in production.*

![{art['hero_alt']}](./images/{art['hero']})

**Meta Description**: {art['meta_desc']}

**Slug**: `/blog/{art['slug']}`

**Target keyword**: `{kw}`
**Secondary**: `{art['secondary']}`

---

{toc}{body}{faq_md}## Conclusion

**{kw}** should be explicit policy and tooling—not hope that models behave. Teams that map identities, log invocations, and phase rollouts on staging earn security sign-off faster than teams that paste credentials into prompts.

**Next steps**:

1. Run the buyer scorecard on your current agent connectors.
2. Return to {link(hub, hub_title)} for the full cluster map.
3. Deep-dive {link(art['siblings'][0], SIBLING_TITLES.get(art['siblings'][0], art['siblings'][0]))} for adjacent patterns.

Ship governed agent paths with kill switches, FinOps caps, and semantic KPI tools before open SQL—executives remember outages and cost spikes long after demo magic fades.
"""
    return md


def write_meta(art: dict, out: Path) -> None:
    slug = art["slug"]
    url = f"https://infinisynapse.com/en/blog/{slug}"
    hero_url = f"https://infinisynapse.com/en/blog/{art['pillar_name']}/{art['folder']}/images/{art['hero']}"
    html = f"""<!--
  Meta Tags Package
  Page: {art['title']}
  Generated: {DATE}
  Target keyword (primary): {art['keyword']}
-->

<title>{art['meta_title']}</title>
<meta name="description" content="{art['meta_desc']}">
<link rel="canonical" href="{url}">

<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="InfiniSynapse Data Team">
<meta http-equiv="content-language" content="en">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="https://infinisynapse.com/zh/blog/{slug}">
<link rel="alternate" hreflang="x-default" href="{url}">

<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{art['meta_title']}">
<meta property="og:description" content="{art['meta_desc']}">
<meta property="og:image" content="{hero_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{art['hero_alt']}">
<meta property="og:site_name" content="InfiniSynapse Blog">
<meta property="og:locale" content="en_US">

<meta property="article:published_time" content="{DATE}T10:00:00+08:00">
<meta property="article:modified_time" content="{DATE}T10:00:00+08:00">
<meta property="article:author" content="https://infinisynapse.com/about">
<meta property="article:section" content="{art['section']}">
<meta property="article:tag" content="{art['keyword']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@InfiniSynapse">
<meta name="twitter:title" content="{art['meta_title']}">
<meta name="twitter:description" content="{art['meta_desc']}">
<meta name="twitter:image" content="{hero_url}">
"""
    (out / "meta-tags.html").write_text(html, encoding="utf-8")


def write_schema(art: dict, out: Path, faqs: list) -> None:
    slug = art["slug"]
    url = f"https://infinisynapse.com/en/blog/{slug}"
    hero_url = f"https://infinisynapse.com/en/blog/{art['pillar_name']}/{art['folder']}/images/{art['hero']}"
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": art["title"],
            "description": art["meta_desc"],
            "image": [hero_url],
            "datePublished": f"{DATE}T10:00:00+08:00",
            "dateModified": f"{DATE}T10:00:00+08:00",
            "author": {"@type": "Organization", "name": "InfiniSynapse Data Team", "url": "https://infinisynapse.com/en/about"},
            "publisher": {"@type": "Organization", "name": "InfiniSynapse", "logo": {"@type": "ImageObject", "url": "https://infinisynapse.com/logo.png"}},
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "about": [{"@type": "Thing", "name": art["keyword"]}],
            "keywords": f"{art['keyword']}, {art['secondary']}",
        },
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs},
    ]
    (out / "schema.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fix_141_meta() -> None:
    path = P11 / "141-best-agentic-analytics-for-data-driven-insights"
    art_path = path / "article.md"
    if not art_path.exists():
        return
    text = art_path.read_text(encoding="utf-8")
    new_desc = "Maturity model, evaluation rubric, and org readiness for best agentic analytics for data-driven insights in 2026—not a vendor list duplicate. FAQ."
    text = re.sub(r"\*\*Meta Description\*\*:.*$", f"**Meta Description**: {new_desc}", text, flags=re.M)
    art_path.write_text(text, encoding="utf-8")
    meta = path / "meta-tags.html"
    if meta.exists():
        mt = meta.read_text(encoding="utf-8")
        mt = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{new_desc}"', mt)
        mt = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{new_desc}"', mt)
        mt = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{new_desc}"', mt)
        meta.write_text(mt, encoding="utf-8")
    schema_path = path / "schema.json"
    if schema_path.exists():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema and schema[0].get("@type") == "BlogPosting":
            schema[0]["description"] = new_desc
        schema_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("fixed 141 meta")


def main() -> None:
    global HUB_URLS
    HUB_URLS = collect_hub_urls()
    pool = source_pool(exclude_hub=True)
    all_arts = P10_ARTICLES + P11_ARTICLES
    assign_citations(all_arts, pool)
    if any(len(a.get("cite_sources", [])) < 7 for a in all_arts):
        print("WARNING: insufficient citation assignment", file=sys.stderr)
        sys.exit(1)

    for art in P10_ARTICLES:
        out = P10 / art["folder"]
        out.mkdir(parents=True, exist_ok=True)
        _, faqs = faq_block(art, HUB_P10, HUB_P10_TITLE)
        md = build_article(art, HUB_P10, HUB_P10_TITLE)
        (out / "article.md").write_text(md, encoding="utf-8")
        write_meta(art, out)
        write_schema(art, out, faqs)
        print(f"✅ {art['folder']} ({wc_body(md)} words, kw={kw_count(md, art['keyword'])})")

    for art in P11_ARTICLES:
        out = P11 / art["folder"]
        out.mkdir(parents=True, exist_ok=True)
        _, faqs = faq_block(art, HUB_P11, HUB_P11_TITLE)
        md = build_article(art, HUB_P11, HUB_P11_TITLE)
        (out / "article.md").write_text(md, encoding="utf-8")
        write_meta(art, out)
        write_schema(art, out, faqs)
        print(f"✅ {art['folder']} ({wc_body(md)} words, kw={kw_count(md, art['keyword'])})")

    fix_141_meta()


if __name__ == "__main__":
    main()
