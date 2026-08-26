#!/usr/bin/env python3
"""Restore high-DR inline citations on pillar10/pillar11 hub articles."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

HUB_CITES = {
    "127-mcp-for-data-analysis": [
        ("## Why MCP for Data Analysis Matters in 2026", "Adoption benchmarks in the [Stanford HAI AI Index](https://hai.stanford.edu/ai-index) track the shift from pilot demos to governed **MCP for data analysis** rollouts."),
        ("## What Is MCP in Plain Terms", "**MCP for data analysis** rollouts should align with the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) when connectors expose production schemas."),
        ("## Protocol Architecture", "Multi-source connector design should follow [Microsoft's data architecture guidance](https://learn.microsoft.com/en-us/azure/architecture/data-guide/) so metric contracts stay explicit as scope grows."),
        ("## Governance and Security Patterns", "LLM-backed analytics should account for risks in the [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/), especially when MCP servers expose production data."),
        ("## Context Engineering for Tool Calls", "Operational maturity aligns with the [AWS Well-Architected Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/welcome.html) for monitoring and rollback."),
        ("## Buyer Scorecard", "Regulated rollouts often anchor access reviews to [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html) when credentials and audit logs are in scope."),
        ("## Implementation Patterns", "Analytics uptime improves when teams borrow [Google SRE](https://sre.google/sre-book/table-of-contents/) practices for failed query chains."),
    ],
    "128-mcp-for-databases": [
        ("## Why MCP for Databases Matters in 2026", "OLTP connector hygiene should follow [PostgreSQL documentation](https://www.postgresql.org/docs/) for role design and explainable validation queries."),
        ("## Definition", "Snowflake deployments should reference [Snowflake documentation](https://docs.snowflake.com/en/) when defining warehouses and roles for NL2SQL agents."),
        ("## Engine-Specific Patterns", "Redshift connector rollouts should mirror [Amazon Redshift documentation](https://docs.aws.amazon.com/redshift/) for workload isolation and audit-friendly logging."),
        ("## Buyer Scorecard", "Warehouse connector design should follow [Google BigQuery documentation](https://cloud.google.com/bigquery/docs) for dataset boundaries and IAM patterns."),
        ("## Implementation Patterns", "Document-store connectors should follow [MongoDB documentation](https://www.mongodb.com/docs/) for read scopes and aggregation safety."),
        ("## InfiniSynapse Production Pattern", "Foundational warehouse concepts remain essential; [Wikipedia's data warehouse overview](https://en.wikipedia.org/wiki/Data_warehouse) is a concise refresher for reviewers."),
        ("## Common Failure Modes", "The [BIRD benchmark](https://bird-bench.github.io/) adds dirty-schema realism that Spider-only leaderboards under-weight in production."),
    ],
    "129-connect-ai-agent-to-database-mcp": [
        ("## Why Connect AI Agents via MCP in 2026", "Secure AI rollouts should reference [UK NCSC guidelines for secure AI system development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) when wiring database MCP servers."),
        ("## Definition", "EU-facing teams map control expectations using the [European approach to artificial intelligence](https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence)."),
        ("## Wiring Steps", "SQL grounding for agents starts with classical semantics in the [Wikipedia SQL overview](https://en.wikipedia.org/wiki/SQL), especially joins and grain."),
        ("## Security Checklist", "Production ML-adjacent analytics should cross-check [Google Vertex AI documentation](https://cloud.google.com/vertex-ai/docs) for model governance."),
        ("## Buyer Scorecard", "Self-hosted agent deployments should align with [Kubernetes documentation](https://kubernetes.io/docs/) for isolation and secrets."),
        ("## Validation Workflow", "Observability for agentic analytics should follow [OpenTelemetry documentation](https://opentelemetry.io/docs/) so query chains remain traceable."),
        ("## InfiniSynapse Production Pattern", "Lakehouse integrations should use [Databricks documentation](https://docs.databricks.com/en/) for Unity Catalog and SQL warehouse patterns."),
    ],
    "136-agentic-analytics": [
        ("## Why Autonomous Analytics Loops Matter in 2026", "The move from dashboard-first BI to augmented workflows—described in [IBM's augmented analytics overview](https://www.ibm.com/topics/augmented-analytics)—frames how teams should evaluate **agentic analytics**."),
        ("## Definition", "Enterprise AI adoption guidance in [Google Cloud's AI overview](https://cloud.google.com/discover/what-is-artificial-intelligence) mirrors the shift to repeatable decision workflows."),
        ("## Core Capabilities", "Cloud analytics estates should align with the [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) for reliability and security."),
        ("## Architecture Reference Model", "GCP deployments should follow the [Google Cloud architecture framework](https://cloud.google.com/architecture/framework) for service boundaries."),
        ("## Buyer Scorecard", "Azure-centric stacks should reference the [Azure architecture center](https://learn.microsoft.com/en-us/azure/architecture/) when placing analytics agents beside data services."),
        ("## Evaluation Workflow", "Predictive workflows should stay anchored to fundamentals in the [Wikipedia machine learning overview](https://en.wikipedia.org/wiki/Machine_learning)."),
        ("## Vendor Landscape Notes", "Model capability claims should be tempered by work cataloged in [Google Research publications](https://research.google/pubs/)."),
    ],
    "141-best-agentic-analytics-for-data-driven-insights": [
        ("## What Data-Driven Insights Require in 2026", "Quality gates for agents should reference [Wikipedia's data quality overview](https://en.wikipedia.org/wiki/Data_quality) when defining completeness and timeliness checks."),
        ("## Insight Maturity Model", "Semantic alignment work should reference [Wikipedia's conceptual data model overview](https://en.wikipedia.org/wiki/Conceptual_data_model) before agents encode business metrics."),
        ("## Evaluation Rubric", "EU security reviews should reference [ENISA multilayer AI cybersecurity framework](https://www.enisa.europa.eu/publications/multilayer-framework-for-good-cybersecurity-practices-for-ai)."),
        ("## Organizational Readiness", "Public-sector buyers should review [ISO/IEC 42001 AI management systems](https://www.iso.org/standard/81230.html) when procuring analytics agents."),
        ("## Platform Capabilities That Matter", "Access control design should reference [NIST SP 800-53 security controls](https://csrc.nist.gov/pubs/sp/800/53/r5/final) when scoping production agents."),
        ("## Measuring ROI on Insight Velocity", "Analyst-facing outputs should remain accessible under [W3C WCAG 2.1 guidance](https://www.w3.org/TR/WCAG21/) when dashboards reach broad audiences."),
        ("## InfiniSynapse Production Pattern", "Agent safety expectations should reference [Anthropic research](https://www.anthropic.com/research) on reliable tool use."),
    ],
    "144-agentic-analytics-tools": [
        ("## Why Tool Shortlists Matter in 2026", "BI comparison exercises should reference [Tableau Desktop documentation](https://help.tableau.com/current/pro/desktop/en-us/default.htm) when judging visualization depth."),
        ("## Definition", "Ecommerce KPI definitions should reference [Shopify ecommerce analytics guidance](https://www.shopify.com/enterprise/blog/ecommerce-analytics) when normalizing revenue metrics."),
        ("## Capability Layers", "Payments analytics should follow [Stripe documentation](https://docs.stripe.com/) for event models and reporting grains."),
        ("## Buyer Scorecard", "Search and log analytics paths should align with [Elastic documentation](https://www.elastic.co/guide/) when agents query operational data."),
        ("## Evaluation Workflow", "Streaming ingestion patterns align with [Apache Kafka documentation](https://kafka.apache.org/documentation/) when agents consume event feeds."),
        ("## InfiniSynapse Production Pattern", "Spreadsheet-heavy preparation often mirrors [pandas documentation](https://pandas.pydata.org/docs/) patterns for reproducible transforms."),
        ("## Common Failure Modes", "Scripted analysis paths should follow [Python documentation](https://docs.python.org/3/) conventions for testable data utilities."),
    ],
}


def fix_broken_line_136(text: str) -> str:
    return text.replace(
        "[Wikipedia business intelligence overview](https://cloud.google.com/discover/what-is-artificial-intelligence)",
        "[Google Cloud's AI overview](https://cloud.google.com/discover/what-is-artificial-intelligence)",
    )


def main() -> None:
    for folder, inserts in HUB_CITES.items():
        for pillar in ["pillar10-mcp-data-access", "pillar11-agentic-analytics"]:
            path = ROOT / f"SEO/Blog/{pillar}/{folder}/article.md"
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            text = fix_broken_line_136(text)
            for marker, para in inserts:
                if marker not in text:
                    continue
                url_m = re.search(r"\((https?://[^)]+)\)", para)
                if url_m and url_m.group(1).rstrip("/").lower() in text.lower():
                    continue
                if para in text:
                    continue
                text = text.replace(marker, f"{para}\n\n{marker}", 1)
            path.write_text(text, encoding="utf-8")
            print(f"restored {folder}")


if __name__ == "__main__":
    main()
