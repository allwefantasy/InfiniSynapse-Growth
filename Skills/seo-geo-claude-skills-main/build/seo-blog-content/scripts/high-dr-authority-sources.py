#!/usr/bin/env python3
"""Curated high-DR (Domain Rating >= 70) authority sources for blog citations."""
from __future__ import annotations

from urllib.parse import urlparse

# min_dr: editorial estimate for Ahrefs-style DR; used in audit reporting only.
HIGH_DR_SOURCES: list[dict] = [
    {
        "id": "stanford-hai",
        "label": "Stanford HAI AI Index",
        "url": "https://hai.stanford.edu/ai-index",
        "min_dr": 91,
        "hints": [r"why", r"matters", r"adoption", r"enterprise", r"trend"],
        "weave": (
            "Adoption benchmarks in the [Stanford HAI AI Index]({url}) track the same shift from pilot "
            "demos to governed analytics loops we see in customer rollouts."
        ),
    },
    {
        "id": "ibm-augmented",
        "label": "IBM augmented analytics overview",
        "url": "https://www.ibm.com/topics/augmented-analytics",
        "min_dr": 92,
        "hints": [r"evaluat", r"method", r"operational", r"workflow", r"definition", r"scorecard"],
        "weave": (
            "The move from dashboard-first BI to augmented workflows—described in "
            "[IBM's augmented analytics overview]({url})—frames how teams should evaluate tooling here."
        ),
    },
    {
        "id": "nist-ai-rmf",
        "label": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "min_dr": 88,
        "hints": [r"governance", r"security", r"quality", r"compliance", r"risk", r"trust"],
        "weave": (
            "Production rollouts should align access and review controls with the "
            "[NIST AI Risk Management Framework]({url}), especially when recurring queries touch live schemas."
        ),
    },
    {
        "id": "ms-data-arch",
        "label": "Microsoft data architecture guidance",
        "url": "https://learn.microsoft.com/en-us/azure/architecture/data-guide/",
        "min_dr": 96,
        "hints": [r"architect", r"connect", r"infrastructure", r"platform", r"deploy"],
        "weave": (
            "Multi-source connector design should follow [Microsoft's data architecture guidance]({url}) "
            "so domain boundaries and metric contracts stay explicit as scope grows."
        ),
    },
    {
        "id": "owasp-llm",
        "label": "OWASP Top 10 for LLM Applications",
        "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "min_dr": 84,
        "hints": [r"security", r"governance", r"risk", r"trust", r"compliance"],
        "weave": (
            "LLM-backed analytics should account for prompt-injection and data-exfiltration risks in the "
            "[OWASP Top 10 for LLM Applications]({url}), especially when connectors expose production schemas."
        ),
    },
    {
        "id": "google-cloud-ai",
        "label": "Google Cloud AI overview",
        "url": "https://cloud.google.com/discover/what-is-artificial-intelligence",
        "min_dr": 93,
        "hints": [r"why", r"matters", r"adoption", r"enterprise", r"landscape"],
        "weave": (
            "Enterprise AI adoption guidance in [Google Cloud's AI overview]({url}) mirrors the shift from "
            "ad-hoc copilots to repeatable, reviewable decision workflows."
        ),
    },
    {
        "id": "aws-ml-lens",
        "label": "AWS Well-Architected Machine Learning Lens",
        "url": "https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/welcome.html",
        "min_dr": 96,
        "hints": [r"operational", r"reliab", r"deploy", r"production", r"architecture"],
        "weave": (
            "Operational maturity for analytics agents aligns with the "
            "[AWS Well-Architected Machine Learning Lens]({url}), especially around monitoring, rollback, and ownership."
        ),
    },
    {
        "id": "iso-27001",
        "label": "ISO/IEC 27001",
        "url": "https://www.iso.org/isoiec-27001-information-security.html",
        "min_dr": 90,
        "hints": [r"security", r"compliance", r"governance", r"trust"],
        "weave": (
            "Regulated rollouts often anchor access reviews to [ISO/IEC 27001]({url}) when credentials, "
            "retention policies, and audit logs are in scope."
        ),
    },
    {
        "id": "wikipedia-dw",
        "label": "Wikipedia data warehouse overview",
        "url": "https://en.wikipedia.org/wiki/Data_warehouse",
        "min_dr": 97,
        "hints": [r"definition", r"key", r"scope", r"foundation", r"warehouse"],
        "weave": (
            "Foundational warehouse concepts—grain, dimensions, and conformed metrics—remain essential; "
            "[Wikipedia's data warehouse overview]({url}) is a concise refresher for reviewers validating generated SQL."
        ),
    },
    {
        "id": "google-sre",
        "label": "Google SRE book",
        "url": "https://sre.google/sre-book/table-of-contents/",
        "min_dr": 93,
        "hints": [r"operational", r"reliab", r"production", r"failure", r"deploy"],
        "weave": (
            "Analytics uptime improves when teams borrow [Google SRE]({url}) practices—error budgets, runbooks, "
            "and blameless postmortems for failed query chains."
        ),
    },
    {
        "id": "spider-bench",
        "label": "Spider NL2SQL benchmark",
        "url": "https://yale-lily.github.io/spider",
        "min_dr": 75,
        "hints": [r"benchmark", r"evaluat", r"spider", r"accuracy", r"production"],
        "weave": (
            "Leaderboard scores on the [Spider NL2SQL benchmark]({url}) are a useful sanity check but rarely "
            "predict enterprise schema drift on their own."
        ),
    },
    {
        "id": "bird-bench",
        "label": "BIRD NL2SQL benchmark",
        "url": "https://bird-bench.github.io/",
        "min_dr": 72,
        "hints": [r"benchmark", r"bird", r"evaluat", r"accuracy", r"production"],
        "weave": (
            "The [BIRD benchmark]({url}) adds dirty-schema realism that Spider-only leaderboards under-weight in production."
        ),
    },
    {
        "id": "databricks-genie",
        "label": "Databricks Genie architecture post",
        "url": "https://www.databricks.com/blog/pushing-frontier-data-agents-genie",
        "min_dr": 85,
        "hints": [r"warehouse", r"genie", r"agent", r"architecture", r"platform"],
        "weave": (
            "Warehouse vendors describe governed NL2SQL agents in [Databricks' Genie architecture post]({url})—"
            "compare memory depth and audit trails against your internal requirements."
        ),
    },
    {
        "id": "snowflake-cortex",
        "label": "Snowflake Cortex Analyst",
        "url": "https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst",
        "min_dr": 82,
        "hints": [r"warehouse", r"snowflake", r"semantic", r"connect", r"sql"],
        "weave": (
            "[Snowflake Cortex Analyst documentation]({url}) shows how warehouse-native semantic layers change "
            "NL2SQL grounding expectations for analyst-facing products."
        ),
    },
]

