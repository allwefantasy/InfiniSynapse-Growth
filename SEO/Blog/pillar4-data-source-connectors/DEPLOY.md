# 前端部署手册 · Pillar 4（15 篇）

> **内容集群**：Data Source Connectors / How-to Integration（规划文档 044–058）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `connect-supabase-to-ai-data-analyst` | `044-connect-supabase-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-supabase-to-ai-data-analyst` |
| `connect-postgres-to-ai-data-analyst` | `045-connect-postgres-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-postgres-to-ai-data-analyst` |
| `connect-mysql-to-ai-data-analyst` | `046-connect-mysql-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-mysql-to-ai-data-analyst` |
| `connect-snowflake-to-ai-analyst` | `047-connect-snowflake-to-ai-analyst/` | `https://infinisynapse.cn/blog/connect-snowflake-to-ai-analyst` |
| `connect-bigquery-to-ai-data-analyst` | `048-connect-bigquery-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-bigquery-to-ai-data-analyst` |
| `connect-databricks-to-ai-analyst` | `049-connect-databricks-to-ai-analyst/` | `https://infinisynapse.cn/blog/connect-databricks-to-ai-analyst` |
| `connect-mongodb-to-ai-data-analyst` | `050-connect-mongodb-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-mongodb-to-ai-data-analyst` |
| `ai-data-analysis-google-sheets` | `051-ai-data-analysis-google-sheets/` | `https://infinisynapse.cn/blog/ai-data-analysis-google-sheets` |
| `ai-data-analysis-csv-files` | `052-ai-data-analysis-csv-files/` | `https://infinisynapse.cn/blog/ai-data-analysis-csv-files` |
| `ai-data-analysis-airtable` | `053-ai-data-analysis-airtable/` | `https://infinisynapse.cn/blog/ai-data-analysis-airtable` |
| `ai-analysis-notion-database` | `054-ai-analysis-notion-database/` | `https://infinisynapse.cn/blog/ai-analysis-notion-database` |
| `connect-clickhouse-to-ai-analyst` | `055-connect-clickhouse-to-ai-analyst/` | `https://infinisynapse.cn/blog/connect-clickhouse-to-ai-analyst` |
| `connect-redshift-to-ai-data-analyst` | `056-connect-redshift-to-ai-data-analyst/` | `https://infinisynapse.cn/blog/connect-redshift-to-ai-data-analyst` |
| `analyze-stripe-data-with-ai` | `057-analyze-stripe-data-with-ai/` | `https://infinisynapse.cn/blog/analyze-stripe-data-with-ai` |
| `analyze-shopify-data-with-ai` | `058-analyze-shopify-data-with-ai/` | `https://infinisynapse.cn/blog/analyze-shopify-data-with-ai` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar4-data-source-connectors/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar4-data-source-connectors
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar4-data-source-connectors
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar4-data-source-connectors
python3 SEO/Blog/sync-audit-gates.py
```

| 指标 | 要求 |
|---|---|
| 正文字数 | 2000–2500（从 `## TL;DR` 起） |
| 关键词密度 | 1.2%–1.7% |
| EEAT 快速扫描 | 12/12 |
| 高 DR 外链 | ≥5 条（DR≥70，叙事嵌入）· `audit-high-dr-links.py` |

## 4. 预览

```bash
python3 SEO/Blog/pillar4-data-source-connectors/build-preview.py
open SEO/Blog/pillar4-data-source-connectors/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar4-data-source-connectors
bash SEO/Blog/pillar4-data-source-connectors/render-all-images.sh
```
