# 前端部署手册 · Pillar 5（10 篇）

> **内容集群**：NL2SQL / Text-to-SQL / AI SQL（规划文档 059–068）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `natural-language-to-sql` | `059-natural-language-to-sql/` | `https://infinisynapse.cn/blog/natural-language-to-sql` |
| `text-to-sql-llm` | `060-text-to-sql-llm/` | `https://infinisynapse.cn/blog/text-to-sql-llm` |
| `nl2sql-benchmark-spider-bird` | `061-nl2sql-benchmark-spider-bird/` | `https://infinisynapse.cn/blog/nl2sql-benchmark-spider-bird` |
| `ai-sql-generator` | `062-ai-sql-generator/` | `https://infinisynapse.cn/blog/ai-sql-generator` |
| `llm-sql-generation-architecture` | `063-llm-sql-generation-architecture/` | `https://infinisynapse.cn/blog/llm-sql-generation-architecture` |
| `sql-rag-vs-semantic-layer` | `064-sql-rag-vs-semantic-layer/` | `https://infinisynapse.cn/blog/sql-rag-vs-semantic-layer` |
| `text-to-sql-fine-tuning` | `065-text-to-sql-fine-tuning/` | `https://infinisynapse.cn/blog/text-to-sql-fine-tuning` |
| `sql-agent-vs-text-to-sql` | `066-sql-agent-vs-text-to-sql/` | `https://infinisynapse.cn/blog/sql-agent-vs-text-to-sql` |
| `nl2sql-production-failure-modes` | `067-nl2sql-production-failure-modes/` | `https://infinisynapse.cn/blog/nl2sql-production-failure-modes` |
| `dialect-aware-sql-generation` | `068-dialect-aware-sql-generation/` | `https://infinisynapse.cn/blog/dialect-aware-sql-generation` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar5-nl2sql-text-to-sql/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar5-nl2sql-text-to-sql
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar5-nl2sql-text-to-sql
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar5-nl2sql-text-to-sql
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
python3 SEO/Blog/pillar5-nl2sql-text-to-sql/build-preview.py
open SEO/Blog/pillar5-nl2sql-text-to-sql/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar5-nl2sql-text-to-sql
bash SEO/Blog/pillar5-nl2sql-text-to-sql/render-all-images.sh
```
