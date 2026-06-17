# InfiniSynapse 100 词 P0/P1/P2 重排 prompt

> **执行环境**：`app.infinisynapse.com/tasks` 首页输入框（不开模板提问，直接粘贴）
> **前置**：上传两个数据源到 `/database/private`
>   1. `keywords_100_master`（CSV）→ `SEO/100页关键词验证/keywords-100-master.csv`
>   2. `semrush_bulk_2026_06`（CSV）→ `SEO/100页关键词验证/output/bulk-export-<YYYY-MM-DD>.csv`
> **预期跑动时长**：90-150 秒（5 个 phase）

---

## 提问全文（直接复制）

```text
你是 InfiniSynapse 的 SEO 内容增长 Copilot, 现在用以下两个 CSV 数据源,
为我把 100 个英文 SEO 关键词的优先级 P0 / P1 / P2 用真实 SEMrush 数据重新排定.

【数据源】
1. keywords_100_master            (CSV, 100 行)
   字段: no / keyword / pillar / slug / planned_priority / content_type /
        buyer_stage / is_published / published_url / notes
   说明: planned_priority 是策略侧的先验分级 (P0/P1/P2/SHIPPED).
         这次任务要用 SEMrush 数据校准它.

2. semrush_bulk_2026_06           (CSV, 100 行)
   字段: keyword / volume / kd / cpc / intent / trend_3m /
        has_ai_overview / has_featured_snippet / has_paa / serp_features_raw

【任务】

Step 1. 用 keyword 做 inner join 把两表合并 (应得 100 行, is_published=TRUE 的 6 行也参与计算
        但最终只输出"非 SHIPPED 的 94 行"作为决策范围).

Step 2. 套用以下评分模型 (来自 SEO/100页主题集群规划-v1.md §11):

   【硬性筛选, 必须全部满足才进决策池】
   - volume >= 300
   - kd <= 35
   - intent IN ('commercial', 'informational', 'mixed')
   - (品牌词例外: 关键词包含 'infinisynapse' 的不卡 volume 下限)

   【基础分: 60 分】每个进入决策池的词起跳 60 分.

   【加分项, 累加到 total_score】
   A. has_ai_overview = TRUE        → +15 分  (GEO 流量放大器)
   B. has_featured_snippet = TRUE   → +15 分  (传统 SEO 放大器)
   C. has_paa = TRUE                → +10 分  (PAA 命中)
   D. trend_3m = 'up'               → +20 分  (Phase 3 同口径)
   E. cpc >= 3.0                    → +10 分  (商业意图强)
   F. intent = 'commercial'         → +10 分  (vs informational)
   G. buyer_stage = 'BOFU'          → +10 分  (vs MOFU/TOFU, 转化漏斗近)
   H. content_type IN ('comparison', 'alternatives', 'product review')
                                    → +10 分  (高商业意图模板)
   I. pillar IN ('P3', 'P4')        → +5 分   (转化主力 Pillar 略加权)

   【硬性扣分】
   - volume < 500 但 kd > 25         → -10 分  (性价比差)
   - 关键词与已发 6 篇主词重合度 > 60%  → 标记 'CANNIBALIZATION_WARN', 不重排
     (重合度计算: 关键词之间 word-overlap ratio. 如 'best ai tools for sql data analysis'
      与已发 'best ai tools for data analysis' 重合度 = 6/7 = 86% → 标记)

Step 3. 按 total_score 分层:
   - total_score >= 90  → final_priority = 'P0' (cap 24 篇, 超过 24 按分数截断, 截断的降到 P1)
   - 75 <= total_score < 90 → final_priority = 'P1'
   - total_score < 75      → final_priority = 'P2'
   - 硬性筛选 fail 的     → final_priority = 'DROP' (建议从 100 页清单移出)

Step 4. 与 planned_priority 对比, 标 priority_movement:
   - 升级: P1→P0 / P2→P1 → 'UPGRADED'
   - 降级: P0→P1 / P1→P2 → 'DOWNGRADED'
   - 不动: 'STABLE'
   - 进 DROP: 'DROPPED'

【最终输出】

1. **完整重排表 (94 行)**, 列:
   no / keyword / pillar / planned_priority / final_priority / total_score /
   score_breakdown (拆解到每个加分项) / priority_movement / volume / kd /
   trend_3m / 一句话推荐动作 (15 字内)

2. **Q3 2026 发布日历建议** (按 final_priority='P0' 取 Top 24, 按 score 倒序):
   week_of (从 2026-07-06 开始, 每周 2 篇) / no / keyword / slug /
   content_type / pillar / score / 关联已发文 (做内链回流)

3. **变动汇总段落** (150 字内), 必须点出:
   - 多少篇 UPGRADED / DOWNGRADED / DROPPED
   - 哪几个 Pillar 整体被升级 / 降级 (Pillar 级洞察)
   - DROP 列表的 3 个最大原因 (volume 不够? kd 太高? intent 不符?)
   - 是否触发 CANNIBALIZATION_WARN, 涉及哪几篇

4. **3 张图表**:
   (1) 决策池散点图: volume × kd, 用 final_priority 染色 (P0 红 / P1 橙 / P2 灰 / DROP 黑×)
   (2) Pillar 维度堆叠柱状图: 每个 Pillar 的 P0 / P1 / P2 / DROP 数量分布
   (3) 24 篇 P0 的 total_score 水平条形图, 按 score 倒序, 标注每篇所属 Pillar

【格式要求】
- 每条结论必须可追溯到具体 SQL (展开 .compact-tool-row 必须看得到原始数据)
- 用 markdown table 输出文本类结果, 图表用 SVG (后续要下载嵌进 v1.2 文档)
- 输出末尾给一段 100 字"赛道结构判断": 100 页主题集群在 2026 Q3 是仍处于
  蓝海 (P0 多 / DROP 少) 还是已经红海 (P0 少 / DROP 多), 战略上要继续扩还是先聚焦.
```

