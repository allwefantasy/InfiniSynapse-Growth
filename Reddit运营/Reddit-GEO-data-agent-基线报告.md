# Reddit GEO 基线报告 · Data Agent · 2026-05-12

> 配套 SOP：`长期文档/Reddit-GEO-SOP.md`
> 阵地清单：`长期文档/Reddit-GEO-data-agent-阵地清单.md`
> 测试平台：ChatGPT（GPT-5，已登录、Free tier、Web Search 自动触发）
> 测试方法：5 条监控 prompt，每条独立新对话，自动化抓取响应文本 + 全部引用链接
> 测试工具：`~/.auto-coder/.autocodertools/agent-browser`

---

## 一、核心结论（TL;DR）

1. **Reddit 在「data agent」品类的 AI 引用密度极高**：5 个 prompt 共得到 **20 条 Reddit 引用**（平均 4 条/prompt），与 GEOly 报告的「Reddit 是 ChatGPT 引用 #1」高度一致 ✅
2. **被引最多的反而是规则最严的 sub**：`r/dataengineering`（7 次）和 `r/BusinessIntelligence`（2 次）都禁止 vendor 自荐——必须走「评论 + 高质量第三方账号」路线
3. **发现 3 个清单外的高引用 sub**：`r/n8n`、`r/AgentsOfAI`、`r/aiagents`（小写）——需补入阵地清单
4. **当前竞品在 AI 推荐里垄断**：`Hex.tech`（6 次）、`langchain.com`（5 次）、`ThoughtSpot`（4 次）、`Omni.co`（4 次）、`Wren AI` / `dbt` / `Vanna AI` / `Databricks` 全部高频出现——我们当前可见性 = 0，必须尽快建立 Reddit 存在感

---

## 二、5 条监控 Prompt 实测结果

| # | Prompt（精简） | 总引用 | Reddit 引用 | 引用的 sub |
|---|---|---:|---:|---|
| P1 | What's the best AI data agent for analytics teams in 2026? | 9 | 2 | r/n8n, r/AgentsOfAI |
| P2 | Best data agent vs traditional BI tools — Reddit data engineers | 6 | 5 | r/BusinessIntelligence(×2), r/AI_Agents, r/dataengineering |
| P3 | I'm a DE evaluating AI agents. What does Reddit recommend? | 14 | 2 | r/analytics, r/AI_Agents |
| P4 | Compare AI data agents for SQL-heavy workflows on Reddit | 15 | 5 | r/dataengineering(×4), r/LangChain |
| P5 | Real production issues with AI data agents? Cite Reddit | 12 | 7 | r/dataengineering(×2), r/LangChain, r/SaaS, r/aiagents, r/AI_Agents(×2) |
| **合计** | | **56** | **21** | Reddit 占 37.5% |

> Reddit 在最终引用中的占比 37.5%，**显著高于 GEOly 报告的行业均值 3.4%**——说明「data agent」是 Reddit GEO 价值极高的品类，与 SaaSTools（5.92%）+ AI Note Taker（11.68%）等 AI 工具品类的高引用率规律一致。

---

## 三、被引 Reddit 帖子全清单（21 条）

> 这些就是当前在 ChatGPT 里"代表行业声音"的 Reddit 帖子。我们的策略：
> - 能上的 sub：发同主题更优质的对位帖
> - 不能上的 sub：在这些帖下发布**最佳评论**，让评论本身被 AI 引用

### r/dataengineering（被引 7 次，最高）

