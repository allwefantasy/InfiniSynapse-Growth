---
name: setup-alert
description: Configure monitoring alerts for critical SEO and GEO metrics
argument-hint: "<metric type> <threshold>"
parameters:
  - name: alert_type
    type: string
    required: true
    description: "Alert type: ranking-drop, traffic-change, indexing-issue, backlink-change, geo-visibility, core-web-vitals, technical-error, conversion-rate, all-critical"
  - name: threshold
    type: string
    required: false
    description: Numeric or percentage threshold (e.g., -5, -20%, poor)
  - name: keywords
    type: string
    required: false
    description: Specific keywords to monitor (comma-separated)
  - name: severity
    type: string
    required: false
    description: "Alert priority: high, medium, low"
---

# Setup Alert Command

Configure alerts for SEO/GEO monitoring.

## Route

Use [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md).

## Steps

1. Select alert type, threshold, scope, and severity.
2. Define data source, cadence, trigger logic, and notification owner.
3. Add escalation and false-positive handling.
4. Save configuration when requested.

## Output

Alert name, metric, threshold, cadence, source, severity, owner, and response playbook.
