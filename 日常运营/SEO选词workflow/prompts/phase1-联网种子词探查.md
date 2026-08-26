# Phase 1 · InfiniSynapse 联网搜索 · 种子词探查 prompt

> **录制时机**：Case B 第 [02] 段（0:05 – 0:14）
> **执行环境**：`app.infinisynapse.com/tasks` 首页输入框（**不开模板提问，直接用普通输入框**——视觉上要让观众清楚看到联网搜索图标被触发）
> **预期跑动时长**：80–110 秒（含联网取证 + 整理）

---

## 提问全文（直接复制）

```text
我们是 InfiniSynapse —— 一款面向企业 / 团队的 AI Data Agent 工具，
主功能：跨数据源联合分析（零 ETL）、可解释 SQL 推理、自然语言出报告 + 图表 + PDF。
核心差异化：每一步推理都有 SQL / RAG / 联网证据可点开追溯。

现在我们要做 SEO 内容投放，目标主词赛道是 "AI data analysis"。

请联网检索以下渠道，找出 2026 年近 90 天内真实用户在讨论这个主题时
反复出现的"长尾搜索意图 / 真实问句 / 痛点措辞"，输出 60 个种子词候选：

【必须覆盖的渠道】
1. Reddit:    r/dataanalysis, r/SQL, r/datascience, r/SEO, r/Excel, r/analytics
2. Hacker News: 含 "AI" + "data" 的近期讨论
3. Quora:     "AI data analysis" 主题问答
4. GitHub Discussions: 主流 BI / 数据分析开源项目里的 issue 标题
5. Indie Hackers / Product Hunt: 相关产品的评论区
6. X (Twitter): 数据从业者的近期热门 thread

【每个种子词必须标注】
- keyword（不超过 6 个英文单词）
- source_type（reddit / hn / quora / github / ph / x）
- source_url（真实可点击链接）
- raw_quote（用户原话片段,不超过 30 字,作为该词的"出处证据"）
- intent（informational / commercial / transactional / navigational）
- pain_signal（一句话描述这词背后的真实痛点,不超过 25 字）

【筛选规则】
- 同义合并:"AI for data analysis" 和 "AI to analyze data" 算一个
- 必须是真实人问出来的句式,不要机器扩写
- 优先收 commercial + informational,排除纯 navigational(如 "tableau login")
- 至少含 15 个含具体场景的长尾(如 "ai data analysis for excel files")

【输出格式】
表格 + 一段 100 字总结,总结里点出这次扫描发现的 3 个反常识的搜索意图。
```

---

## 录屏关注点

| 时机 | 镜头 | 字幕（EN / 中文同款） |
|---|---|---|
| 提问发出后 0–2s | 联网图标亮起、`.compact-tool-row` 出现 `Searching the web...` | `Listening to real users` / 听真实人话 |
| 大约 30s | 工具行展开能看到 Reddit / HN / Quora 的来源 logo 或 url | `Reddit · Hacker News · Quora` |
| 大约 80s | 终版表格一闪而过（不停留太久，留悬念） | `60 seed keywords with citations` / 60 个带引文的种子词 |

---

## 备份策略

如果联网搜索某次抽风（被 reddit / quora 限流），把上一次成功跑过的 `taskId` 记录在 `raw/phase1-fallback-taskId.txt`，剪辑时直接复用历史录屏的 Phase 1 段落即可（视觉上观众看不出区别）。