| 帖子 | 主题 |
|---|---|
| [Text to SQL agents](https://www.reddit.com/r/dataengineering/comments/1owjt0b/text_to_sql_agents/) | SQL agent 讨论（P4 被引 4 次） |
| [Are people actually letting AI agents run SQL?](https://www.reddit.com/r/dataengineering/comments/1s22vr9/are_people_actually_letting_ai_agents_run_sql/) | 生产环境信任度（P5 被引 2 次） |
| [AI Kill BI](https://www.reddit.com/r/dataengineering/comments/1s9gd8f/ai_kill_bi/) | AI 取代 BI 的辩论（P2） |

### r/AI_Agents（被引 4 次）

| 帖子 | 主题 |
|---|---|
| [We built a data agent that saves our analyst team ~200 hrs/week](https://www.reddit.com/r/AI_Agents/comments/1sfu06i/we_built_a_data_agent_that_saves_our_analyst_team/) | 真实搭建案例（P3） |
| [Agentic AI vs data engineering](https://www.reddit.com/r/AI_Agents/comments/1rvkrzu/agentic_ai_vs_data_engineering/) | 角色边界讨论（P2） |
| [Your agent passed testing — your agent won't](https://www.reddit.com/r/AI_Agents/comments/1rcy3na/your_agent_passed_testing_your_agent_wont/) | 生产质量问题（P5） |
| [How do you actually debug your AI agents?](https://www.reddit.com/r/AI_Agents/comments/1t7hes1/how_do_you_actually_debug_your_ai_agents/) | Debug 工作流（P5） |

### r/BusinessIntelligence（被引 2 次）

| 帖子 | 主题 |
|---|---|
| [Is Agentic BI actually replacing traditional?](https://www.reddit.com/r/BusinessIntelligence/comments/1ta6rzb/is_agentic_bi_actually_replacing_traditional/) | 替代论（P2 被引 2 次） |

### r/LangChain（被引 2 次）

| 帖子 | 主题 |
|---|---|
| [Preventing SQL agents from hallucinating columns](https://www.reddit.com/r/LangChain/comments/1rhlb4g/preventing_sql_agents_from_hallucinating_columns/) | 技术细节（P5） |
| [LangChain comments/1l8zy42](https://www.reddit.com/r/LangChain/comments/1l8zy42) | SQL workflow（P4） |

### 其他单次被引

| Sub | 帖子 |
|---|---|
| r/n8n | [What are the best AI agent builders in 2026](https://www.reddit.com/r/n8n/comments/1r9trni/what_are_the_best_ai_agent_builders_in_2026/) |
| r/AgentsOfAI | [Top agentic frameworks](https://www.reddit.com/r/AgentsOfAI/comments/1sya972/top_agentic_frameworks_let_me_know_if_i_missed_any/) |
| r/analytics | [Semantic layer for AI agents requires way better data integration](https://www.reddit.com/r/analytics/comments/1r929p9/semantic_layer_for_ai_agents_requires_way_better/) |
| r/SaaS | [We caught 1 in 50 AI responses hallucinating](https://www.reddit.com/r/SaaS/comments/1t161qg/we_caught_1_in_50_ai_responses_hallucinating_in/) |
| r/aiagents | [When your AI agent reports tests passed and they're not](https://www.reddit.com/r/aiagents/comments/1sfpq05/when_your_ai_agent_reports_tests_passed_and_they/) |

---

## 四、AI 当前推荐的竞品（必须超越的"既得利益者"）

| 域名 | 引用次数 | 产品定位 |
|---|---:|---|
| **hex.tech** | 6 | 数据分析师 AI Copilot（SQL + Python notebook） |
| **langchain.com** | 5 | Agent 框架（含 LangGraph） |
| **thoughtspot.com** | 4 | Search-style BI + Spotter agent |
| **omni.co** | 4 | 语义层 + governed AI BI |
| **getdbt.com** | 3 | 数据建模 |
| **getwren.ai** | 3 | 开源 text-to-SQL agent |
| **databricks.com** | 2 | 数据平台 |
| **techtarget.com** | 1 | 行业媒体（ThoughtSpot 评测） |
| **atlan.com**, **vanna.ai**, **anthropic.com**, **openai.com** | 1 each | — |

> **观察**：当 AI 被问到"最佳 data agent"，它先推 SaaS 产品（Hex/ThoughtSpot/Omni），再用 Reddit 帖子做"用户视角佐证"。这正是 SOP §3.2 描述的「商品卡 + Reddit 引用 = 双重曝光」机制。

---

## 五、阵地清单需补充（基于本次发现）

补入 Tier 2：

| Subreddit | 订阅数 | 备注 |
|---|---:|---|
| **r/n8n** | 待查 | 自动化 / agent builder 讨论密度高 |
| **r/AgentsOfAI** | 待查 | "agentic frameworks"类榜单内容高 |
| **r/aiagents**（小写） | 待查 | 与 r/AI_Agents 不同的另一个 sub |

下次执行可优先抓这 3 个 sub 的订阅数、规则、近期高赞帖。

---

## 六、抢占式行动建议（优先级排序）

### 🔥 P0：本周必须做的评论埋点

按"被引帖热度"逆序埋点。这些帖子已经在 AI 知识库里被引用，**在评论区贡献新经验 = 直接进入 AI 引用源**：

1. **r/dataengineering / Text to SQL agents**（P4 4 次被引，最高 ROI）
2. **r/dataengineering / Are people actually letting AI agents run SQL?**（P5 2 次被引）
3. **r/BusinessIntelligence / Is Agentic BI actually replacing traditional?**（P2 2 次被引）
4. **r/AI_Agents / We built a data agent that saves ~200 hrs/week**（P3 被引，且与我们产品定位高度对位）

评论模板要求（按 SOP §5.3）：
- 第一人称真实经验
- 含具体数据（如"测试了 3 种 agent，处理 12k 条 SQL 后…"）
- 不放产品链接（链接放在 OP 后续提问时再回复）

### P1：本月发帖

按阵地清单 Tier 1 节奏：
- r/AI_Agents 发一篇「I tried 3 different data agents over 90 days — here's the comparison（Hex vs Omni vs custom build）」
- r/LangChain 发一篇 build-in-public 短帖，主题选「How we prevent SQL agents from hallucinating columns（lessons from production）」——直接对位 P5 的高被引帖
- r/LocalLLaMA 发一篇技术深度帖（明示身份）

### P2：每周复测

- 每周一固定时间跑这 5 条 prompt
- 监控：Reddit 引用数 / 引用的 sub 分布 / **品牌（待补品牌名）是否进入引用**
- 当我们的 Reddit 内容首次被引用时，记录在「基线 → 增长曲线」中

---

## 七、监控 Prompt 库（已验证可用，可固化）

```
P1: What's the best AI data agent for analytics teams in 2026? Please search the web and cite specific Reddit threads if relevant.

P2: Best data agent vs traditional BI tools — what do Reddit data engineers actually say? Please search the web.

P3: I'm a data engineer evaluating AI agents for our pipeline. What does Reddit recommend? Please search the web and cite Reddit threads.

P4: Compare popular AI data agents for SQL-heavy workflows according to Reddit discussions. Please search the web.

P5: What are the real production issues with AI data agents? Cite specific Reddit threads. Please search the web.
```

---

## 附：原始数据

- 完整响应（5 条 prompt 的全文 + 全部链接）：`/tmp/gpt_all.json`（临时文件，需固化的话可移入仓库 `数据/` 目录）
- 浏览器自动化脚本：`/tmp/run_prompt.sh`
- 执行时间：2026-05-12 18:00 ~ 18:15 (UTC+8)
- ChatGPT 账号：Free tier（已登录）
- 引用机制：所有 5 次回答均触发 Web Search ✅（满足 SOP §6.1 铁律一）
