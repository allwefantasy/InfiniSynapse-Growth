# 程序员部署指南 · 100 篇博客 SEO 合规（代码版）

> 面向直接控制部署的程序员。所有 SEO 修复已落到源文件，**照下面接入即可 100% 合规**，无需任何 QuickCreator 后台操作。

## 这次修了什么（源文件已改好）

| 之前的报错 | 修复方式（已完成） |
|---|---|
| Meta 描述不在 150–160 | 100 篇全部重写到 150–160，`article.md` / `meta-tags.html` / `schema.json` / `head.html` / `seo-meta.json` 已同步 |
| 多个 H1 | **已从每篇 `article.md` 正文删除 `# 标题`**；页面 H1 改由模板用标题字段渲染 |
| Canonical 缺失 | 每篇 `head.html` / `seo-meta.json` 已含 canonical |
| 社交标签缺失 | 每篇 `head.html` / `seo-meta.json` 已含完整 OG + Twitter |

## 你拿到的现成产物

| 文件 | 用途 |
|---|---|
| `<article>/head.html` | 每篇一个，**去注释的 `<head>` 片段 + JSON-LD**，直接塞进页面 `<head>` |
| `seo-meta.json` | 100 篇 SEO 元数据合集（按 slug），用于程序化注入（Next.js / SSR / API） |
| `<article>/article.md` | 正文（**已无 H1**，渲染进 `<body>`） |
| `blog-index-import-master.json` | 列表页数据（标题、摘要、分类、slug） |

## 详情页装配（每篇 3 块，规则统一）

```
1) 页面 H1   ← 用文章标题（seo-meta.json 的 title，或列表 JSON 的 title）渲染 <h1>{title}</h1>
2) <head>    ← 注入 head.html（含 canonical / meta description / OG / Twitter / JSON-LD）
3) <body>    ← 渲染 article.md（已无 H1，章节从 H2 开始）
```

### 关键规则（决定 SEO 是否合规）

1. **页面有且仅有 1 个 H1**：由模板从标题渲染。`article.md` 已无 H1，**不要再手动加 H1**。
2. **head.html 原样注入**，不要改里面的 URL（canonical / og:url 已配好）。
3. **所有 H2/H3 生成 `id`**，与正文目录（TOC）锚点一致（如 `## TL;DR` → `<h2 id="tldr">`）。
4. **站内链接 `/blog/xxx` 保持相对路径，不加 `nofollow`**。
5. **正文 SSR/SSG 输出**，不要用 JS 延迟渲染整篇。
6. 图片保留 `alt`（Markdown 已写好）。

## 两种接入方式（任选）

### 方式 A：直接注入 head.html（最简单）

```text
对每篇 /blog/{slug}：
  <head> 内 paste  content/{pillar}/{folder}/head.html
  <body> 内 render content/{pillar}/{folder}/article.md  (markdown→html, 加 heading id)
  <h1>  来自  seo-meta.json[slug].title
```

### 方式 B：用 seo-meta.json 程序化注入（Next.js 示例）

```ts
import seo from '@/content/seo-meta.json';

const bySlug = Object.fromEntries(seo.articles.map(a => [a.slug, a]));

export async function generateMetadata({ params }) {
  const a = bySlug[params.slug];
  return {
    title: a.title,
    description: a.meta_description,
    alternates: { canonical: a.canonical, languages: a.hreflang },
    robots: a.robots,
    openGraph: {
      type: a.og.type, url: a.og.url, title: a.og.title,
      description: a.og.description, siteName: a.og.site_name,
      locale: a.og.locale,
      images: [{ url: a.og.image, width: 1200, height: 630, alt: a.og.image_alt }],
    },
    twitter: {
      card: a.twitter.card, site: a.twitter.site, title: a.twitter.title,
      description: a.twitter.description, images: [a.twitter.image],
    },
  };
}

// JSON-LD: 在页面里输出
// <script type="application/ld+json">{JSON.stringify(a.jsonld)}</script>
```

`seo-meta.json` 每条记录字段：

```jsonc
{
  "slug": "julius-ai-alternatives",
  "url": "https://infinisynapse.cn/blog/julius-ai-alternatives",
  "title": "...", "meta_description": "...(150-160)", "canonical": "...",
  "robots": "index, follow, ...",
  "hreflang": { "en": "...", "zh-CN": "...", "x-default": "..." },
  "og": { "type","url","title","description","image","image_alt","site_name","locale" },
  "twitter": { "card","site","title","description","image" },
  "article": { "published_time","modified_time","section","tags":[...] },
  "jsonld": [ /* BlogPosting + FAQPage + BreadcrumbList */ ]
}
```

## 图片注意

`og.image` / `twitter.image` 是线上图片 URL（如 `/blog/assets/pillar3/.../hero.png`）。
**确保这些图已上传到对应路径能 200 打开**，否则社交分享无图。打不开就替换为已上线的封面图 URL。

## 验收（抽 5 篇，或写自动化）

- [ ] 页面只有 1 个 `<h1>`（DevTools 里 `document.querySelectorAll('h1').length === 1`）
- [ ] `<head>` 有 `<link rel="canonical">`，无尾斜杠
- [ ] `<meta name="description">` 字数 150–160
- [ ] 有 `og:*` 和 `twitter:*` 标签
- [ ] 有 `<script type="application/ld+json">`，内含 FAQPage
- [ ] 正文目录锚点可跳转；`/blog/...` 内链不 404

## 复跑（内容更新后）

```bash
cd SEO/Blog
python3 fix-meta-descriptions.py     # 描述长度归一化（幂等）
python3 strip-leading-h1.py          # 移除正文 H1（幂等）
python3 generate-deploy-meta.py      # 重生成 head.html + seo-meta.json
python3 audit-quickcreator-onpage.py # 复验 4 项（应全 0）
```

---

*审计：`audit-quickcreator-onpage.py`（H1 现要求正文 0 个，页面 H1 由模板渲染）*
