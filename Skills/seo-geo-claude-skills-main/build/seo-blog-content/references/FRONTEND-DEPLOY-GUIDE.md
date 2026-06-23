# 博客 100 篇 · 前端部署总手册（零 SEO 背景版）

> **读者**：前端 / 全栈 / CMS 集成工程师，不需要懂 SEO。  
> **目标**：知道要建几个页面、每篇文章怎么组装、哪些文件必须原样上线。  
> **内容已写好**：你的工作是「渲染 + 路由 + 列表页」，不是改文案。

---

## 0. 先建立正确心智模型

| 误区 | 实际情况 |
|---|---|
| 要做 100 个不同页面设计 | **只做 1 套文章详情模板** + 约 **12 种内容区块变体** |
| 每篇都要手写 `<head>` | 每篇已有 `meta-tags.html`，**复制粘贴**即可 |
| 要自己写 FAQ 结构化数据 | 每篇已有 `schema.json`，**原样注入** |
| SEO 团队会再改正文 | 正文 `article.md` **不要改**；有问题找内容负责人 |

**你要交付的页面类型：**

```
/blog                          ← 列表页（卡片网格 + 分类筛选）     【1 页】
/blog/:slug                    ← 文章详情（100 个 URL，同一模板）   【1 模板 × 100 路由】
/blog/pillar/:pillar-slug      ← 集群 Hub（可选，8 个）            【MVP-2】
```

机器可读索引：
- **[`blog-index-import-master.json`](./blog-index-import-master.json)** — 列表页直接 import（100 posts）
- [`blog-cms-import-100.csv`](./blog-cms-import-100.csv) — 同数据 CSV 版

本地视觉参考：任意文章文件夹里的 **`preview.html`**（双击浏览器打开，**不要部署到线上**）

---

## 1. 每篇文章 = 一个「发布包」

仓库路径示例：

```
SEO/Blog/pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/
├── article.md          ✅ 必部署（Markdown 正文）
├── meta-tags.html      ✅ 必部署（<head> 标签，见 §3）
├── schema.json         ✅ 必部署（JSON-LD，见 §4）
├── images/             ✅ 必部署（hero + 正文插图）
├── preview.html        ❌ 仅本地预览
├── audit.md            ❌ 运营 QA，不上线
└── README.md           ❌ 交付说明，不上线
```

**路由规则（100 篇统一）：**

```
URL:     https://infinisynapse.com/en/blog/{slug}
slug:    来自 article.md 的 **Slug** 行，或 CSV 的 slug 列
         例：/blog/code-agent-vs-data-agent  →  slug = code-agent-vs-data-agent
注意:    无日期前缀、URL 末尾无斜杠
```

---

## 2. 四步装配流水线（每篇文章相同）

```
article.md  ──→  Markdown 渲染为 HTML body
meta-tags.html ──→  插入 <head>（去注释）
schema.json ──→  插入 <script type="application/ld+json">
images/   ──→  上传 CDN，替换正文与 og:image 路径
```

### Step A · 渲染正文

1. 读 `article.md`
2. **跳过**顶部元数据区（`**Slug**`、`**Target keyword**` 等，在第一个 `---` 之前或之后均可映射为 CMS 字段，但**不要渲染进正文**）
3. Markdown → HTML（支持表格、代码块、链接）
4. **所有 `##` / `###` 标题必须生成 `id`**，与文内 TOC 锚点一致  
   - 例：`## TL;DR` → `<h2 id="tldr">`  
   - 例：`## Frequently Asked Questions` → `<h2 id="frequently-asked-questions">`  
   - slug 算法：小写、空格改 `-`、去掉标点（与 Markdown TOC 链接一致）

5. 内链格式已是 `/en/blog/other-slug` → 保持**站内相对路径**，**不要**加 `rel="nofollow"`

### Step B · 注入 `<head>`

打开 `meta-tags.html`：

- **只复制 HTML 注释以外的行**（`<title>`、`<meta>`、`<link>`）
- 顶部大段 `<!-- ... -->` 是备选标题/描述，**不要上线**
- **不要改** `canonical`、`og:url` 里的 URL — 内容团队已对齐

### Step C · 注入结构化数据