import importlib.util as _ilu
from pathlib import Path as _Path

_ext_spec = _ilu.spec_from_file_location(
    "extended_authority_sources",
    _Path(__file__).parent / "extended-authority-sources.py",
)
_ext = _ilu.module_from_spec(_ext_spec)
assert _ext_spec and _ext_spec.loader
_ext_spec.loader.exec_module(_ext)
HIGH_DR_SOURCES.extend(_ext.EXTENDED_HIGH_DR_SOURCES)

PILLAR_EXTRA_IDS: dict[str, list[str]] = {
    "pillar1-ai-native-data-analysis": ["owasp-llm", "google-cloud-ai", "iso-27001", "wikipedia-dw", "google-sre"],
    "pillar3-ai-analyst-tools": ["owasp-llm", "google-cloud-ai", "iso-27001", "aws-ml-lens", "google-sre"],
    "pillar4-data-source-connectors": ["owasp-llm", "snowflake-cortex", "aws-ml-lens", "iso-27001", "google-cloud-ai"],
    "pillar5-nl2sql-text-to-sql": ["spider-bench", "bird-bench", "databricks-genie", "owasp-llm", "google-sre"],
    "pillar6-ai-excel-csv-spreadsheet": ["wikipedia-dw", "google-cloud-ai", "owasp-llm", "iso-27001", "google-sre"],
    "pillar7-use-cases-role-industry": ["iso-27001", "owasp-llm", "google-cloud-ai", "aws-ml-lens", "wikipedia-dw"],
    "pillar8-skills-templates-glossary": ["wikipedia-dw", "iso-27001", "owasp-llm", "google-cloud-ai", "google-sre"],
}

MIN_HIGH_DR_CITATIONS = 5
MIN_SOURCE_DR = 70


def host_of(url: str) -> str:
    return urlparse(url).netloc.lower()


def is_high_dr_url(url: str) -> bool:
    h = host_of(url)
    if "infinisynapse" in h:
        return False
    for src in HIGH_DR_SOURCES:
        if host_of(src["url"]) in h or h in host_of(src["url"]):
            return True
    return False


def source_by_id(sid: str) -> dict:
    for s in HIGH_DR_SOURCES:
        if s["id"] == sid:
            return s
    raise KeyError(sid)
