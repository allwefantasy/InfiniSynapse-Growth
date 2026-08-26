# Phase 3 · InfiniSynapse CSV 决策分析 prompt

> **录制时机**：Case B 第 [05]–[06] 段（0:32 – 0:50）
> **执行环境**：`app.infinisynapse.com/tasks` 首页输入框
> **前置条件**：
> 1. 已上传 `semrush-ai-data-analysis-export.csv`（5,400 行）到 `/database/private`，数据源命名 `semrush_ai_data_analysis_2026_06`
> 2. Phase 1 跑出的 60 个种子词已写进 `seeds.csv`（4 列：keyword / source_url / raw_quote / pain_signal），同样作为 CSV 数据源 `seeds_reddit_hn_quora_2026_06` 接入
> 3. （可选）已发布的 4 篇博客标题作为 RAG 上下文：`infinisynapse_blog_published_2026`
> **预期跑动时长**：50–80 秒（5 个 phase）

---

## 提问全文（直接复制）

```text
你是 InfiniSynapse 的内容增长 Copilot,基于以下三个已接入的数据源,
给我产出 "AI data analysis" 赛道的最终投放词表。

【数据源】
1. semrush_ai_data_analysis_2026_06   (CSV, 5,400 行 SEMrush 全量导出)
   字段: keyword / volume / kd / cpc / intent / serp_features / trend_3m
2. seeds_reddit_hn_quora_2026_06       (CSV, 60 行 Phase 1 真实用户种子词)
   字段: keyword / source_url / raw_quote / pain_signal
3. infinisynapse_blog_published_2026   (RAG, 已发 4 篇博客的主题词)

【硬性筛选规则,必须全部满足】
- volume >= 300
- kd <= 35
- intent ∈ {commercial, informational}
- 与 infinisynapse_blog_published_2026 主题重合度 < 60% (避免内卷自家)

【加分项,用于排序】
- A. 出现在 seeds 表里(双源命中) → +30 分
- B. trend_3m 上升 → +20 分
- C. serp_features 含 "AI Overview" 或 "Featured Snippet" → +15 分
   (我们做 GEO 友好的内容,这俩是流量放大器)
- D. cpc >= 3 USD → +10 分(商业意图强)

【最终输出】
1. Top 17 投放词表(按总分倒序),每行包含:
   - rank / keyword / volume / kd / intent / total_score
   - priority(P0/P1/P2,按分数自然分层)
   - landing_page_type(对照表/教程/品类定义/工具评测/集成指南 五选一)
   - reason_one_liner(20 字内一句话讲清为什么入选,
     必须引用 seeds 原话或 SEMrush 数据)

2. Bottom 5 被淘汰代表词,每行说明:
   - keyword / volume / kd
   - rejected_because(20 字内,具体到哪条规则没满足)

3. 一段 80 字的赛道判断:
   "AI data analysis" 这个词族在 2026 Q2 是蓝海还是红海?
   我们应该主攻哪个长尾分支?

【格式要求】
- 用三张图表呈现:
  (1) Top 17 词表 (按 priority 染色的水平条形图,横轴 = total_score)
  (2) volume × kd 散点图,Top 17 用绿点,被淘汰的用灰点
  (3) trend_3m 折线图,只画 Top 17 中 trend 上升的词
- 每条结论必须可追溯到具体行(给出 SQL 或 RAG 引用)
```

---

## 录屏关注点（[05] + [06] 段共用）

| 时间码 | 镜头 | 关键字幕 |
|---|---|---|
| 0:32–0:34 | CSV 文件从 Finder 拖进 InfiniSynapse 输入框（**Drop**） | `Drop your SEMrush export` / 把 SEMrush 词表拖进来 |
| 0:34–0:38 | prompt 文本逐字打出（用 **typewriter** 效果，不要一次全显示，节奏感强） | `One question. Three sources.` / 一句话，三个源 |
| 0:38–0:48 | 5 个 phase 工具行依次出现，特写 Phase 4 的"双源命中加分计算"那一行 | `Cross-checking SEMrush × Reddit` / SEMrush × Reddit 双源命中校验 |
| 0:48–0:50 | 终版输出：Top 17 水平条形图 + 散点图（鼠标在某个绿点上停留 0.5s 弹出 hover 推理） | `17 winners. Every reason explained.` / 17 个入选词，每条理由都给到 |

---

## "现场感"加料镜头（[06] 段最后 4 秒灵魂帧）

Phase 5 跑完以后，**鼠标点开终版词表里某一行的 `.compact-tool-row`**，让推理面板弹出：

```
[ keyword: ai data analysis for excel files ]
✓ rule_volume_300:        2,400 ✓
✓ rule_kd_35:             KD 28 ✓
✓ rule_intent_filter:     informational ✓
✓ rule_blog_overlap:      8% ✓
+ bonus_double_hit:       seeds.csv row 23 → reddit.com/r/Excel/...
+ bonus_trend_up:         +47% in 3m
+ bonus_serp_features:    AI Overview present
total_score: 92  →  P0
landing_page: 教程
```

这一帧停留 4s，是 [06] 段最后一个画面，**让"可解释"具象到一帧之内能看完**。

---

## 备份 & 复用

- 这次 prompt + 数据源 + 任务结果，**录完后用 §5.1 三点菜单 → "Save to memory"** 存进记忆库，命名 `seo-keyword-research-ai-data-analysis-2026-06`。后续如果要拍 Case D（记忆功能延伸）可直接召回。
- `taskId` 跑完回填到 `raw/phase3-taskId.txt`。
