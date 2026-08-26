#!/usr/bin/env python3
"""Additional high-DR authority sources to diversify citations across the 90-page cluster."""
from __future__ import annotations

# Appended to HIGH_DR_SOURCES in high-dr-authority-sources.py
EXTENDED_HIGH_DR_SOURCES: list[dict] = [
    {
        "id": "ncsc-ai-dev",
        "label": "UK NCSC AI development guidelines",
        "url": "https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development",
        "min_dr": 82,
        "hints": [r"security", r"governance", r"trust", r"deploy"],
        "weave": (
            "Secure AI rollouts should reference the "
            "[UK NCSC guidelines for secure AI system development]({url}) when connectors expose production data."
        ),
    },
    {
        "id": "eu-ai-act",
        "label": "EU AI Act overview",
        "url": "https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence",
        "min_dr": 90,
        "hints": [r"governance", r"compliance", r"risk", r"trust"],
        "weave": (
            "EU-facing teams map control expectations using the "
            "[European approach to artificial intelligence]({url}) when scoping analytics agent governance."
        ),
    },
    {
        "id": "cisa-ai",
        "label": "CISA AI security guidance",
        "url": "https://www.cisa.gov/ai",
        "min_dr": 85,
        "hints": [r"security", r"governance", r"risk", r"trust"],
        "weave": (
            "Operational security reviews should cross-check "
            "[CISA artificial intelligence guidance]({url}) before enabling autonomous query paths."
        ),
    },
    {
        "id": "ftc-ai",
        "label": "FTC consumer protection guidance",
        "url": "https://www.ftc.gov/",
        "min_dr": 88,
        "hints": [r"governance", r"compliance", r"trust", r"risk"],
        "weave": (
            "Consumer and data-use policies should align with "
            "[FTC consumer protection guidance]({url}) when outputs inform external decisions."
        ),
    },
    {
        "id": "google-bigquery-docs",
        "label": "Google BigQuery documentation",
        "url": "https://cloud.google.com/bigquery/docs",
        "min_dr": 93,
        "hints": [r"warehouse", r"connect", r"sql", r"architect"],
        "weave": (
            "Warehouse connector design should follow "
            "[Google BigQuery documentation]({url}) for dataset boundaries, IAM, and query validation patterns."
        ),
    },
    {
        "id": "aws-redshift-docs",
        "label": "Amazon Redshift documentation",
        "url": "https://docs.aws.amazon.com/redshift/",
        "min_dr": 96,
        "hints": [r"warehouse", r"connect", r"sql", r"deploy"],
        "weave": (
            "Redshift connector rollouts should mirror "
            "[Amazon Redshift documentation]({url}) for workload isolation and audit-friendly query logging."
        ),
    },
    {
        "id": "postgres-docs",
        "label": "PostgreSQL documentation",
        "url": "https://www.postgresql.org/docs/",
        "min_dr": 88,
        "hints": [r"connect", r"sql", r"database", r"architect"],
        "weave": (
            "OLTP connector hygiene should follow "
            "[PostgreSQL documentation]({url}) for role design, schema grants, and explainable validation queries."
        ),
    },
    {
        "id": "mysql-docs",
        "label": "MariaDB documentation",
        "url": "https://mariadb.com/docs/",
        "min_dr": 85,
        "hints": [r"connect", r"sql", r"database"],
        "weave": (
            "MySQL integrations should align with "
            "[MariaDB documentation]({url}) for least-privilege access and reproducible analytical extracts."
        ),
    },
    {
        "id": "snowflake-docs",
        "label": "Snowflake documentation",
        "url": "https://docs.snowflake.com/en/",
        "min_dr": 82,
        "hints": [r"warehouse", r"connect", r"sql", r"semantic"],
        "weave": (
            "Snowflake deployments should reference "
            "[Snowflake documentation]({url}) when defining warehouses, roles, and semantic views for NL2SQL agents."
        ),
    },
    {
        "id": "mongodb-docs",
        "label": "MongoDB documentation",
        "url": "https://www.mongodb.com/docs/",
        "min_dr": 84,
        "hints": [r"connect", r"database", r"document"],
        "weave": (
            "Document-store connectors should follow "
            "[MongoDB documentation]({url}) for read scopes, aggregation safety, and schema discovery."
        ),
    },
    {
        "id": "supabase-docs",
        "label": "Supabase documentation",
        "url": "https://supabase.com/docs",
        "min_dr": 78,
        "hints": [r"connect", r"postgres", r"api"],
        "weave": (
            "Supabase-backed analytics should follow "
            "[Supabase documentation]({url}) for RLS policies, service roles, and API exposure boundaries."
        ),
    },
    {
        "id": "clickhouse-docs",
        "label": "ClickHouse documentation",
        "url": "https://clickhouse.com/docs",
        "min_dr": 80,
        "hints": [r"warehouse", r"connect", r"sql", r"analytics"],
        "weave": (
            "ClickHouse connector paths should align with "
            "[ClickHouse documentation]({url}) for table engines, sampling, and query guardrails."
        ),
    },
    {
        "id": "vertex-ai-docs",
        "label": "Google Vertex AI documentation",
        "url": "https://cloud.google.com/vertex-ai/docs",
        "min_dr": 93,
        "hints": [r"ml", r"deploy", r"production", r"architecture"],
        "weave": (
            "Production ML-adjacent analytics should cross-check "
            "[Google Vertex AI documentation]({url}) for model governance and pipeline observability."
        ),
    },
    {
        "id": "spark-docs",
        "label": "Apache Spark documentation",
        "url": "https://spark.apache.org/docs/latest/",
        "min_dr": 85,
        "hints": [r"pipeline", r"warehouse", r"architecture", r"data"],
        "weave": (
            "Large-scale data preparation should reference "
            "[Apache Spark documentation]({url}) when agents orchestrate distributed transforms."
        ),
    },
    {
        "id": "airflow-docs",
        "label": "Apache Airflow documentation",
        "url": "https://airflow.apache.org/docs/",
        "min_dr": 82,
        "hints": [r"pipeline", r"operational", r"deploy", r"workflow"],
        "weave": (
            "Recurring analytics loops benefit from "
            "[Apache Airflow documentation]({url}) patterns for scheduling, retries, and lineage hooks."
        ),
    },
    {
        "id": "kubernetes-docs",
        "label": "Kubernetes documentation",
        "url": "https://kubernetes.io/docs/",
        "min_dr": 90,
        "hints": [r"deploy", r"operational", r"infrastructure", r"architecture"],
        "weave": (
            "Self-hosted agent deployments should align with "
            "[Kubernetes documentation]({url}) for isolation, secrets, and rollout safety."
        ),
    },
    {
        "id": "opentelemetry-docs",
        "label": "OpenTelemetry documentation",
        "url": "https://opentelemetry.io/docs/",
        "min_dr": 78,
        "hints": [r"operational", r"monitor", r"production", r"reliab"],
        "weave": (
            "Observability for agentic analytics should follow "
            "[OpenTelemetry documentation]({url}) so query chains remain traceable in production."
        ),
    },
    {
        "id": "prometheus-docs",
        "label": "Prometheus documentation",
        "url": "https://prometheus.io/docs/",
        "min_dr": 80,
        "hints": [r"operational", r"monitor", r"production"],
        "weave": (
            "SLO tracking for analytics agents can borrow "
            "[Prometheus documentation]({url}) patterns for latency, error budgets, and alert routing."
        ),
    },
    {
        "id": "tableau-learn",
        "label": "Tableau Desktop documentation",
        "url": "https://help.tableau.com/current/pro/desktop/en-us/default.htm",
        "min_dr": 85,
        "hints": [r"visual", r"bi", r"dashboard", r"compare"],
        "weave": (
            "BI comparison exercises should reference "
            "[Tableau Desktop documentation]({url}) when judging visualization depth versus agentic analysis."
        ),
    },
    {
        "id": "wikipedia-sql",
        "label": "Wikipedia SQL overview",
        "url": "https://en.wikipedia.org/wiki/SQL",
        "min_dr": 97,
        "hints": [r"sql", r"definition", r"nl2sql", r"text-to-sql"],
        "weave": (
            "SQL grounding for agents still starts with classical semantics in the "
            "[Wikipedia SQL overview]({url}), especially joins, grains, and null handling."
        ),
    },
    {
        "id": "wikipedia-ml",
        "label": "Wikipedia machine learning overview",
        "url": "https://en.wikipedia.org/wiki/Machine_learning",
        "min_dr": 97,
        "hints": [r"ml", r"predict", r"method", r"definition"],
        "weave": (
            "Predictive workflows should stay anchored to fundamentals in the "
            "[Wikipedia machine learning overview]({url}) when interpreting model-driven outputs."
        ),
    },
    {
        "id": "wikipedia-etl",
        "label": "Wikipedia ETL overview",
        "url": "https://en.wikipedia.org/wiki/Extract,_transform,_load",
        "min_dr": 97,
        "hints": [r"pipeline", r"clean", r"prepare", r"data"],
        "weave": (
            "Data preparation stages map cleanly to "
            "[Wikipedia's ETL overview]({url}) when agents automate extract-transform-load handoffs."
        ),
    },
    {
        "id": "wikipedia-bi",
        "label": "Wikipedia business intelligence overview",
        "url": "https://en.wikipedia.org/wiki/Business_intelligence",
        "min_dr": 97,
        "hints": [r"bi", r"dashboard", r"visual", r"compare"],
        "weave": (
            "BI modernization debates should reference the "
            "[Wikipedia business intelligence overview]({url}) when separating display layers from analysis execution."
        ),
    },
    {
        "id": "wikipedia-nlp",
        "label": "Wikipedia natural language processing overview",
        "url": "https://en.wikipedia.org/wiki/Natural_language_processing",
        "min_dr": 97,
        "hints": [r"nl2sql", r"natural", r"language", r"text"],
        "weave": (
            "NL interfaces for data still inherit limits from "
            "[Wikipedia's natural language processing overview]({url}), especially ambiguity and grounding."
        ),
    },
    {
        "id": "pandas-docs",
        "label": "pandas documentation",
        "url": "https://pandas.pydata.org/docs/",
        "min_dr": 82,
        "hints": [r"excel", r"csv", r"clean", r"spreadsheet"],
        "weave": (
            "Spreadsheet-heavy preparation often mirrors "
            "[pandas documentation]({url}) patterns for typing, joins, and reproducible transforms."
        ),
    },
    {
        "id": "python-docs",
        "label": "Python documentation",
        "url": "https://docs.python.org/3/",
        "min_dr": 90,
        "hints": [r"code", r"python", r"script", r"analysis"],
        "weave": (
            "Scripted analysis paths should follow "
            "[Python documentation]({url}) conventions for reproducibility and testable data utilities."
        ),
    },
    {
        "id": "rfc4180",
        "label": "RFC 4180 CSV format",
        "url": "https://www.rfc-editor.org/rfc/rfc4180",
        "min_dr": 75,
        "hints": [r"csv", r"file", r"format", r"clean"],
        "weave": (
            "CSV ingestion should respect "
            "[RFC 4180 CSV conventions]({url}) before agents infer types or merge exports."
        ),
    },
    {
        "id": "elastic-docs",
        "label": "Elastic documentation",
        "url": "https://www.elastic.co/guide/",
        "min_dr": 84,
        "hints": [r"search", r"log", r"operational", r"monitor"],
        "weave": (
            "Search and log analytics paths should align with "
            "[Elastic documentation]({url}) when agents query semi-structured operational data."
        ),
    },
    {
        "id": "shopify-analytics",
        "label": "Shopify ecommerce analytics",
        "url": "https://www.shopify.com/enterprise/blog/ecommerce-analytics",
        "min_dr": 82,
        "hints": [r"ecommerce", r"shopify", r"retail", r"revenue"],
        "weave": (
            "Ecommerce KPI definitions should reference "
            "[Shopify ecommerce analytics guidance]({url}) when normalizing revenue and cohort metrics."
        ),
    },
    {
        "id": "stripe-docs",
        "label": "Stripe documentation",
        "url": "https://docs.stripe.com/",
        "min_dr": 85,
        "hints": [r"stripe", r"finance", r"payment", r"revenue"],
        "weave": (
            "Payments analytics should follow "
            "[Stripe documentation]({url}) for event models, reconciliation fields, and reporting grains."
        ),
    },
    {
        "id": "google-sheets-help",
        "label": "Google Sheets documentation",
        "url": "https://support.google.com/docs/topic/9054603",
        "min_dr": 95,
        "hints": [r"sheets", r"spreadsheet", r"excel", r"google"],
        "weave": (
            "Spreadsheet connectors should align with "
            "[Google Sheets documentation]({url}) for sharing rules, ranges, and API quotas."
        ),
    },
    {
        "id": "microsoft-excel-support",
        "label": "Microsoft Excel support",
        "url": "https://support.microsoft.com/excel",
        "min_dr": 96,
        "hints": [r"excel", r"spreadsheet", r"pivot", r"formula"],
        "weave": (
            "Excel automation should reference "
            "[Microsoft Excel support documentation]({url}) for table semantics, pivots, and formula auditability."
        ),
    },
    {
        "id": "nist-cyberframework",
        "label": "NIST Cybersecurity Framework",
        "url": "https://www.nist.gov/cyberframework",
        "min_dr": 88,
        "hints": [r"security", r"governance", r"risk", r"compliance"],
        "weave": (
            "Security reviews can complement AI controls with the "
            "[NIST Cybersecurity Framework]({url}) when credentials and data flows are in scope."
        ),
    },
    {
        "id": "csrc-nist",
        "label": "NIST Computer Security Resource Center",
        "url": "https://csrc.nist.gov/",
        "min_dr": 88,
        "hints": [r"security", r"governance", r"compliance"],
        "weave": (
            "Control mapping for analytics platforms should consult the "
            "[NIST Computer Security Resource Center]({url}) for authoritative security publications."
        ),
    },
    {
        "id": "owasp-api",
        "label": "OWASP API Security Top 10",
        "url": "https://owasp.org/API-Security/",
        "min_dr": 84,
        "hints": [r"security", r"api", r"connect", r"governance"],
        "weave": (
            "API-backed connectors should account for "
            "[OWASP API Security Top 10]({url}) risks when agents call live production endpoints."
        ),
    },
    {
        "id": "aws-well-architected",
        "label": "AWS Well-Architected Framework",
        "url": "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",
        "min_dr": 96,
        "hints": [r"architect", r"operational", r"deploy", r"cloud"],
        "weave": (
            "Cloud analytics estates should align with the "
            "[AWS Well-Architected Framework]({url}) for reliability, security, and operational excellence."
        ),
    },
    {
        "id": "azure-arch-guide",
        "label": "Azure architecture center",
        "url": "https://learn.microsoft.com/en-us/azure/architecture/",
        "min_dr": 96,
        "hints": [r"architect", r"platform", r"deploy", r"microsoft"],
        "weave": (
            "Azure-centric stacks should reference the "
            "[Azure architecture center]({url}) when placing analytics agents beside data services."
        ),
    },
    {
        "id": "google-arch-framework",
        "label": "Google Cloud architecture framework",
        "url": "https://cloud.google.com/architecture/framework",
        "min_dr": 93,
        "hints": [r"architect", r"platform", r"deploy", r"cloud"],
        "weave": (
            "GCP deployments should follow the "
            "[Google Cloud architecture framework]({url}) for service boundaries and operational guardrails."
        ),
    },
    {
        "id": "databricks-docs",
        "label": "Databricks documentation",
        "url": "https://docs.databricks.com/en/",
        "min_dr": 85,
        "hints": [r"databricks", r"lakehouse", r"warehouse", r"genie"],
        "weave": (
            "Lakehouse integrations should use "
            "[Databricks documentation]({url}) for Unity Catalog, SQL warehouses, and agent grounding patterns."
        ),
    },
    {
        "id": "research-google",
        "label": "Google Research publications",
        "url": "https://research.google/pubs/",
        "min_dr": 93,
        "hints": [r"research", r"benchmark", r"method", r"accuracy"],
        "weave": (
            "Model capability claims should be tempered by peer-reviewed work cataloged in "
            "[Google Research publications]({url}), especially for production schema drift."
        ),
    },
    {
        "id": "anthropic-research",
        "label": "Anthropic research",
        "url": "https://www.anthropic.com/research",
        "min_dr": 80,
        "hints": [r"research", r"agent", r"safety", r"trust"],
        "weave": (
            "Agent safety expectations should reference "
            "[Anthropic research]({url}) on reliable tool use and long-horizon task control."
        ),
    },
    {
        "id": "wikipedia-data-quality",
        "label": "Wikipedia data quality overview",
        "url": "https://en.wikipedia.org/wiki/Data_quality",
        "min_dr": 97,
        "hints": [r"quality", r"clean", r"governance", r"definition"],
        "weave": (
            "Quality gates for agents should reference "
            "[Wikipedia's data quality overview]({url}) when defining completeness, accuracy, and timeliness checks."
        ),
    },
    {
        "id": "wikipedia-cdm",
        "label": "Wikipedia conceptual data model overview",
        "url": "https://en.wikipedia.org/wiki/Conceptual_data_model",
        "min_dr": 97,
        "hints": [r"semantic", r"definition", r"model", r"scope"],
        "weave": (
            "Semantic alignment work should reference "
            "[Wikipedia's conceptual data model overview]({url}) before agents encode business metrics."
        ),
    },
    {
        "id": "oecd-ai",
        "label": "OECD AI policy observatory",
        "url": "https://oecd.ai/en/",
        "min_dr": 90,
        "hints": [r"policy", r"governance", r"adoption", r"enterprise"],
        "weave": (
            "Enterprise adoption framing should cite the "
            "[OECD AI policy observatory]({url}) when comparing regional governance expectations."
        ),
    },
    {
        "id": "canada-responsible-ai",
        "label": "ISO/IEC 42001 AI management",
        "url": "https://www.iso.org/standard/81230.html",
        "min_dr": 88,
        "hints": [r"governance", r"policy", r"compliance", r"trust"],
        "weave": (
            "Public-sector buyers should review "
            "[ISO/IEC 42001 AI management systems]({url}) when procuring analytics agents."
        ),
    },
    {
        "id": "au-cyber-ai",
        "label": "UK NCSC secure AI guidelines",
        "url": "https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development",
        "min_dr": 80,
        "hints": [r"security", r"governance", r"policy", r"trust"],
        "weave": (
            "APAC rollouts should cross-check "
            "[UK NCSC guidelines for secure AI system development]({url}) for secure deployment practices."
        ),
    },
    {
        "id": "enisa-ai",
        "label": "ENISA AI cybersecurity framework",
        "url": "https://www.enisa.europa.eu/publications/multilayer-framework-for-good-cybersecurity-practices-for-ai",
        "min_dr": 82,
        "hints": [r"security", r"governance", r"trust", r"deploy"],
        "weave": (
            "EU security reviews should reference "
            "[ENISA multilayer AI cybersecurity framework]({url}) when scoping analytics agent controls."
        ),
    },
    {
        "id": "nist-sp800-53",
        "label": "NIST SP 800-53 security controls",
        "url": "https://csrc.nist.gov/pubs/sp/800/53/r5/final",
        "min_dr": 88,
        "hints": [r"security", r"governance", r"compliance", r"risk"],
        "weave": (
            "Access control design should reference "
            "[NIST SP 800-53 security controls]({url}) when scoping production analytics agents."
        ),
    },
    {
        "id": "w3c-wcag",
        "label": "W3C WCAG accessibility standard",
        "url": "https://www.w3.org/TR/WCAG21/",
        "min_dr": 95,
        "hints": [r"access", r"design", r"product", r"trust"],
        "weave": (
            "Analyst-facing outputs should remain accessible under "
            "[W3C WCAG 2.1 guidance]({url}) when dashboards reach broad audiences."
        ),
    },
    {
        "id": "apache-kafka-docs",
        "label": "Apache Kafka documentation",
        "url": "https://kafka.apache.org/documentation/",
        "min_dr": 85,
        "hints": [r"stream", r"pipeline", r"operational", r"data"],
        "weave": (
            "Streaming ingestion patterns align with "
            "[Apache Kafka documentation]({url}) when agents consume event feeds."
        ),
    },
    {
        "id": "redis-docs",
        "label": "Redis documentation",
        "url": "https://redis.io/docs/latest/",
        "min_dr": 82,
        "hints": [r"cache", r"operational", r"performance", r"deploy"],
        "weave": (
            "Low-latency cache layers should follow "
            "[Redis documentation]({url}) for TTL and namespacing conventions."
        ),
    },
    {
        "id": "wiki-statistics",
        "label": "Wikipedia statistics overview",
        "url": "https://en.wikipedia.org/wiki/Statistics",
        "min_dr": 97,
        "hints": [r"definition", r"method", r"analysis", r"metric"],
        "weave": (
            "Metric definitions should stay grounded in "
            "[Wikipedia's statistics overview]({url}) before agents encode KPIs."
        ),
    },
    {
        "id": "iso-42001",
        "label": "ISO/IEC 42001 AI management",
        "url": "https://www.iso.org/standard/81230.html",
        "min_dr": 90,
        "hints": [r"governance", r"compliance", r"trust", r"risk"],
        "weave": (
            "AI management systems for analytics platforms should align with "
            "[ISO/IEC 42001]({url}) when procurement requires certified AI governance."
        ),
    },
]