---

## 跑完后的 4 个动作

| 动作 | 操作 |
|---|---|
| **1. 存进记忆库** | 任务跑完, 点 `.task-item.active .task-more-btn` → "Save to memory", 命名 `seo-100-keywords-rerank-2026-06` |
| **2. 下载 3 张 SVG** | 走 `Skills/infinisynapse-app-skill/SKILL.md` §5.3 "文件" tab 的 `URL.createObjectURL` monkeypatch workaround, 拿到 3 张图后嵌到 v1.2 文档 |
| **3. 导出最终 CSV** | 把第 1 张 "完整重排表" 导出为 CSV → `output/keywords-100-final-priority-<YYYY-MM-DD>.csv` |
| **4. 反向更新 v1.1 → v1.2** | 用最终 CSV 改 `SEO/100页主题集群规划-v1.md` 附录 A 速查表的 P0/P1/P2 分级, 文件升级为 `100页主题集群规划-v1.2.md`; 把第 2 张 Q3 发布日历嵌进 §14 时间表 |

---

## 录屏 / 演示亮点（可选）

如果想把这次 rerank 录成 demo 视频（呼应 `日常运营/SEO选词case-AI-data-analysis/` 已有的录屏），4 个关键帧：

| 时机 | 镜头 | 字幕 |
|---|---|---|
| 0:00-0:05 | 拖两个 CSV 进 `/database/private`, 鼠标特写 | `Two CSVs. One question.` |
| 0:05-0:15 | prompt 用 typewriter 打出, 强调"硬筛选 + 9 加分项"那一段 | `9 scoring rules, cited inline` |
| 0:30-0:50 | Phase 2-4 的 .compact-tool-row 依次展开, 看 SQL join + 加分计算 | `Every score has a SQL trace` |
| 1:10-1:20 | 终版散点图浮现, 鼠标停在某个 P0 红点上 hover 出 breakdown | `100 keywords. 24 P0. All explained.` |
| 1:20-1:25 | 切到第 3 张水平条形图, 圈出 Top 3 | `Week 1 of Q3: ship these three` |

---

## 失败兜底

| 现象 | 修法 |
|---|---|
| Phase 2 报 "keyword join 失败" | 检查两个 CSV 的 keyword 列是否有 trailing whitespace / 大小写不一致, 用 LOWER(TRIM(keyword)) 重跑 |
| 输出表少于 94 行 | 大概率是某些关键词在 SEMrush 拿不到数据 (volume = N/A 被吃掉了), 让 Agent 用 LEFT JOIN 改写, 缺失数据当作 volume=0 / kd=null 一并显示 |
| Top 24 全集中在 1-2 个 Pillar | 检查加分项 I (Pillar 加权) 是否调过头, 可以让 Agent 重跑去掉 I 加分项做对比 |
| `CANNIBALIZATION_WARN` 触发 > 10 项 | 说明 100 页主题密度过高, 反向回到 v1.1 文档把 warn 项替换为更长尾的子词 |
