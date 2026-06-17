# 文章质量检验规则（Pillar 1–8 · 90 篇）

> **适用范围**：`SEO/Blog/pillar1` … `pillar8` 下所有 `article.md`。  
> **活文档入口**：[`SKILL.md`](./SKILL.md)（外链/内链/关键词/大纲硬规则）+ 本文（内容深度、EEAT、反 AI 模板、发布门禁）。  
> **产品背景**：InfiniSynapse — AI Data Agent 平台（InfiniSQL、InfiniRAG、私有化部署、多源数据分析）。

---

## 角色与目标

执行质检时，以**专业内容质量审核专家**身份工作：从 SEO 技术标准、内容深度、用户体验、品牌一致性四个维度系统性评估，**优先保证质量而非速度**。单篇或批量修改后，须跑通 **11 项离线审计** 至 **90/90 Pass**，并对 Flag 篇做人工通读。

---

## 发布门禁 · 11 项审计（必跑）

在仓库根目录执行；目标 **每脚本 90/90 Pass**，外链重合度 **0 violations / 4005 pairs**。

| # | 脚本 | 检验内容 |
|---|------|----------|
| 1 | `audit-keyword-placeholder.py` | 禁止 `this workflow` / `this connector workflow` 顶替 Target keyword（>1 处 Fail） |
| 2 | `audit-keyword-in-title-desc.py` | H1 + meta title + 两处 description 均含 Target keyword **完整短语** |
| 3 | `audit-keyword-meta-stuffing.py` | 标题/描述各仅 1 次关键词；禁止模板化堆砌 |
| 4 | `audit-outline-structure.py` | **1×H1**；**H2+H3+H4 = 20–30**；层级不跳级 |
| 5 | `audit-internal-links.py` | 禁止 Related Reading；Pillar/Cluster 最低内链覆盖 |
| 6 | `audit-link-placement.py` | 外链叙事嵌入；禁止 `## Sources`；分布正文前 85% |
| 7 | `audit-high-dr-links.py` | ≥5 条高 DR（DR≥70）唯一外链 |
| 8 | `audit-external-link-overlap.py` | 跨篇 URL 重合度 ≤30% |
| 9 | `audit-external-links.py` | 外链 HTTP 200 + 数量 ≥5 |
| 10 | `audit-content-quality.py` | EEAT 信号、反 AI 模板、重复句、标题关键词堆砌 |
| 11 | `audit-wordcount.py` | 字数 + **关键词长度自适应密度** |
| — | `audit-eeat.py` | CORE-EEAT 快扫（12 项；FAQ≥4 问、schema 作者等） |

**一键批量（示例）：**

```bash
cd SEO/Blog
for s in audit-keyword-placeholder audit-keyword-in-title-desc audit-keyword-meta-stuffing \
  audit-outline-structure audit-internal-links audit-link-placement audit-high-dr-links \
  audit-external-link-overlap audit-external-links audit-content-quality audit-wordcount audit-eeat; do
  echo "=== $s ==="; python3 $s.py 2>&1 | tail -3
done
```

**通过标准**：上述 11 项主门禁 + `audit-eeat.py` 均为 **90/90 Pass**；`audit-external-link-overlap.py` 为 **0 violations**。

---

## 1. SEO 技术标准

### 1.1 关键词优化

**统计范围**：正文 = `## TL;DR` 至文末（与 `audit-wordcount.py` 一致；去链接/代码后计词）。

**字数**：**1900–2800** 词（软区间；低于 1900 须扩写，高于 2800 须精简或拆分）。

**密度 · 按关键词词数自适应**（避免长句堆砌）：

| Target keyword 词数 | 可接受密度 |
|---------------------|------------|
| 1–3 词 | 0.6% – 1.8% |
| 4–5 词 | 0.35% – 1.5% |
| 6+ 词 | 0.2% – 1.0% |

**分布要求**：

- 首段（TL;DR / Key Definition）须出现至少 1 次完整 Target keyword
- H2/H3 中含关键词的标题 **≤2 个**（≥3 个 → 标题堆砌 Fail）
- 禁止用 `this workflow` 等无搜索量代词替换主关键词（见 [`SKILL.md` § Target keyword](./SKILL.md)）
- 长关键词可用自然变体（数据源名 + 意图词），**不得**为凑密度重复整句

**修复脚本**：`reduce-keyword-density.py`、`weave-brand-keyword.py`、`fix-this-workflow-placeholder.py`

