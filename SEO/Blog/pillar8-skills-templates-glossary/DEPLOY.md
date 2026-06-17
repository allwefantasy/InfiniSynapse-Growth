# 前端部署手册 · Pillar 8（6 篇）

> **内容集群**：AI Data Analyst Skills / Templates / Glossary（规划文档 095–100）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `ai-data-analysis-prompts` | `095-ai-data-analysis-prompts/` | `https://infinisynapse.cn/blog/ai-data-analysis-prompts` |
| `data-analysis-prompt-template` | `096-data-analysis-prompt-template/` | `https://infinisynapse.cn/blog/data-analysis-prompt-template` |
| `ai-data-analyst-skills` | `097-ai-data-analyst-skills/` | `https://infinisynapse.cn/blog/ai-data-analyst-skills` |
| `how-to-evaluate-ai-data-analyst` | `098-how-to-evaluate-ai-data-analyst/` | `https://infinisynapse.cn/blog/how-to-evaluate-ai-data-analyst` |
| `ai-analytics-glossary` | `099-ai-analytics-glossary/` | `https://infinisynapse.cn/blog/ai-analytics-glossary` |
| `data-agent-faq` | `100-data-agent-faq/` | `https://infinisynapse.cn/blog/data-agent-faq` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar8-skills-templates-glossary/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar8-skills-templates-glossary
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar8-skills-templates-glossary
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar8-skills-templates-glossary
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
python3 SEO/Blog/pillar8-skills-templates-glossary/build-preview.py
open SEO/Blog/pillar8-skills-templates-glossary/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar8-skills-templates-glossary
bash SEO/Blog/pillar8-skills-templates-glossary/render-all-images.sh
```
