# SEO 博客 · 规则与脚本文件布局（正本）

> **目的**：生成、审计、修复 SEO 文章时，**规则类文档**与**脚本类文件**有且仅有一个正本位置；`SEO/Blog/` 只放**内容产物**，不放规则与脚本源码。

---

## 两个 Skill 目录的分工

| 目录 | 角色 | 放什么 |
|------|------|--------|
| [`Skills/seo-geo-claude-skills-main/`](../../../../seo-geo-claude-skills-main/) | **正本技能库**（完整规则 + 脚本） | 所有 `references/` 规则文档、`scripts/` 审计/修复/生成脚本、配图模板 |
| [`Skills/seo-blog-content-skill/`](../../../../seo-blog-content-skill/) | **薄入口 Skill**（Cursor 快捷指针） | 仅 `SKILL.md`：何时使用、门禁命令、指向正本文档的链接；**不**在此目录新增脚本或规则正文 |

**原则**：写规则 / 写脚本 → 进 `seo-geo-claude-skills-main`；`seo-blog-content-skill` 只做索引与调用说明。

---

## 正本路径对照表

### 1. 规则类文档 → `references/`

| 类型 | 路径 |
|------|------|
| 发布门禁、外链内链、关键词、大纲 | `build/seo-blog-content/references/infinisynapse-blog-full-rules.md` |
| 内容质量、密度、反 AI 模板 | `build/seo-blog-content/references/content-quality-gates.md` |
| 审计命令清单 | `build/seo-blog-content/references/audit-and-fix-commands.md` |
| Pillar Hub 框架 | `build/seo-blog-content/references/pillar-hub-ultimate-guide-framework.md` |
| 配图 / Hero / 正文图规范 | `build/seo-blog-content/references/image-generation-guide.md` |
| 正文数据图 ≥2 维度 | `build/seo-blog-content/references/body-data-chart-rules.md` |
| Hero 封面规格 | `build/seo-content-writer/references/blog-hero-cover-spec.md` |
| 部署 / CMS / 前端交付 | `build/seo-blog-content/references/FRONTEND-DEPLOY-GUIDE.md` 等 |
| Vibe / Reddit GEO 专项 | `build/seo-blog-content/references/reddit-geo-vibe-series-rules.md` |
| **本布局规则** | `build/seo-blog-content/references/skill-file-layout.md`（本文件） |
| 踩坑活文档 | `build/seo-blog-content/references/seo-content-learnings-log.md` |

**新增规则文档**：一律放在 `build/seo-blog-content/references/`（或 `build/seo-content-writer/references/` 若属写作/配图专项），并在 `SKILL.md` 中登记链接。

### 2. 脚本类文件 → `scripts/`

| 类型 | 路径 |
|------|------|
| 审计脚本 `audit-*.py` | `build/seo-blog-content/scripts/` |
| 修复脚本 `fix-*.py` | `build/seo-blog-content/scripts/` |
| 生成脚本 `gen-*.py`、`build-*.py` | `build/seo-blog-content/scripts/` |
| Shell 渲染 / AI 配图 `*.sh` | `build/seo-blog-content/scripts/` |
| 模板 `*.template` | `build/seo-blog-content/scripts/` |
| 共享模块（如 `article_keyword_meta.py`） | `build/seo-blog-content/scripts/` |
| 一次性历史迁移 | `build/seo-blog-content/scripts/_archive/` |

**脚本约定**：

- 产物读写目标为 `SEO/Blog/`（正文、meta、images、handoff 包等），脚本内用 `BLOG = Path(__file__).resolve().parents[N] / "SEO" / "Blog"` 定位，**不要**把脚本本身放在 `SEO/Blog/`。
- Pillar 专项脚本命名：`audit-internal-links-p21-25.py`、`build-visuals-p21-25.py` 等，仍放在 `scripts/`。
- 从仓库根目录调用：

```bash
S="Skills/seo-geo-claude-skills-main/build/seo-blog-content/scripts"
python3 "$S/audit-content-quality.py"
bash "$S/render-html-to-png.sh" all
```

### 3. Skill 入口

| 文件 | 用途 |
|------|------|
| `Skills/seo-blog-content-skill/SKILL.md` | Cursor 薄入口：门禁命令 + 链接到正本 |
| `Skills/seo-geo-claude-skills-main/build/seo-blog-content/SKILL.md` | 完整技能契约、硬规则摘要、Reference 索引 |

### 4. Cursor 轻量规则 → `.cursor/rules/`

| 类型 | 路径 |
|------|------|
| 会话级提醒（密度、外链、活文档等） | `.cursor/rules/seo-*.mdc` |

`.mdc` 文件写**摘要 + 指向正本的链接**，**不**复制完整规则正文；正本变更时同步更新 `.mdc` 中的链接与关键数字。

---

## `SEO/Blog/` 只允许的内容产物

```
SEO/Blog/
  pillar{N}-{topic}/
    {NNN}-{slug}/
      article.md              # 正文
      article-meta.json       # slug / 关键词 sidecar
      meta-tags.html
      schema.json
      head.html               # 可选，部署用
      images/                 # hero、og-cover、正文配图 PNG
      visuals/                # 本篇 hero.html、table-*.html（渲染源）
      prompts/                # 可选 AI 背景 prompt
    articles_registry.json    # 可选，pillar 级规划
    DEPLOY.md                 # 可选，本篇 pillar 部署备忘
  *-topic-cluster-architecture*.md   # 选题/集群架构规划（内容规划，非脚本）
  programmer-handoff-pack/    # 交付包产物
```

**禁止**在 `SEO/Blog/` 根目录新增：

- `audit-*.py` / `fix-*.py` / `gen-*.py` / `build-*.py`
- 规则类 `*.md`（门禁、配图规范、布局说明等）
- 与 Skill 重复的 `SKILL.md`

> **例外**：每篇文章 bundle 内的 `visuals/*.html` 是**本篇配图渲染源**，属于内容产物，留在文章目录。

---

## 新建 SEO 文章时的检查清单

1. **写正文** → 只改 `SEO/Blog/pillar*/**/article.md` 及同目录 meta / images。
2. **新增门禁或写法规则** → 写入 `references/`，更新两个 `SKILL.md` 索引。
3. **新增审计/修复/生成脚本** → 写入 `scripts/`，在 `audit-and-fix-commands.md` 登记命令。
4. **踩坑修复** → 追加 `seo-content-learnings-log.md`；重复问题 promote 到 `references/`。
5. **Cursor 需常驻提醒** → 新增或更新 `.cursor/rules/seo-*.mdc`（指针，非正本）。
6. **不要**在 `SEO/Blog/` 根目录留下脚本副本；历史遗留脚本应迁回 `scripts/` 后删除 Blog 侧副本。

---

## 历史遗留（已迁移 · 2026-07-09）

Pillar 21–25 批次脚本已从 `SEO/Blog/` 收拢至 `build/seo-blog-content/scripts/`（`*-p21-25.py` / `*-p21-25.sh`）。`article_meta.py` 已合并入 `article_keyword_meta.py`。调用见 [`SEO/Blog/README.md`](../../../../SEO/Blog/README.md)。

---

## 相关文档

- [`seo-content-learnings-log.md`](seo-content-learnings-log.md) §2026-07-03 脚本默认存 Skills
- [`Skills/seo-blog-content-skill/SKILL.md`](../../../../seo-blog-content-skill/SKILL.md)
- [`.cursor/rules/seo-skill-file-layout.mdc`](../../../../.cursor/rules/seo-skill-file-layout.mdc)
