# 前端部署手册 · Pillar 6（12 篇）

> **内容集群**：AI for Excel / CSV / Spreadsheet（规划文档 069–080）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `clean-excel-data-with-ai` | `069-clean-excel-data-with-ai/` | `https://infinisynapse.cn/blog/clean-excel-data-with-ai` |
| `ai-alternative-to-pivot-table` | `070-ai-alternative-to-pivot-table/` | `https://infinisynapse.cn/blog/ai-alternative-to-pivot-table` |
| `ai-vlookup-replacement` | `071-ai-vlookup-replacement/` | `https://infinisynapse.cn/blog/ai-vlookup-replacement` |
| `ai-excel-formula-generator` | `072-ai-excel-formula-generator/` | `https://infinisynapse.cn/blog/ai-excel-formula-generator` |
| `analyze-csv-with-ai` | `073-analyze-csv-with-ai/` | `https://infinisynapse.cn/blog/analyze-csv-with-ai` |
| `merge-multiple-csv-with-ai` | `074-merge-multiple-csv-with-ai/` | `https://infinisynapse.cn/blog/merge-multiple-csv-with-ai` |
| `deduplicate-data-with-ai` | `075-deduplicate-data-with-ai/` | `https://infinisynapse.cn/blog/deduplicate-data-with-ai` |
| `ai-data-cleaning-techniques` | `076-ai-data-cleaning-techniques/` | `https://infinisynapse.cn/blog/ai-data-cleaning-techniques` |
| `ai-excel-chart-generator` | `077-ai-excel-chart-generator/` | `https://infinisynapse.cn/blog/ai-excel-chart-generator` |
| `ai-financial-modeling-excel` | `078-ai-financial-modeling-excel/` | `https://infinisynapse.cn/blog/ai-financial-modeling-excel` |
| `excel-monthly-report-automation-ai` | `079-excel-monthly-report-automation-ai/` | `https://infinisynapse.cn/blog/excel-monthly-report-automation-ai` |
| `ai-data-wrangling-tools` | `080-ai-data-wrangling-tools/` | `https://infinisynapse.cn/blog/ai-data-wrangling-tools` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar6-ai-excel-csv-spreadsheet/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar6-ai-excel-csv-spreadsheet
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar6-ai-excel-csv-spreadsheet
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar6-ai-excel-csv-spreadsheet
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
python3 SEO/Blog/pillar6-ai-excel-csv-spreadsheet/build-preview.py
open SEO/Blog/pillar6-ai-excel-csv-spreadsheet/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar6-ai-excel-csv-spreadsheet
bash SEO/Blog/pillar6-ai-excel-csv-spreadsheet/render-all-images.sh
```