### 1.2 标题层级

见 [`SKILL.md` § 大纲结构](./SKILL.md)。摘要：

- **1×H1**（文章标题）
- **H2+H3+H4 合计 20–30**
- 每个逻辑块有 H2；H3 在 H2 下，H4 在 H3 下
- 禁止 filler H2（见 §3 反模板）

### 1.3 链接质量

外链、内链、重合度、高 DR 规则见 [`SKILL.md`](./SKILL.md)。内容质量附加要求：

- 正文叙事段内联外链 **≥5**（`audit-content-quality.py`）
- 禁止裸 URL 锚文本、bullet 外链列表、`## Sources`
- 跨篇外链重合度 **≤30%**；修改正文时不得意外删除唯一外链导致 overlap 回归

### 1.4 Meta Description

- 与 H1 同步含 Target keyword **完整短语**（不可截断）
- 各出现 **1 次**；禁止 `Connect {源} to InfiniSynapse for {keyword}…` 等模板
- 修改 `article.md` 后同步 `meta-tags.html` + `schema.json`

---

## 2. EEAT 合规性

`audit-eeat.py` 与 `audit-content-quality.py` 共同覆盖：

| 维度 | 要求 | 审计 ID / 启发式 |
|------|------|------------------|
| **Experience** | 第一人称 / 实操信号（We build/evaluate、hands-on、Evaluation basis） | Exp01 |
| **Expertise** | 术语准确、步骤/表格/工作流 | 人工 + 大纲 |
| **Authoritativeness** | ≥5 外链；可量化 claim（%、分钟、scorecard） | R02、E02 |
| **Trust** | `InfiniSynapse Data Team` 署名；`Last updated: 2026` | T04、R06 |
| **Originality** | scorecard / framework / 一手数据 / 案例指标 | E02、ORIGINALITY_PAT |
| **Structure** | TL;DR、Key Definition、TOC、FAQ **≥4 问** | C02、C04、C09、O01 |
| **Schema** | `schema.json` 存在且 BlogPosting 有 author | O05、Ept01 |

**FAQ 规范**：

- 章节名：`## Frequently Asked Questions` 或 `## FAQ`
- 每问 `### …?` 独立 H3；**≥4 个**问句
- 禁止损坏标题（双问号、关键词被 strip 成乱码）→ `fix-faq-and-headers.py`

---

## 3. 反 AI 模板与 Boilerplate（零容忍）

以下内容在 **90 篇集群内不得出现**（批量 grep 应为 0）：

### 3.1 填充句（自动删除）

匹配 `^Pilot note \d+:`、`^Operational note:`、`^Field note:`、`^Practitioner note:` 且**不含链接**的独立行：

```bash
python3 SEO/Blog/cleanup-pilot-note-filler.py
```

### 3.2 复用 H2 标题（禁止）

跨篇相同的 filler 节名，例如：

- `Operational Readiness Notes`
- `Production Debugging Notes`
- `Field Validation Notes`

**要求**：每篇 H2 须**主题唯一**；合并 boilerplate 时保留全部原外链，改写为数据源/场景专属 prose。

### 3.3 AI 模板句（`audit-content-quality.py` 检测）

禁止出现以下（及同类）固定句式：

- `is most valuable when it is implemented as a recurring operating system`
- `performs best when teams prioritize repeatability over one-off demos`
- `The common thread is not intelligence; it is orchestration`
- `Teams get better outcomes when they pair AI speed with metric contracts`

### 3.4 重复句

- 同一完整句子（>40 字符）出现 **≥2 次** → Fail
- 常见原因：独立 citation 行 verbatim 重复 → `dedup-standalone-citations.py`
- 修复后须重跑 `audit-content-quality.py` 与内链/外链门禁，防止删链回归

### 3.5 占位词

- `this SQL workflow` / `this workflow` 批量替换 Target keyword → Fail
- `Within this topic cluster, explore [A], [B], [C]…` 内链罗列段 → Fail

### 3.6 跨篇去重验收

发布前批量检查（目标 **0 命中**）：

```bash
cd SEO/Blog
grep -rl "Pilot note" pillar*/**/article.md | wc -l          # 0
grep -rl "Operational Readiness Notes" pillar*/**/article.md | wc -l  # 0
grep -rl "this workflow" pillar*/**/article.md | wc -l       # 0（或每篇 ≤1）
grep -rl "Within this topic cluster" pillar*/**/article.md | wc -l    # 0
```

