# QuickCreator 上线页面 · 4 个 SEO 报错修复指南

> 适用：QuickCreator 里已发布的 100 篇博客，On-Page SEO 检查器报的 4 个红色/警告问题。  
> 数据表：**`quickcreator-seo-fields.csv`**（每篇一行，照着粘贴即可）

## 问题根因（一句话）

把文章导入 QuickCreator 时，**只导了正文**，没有把我们写好的 canonical、社交标签填进 QuickCreator 的 SEO 设置；同时 QuickCreator 用自己的标题生成 H1，正文里又留了一个 `# 标题`，所以变成 2 个 H1。**内容本身没问题，是这些字段没填。**

| 报错 | 真实原因 | 怎么修 |
|---|---|---|
| ❌ Canonical URL 缺失 | QuickCreator canonical 字段没填 | 填入表里 `canonical_url` |
| ❌ 多个 H1 | QuickCreator 标题 H1 + 正文 `# 标题` | 删掉正文第一行的标题（见下） |
| ❌ Meta 描述不在 150–160 | 原描述长度不达标（已重写） | 填入表里 `meta_description` |
| ❌ 社交标签缺失 | OG/Twitter 字段没填 | 填入表里 `og_*` / `twitter_*` |

> Meta 描述这次已在源文件全部重写为 150–160 字符，表里就是最新版，直接用。

## 修复步骤（每篇 ~2 分钟）

打开 `quickcreator-seo-fields.csv`，对每篇文章在 QuickCreator 编辑器里：

### 1. Canonical URL
SEO 设置 → Canonical URL 字段 → 粘贴 `canonical_url` 列
（例：`https://infinisynapse.cn/blog/julius-ai-alternatives`）

### 2. 多个 H1 → 删掉正文标题
进入文章正文编辑器，**删除最上面那一行大标题**（就是 `h1_fix` 列里提示的那句）。
QuickCreator 已经用「文章标题」自动生成页面 H1，正文不需要再放一个。
删完后正文应从作者署名 / 引言开始，章节都是 H2。

### 3. Meta Description
SEO 设置 → Meta Description 字段 → 粘贴 `meta_description` 列（已是 150–160 字符）

### 4. Social Media Meta Tags
SEO 设置 → 社交分享 / Open Graph 区域，填：
- OG Title → `og_title`
- OG Description → `og_description`
- OG Image → `og_image`
- Twitter Title / Description / Image → `twitter_*`

> 若 QuickCreator 只有一组「社交标题/描述/图」，用 `og_*` 三个即可。

## 批量做法建议

- 按 `id` 顺序逐篇处理，处理完一篇在表上打勾。
- `og_image` / `twitter_image` 是图片 URL，确保这些图已上传到对应路径能打开（打不开就换成已上线的封面图 URL）。
- 全部填完后，回到 QuickCreator 的 On-Page SEO 面板复查，4 项应变绿。

## 验收（抽 5 篇）

- [ ] Canonical URL 有值，无尾斜杠
- [ ] 页面只有 1 个 H1（正文标题已删）
- [ ] Meta Description 字数显示 150–160
- [ ] 社交标签（OG/Twitter）已填，分享有图有标题

## 想一劳永逸？

如果以后还会**重新导入**内容到 QuickCreator，告诉我你们的导入方式，我可以：
- 把每篇 `article.md` 顶部的 `# 标题` 去掉（避免再次出现双 H1）；
- 或把 canonical / 社交标签直接做成 QuickCreator 能识别的导入格式。

---

*Meta 描述修复脚本：`SEO/Blog/fix-meta-descriptions.py`；字段表脚本：`SEO/Blog/generate-quickcreator-fields.py`；审计：`SEO/Blog/audit-quickcreator-onpage.py`*
