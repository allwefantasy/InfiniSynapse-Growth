# InfiniSynapse Blog · 前端交付包（100 篇）

> 内容团队交付 · 可直接 zip 打包集成  
> 生成目录：`SEO/Blog/frontend-handoff/`

## 先看什么（15 分钟）

1. **[FRONTEND-DEPLOY-GUIDE.md](./FRONTEND-DEPLOY-GUIDE.md)** — 部署总手册（零 SEO 背景）
2. **[blog-index-import-master.json](./blog-index-import-master.json)** — 列表页 100 条卡片数据
3. **[PREVIEW-INDEX.html](./PREVIEW-INDEX.html)** — **浏览器打开，点链接预览全部 100 篇文章**

## 如何预览文章（重要）

| 文件 | 双击打开 | 说明 |
|---|---|---|
| **`preview.html`** | ✅ 完整网页 | 本地 UI 参考，**用这个看效果** |
| `meta-tags.html` | ❌ 空白页 | 只是 `<head>` 片段，给前端粘贴用 |
| `article.md` | ✅ 编辑器 | Markdown 源文件 |

桌面浏览器打开 **[PREVIEW-INDEX.html](./PREVIEW-INDEX.html)**，或进入任意文章文件夹打开 `preview.html`。

## 目录结构

```
frontend-handoff/
├── README.md                          ← 本文件
├── PREVIEW-INDEX.html                 ← 100 篇预览入口（浏览器打开）
├── FRONTEND-DEPLOY-GUIDE.md           ← 集成手册
├── blog-index-import-master.json      ← 列表页 import（推荐）
├── blog-cms-import-100.csv            ← 同上，CSV 版
├── ui-modules-reference.json          ← 12 种 UI 变体说明
├── MANIFEST.json                      ← 文件清单统计
└── content/                           ← 100 篇文章发布包
    └── pillar{N}-.../
        └── {id}-{slug}/
            ├── article.md             ← Markdown 正文（上线用）
            ├── meta-tags.html         ← <head> 片段（上线用，勿直接打开）
            ├── schema.json            ← JSON-LD（上线用）
            ├── preview.html           ← 完整预览页（本地看，勿部署）
            └── images/                ← hero + 插图（310 张）
```

## 快速集成

```ts
import blogIndex from './blog-index-import-master.json';

// 列表页
const posts = blogIndex.posts.sort((a, b) => b.sort_priority - a.sort_priority);

// 详情页：slug → source_path
const post = blogIndex.posts.find(p => p.slug === slug);
// 读 content/{pillar}/{folder}/article.md + meta-tags.html + schema.json
```

## 统计

- 文章数：**100**
- 可预览：**100**（均有 preview.html）
- 图片数：**310**
- 路由格式：`/blog/{slug}`（无日期前缀、无尾斜杠）

## 不要部署到线上的文件

| 文件 | 说明 |
|---|---|
| `PREVIEW-INDEX.html` | 本地预览索引 |
| `content/**/preview.html` | 本地 UI 参考 |
| `MANIFEST.json` | 交付清单 |

## 有问题找谁

- 正文 / FAQ / 链接错误 → 内容团队
- 路由 / slug → 查 `blog-index-import-master.json`
- 样式 / 组件 → 按 `ui_module` 字段选变体（见 `ui-modules-reference.json`）
