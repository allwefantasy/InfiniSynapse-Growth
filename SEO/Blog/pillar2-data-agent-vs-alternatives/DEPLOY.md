# 前端部署手册 · Pillar 2（10 篇）

> **内容集群**：Data Agent vs Code Agent vs BI vs Copilot（规划文档 014–023）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `code-agent-vs-data-agent` | `014-code-agent-vs-data-agent/` | `https://infinisynapse.cn/blog/code-agent-vs-data-agent` |
| `data-agent-architecture` | `015-data-agent-architecture/` | `https://infinisynapse.cn/blog/data-agent-architecture` |
| `ai-data-analyst-vs-bi-tools` | `016-ai-data-analyst-vs-bi-tools/` | `https://infinisynapse.cn/blog/ai-data-analyst-vs-bi-tools` |
| `data-agent-vs-llm-chatbot` | `017-data-agent-vs-llm-chatbot/` | `https://infinisynapse.cn/blog/data-agent-vs-llm-chatbot` |
| `chatgpt-data-analysis-limitations` | `018-chatgpt-data-analysis-limitations/` | `https://infinisynapse.cn/blog/chatgpt-data-analysis-limitations` |
| `code-interpreter-vs-data-agent` | `019-code-interpreter-vs-data-agent/` | `https://infinisynapse.cn/blog/code-interpreter-vs-data-agent` |
| `databricks-genie-vs-data-agent` | `020-databricks-genie-vs-data-agent/` | `https://infinisynapse.cn/blog/databricks-genie-vs-data-agent` |
| `ai-data-analyst-vs-human-analyst` | `021-ai-data-analyst-vs-human-analyst/` | `https://infinisynapse.cn/blog/ai-data-analyst-vs-human-analyst` |
| `governance-for-ai-data-analysis` | `022-governance-for-ai-data-analysis/` | `https://infinisynapse.cn/blog/governance-for-ai-data-analysis` |
| `ai-data-analyst-vs-traditional-bi-analyst` | `023-ai-data-analyst-vs-traditional-bi-analyst/` | `https://infinisynapse.cn/blog/ai-data-analyst-vs-traditional-bi-analyst` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar2-data-agent-vs-alternatives/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar2-data-agent-vs-alternatives
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar2-data-agent-vs-alternatives
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar2-data-agent-vs-alternatives
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
python3 SEO/Blog/pillar2-data-agent-vs-alternatives/build-preview.py
open SEO/Blog/pillar2-data-agent-vs-alternatives/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar2-data-agent-vs-alternatives
bash SEO/Blog/pillar2-data-agent-vs-alternatives/render-all-images.sh
```
