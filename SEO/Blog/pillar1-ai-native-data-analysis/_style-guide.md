# Pillar 1 插图风格指南（v5 · 标题封面 + 正文信息图）

> **Hero / OG**：HTML 渲染 — 文章标题 + 抽象几何装饰（左侧标题，右侧蓝紫渐变图形）  
> **正文图**：HTML 信息图 — 表格、矩阵、流程（有实际专业内容）  
> **已应用**：2026-06-08  
> **Skills 规范**：  
> - Hero：`Skills/seo-geo-claude-skills-main/build/seo-content-writer/references/blog-hero-cover-spec.md`  
> - 预览 HTML：`Skills/seo-geo-claude-skills-main/build/seo-content-writer/references/blog-preview-html-spec.md`

## 视觉规范

### Hero 头图（HTML → PNG · 1200×630）

| 维度 | 规范 |
|------|------|
| 标题 | **必须与 `article.md` H1 完全一致** |
| 背景 | 深科技渐变 `#070b14` → `#0f172a` → `#151030` |
| 主色 | 深蓝 `#1d4ed8` + 紫 `#6d28d9` + 青 `#38bdf8` 光晕 |
| 构图 | 左 54% 白字标题，右 46% 网格 + 发光 SVG 几何 |
| 字体 | 系统无衬线，按标题长度自动缩放 28–42px |
| 品牌 | 左下 `InfiniSynapse` 小字 |

### 正文信息图（HTML → PNG · 1200×720）

| 维度 | 规范 |
|------|------|
| 背景 | 浅灰蓝渐变 `#f8fafc` → `#eef2ff` |
| 主色 | 深蓝表头 `#1e3a8a` + 靛蓝节点 `#4338ca` |
| 结构 | 深色徽章 + H1 + 表格/流程/卡片 |
| 气质 | 科技信息图、对比清晰、可引用 |

## 工具链

```bash
# 1. 生成/更新 HTML（hero 标题来自 build-visuals.py HEROES 列表）
python3 SEO/Blog/pillar1-ai-native-data-analysis/build-visuals.py

# 2. 渲染全部 PNG（hero + body，hero 同步 og-cover.png）
bash SEO/Blog/pillar1-ai-native-data-analysis/render-all-images.sh

# 3. 生成预览 HTML（每篇 preview.html + INDEX-preview.html）
python3 SEO/Blog/pillar1-ai-native-data-analysis/build-preview.py
```

**注意**：修改文章标题后，同步更新 `build-visuals.py` 中 `HEROES` 列表再重跑。

## 各篇插图

| # | Hero 标题（= article H1） | 正文图 |
|---|---------------------------|--------|
| 001 | AI for Data Analysis: The Complete 2026 Guide | 五种分析方法矩阵 |
| 002 | The Data Agent Manifesto: Why the First Ship Launches Here | 场景对比表 |
| 003 | What Is a Data Agent? Definition, Architecture, and Examples | 四层架构栈 |
| 004 | What Is an AI-Native Data Platform? (2026 Buyer's Guide) | 五支柱 RFP |
| 005 | Best Agentic Analytics Tools for Data-Driven Insights (2026) | 时间线 + 决策矩阵 |
| 006 | What Is an Autonomous Data Agent? | 自修正决策树 |
| 007 | AI Data Analyst: Role, Tools, and Workflow in 2026 | 职责矩阵 |
| 008 | AI Data Analyst Job Description: 2026 Template + Skills Matrix | 技能矩阵 |
| 009 | AI Agent Memory for Data: Why Distillation Beats Chat History | 记忆卡解剖 |
| 010 | Fabric Data Agent vs Copilot: Which Fits Your Microsoft Stack? | 四象限 + 选型表 |
| 011 | AI-Native vs Augmented Analytics: What's the Real Difference? | 五支柱映射 |
| 012 | AI Data Analysis: Methods, Tools, and Best Practices (2026) | 七阶段流程 |
| 013 | Data Agent Glossary: 15 Terms Every Analytics Team Should Know | 术语关系图 |