---

## 4. 内容深度与用户体验

### 4.1 必备结构块

```
# H1
## Table of Contents
## TL;DR
## Key Definition（或同等定义块）
## 核心章节 × N
## Frequently Asked Questions（≥4 问）
## Conclusion
```

### 4.2 深度信号（人工抽检）

- **表格 / 清单 / 步骤**：连接器、NL2SQL、工具对比类须有可执行步骤或对比维
- **案例 / 指标**：优先 first-party（如 lobster-moonlight、April baseline）；避免 90 篇共用同一段落
- **产品提及**：`[InfiniSynapse web app](https://app.infinisynapse.cn)`；禁止裸域名锚文本
- **可读性**：段落 3–5 句；避免连续 3+ 条 bullet 代替论述

### 4.3 字数不足时的扩写策略

优先 **主题锚定** 新节，而非堆 filler：

```bash
python3 SEO/Blog/expand-topic-section.py    # H2: Priorities, Pitfalls, and Metrics for {topic}
python3 SEO/Blog/expand-topic-section2.py   # H3: From pilot to durable capability
```

扩写须：与 Target keyword / 数据源相关、含至少 1 条新信息（指标、失败模式、检查项），且不重引入 boilerplate。

---

## 5. 品牌一致性

- 语气：专业、实操、B2B 数据团队；避免营销口号堆砌
- InfiniSynapse 定位：**AI Data Agent**（非泛化 "AI 工具"）
- 能力提及与场景一致：InfiniSQL（NL2SQL）、InfiniRAG、连接器、私有化
- 竞品对比文：客观维度表 + 适用边界，不虚假贬损

---

## 6. 修复工作流（推荐顺序）

1. **结构/元数据**：`fix-faq-and-headers.py` → `fix-keyword-in-title-desc.py` → `fix-outline-structure.py`
2. **关键词**：`fix-this-workflow-placeholder.py` → `reduce-keyword-density.py` / `weave-brand-keyword.py`
3. **Boilerplate**：`cleanup-pilot-note-filler.py` → `dedup-standalone-citations.py` → 人工重写 filler H2
4. **链接**：`fix-internal-links.py` → `fix-external-link-overlap.py` → `patch-high-dr-citations.py`
5. **字数/密度**：`expand-topic-section.py` / 人工扩写 → `rebalance-wordcount-density.py`
6. **同步**：`meta-tags.html`、`schema.json`、`build-preview.py`
7. **验收**：跑 § 发布门禁 11 项 + 跨篇 grep（§3.6）

每步修复后跑**对应 audit 脚本**；大批量改动后跑**全套 11 项**。

---

## 7. 单篇质检报告格式（可选输出）

对 Flag 篇或发布前抽检，可输出：

```markdown
# 质量检测报告 · {slug}

| 维度 | 得分 | 说明 |
|------|------|------|
| SEO 技术标准 | /10 | 字数、密度、标题、meta |
| 链接质量 | /10 | 内外链、DR、重合度 |
| EEAT | /10 | audit-eeat + 内容质量信号 |
| 反 AI / 独特性 | /10 | 重复句、boilerplate、模板句 |
| 品牌一致性 | /10 | 产品表述、语气 |

## 门禁状态
| 脚本 | Pass/Fail | 备注 |
|------|-----------|------|

## 必改项（按优先级）
1. …

## 建议项
1. …
```

完整 CORE-EEAT 评分报告见各篇 `audit.md`（`content-quality-auditor` 格式）。

---

## 8. 相关脚本索引

| 用途 | 脚本 |
|------|------|
| 填充句清理 | `cleanup-pilot-note-filler.py` |
| 重复 citation 行 | `dedup-standalone-citations.py` |
| 降密度 | `reduce-keyword-density.py` |
| 品牌词织入 | `weave-brand-keyword.py` |
| Pillar4 boilerplate 合并 | `reduce-pillar4-boilerplate.py` |
| FAQ/标题修复 | `fix-faq-and-headers.py` |
| 主题扩写 | `expand-topic-section.py`, `expand-topic-section2.py` |
| 高 DR 源池 | `high-dr-authority-sources.py` |
| 内链角色表 | `cluster-link-registry.py` |

硬规则全文：[`SKILL.md`](./SKILL.md) · Cursor 规则：`.cursor/rules/seo-blog-high-dr-citations.mdc`