打开 `schema.json`（是一个 **JSON 数组**），整段放进：

```html
<script type="application/ld+json">
[ ... paste schema.json contents ... ]
</script>
```

> **你只需要知道**：这是给搜索引擎看的页面摘要；**原样粘贴**，不要删字段。  
> 其中 `FAQPage` 里的问答必须和页面上 `#frequently-asked-questions` 区块**逐字一致**（内容团队已对齐，你若改 FAQ 展示样式，文字不能变）。

### Step D · 图片

| 用途 | 源文件 | 建议 CDN 路径 |
|---|---|---|
| 社交分享图 | `images/hero*.png` | `/blog/assets/{pillar}/{slug}/hero.png` |
| 正文插图 | `images/*.png` | `/blog/assets/{pillar}/{slug}/{filename}` |

上传后需同步更新三处（可写构建脚本批量替换）：

1. 正文 `<img src>`
2. `meta-tags.html` 里的 `og:image` / `twitter:image`
3. `schema.json` 里的 `image` 数组

Hero 尺寸：**1200 × 630 px**。

---

## 3. 详情页 HTML 骨架（复制即用）

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <!-- ========== 从 meta-tags.html 粘贴（去掉所有注释） ========== -->
  <title>...</title>
  <meta name="description" content="...">
  <link rel="canonical" href="https://infinisynapse.com/en/blog/{slug}">
  <!-- og:* / twitter:* / hreflang ... -->

  <script type="application/ld+json">
  <!-- ========== 粘贴 schema.json 全文 ========== -->
  </script>
</head>
<body>
  <!-- 站点 Header / Nav（你们现有组件） -->

  <article class="blog-post" data-ui-module="{从 CSV 读取 ui_module}">
    <!-- article.md 渲染结果 -->
  </article>

  <!-- 站点 Footer -->
</body>
</html>
```

**参考成品**：[`pillar2/.../014-code-agent-vs-data-agent/preview.html`](./pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/preview.html)  
（含样式 + 完整 head + 正文，本地打开即所见）

---

## 4. 列表页 `/blog` 怎么接

### 数据源

**推荐（100 篇全量，直接 import）：**

[`blog-index-import-master.json`](./blog-index-import-master.json)

```ts
import blogIndex from '@/content/blog-index-import-master.json';

const posts = blogIndex.posts; // 100 条，已含 excerpt / hero_image / ui_module
const categories = blogIndex.category_labels; // 筛选计数
```

若只需 CSV 字段，用 [`blog-cms-import-100.csv`](./blog-cms-import-100.csv)。重新生成：

```bash
python3 SEO/Blog/generate-cms-import-csv.py
python3 SEO/Blog/generate-blog-index-master.py
```

**分 Pillar 增量（历史，已被 master 覆盖）：**

| CSV / JSON 列 | 列表卡片用途 |
|---|---|
| `title` | 卡片标题 |
| `excerpt` | 卡片摘要（120–160 字符，来自 meta description） |
| `url` | 链接 `/blog/{slug}` |
| `hero_image` | 卡片缩略图 |
| `card_tag` | 左上角小标签（Guides / Comparisons / Tools & Reviews …） |
| `filter_category` | 顶部分类筛选 key |
| `sort_priority` | 排序权重（越大越靠前） |
| `ui_module` | 详情页用哪套内容区块（见 §5） |
| `source_path` | 详情页内容包路径 |

### 分类筛选 key（与现有西语 UI 对齐）

| filter_category | 列表标签（西班牙语示例） |
|---|---|
| `all` | Todos |
| `knowledge` | Base de conocimiento y explicaciones |
| `comparisons` | Comparativas y alternativas |
| `tools_reviews` | Herramientas y reseñas |
| `deep_dive` | Análisis técnico a fondo |
| `tutorials` | Tutoriales y buenas prácticas |

文章标题保持**英文**（与现有 24 篇一致）；只有分类标签走 i18n。

### 伪代码

```ts
import blogIndex from './blog-index-import-master.json';
import legacyPosts from './existing-blog-posts';

const allPosts = [...blogIndex.posts, ...legacyPosts]
  .sort((a, b) => b.sort_priority - a.sort_priority);

