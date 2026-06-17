# InfiniSynapse · Reddit 90 天可执行操作手册

> **对应增长方案**：[`index.html#reddit-weekly`](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/index.html#reddit-weekly) · [`增长方案.md` §4.4](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/增长方案.md)  
> **看板任务**：InfiniSynapse 组织 · 运营指标看板 · #11 Reddit GEO 90天运营  
> **编制日期**：2026-06-15  
> **目标**：90 天内完成 **10 条长评 + 2 篇主帖**，且每条动作都有**可查来源**（基线报告、SOP、高被引原帖、写法参考稿）。

---

## 0. 为什么要做 Reddit（权威依据）

| 结论 | 来源 |
|------|------|
| ChatGPT 引用域名中 **Reddit 排名第 1**（30,942 次），引用转化率 **49.64%** | [GEOly《2026 Reddit GEO 洞察报告》](https://mp.weixin.qq.com/s/zV_KLvCCA8rwOP-Y-d-fDw) · 见 [`Reddit-GEO-SOP.md` §0–§1](./Reddit-GEO-SOP.md) |
| 本品类「data agent」监测中，**37.5%**（21/56）的 AI 引用来自 Reddit | [`Reddit-GEO-data-agent-基线报告.md` §二](./Reddit-GEO-data-agent-基线报告.md) |
| Hex 在同类测试中 **被引用 6 次**，我们 **0 次** — Reddit 是缩小差距的最短路径之一 | 同上 · §四；增长方案 [`index.html#geo`](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/index.html#geo) |
| 含 Reddit 引用的回答 **99.97% 触发联网搜索** — 帖子标题清晰、有人互动，才容易被 AI 读到 | [`Reddit-GEO-SOP.md` §6.1](./Reddit-GEO-SOP.md) |

**本手册策略（与基线报告 §六一致）**  
- 已在 ChatGPT 里被引用的帖 → **优先去评论**（评论本身也可能被引用）  
- 规则宽松的 sub → **发主帖**（r/AI_Agents、r/LangChain）  
- r/dataengineering / r/BusinessIntelligence → **几乎只做评论**，禁止 vendor 口吻（见 [`阵地清单` §一](./Reddit-GEO-data-agent-阵地清单.md)）

---

## 1. 发布前总规则（每次必查）

### 1.1 写法依据（SOP 原文）

| 要做 | 不要做 | 出处 |
|------|--------|------|
| 第一人称：「我试过」「我们踩坑」 | 品牌官网腔、促销语 | [SOP §5.3 DO](./Reddit-GEO-SOP.md) |
| 标题像真实经历：「tested 4 … over 90 days」 | 「XX 品牌发布」「game-changer」 | [SOP §5.2 标题公式](./Reddit-GEO-SOP.md) |
| 先 3 段经验，最后才可选 1 个链接 | 正文首段放链接 | [SOP §5.4 DON'T](./Reddit-GEO-SOP.md) · [内容包 v2 §二](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |
| 数字用「大约」「~11/12 题」 | 「exactly 91%」式假精确 | [内容包 v2 去 AI 化表](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |

### 1.2 分区规则速查

| 分区 | 自荐 | 对我们 | 出处 |
|------|------|--------|------|
| **r/AI_Agents** | 1:10；**链接放评论，不放正文** | ✅ 主帖主战场 | [阵地清单 §二 r/AI_Agents](./Reddit-GEO-data-agent-阵地清单.md) |
| **r/LangChain** | 较宽松，禁 spam | ✅ 主帖 / 技术帖 | [阵地清单 §二 r/LangChain](./Reddit-GEO-data-agent-阵地清单.md) |
| **r/dataengineering** | **禁 vendor**；自荐约 1 次/月 | ⚠️ **只评论**为主 | [阵地清单 §一 T3](./Reddit-GEO-data-agent-阵地清单.md) |
| **r/BusinessIntelligence** | **完全禁 vendor** | ⚠️ **只评论** | 同上 |
| **r/analytics** | 禁 blog spam | ⚠️ **只评论** | 同上 |

### 1.3 可引用的「自家权威数字」（统一口径）

| 内容 | 权威出处 |
|------|----------|
| 十二项标准化分析测试 · **11.0/12 分** · 样本 v1.2 | [InfiniSynapse 买家指南（官网）](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) · 增长方案 [`index.html#benchmark`](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/index.html#benchmark) |
| 对外话术模板 | 见本文 **附录 B** |

### 1.4 发完 24 小时内必做

1. 复制 **永久链接**（Share → 链接）  
2. 填入 **附录 C 台账**  
3. 截图留存（防删帖无据）

---

## 2. 90 天按周执行（每条含：原帖 · 依据 · 角度 · 参考稿）

---

### 第 1 周 · 2 条长评

#### 动作 1-1 · r/dataengineering · Text to SQL agents

| 项 | 内容 |
|----|------|
| **去哪个帖** | [Text to SQL agents](https://www.reddit.com/r/dataengineering/comments/1owjt0b/text_to_sql_agents/) |
| **为什么是这个帖** | 监测问题 P4 下 **被 ChatGPT 引用 4 次**（品类最高 ROI） | [基线报告 §三 r/dataengineering #1](./Reddit-GEO-data-agent-基线报告.md) · [§六 P0-1](./Reddit-GEO-data-agent-基线报告.md) |
| **分区规则** | 禁 vendor；只分享工程经验 | [阵地清单 T3 r/dataengineering](./Reddit-GEO-data-agent-阵地清单.md) |
| **回复角度** | ① 别一上来接「整个仓库」，先圈 15–20 个真实高频问题 ② 多库/跨源时 semantic layer 比模型更重要 ③ 工具层硬限制（只读、超时、LIMIT） |
| **写法参考（勿照抄，改数字与细节）** | [内容包 v2 · 评论 1](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md)（账号 A · data engineer 人设） |
| **链接策略** | 本条 **建议不放链接**；若有人追问「你们怎么测准确率」，再回复链 [买家指南](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) |
| **验收** | 永久链接存表 · 未被删 · ≥150 字 |

#### 动作 1-2 · 同帖楼中楼或第二段经验

| 项 | 内容 |
|----|------|
| **去哪个帖** | 同上帖，或 [AI Kill BI](https://www.reddit.com/r/dataengineering/comments/1s9gd8f/ai_kill_bi/)（P2 被引，基线 §三） |
| **角度** | 「单库 NL2SQL 在 PO 问跨 region、跨系统指标时对不上」— 对应 InfiniSynapse **多库联邦**叙事（增长方案 [`hex.html` 差异化](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/competitors/hex.html)） |
| **竞品语境（勿点名踩）** | Hex 占 AI 引用 #1，叙事偏 notebook/SQL；我们强调 **跨源 + 私有化** | [基线报告 §四 hex.tech](./Reddit-GEO-data-agent-基线报告.md) |

---

### 第 2 周 · 2 条长评

#### 动作 2-1 · r/dataengineering · 生产环境敢让 AI 跑 SQL 吗

| 项 | 内容 |
|----|------|
| **去哪个帖** | [Are people actually letting AI agents run SQL in production?](https://www.reddit.com/r/dataengineering/comments/1s22vr9/are_people_actually_letting_ai_agents_run_sql/) |
| **为什么是这个帖** | P5 监测下 **被引用 2 次** | [基线报告 §三 #2](./Reddit-GEO-data-agent-基线报告.md) · [§六 P0-2](./Reddit-GEO-data-agent-基线报告.md) |
| **回复角度** | 只读副本 · SQL 解析拦截 · 单次预算上限 · 每周回放查询找「业务错但 SQL 对」 |
| **写法参考** | [内容包 v2 · 评论 2](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |
| **可提数字** | 「我们跑过一套公开的可复现测试，大约 **11/12** 题能过，但生产里更怕的是指标定义漂移」→ 链 [买家指南](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) **仅在被问及时** |
| **验收** | 2 条链接（含本周第二条）· 无删帖 |

#### 动作 2-2 · r/dataengineering 当周热帖（备选）

| 项 | 内容 |
|----|------|
| **怎么找帖** | 打开 [r/dataengineering](https://www.reddit.com/r/dataengineering/) · 排序 Top · 本周 · 选与 SQL/agent/BI 相关 |
| **依据** | SOP 要求标题含清晰关键词、常青讨论 | [SOP §6.3 常青内容](./Reddit-GEO-SOP.md) |
| **角度** | 审计留痕、私有化部署（对齐增长方案 Reddit 表） |

---

### 第 3 周 · 2 条长评

#### 动作 3-1 · r/BusinessIntelligence · Agentic BI 会取代传统 BI 吗

| 项 | 内容 |
|----|------|
| **去哪个帖** | [Is Agentic BI actually replacing traditional?](https://www.reddit.com/r/BusinessIntelligence/comments/1ta6rzb/is_agentic_bi_actually_replacing_traditional/) |
| **为什么是这个帖** | P2 下 **被引用 2 次** | [基线报告 §三 r/BI](./Reddit-GEO-data-agent-基线报告.md) · [§六 P0-3](./Reddit-GEO-data-agent-基线报告.md) |
| **分区规则** | **完全禁 vendor** | [阵地清单 T3 r/BusinessIntelligence](./Reddit-GEO-data-agent-阵地清单.md) |
| **回复角度** | 不取代 dashboard，取代「没人愿意单独做 dashboard 的 ad-hoc 问题」；指标定义 fuzzy 时 agent 会翻车 |
| **写法参考** | [内容包 v2 · 评论 3](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md)（账号 B · BI 负责人人设） |

#### 动作 3-2 · r/LangChain · SQL 幻觉列名

| 项 | 内容 |
|----|------|
| **去哪个帖** | [Preventing SQL agents from hallucinating columns](https://www.reddit.com/r/LangChain/comments/1rhlb4g/preventing_sql_agents_from_hallucinating_columns/) |
| **为什么是这个帖** | P5 被引；与 P4 [LangChain 帖](https://www.reddit.com/r/LangChain/comments/1l8zy42) 同属 SQL 工作流讨论 | [基线报告 §三 r/LangChain](./Reddit-GEO-data-agent-基线报告.md) |
| **回复角度** | schema 实时 introspection → 先英文计划再 SQL → SQLGlot 校验 → 小模型 judge |
| **写法参考** | [内容包 v2 · 评论 5](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |
| **后续主帖伏笔** | 第 6–9 周可在 r/LangChain 发「guardrail stack」长帖 | [内容包 v2 · 帖 #2](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) · [基线 §六 P1 LangChain 建议](./Reddit-GEO-data-agent-基线报告.md) |

---

### 第 4 周 · 2 条长评（第一阶段收官：累计 10 评）

#### 动作 4-1 · r/analytics · 语义层与集成

| 项 | 内容 |
|----|------|
| **去哪个帖** | [Semantic layer for AI agents requires way better data integration](https://www.reddit.com/r/analytics/comments/1r929p9/semantic_layer_for_ai_agents_requires_way_better/) |
| **为什么是这个帖** | P3 被引 | [基线报告 §三 r/analytics](./Reddit-GEO-data-agent-基线报告.md) |
| **角度** | 跨源集成、联邦查询；版规允许时可链一篇官网 **对比文**（非首页推销） |

#### 动作 4-2 · 高 ROI 补位（二选一）

| 选项 | 帖子 | 被引依据 |
|------|------|----------|
| A | [r/AI_Agents · We built a data agent ~200 hrs/week](https://www.reddit.com/r/AI_Agents/comments/1sfu06i/we_built_a_data_agent_that_saves_our_analyst_team/) | P3 · [基线 §三](./Reddit-GEO-data-agent-基线报告.md) · [§六 P0-4](./Reddit-GEO-data-agent-基线报告.md) |
| B | [r/AI_Agents · Your agent passed testing — your agent won't](https://www.reddit.com/r/AI_Agents/comments/1rcy3na/your_agent_passed_testing_your_agent_wont/) | P5 · [基线 §三](./Reddit-GEO-data-agent-基线报告.md) |

**写法参考（选项 A）**：[内容包 v2 · 评论 4](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md)

**✅ 第 4 周末验收**：台账累计 **10 条**评论永久链接

---

### 第 5 周 · 主帖 #1 草稿（不发布）

#### 动作 5-1 · 起草 + 内部审阅

| 项 | 内容 |
|----|------|
| **目标阵地** | **r/AI_Agents**（主战场） | [阵地清单 §二](./Reddit-GEO-data-agent-阵地清单.md) |
| **对标原帖（结构参考）** | [We built a data agent that saves ~200 hrs/week](https://www.reddit.com/r/AI_Agents/comments/1sfu06i/we_built_a_data_agent_that_saves_our_analyst_team/) | [基线 §三](./Reddit-GEO-data-agent-基线报告.md) |
| **标题公式依据** | 「tested N approaches over 90 days」 | [SOP §5.2 公式一/四](./Reddit-GEO-SOP.md) |
| **正文参考稿** | [内容包 v2 · 帖 #1 全文](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |
| **必改项** | ① 所有百分比/金额换 **真实** 内部或 [十二项测试](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) 数据 ② 文末披露身份 ③ **正文不放链接**（规则要求链在评论） |
| **审阅清单** | [内容包 v2 §二 去 AI 化表](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) · [内容包 v2 文末 checklist](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |
| **验收** | 草稿通过 · 标题 ≤100 字 · 准备 1 条「评论区自荐回复」 |

**建议标题（可微调）**  
`tested 4 different data agent setups over ~90 days on the same warehouse — what actually held up`

---

### 第 6 周 · 发布主帖 #1

#### 动作 6-1 · 发帖 + 置顶评论

| 项 | 内容 |
|----|------|
| **阵地** | [r/AI_Agents](https://www.reddit.com/r/AI_Agents/) |
| **规则** | 链接 **仅放评论** · 自荐 ≤10% | [阵地清单 r/AI_Agents 规则](./Reddit-GEO-data-agent-阵地清单.md) |
| **正文** | 使用第 5 周定稿（基于 [内容包 v2 帖 #1](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md)） |
| **发布后第 1 条评论（自荐）模板** | 见 **附录 A-1** |
| **动作 6-2** | 在自己帖下回答 1 个技术追问（不 spam） |
| **验收** | 主帖永久链接 · ≥3 upvote 或回复 |

---

### 第 7 周 · 2 条维护评论

#### 动作 7-1 · 主帖 #1 跟评

| 项 | 内容 |
|----|------|
| **去哪** | 第 6 周主帖 thread |
| **角度** | 补「怎么评测 agent」→ 自然引出十二项公开测试 | [买家指南](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) |

#### 动作 7-2 · 新热帖长评

| 项 | 内容 |
|----|------|
| **优先帖** | [How do you actually debug your AI agents?](https://www.reddit.com/r/AI_Agents/comments/1t7hes1/how_do_you_actually_debug_your_ai_agents/)（P5 被引） | [基线 §三](./Reddit-GEO-data-agent-基线报告.md) |
| **写法参考** | [内容包 v2 · 评论 6](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) |

**同步（增长方案 ChatGPT 线）**：用 [基线 §七 5 条 prompt](./Reddit-GEO-data-agent-基线报告.md) 做中期复测

---

### 第 8 周 · 1 条长评

#### 动作 8-1 · r/dataengineering 当周 Top 帖

| 项 | 内容 |
|----|------|
| **怎么找** | [r/dataengineering](https://www.reddit.com/r/dataengineering/) · Top · This Week |
| **角度** | 生产踩坑 · **多库联邦 / 私有化**（与 Hex 叙事差异常） | [Hex 详情 · GEO 叙事](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/competitors/hex.html) · [基线 hex.tech 6 次](./Reddit-GEO-data-agent-基线报告.md) |
| **监测** | 每 2 周扫一次新帖 | [增长方案 index §plan 固定习惯](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/index.html#plan) |

---

### 第 9 周 · 主帖 #2（评测 / 案例向）

> ⚠️ **r/dataengineering 禁 vendor**（[阵地清单](./Reddit-GEO-data-agent-阵地清单.md)）。增长方案原意「数据工程版 + 录屏」建议拆成：  
> **方案 A（推荐）**：r/LangChain 发评测方法帖 · **方案 B**：r/dataengineering 仅在高赞帖下长评 + 录屏链放楼中楼（被问及时）。

#### 动作 9-1A · 主帖 #2 · r/LangChain（推荐）

| 项 | 内容 |
|----|------|
| **阵地** | [r/LangChain](https://www.reddit.com/r/LangChain/) |
| **对标原帖** | [Preventing SQL agents from hallucinating columns](https://www.reddit.com/r/LangChain/comments/1rhlb4g/preventing_sql_agents_from_hallucinating_columns/)（P5 被引） |
| **标题参考** | `how we benchmark data agents on real analyst questions (12-task public protocol + replay links)` |
| **正文结构参考** | [内容包 v2 · 帖 #2](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md)（guardrail + eval 叙事） |
| **权威数字** | 十二项测试 **11.0/12** · [买家指南](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) |
| **录屏** | 配合增长方案第 9 周 SEO 案例页；**链接放评论** |
| **验收** | 第 2 篇主帖永久链接 |

#### 动作 9-1B · 若坚持 r/dataengineering · 仅评论模式

| 项 | 内容 |
|----|------|
| **去哪个帖** | 再次 [Text to SQL agents](https://www.reddit.com/r/dataengineering/comments/1owjt0b/text_to_sql_agents/) 或 [prod SQL 帖](https://www.reddit.com/r/dataengineering/comments/1s22vr9/) |
| **角度** | 「我们公开跑过 12 道题的 benchmark，录屏在回复里」— **不要单开 vendor 主帖** |
| **依据** | [基线 §二「规则最严的 sub 只能评论」](./Reddit-GEO-data-agent-基线报告.md) |

---

### 第 10–12 周 · 每周 1 条维护评 + 台账

| 周 | 建议动作 | 权威参考帖（任选其一深入回复） |
|----|----------|--------------------------------|
| **10** | 1 长评 · 可链 SEO 案例页 | [r/BI · Agentic BI](https://www.reddit.com/r/BusinessIntelligence/comments/1ta6rzb/) 或 [r/AI_Agents · 200hrs](https://www.reddit.com/r/AI_Agents/comments/1sfu06i/) |
| **11** | 1 长评 · 更新高价值帖清单 | [基线 §三 全清单 21 帖](./Reddit-GEO-data-agent-基线报告.md) |
| **12** | 1 长评 + **90 天台账归档** + Q2 待跟帖列表 | 用 [§七 prompt](./Reddit-GEO-data-agent-基线报告.md) 终测 |

**✅ 第 12 周末验收**：10 评 + 2 主帖 · 台账完整 · 5 prompt 终测报告存档

---

## 3. 扩展阵地（有余力再做）

基线发现、尚未纳入 90 天 mandatory 的高引用 sub：

| 分区 | 原帖 | 被引 | 出处 |
|------|------|------|------|
| r/n8n | [best AI agent builders 2026](https://www.reddit.com/r/n8n/comments/1r9trni/what_are_the_best_ai_agent_builders_in_2026/) | P1 | [基线 §三](./Reddit-GEO-data-agent-基线报告.md) · [§五](./Reddit-GEO-data-agent-基线报告.md) |
| r/AgentsOfAI | [Top agentic frameworks](https://www.reddit.com/r/AgentsOfAI/comments/1sya972/top_agentic_frameworks_let_me_know_if_i_missed_any/) | P1 | 同上 |
| r/SaaS | [1 in 50 hallucinating](https://www.reddit.com/r/SaaS/comments/1t161qg/we_caught_1_in_50_ai_responses_hallucinating_in/) | P5 | [基线 §三](./Reddit-GEO-data-agent-基线报告.md) |
| r/aiagents | [tests passed but they're not](https://www.reddit.com/r/aiagents/comments/1sfpq05/when_your_ai_agent_reports_tests_passed_and_they/) | P5 | 同上 |

---

## 附录 A · 可复制片段

### A-1 主帖 #1 发布后 · r/AI_Agents 评论区自荐（链放评论，符合规则）

```text
few people asked — i work on InfiniSynapse (data agent for multi-source / governed analytics). the numbers in the post are from internal runs, not marketing slides.

we also published a reproducible 12-task comparison protocol (11/12 on our stack in the public writeup): https://infinisynapse.com/use-cases/best-data-analysis-software/index.html

happy to go deeper on eval setup or federated query guardrails if useful.
```

**规则依据**：[r/AI_Agents 链接放评论区](https://www.reddit.com/r/AI_Agents/) · [阵地清单 §二](./Reddit-GEO-data-agent-阵地清单.md)

### A-2 被追问「准确率怎么测」时 · 短回复

```text
we fixed a 12-question set on a public dataset (v1.2), score each tool 0–1 per task, full rubric is here: https://infinisynapse.com/use-cases/best-data-analysis-software/index.html — we got ~11/12 on our side but ymmv depending on your schema messiness.
```

---

## 附录 B · 标准话术（十二项测试）

| 字段 | 内容 |
|------|------|
| 测试名称 | 十二项自然语言分析标准化测试（v1.2 样本） |
| 我方得分 | 11.0 / 12（约 91.7%） |
| 权威页 | https://infinisynapse.com/use-cases/best-data-analysis-software/index.html |
| 增长方案说明 | [`index.html#benchmark`](../日常运营/2026-InfiniSynapse增长方案-渠道与竞品分析/index.html#benchmark) |

---

## 附录 C · 执行台账（复制到 Excel / 飞书）

| 周 | 类型 | 分区 | 原帖 URL | 我们的永久链接 | 角度摘要 | 删帖? | ChatGPT 复测是否出现 |
|----|------|------|----------|--------------|----------|-------|---------------------|
| 1 | 评论 | r/dataengineering | https://www.reddit.com/r/dataengineering/comments/1owjt0b/ | | 多库/semantic layer | | |
| 1 | 评论 | r/dataengineering | | | | | |
| … | | | | | | | |
| 6 | 主帖 | r/AI_Agents | — | | 90天四方案对比 | | |
| 9 | 主帖 | r/LangChain | — | | 12-task benchmark | | |

---

## 附录 D · 监测 Prompt（与基线一致，第 7 / 12 周必跑）

来源：[基线报告 §七](./Reddit-GEO-data-agent-基线报告.md)

```
P1: What's the best AI data agent for analytics teams in 2026? Please search the web and cite specific Reddit threads if relevant.

P2: Best data agent vs traditional BI tools — what do Reddit data engineers actually say? Please search the web.

P3: I'm a data engineer evaluating AI agents for our pipeline. What does Reddit recommend? Please search the web and cite Reddit threads.

P4: Compare popular AI data agents for SQL-heavy workflows according to Reddit discussions. Please search the web.

P5: What are the real production issues with AI data agents? Cite specific Reddit threads. Please search the web.
```

记录：`infinisynapse.com` 出现次数 · 引用的 Reddit 链接是否含我们的 permalink

---

## 附录 E · 文档索引（全部权威原文）

| 文档 | 路径 | 用途 |
|------|------|------|
| Reddit GEO SOP | [`Reddit运营/Reddit-GEO-SOP.md`](./Reddit-GEO-SOP.md) | 写法、标题公式、三铁律 |
| GEOly 原始报告 | [微信公众号](https://mp.weixin.qq.com/s/zV_KLvCCA8rwOP-Y-d-fDw) | 行业 Reddit 引用数据 |
| Data Agent 基线 | [`Reddit-GEO-data-agent-基线报告.md`](./Reddit-GEO-data-agent-基线报告.md) | **21 条被引原帖** · 5 prompt |
| 阵地清单 | [`Reddit-GEO-data-agent-阵地清单.md`](./Reddit-GEO-data-agent-阵地清单.md) | 各 sub 规则 |
| 内容包 v2 | [`Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md`](./Reddit-GEO-data-agent-内容包v2-去AI化+双账号日历.md) | **6 评论 + 3 主帖参考稿** |
| 增长方案 Reddit 周历 | [`index.html#reddit-weekly`](./index.html#reddit-weekly) | 90 天节奏 |
| Hex 竞品 GEO | [`competitors/hex.html`](../competitors/hex.html) | 差异化叙事 |
| 十二项测试 | [官网买家指南](https://infinisynapse.com/use-cases/best-data-analysis-software/index.html) | 唯一对外数字源 |

---

*本手册随基线复测更新；若 ChatGPT 引用榜变化，优先调整 §2 中「去哪个帖」列，写法原则不变。*
