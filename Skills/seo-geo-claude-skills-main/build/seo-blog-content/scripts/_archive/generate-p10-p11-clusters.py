#!/usr/bin/env python3
"""One-off generator for pillar10/pillar11 cluster articles. Run from repo root."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB_P10 = "/en/blog/mcp-for-data-analysis"
HUB_P11 = "/en/blog/agentic-analytics"

ARTICLES = [
    {
        "pillar": "pillar10-mcp-data-access",
        "folder": "130-effective-context-engineering-for-ai-agents",
        "slug": "effective-context-engineering-for-ai-agents",
        "keyword": "effective context engineering for ai agents",
        "title": "Effective Context Engineering for AI Agents: A Data Guide",
        "h1": "Effective Context Engineering for AI Agents: A Data Guide",
        "hero": "hero-effective-context-engineering-for-ai-agents.png",
        "alt": "Effective context engineering for AI agents in data workflows",
        "meta_desc": "Effective context engineering for ai agents: token budgets, tool payloads, session memory, error codes, and rollout scorecard for 2026 data agent teams. FAQ.",
        "meta_title": "Effective Context Engineering for AI Agents",
        "siblings": [
            ("connect-ai-agent-to-database-mcp", "How to Connect an AI Agent to a Database With MCP (2026)"),
            ("data-access", "Data Access for AI Agents: Governance and Patterns (2026)"),
            ("data-accessing", "How AI Agents Handle Data Accessing Safely in 2026"),
        ],
        "sections": [
            ("Why Context Engineering Matters for Data Agents", "Agents fail when tools return megabyte JSON blobs or opaque stack traces. **Effective context engineering for ai agents** treats every token as a budgeted resource—metadata paginated, errors typed, and session state persisted server-side so planners replan instead of drowning in noise."),
            ("Definition", "Citable definition: **effective context engineering for ai agents** is the practice of shaping tool outputs, retrieval payloads, and session memory so LLM planners receive minimal, structured context that preserves task signal while staying within token and cost limits."),
            ("Context Layers in Agent Stacks", "Four layers matter: (1) system instructions, (2) retrieved resources, (3) tool call results, (4) conversation history. Data agents add a fifth—compiled metric context that must not be duplicated each turn."),
            ("Token Budget Framework", "Assign explicit budgets per layer. Metadata discovery: 5–15% of context. Tool results: 40–60%. History: 20–30%. Reserve 10% for replanning. Exceeding budgets triggers server-side summarization—not silent truncation."),
            ("Tool Output Shaping", "Paginate `list_tables`. Return column types and descriptions, not CREATE statements. Cap `run_query` rows server-side. Emit JSON schemas in tool definitions so hosts validate arguments before execution."),
            ("Structured Error Taxonomy", "Replace stack traces with codes: `GRAIN_MISMATCH`, `TIMEOUT`, `POLICY_DENIED`, `SYNTAX_INVALID`. Agents replan when errors are actionable; they hallucinate fixes when errors are opaque."),
            ("Session Memory Patterns", "Persist approved filters, metric versions, and domain scope in the MCP server session—not in the prompt. Reload only deltas each turn. Reduces duplicate catalog fetches by 60–80% in pilot measurements."),
            ("RAG vs Tool Context", "RAG supplies documentation; tools supply live numbers. Mixing them without boundaries causes stale doc context to override fresh query results. Separate channels and label provenance in planner prompts."),
            ("Semantic Layer Context", "When KPI tools exist, inject metric IDs and grain—not raw table lists. Semantic compile outputs are smaller and more accurate than schema dumps for executive questions."),
            ("Multi-Host Consistency", "Document context defaults per host—Claude Desktop, Cursor, internal runtimes. Host-specific limits differ; context engineering must be server-centric so policies survive host swaps."),
            ("Buyer Scorecard", "Score dimensions: pagination, typed errors, session memory, budget enforcement, provenance labels, semantic-first tools. Sub-8/12 means rework before widening tool scope."),
            ("Rollout Playbook", "Week 1: measure baseline tokens per successful answer. Week 2: paginate metadata tools. Week 3: deploy error taxonomy. Week 4: enable session memory. Week 5+: tune budgets with FinOps data."),
            ("InfiniSynapse Production Pattern", "InfiniSynapse applies **effective context engineering for ai agents** in InfiniAgent plans—InfiniRAG retrieval capped per task, InfiniSQL results summarized server-side, metric bindings injected by ID."),
            ("Common Failure Modes", "Failure 1: full schema dumps. Failure 2: stack traces to model. Failure 3: unbounded history. Failure 4: duplicate metric context each turn."),
        ],
        "faqs": [
            ("What is the first context fix?", "Paginate metadata tools and cap query row limits server-side."),
            ("How big should tool results be?", "Enough for the next plan step—typically under 2k tokens for analytics."),
            ("Does context engineering replace governance?", "No. It complements IAM and access policies."),
            ("Where is the MCP hub?", "See MCP for Data Analysis: Connect AI Agents to Your Data (2026)."),
        ],
    },
    {
        "pillar": "pillar10-mcp-data-access",
        "folder": "131-data-access",
        "slug": "data-access",
        "keyword": "data access",
        "title": "Data Access for AI Agents: Governance and Patterns (2026)",
        "h1": "Data Access for AI Agents: Governance and Patterns (2026)",
        "hero": "hero-data-access.png",
        "alt": "Data access governance for AI agents",
        "meta_desc": "Data access for AI agents in 2026: least privilege, policy models, audit patterns, MCP tool boundaries, and buyer scorecard for governed warehouse connectivity. FAQ.",
        "meta_title": "Data Access for AI Agents (2026)",
        "siblings": [
            ("data-access-management", "Data Access Management for AI Analytics: A 2026 Playbook"),
            ("access-management", "Access Management for AI Data Agents: Roles and Controls"),
            ("mcp-for-databases", "MCP for Databases: A 2026 Guide to Agent Data Access"),
        ],
        "sections": [
            ("Why Data Access Matters for Agents", "Generic chat can ignore **data access** rules; production agents must enforce them on every tool call. Without explicit access boundaries, NL2SQL pilots become security incidents."),
            ("Definition", "Citable definition: **data access** for AI agents is the set of policies, roles, and technical controls that determine which principals can invoke which data operations through agent tools—with audit trails suitable for production metrics."),
            ("Policy Models", "Three common models: role-based (RBAC), attribute-based (ABAC), and purpose-based (require justification strings). Agents amplify blast radius—combine models rather than choosing one."),
            ("Least Privilege for Agents", "Default read-only. Expand scopes by ticket, not by prompt. Separate metadata tools from execution tools so discovery does not imply mutation rights."),
            ("Row and Column Controls", "Embed filters at compile time—region, department, data class. Masking PII columns at the server beats hoping the model forgets sensitive fields."),
            ("Audit and Lineage", "Log agent ID, tool name, SQL hash, role, duration, rows returned. Export to the same SIEM used for JDBC. Chat history is not audit."),
            ("MCP as Access Boundary", "MCP servers centralize **data access** enforcement. Hosts never hold superuser credentials. Compare patterns in the MCP hub and database MCP guide."),
            ("Cross-Domain Separation", "Finance, HR, and product should not share one agent role. Domain-scoped MCP servers simplify reviews and incident response."),
            ("Temporary Elevation", "Time-bound scope expansion with approver ID in logs. Auto-revoke after session end. Executives prefer this over permanent broad roles."),
            ("Buyer Scorecard", "Dimensions: least privilege, audit completeness, compile-time filters, separation of duties, kill switches, semantic KPI paths."),
            ("Rollout Playbook", "Inventory data classes. Map agent personas. Stand up read-only metadata. Add KPI tools. Enable SQL only after red-team."),
            ("InfiniSynapse Production Pattern", "InfiniSynapse enforces **data access** through InfiniSQL roles, metric bindings, and workflow logs—same policies for UI and agent paths."),
            ("Common Failure Modes", "Shared service accounts. Schema-only grounding without access rules. Chat logs as audit. Permanent elevation after one demo."),
        ],
        "faqs": [
            ("Is read-only enough for agents?", "Often for pilots—but metadata can still leak sensitive schema hints."),
            ("How does data access differ from access management?", "Access management defines roles; data access applies them per tool invocation."),
            ("Can agents bypass BI governance?", "Only if you let them—MCP servers should mirror BI role mappings."),
            ("Where is the MCP hub?", "See MCP for Data Analysis: Connect AI Agents to Your Data (2026)."),
        ],
    },
    # ... truncated for script - will add all articles in full file
]

if __name__ == "__main__":
    print("Use expanded script")