const visible = category === 'all'
  ? allPosts
  : allPosts.filter(p => p.filter_category === category);
```

---

## 5. 详情模板：12 种 UI 模块（不是 12 套页面）

所有文章共用**同一壳**，按 `ui_module` 切换部分区块样式/组件：

| ui_module | 篇数 | 你额外要做的 UI | 参考 slug |
|---|---:|---|---|
| `long-form-guide` | 26 | 标准长文 + TL;DR 高亮框 | `ai-for-data-analysis` |
| `how-to-steps` | 21 | 步骤编号 / 连接教程卡片 | `connect-supabase-to-ai-data-analyst` |
| `versus-scorecard` | 16 | 对比维度表 + 打分表样式 | `code-agent-vs-data-agent` |
| `use-case-persona` | 13 | 角色/行业标签 + 场景卡片 | `ai-data-analysis-finance` |
| `tool-listicle` | 8 | 工具卡片网格（排名列表） | `best-ai-tools-for-data-analysis` |
| `alternatives-matrix` | 7 | 「替代方案」对比表 | `chatgpt-data-analysis-alternatives` |
| `definition-box` | 2 | 首屏 Key Definition 强调框 | `what-is-a-data-agent` |
| `glossary-terms` | 2 | 术语表 dl/dt/dd 样式 | `data-agent-glossary` |
| `prompt-resource` | 2 | 可复制 Prompt 代码块 | `ai-data-analysis-prompts` |
| `copy-block` | 1 | 一键复制 JD 模板 | `ai-data-analyst-job-description` |
| `product-review` | 1 | 评分卡 Pros/Cons | `infinisynapse-review` |
| `faq-hub` | 1 | FAQ 为主的内容布局 | `ai-analytics-glossary` |

### 每篇文章都有的通用模块（壳层）

这些在 **100 篇里结构一致**，做成固定组件即可：

```
┌─────────────────────────────────────────┐
│ Hero 图 (1200×630) + H1                 │
│ Byline: InfiniSynapse Data Team         │
│ Last updated                            │
├─────────────────────────────────────────┤
│ Sticky TOC（来自 ## Table of Contents） │
├─────────────────────────────────────────┤
│ ## TL;DR              ← Callout 样式    │
│ ## Key Definition     ← 部分文章有      │
│ ## Evaluation basis   ← 部分文章有      │
│ ... 正文 H2/H3 ...                        │
│ ## Frequently Asked Questions ← Accordion│
│ ## Related Reading    ← 内链列表        │
│ ## Conclusion                           │
└─────────────────────────────────────────┘
```

**Versus 类参考正文结构**：[`014-code-agent-vs-data-agent/article.md`](./pillar2-data-agent-vs-alternatives/014-code-agent-vs-data-agent/article.md)

---

## 6. MVP 分期（建议排期）

| 阶段 | 交付 | 覆盖 |
|---|---|---|
| **MVP-1** | 列表页 + 1 套详情壳（长文 + FAQ accordion + TOC） | 可先上 100 篇，样式统一 |
| **MVP-2** | + versus-scorecard / tool-listicle / alternatives-matrix | Pillar 2–3 商业意图页 |
| **MVP-3** | + how-to-steps / glossary / prompt-resource / copy-block | Pillar 4–8 |
| **MVP-4** | 8 个 Pillar Hub 页 + 面包屑 | 内链集群（可选） |

MVP-1 即可全量发布；模块变体可渐进增强，**不影响 URL 与 meta**。

---

## 7. 前端验收清单（不涉及 SEO 审计）

上线前每篇自查（或写自动化测试）：

- [ ] `/blog/{slug}` 200，且与 CSV 中 `url` 一致
- [ ] `<title>` 与页面 H1 主旨一致（都来自 meta-tags / article.md）
- [ ] `canonical` 无尾斜杠
- [ ] `og:image` 可访问，1200×630
- [ ] 正文所有 `/blog/...` 内链可点击
- [ ] 所有 H2/H3 有 `id`，TOC 锚点可跳转
- [ ] FAQ 区块可见，条数与 `schema.json` 中 `FAQPage.mainEntity` 一致
- [ ] 外链 `target="_blank"` + `rel="noopener"`（可选，非必须）
- [ ] 图片均有非空 `alt`（来自 Markdown）

**不需要你跑的内容门禁**（内容团队负责）：

```bash
# 以下脚本由运营/SEO 跑，前端可忽略
python3 SEO/Blog/audit-wordcount.py
python3 SEO/Blog/audit-external-links.py
python3 SEO/Blog/audit-eeat.py
```

---

## 8. 禁止事项（踩了会由内容团队打回）

| 不要做 | 原因 |
|---|---|
| 改 `canonical` / `og:url` 域名或路径 | 会导致重复 URL |
| 给站内 `/blog/...` 内链加 `nofollow` | 破坏内链集群 |
| 删改 FAQ 文案或条数 | 与 schema 不一致，搜索引擎拒收 |
| 把 `audit.md` / `preview.html` 部署上线 | 非用户内容 |
| 在正文加 `## Sources` 外链列表 | 内容已嵌入正文，无需重复 |
| 用 JS 延迟渲染正文 | 影响抓取（SSR/SSG 优先） |

