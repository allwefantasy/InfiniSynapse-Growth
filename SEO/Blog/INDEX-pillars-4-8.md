# SEO Blog · Pillars 4–8 总索引（044–100）

> 基于 [100页主题集群规划-v1-替换后主关键词版.md](../100页主题集群规划-v1-替换后主关键词版.md) · 生成日期 2026-06-09  
> 规范：`Skills/seo-geo-claude-skills-main/` · 门禁：`audit-wordcount.py` / `audit-eeat.py` / `audit-external-links.py`

| Pillar | 目录 | 篇数 | ID 范围 | DEPLOY |
|--------|------|------|---------|--------|
| **4** Data Source Connectors | [pillar4-data-source-connectors](./pillar4-data-source-connectors/) | 15 | 044–058 | [DEPLOY](./pillar4-data-source-connectors/DEPLOY.md) |
| **5** NL2SQL / Text-to-SQL | [pillar5-nl2sql-text-to-sql](./pillar5-nl2sql-text-to-sql/) | 10 | 059–068 | [DEPLOY](./pillar5-nl2sql-text-to-sql/DEPLOY.md) |
| **6** Excel / CSV / Spreadsheet | [pillar6-ai-excel-csv-spreadsheet](./pillar6-ai-excel-csv-spreadsheet/) | 12 | 069–080 | [DEPLOY](./pillar6-ai-excel-csv-spreadsheet/DEPLOY.md) |
| **7** Use Cases · Role / Industry | [pillar7-use-cases-role-industry](./pillar7-use-cases-role-industry/) | 14 | 081–094 | [DEPLOY](./pillar7-use-cases-role-industry/DEPLOY.md) |
| **8** Skills / Templates / Glossary | [pillar8-skills-templates-glossary](./pillar8-skills-templates-glossary/) | 6 | 095–100 | [DEPLOY](./pillar8-skills-templates-glossary/DEPLOY.md) |

**合计：57 篇**（与 Pillar 1 + 3 合计 90 篇可发布包）

## 本地预览

```bash
open SEO/Blog/pillar4-data-source-connectors/INDEX-preview.html
open SEO/Blog/pillar5-nl2sql-text-to-sql/INDEX-preview.html
open SEO/Blog/pillar6-ai-excel-csv-spreadsheet/INDEX-preview.html
open SEO/Blog/pillar7-use-cases-role-industry/INDEX-preview.html
open SEO/Blog/pillar8-skills-templates-glossary/INDEX-preview.html
```

## 批量门禁

```bash
python3 SEO/Blog/audit-wordcount.py
python3 SEO/Blog/audit-eeat.py
python3 SEO/Blog/audit-external-links.py
python3 SEO/Blog/sync-audit-gates.py
```

## Hero 图批量渲染

```bash
python3 SEO/Blog/build-pillar-heroes.py
bash SEO/Blog/render-pillars-4-8-heroes.sh
```

注册表：[pillar-manifests/pillar4-8-articles.json](./pillar-manifests/pillar4-8-articles.json)
