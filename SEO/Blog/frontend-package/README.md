# InfiniSynapse 博客 · 前端集成包

> 共 **100** 篇文章 · **310** 张图片 · 可直接 zip 发给前端  
> 生成目录：`SEO/Blog/frontend-package/`

---

## 1. 这个包里有什么

| 文件/目录 | 用途 |
|-----------|------|
| **`集成手册.md`** | 怎么接路由、怎么拼页面（先看这个） |
| **`blog-content-catalog.csv`** | **100 篇内容总目录**（路径、slug、组件类型、部署顺序） |
| **`blog-list.csv`** | 列表页 `/blog` 卡片数据（精简版） |
| **`blog-list.json`** | 同上，JSON 格式 |
| **`articles/`** | 每篇文章的发布文件 |

**本包 intentionally 不包含：** `preview.html`、`audit.md`、SEO 审计脚本、运营说明 — 那些不是上线所需。

---

## 2. 每篇文章文件夹里只有 4 样东西

```
articles/037-infinisynapse-vs-julius-ai/
├── article.md        ← Markdown 正文（渲染成 HTML body）
├── meta-tags.html    ← 复制进 <head>（不是完整网页，浏览器打开会空白）
├── schema.json       ← 粘贴进 <script type="application/ld+json">
└── images/           ← 封面 + 正文插图
```

---

## 3. 三分钟接入

### 列表页 `/blog`

```ts
import rows from './blog-list.json';

const posts = rows.sort((a, b) => b.sort_priority - a.sort_priority);
// 卡片：title, excerpt, url, card_tag, filter_category, hero_filename
```

### 详情页 `/blog/:slug`

1. 在 **`blog-content-catalog.csv`** 里用 `slug` 查到 `内容目录`
2. 读取该目录下的 `article.md` + `meta-tags.html` + `schema.json`
3. 上传 `images/` 到 CDN，替换正文与 og:image 路径

### 路由规则

- URL 格式：`/blog/{slug}`（无日期、无尾斜杠）
- 示例：`/blog/julius-ai-alternatives`

---

## 4. 部署顺序

按 **`blog-content-catalog.csv`** 的 **`部署序号`** 列执行（已按支柱 P1→P8、文章编号排序）。  
`部署动作` 列标明：新发 / 已发更新 / Q2 候选。

---

## 5. 验收（前端自查）

- [ ] `/blog/{slug}` 200，与 CSV 中 `页面URL` 一致
- [ ] `<title>` 来自 `meta-tags.html`，与 H1 一致
- [ ] FAQ 条数与 `schema.json` 里 FAQPage 一致
- [ ] 站内链接 `/blog/...` 可点击，不加 nofollow
- [ ] 图片已上传 CDN，`alt` 非空

**正文/FAQ 内容有问题 → 找内容团队，前端不要改文案。**

---

## 6. 打包命令

```bash
cd SEO/Blog && zip -r frontend-package.zip frontend-package
```