---

## 9. 批量注册路由（构建脚本示例）

```bash
# 列出全部 100 篇路由与源文件
python3 SEO/Blog/generate-cms-import-csv.py   # 刷新 CSV

# 或 shell 遍历
for dir in SEO/Blog/pillar*/[0-9][0-9][0-9]-*/; do
  [ -f "$dir/article.md" ] || continue
  slug=$(basename "$dir" | sed 's/^[0-9]*-//')
  echo "/blog/$slug  →  $dir"
done
```

Next.js App Router 示例：

```ts
// app/blog/[slug]/page.tsx
const posts = loadCsv('SEO/Blog/blog-cms-import-100.csv');

export async function generateStaticParams() {
  return posts.map(p => ({ slug: p.slug }));
}

export async function generateMetadata({ params }) {
  const pkg = getPostPackage(params.slug); // 读 meta-tags.html
  return parseMetaTags(pkg.metaTagsHtml);
}
```

---

## 10. 附录：分 Pillar 详细手册

| Pillar | 篇号 | 详细 DEPLOY |
|---|---|---|
| AI-Native Data Analysis | 001–013 | [pillar1/DEPLOY.md](./pillar1-ai-native-data-analysis/DEPLOY.md) |
| Data Agent vs Alternatives | 014–023 | [pillar2/DEPLOY.md](./pillar2-data-agent-vs-alternatives/DEPLOY.md) |
| AI Analyst Tools | 024–043 | [pillar3/DEPLOY.md](./pillar3-ai-analyst-tools/DEPLOY.md) |
| Data Source Connectors | 044–058 | [pillar4/DEPLOY.md](./pillar4-data-source-connectors/DEPLOY.md) |
| NL2SQL / Text-to-SQL | 059–068 | [pillar5/DEPLOY.md](./pillar5-nl2sql-text-to-sql/DEPLOY.md) |
| Excel / CSV / Spreadsheet | 069–078 | [pillar6/DEPLOY.md](./pillar6-ai-excel-csv-spreadsheet/DEPLOY.md) |
| Use Cases / Role / Industry | 079–094 | [pillar7/DEPLOY.md](./pillar7-use-cases-role-industry/DEPLOY.md) |
| Skills / Templates / Glossary | 095–100 | [pillar8/DEPLOY.md](./pillar8-skills-templates-glossary/DEPLOY.md) |

---

## 11. 一张图总结

```
                    blog-cms-import-100.csv
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
        /blog 列表页                 /blog/:slug 详情
     card_tag / filter            article.md → body
     sort_priority                 meta-tags.html → head
                                   schema.json → JSON-LD
                                   images/ → CDN
              │                           │
              └──────── ui_module ────────┘
                    （12 种区块变体，同一模板）
```

**有问题找谁：**

- 正文/FAQ/链接错了 → 内容团队改 `article.md` + 同步 `schema.json`
- 路由/slug 错了 → 查 CSV 的 `slug` 列
- 样式/交互 → 前端按 `preview.html` 对齐

---

*Last updated: 2026-06-12 · 维护：内容团队更新 CSV；前端更新模板与列表页*
