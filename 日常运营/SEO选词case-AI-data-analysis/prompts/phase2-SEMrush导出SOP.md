# Phase 2 · SEMrush 量化导出 SOP

> **执行人**：运营（不需要视频同学，**录屏前 24h 完成**）
> **耗时**：约 25 分钟（含等待导出）
> **产物**：`semrush-ai-data-analysis-export.csv`，约 5,400 行

---

## 步骤 1 · 拿到 Phase 1 的 60 个种子词

跑完 Phase 1 任务后，走 §5.3 "文件" tab → 单文件下载，把 Agent 输出的种子词表存为 `data/seeds_reddit_hn_quora_2026_06.csv`，2 列必备：

| keyword | source_url |
|---|---|
| ai data analysis for excel files | https://reddit.com/r/Excel/comments/... |
| natural language to sql | https://news.ycombinator.com/item?id=... |
| ... | ... |

---

## 步骤 2 · SEMrush Keyword Magic Tool 批量扩词

1. 登录 [semrush.com](https://www.semrush.com/) → **Keyword Magic Tool**
2. 主词输入：`AI data analysis`，Country = `United States`（先做英文池，中文版后续可加 China/.cn 视角）
3. 左侧 filter 设：
   - Volume: `300+`
   - KD %: `0–40`（**先放宽 5 分给 Phase 3 加分项留空间**）
   - Intent: 勾选 `Commercial` + `Informational`，去掉 `Navigational` + `Transactional`
4. 默认会跑出 ~3,800 行，**先按 Volume 倒序**

---

## 步骤 3 · 把 60 个种子词单独跑一遍 Bulk Analysis

1. SEMrush → **Bulk Keyword Analysis**（一次最多 100 个）
2. 把 `seeds.csv` 的 keyword 列**全部粘贴进去**
3. 拿到 60 行结果（含每个种子词的 volume / KD / CPC）
4. 标记一个临时列 `_from_seeds = TRUE`

---

## 步骤 4 · 合并 + 导出

1. **下载步骤 2 的 3,800 行**：右上 Export → CSV → 命名 `magic_tool.csv`
2. **下载步骤 3 的 60 行**：Export → CSV → 命名 `bulk_seeds.csv`
3. 在本地用 Numbers / Excel 按 `keyword` 列做 outer join：
   - magic_tool.csv 没有的种子词追加进去
   - 共享行的 `_from_seeds` 标 `TRUE`，否则空
4. 加一个 `trend_3m` 列：
   - SEMrush Magic Tool 默认带 12 个月 trend，把最近 3 个月的相对斜率算成 `+12%` 这样的字符串
5. 加一个 `serp_features` 列（SEMrush 默认提供，逗号分隔，如 `AI Overview, People Also Ask, Featured Snippet`）
6. 最终保留列（**严格按这个顺序，Phase 3 的 prompt 直接 SQL 引用**）：

```
keyword, volume, kd, cpc, intent, serp_features, trend_3m
```

7. 总行数控制在 **5,000 – 5,500** —— 视觉上是个"看起来很重"的池子，但 InfiniSynapse 跑起来不会卡

---

## 步骤 5 · 上传到 InfiniSynapse

1. `app.infinisynapse.com/database/private` → **新建数据源** → CSV
2. 数据源名：`semrush_ai_data_analysis_2026_06`
3. 表名（自动推断或手填）：`semrush_keywords`
4. 上传完成后**先在普通输入框跑一次基线提问验证**：

```text
用 semrush_ai_data_analysis_2026_06 数据源
统计这个表里 volume >= 1000 且 kd <= 30 的关键词数量,
并按 intent 分组给我一个饼图。
```

能跑出图 + 数字即合格。

---

## 步骤 6 · 把种子词表也上传一份

`seeds_reddit_hn_quora_2026_06.csv` 同样上传成数据源（不要只放本地，否则 Phase 3 跑不到）：

| 字段 | 来源 |
|---|---|
| keyword | Phase 1 输出 |
| source_url | Phase 1 输出 |
| raw_quote | Phase 1 输出 |
| pain_signal | Phase 1 输出 |

---

## ⚠️ 录屏前必检项

| ✅ | 检查项 |
|---|---|
| ☐ | InfiniSynapse 已登录，配额充足（Phase 3 一次任务约消耗 5–8 配额单位） |
| ☐ | 三个数据源都在 `/database/private` 看得到，状态都是"已启用"（不是订阅中） |
| ☐ | SEMrush 浏览器已登录，Magic Tool 页面停在 `AI data analysis` 关键词的搜索结果上（[03] 段镜头要切到这里） |
| ☐ | 桌面只留一个 `semrush-ai-data-analysis-export.csv`，文件名清晰能被观众看清（[04] 段拖文件用） |
| ☐ | 录屏分辨率 1920×1080，OBS 计时器待命 |
