# 前端部署手册 · Pillar 7（14 篇）

> **内容集群**：Use Cases by Role / Industry（规划文档 081–094）

## 1. 路由映射

| slug | 源目录 | 发布 URL |
|---|---|---|
| `ai-tools-for-data-analysts` | `081-ai-tools-for-data-analysts/` | `https://infinisynapse.cn/blog/ai-tools-for-data-analysts` |
| `ai-data-analysis-product-managers` | `082-ai-data-analysis-product-managers/` | `https://infinisynapse.cn/blog/ai-data-analysis-product-managers` |
| `ai-data-analysis-finance-teams` | `083-ai-data-analysis-finance-teams/` | `https://infinisynapse.cn/blog/ai-data-analysis-finance-teams` |
| `ai-data-analysis-marketing` | `084-ai-data-analysis-marketing/` | `https://infinisynapse.cn/blog/ai-data-analysis-marketing` |
| `ai-data-analysis-operations` | `085-ai-data-analysis-operations/` | `https://infinisynapse.cn/blog/ai-data-analysis-operations` |
| `ai-for-data-engineers` | `086-ai-for-data-engineers/` | `https://infinisynapse.cn/blog/ai-for-data-engineers` |
| `ai-data-strategy-cto` | `087-ai-data-strategy-cto/` | `https://infinisynapse.cn/blog/ai-data-strategy-cto` |
| `ai-data-analysis-founders` | `088-ai-data-analysis-founders/` | `https://infinisynapse.cn/blog/ai-data-analysis-founders` |
| `ai-data-analysis-ecommerce` | `089-ai-data-analysis-ecommerce/` | `https://infinisynapse.cn/blog/ai-data-analysis-ecommerce` |
| `ai-data-analysis-saas` | `090-ai-data-analysis-saas/` | `https://infinisynapse.cn/blog/ai-data-analysis-saas` |
| `ai-data-analysis-financial-services` | `091-ai-data-analysis-financial-services/` | `https://infinisynapse.cn/blog/ai-data-analysis-financial-services` |
| `ai-data-analysis-supply-chain` | `092-ai-data-analysis-supply-chain/` | `https://infinisynapse.cn/blog/ai-data-analysis-supply-chain` |
| `ai-data-analysis-healthcare` | `093-ai-data-analysis-healthcare/` | `https://infinisynapse.cn/blog/ai-data-analysis-healthcare` |
| `ai-data-analysis-logistics` | `094-ai-data-analysis-logistics/` | `https://infinisynapse.cn/blog/ai-data-analysis-logistics` |

机器可读清单：[manifest.json](./manifest.json)

## 2. 集成要点

- 正文：`article.md` → HTML，H2/H3 需与 TOC 锚点一致
- `<head>`：`meta-tags.html` + `schema.json` JSON-LD
- 图片 CDN：`/blog/assets/pillar7-use-cases-role-industry/<slug>/hero.png`
- 内链：保持 `/blog/<slug>` 相对路径

## 3. 质量门禁

```bash
python3 SEO/Blog/audit-wordcount.py SEO/Blog/pillar7-use-cases-role-industry
python3 SEO/Blog/audit-eeat.py SEO/Blog/pillar7-use-cases-role-industry
python3 SEO/Blog/audit-external-links.py SEO/Blog/pillar7-use-cases-role-industry
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
python3 SEO/Blog/pillar7-use-cases-role-industry/build-preview.py
open SEO/Blog/pillar7-use-cases-role-industry/INDEX-preview.html
```

## 5. Hero 图

```bash
python3 SEO/Blog/build-pillar-heroes.py pillar7-use-cases-role-industry
bash SEO/Blog/pillar7-use-cases-role-industry/render-all-images.sh
```
