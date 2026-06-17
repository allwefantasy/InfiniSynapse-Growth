# Reddit GEO 阵地清单 · Data Agent

> 配套 SOP：`长期文档/Reddit-GEO-SOP.md`
> 产品：**data agent**（通用调研，未带具体品牌）
> 调研工具：`agent-browser` + Reddit 公开 JSON API
> 调研时间：2026-05-12
> 数据维度：订阅数、规则、近 1 年「data agent」相关帖热度

---

## 一、Tier 划分总览

按「话题契合度 × 流量 × 规则友好度」综合打分。

| Tier | Subreddit | 订阅数 | 规则友好度 | 自荐配额 | 综合推荐 |
|---|---|---:|---|---|:---:|
| **T1** | r/AI_Agents | 360,368 | 🟢 高 | 1:10，链接放评论区 | ⭐⭐⭐⭐⭐ |
| **T1** | r/LocalLLaMA | 718,338 | 🟡 中 | 1:10 + 必须披露利益相关 | ⭐⭐⭐⭐⭐ |
| **T1** | r/LangChain | 98,083 | 🟢 高 | 仅禁 spam，无明确比例 | ⭐⭐⭐⭐⭐ |
| **T2** | r/datascience | 2,743,047 | 🟡 中 | 1:9，禁 listicles/videos | ⭐⭐⭐⭐ |
| **T2** | r/ChatGPTPro | 581,215 | 🟡 中 | 1:10 + 禁纯链接 | ⭐⭐⭐⭐ |
| **T2** | r/SaaS | 687,995 | 🟡 中 | 60 天 1 次提及 | ⭐⭐⭐⭐ |
| **T2** | r/PromptEngineering | 373,526 | 🟢 高 | 较宽松 | ⭐⭐⭐⭐ |
| **T3** | r/dataengineering | 452,642 | 🔴 严 | 自荐 1 月 1 次 + 禁 AI 内容 + 禁 vendor | ⭐⭐⭐（只做评论） |
| **T3** | r/BusinessIntelligence | 231,865 | 🔴 严 | **完全禁 vendor + 禁 AI 内容** | ⭐⭐（只做评论） |
| **T3** | r/LLMDevs | 146,955 | 🔴 严 | **完全禁商业自荐** | ⭐⭐（只做评论） |
| **T3** | r/analytics | 266,519 | 🔴 严 | 禁 blog spam + 推广限制 | ⭐⭐（只做评论） |
| 备 | r/Entrepreneur | 5,173,512 | 🟡 中 | 禁推广 | ⭐⭐⭐ |
| 备 | r/MachineLearning | 3,045,425 | 🟡 中 | 偏学术 | ⭐⭐⭐ |
| 备 | r/OpenAI | 2,748,361 | 🟡 中 | — | ⭐⭐⭐ |
| 备 | r/AINoteTaker | 13,441 | 🟢 高 | 圈层小但精准 | ⭐⭐⭐ |

---

## 二、Tier 1 阵地详解（重点投入）

### 🥇 r/AI_Agents（360k）—— 主战场

- **创建时间**：2023-04-28
- **话题契合度**：⭐⭐⭐⭐⭐（直接对位）
- **规则**：
  - Be respectful / No spam
  - **链接必须放评论区，不能放正文**
  - 自荐 ≤ 10%（1:10）
  - 禁低质内容
- **近 1 年「data agent」相关高赞帖**：
  - 「**I build AI agents for a living. It's a mess out there.**」2,480 pts / 464 条评论
  - 「I Built a multi-agent pipeline to fully automate my blog & backlink building. 3 months」89 pts / 105 条评论
  - 「We built a data agent that saves our analyst team ~200 hrs/week.」4 pts / 13 条评论
- **打法**：
  - 主力发「真实搭建经验 + 踩坑分享」长帖（不放链接，链接放在置顶评论）
  - 标题套用 §5.2 公式四（横向对比）/ 公式一（数量 + 时间）
  - 例：`I built a data agent for analytics in 3 months — here's what actually worked vs what failed`

### 🥇 r/LocalLLaMA（718k）—— 技术信任层

- **话题契合度**：⭐⭐⭐⭐（技术决策者社区，对 agentic 数据分析高度关注）
- **规则**：
  - 必须与 LLM 相关
  - **必须披露利益相关**（"Affiliation must be disclosed"）
  - 1:10 自荐比例
  - 禁 engagement farming
- **高赞参考帖**：
  - 「[Model Release] I trained a 9B model to be agentic Data Analyst (Qwen3.5-9B + LoRA)」131 pts / 43 条评论
  - 「I was backend lead at Manus. After building agents for 2 years, I stopped using function calls」1,957 pts / 423 条评论
- **打法**：
  - 走「技术深度 + 公开 benchmark/复现」路线
  - 标题前缀用 `[Discussion]` / `[Project]` / `[Tutorial]`
  - 公开承认是项目维护者，反而比"伪装独立用户"更受欢迎

### 🥇 r/LangChain（98k）—— 开发者精准池

- **话题契合度**：⭐⭐⭐⭐⭐（直接覆盖 agent 框架开发者）
- **规则**：最宽松。只要不发明显 spam 即可
- **高赞参考帖**：
  - 「Built a data layer with ~300 capabilities for agents and apps that need real-world data」(1 pts / 8 cmts，新帖)
  - 「Building an API that turns messy bank transactions into parsable data for AI Agents」
- **打法**：
  - 偏「实操经验 + 代码片段」型短帖
  - 主动求反馈，参与度高
  - 适合做产品迭代过程中的 build-in-public

---

## 三、Tier 2 阵地（次重点 + 长尾流量）

### r/datascience（2.7M）

- 1:9 自荐比例；**禁 listicles / 视频链接 / 周话题（career 必须发到 weekly thread）**
- 高赞参考：
  - 「Are you using any AI agent in your work in data science/analytics?」55 pts / 63 cmts
  - 「Google DS-STAR: A state-of-the-art versatile data science agent」68 pts / 13 cmts
- 打法：发「真实工作流测评」「DS 团队接入 agent 的得失」类长文

### r/ChatGPTPro（581k）

- 1:10；禁纯链接帖
- 高赞参考：「OpenAI Releases ChatGPT Agent」267 pts / 99 cmts
- 打法：紧贴官方 ChatGPT Agent 发布节奏发对比测评

### r/SaaS（688k）

- ⚠ **60 天只能提及 1 次**，规则非常严
- 高赞参考：「I'm building an agentic AI platform that connects to your database」3 pts / 15 cmts
- 打法：建议用「无品牌的方法论长文」+ 评论区与用户对话

### r/PromptEngineering（373k）

- 较宽松
- 打法：发「让 data agent 不漂移的 prompt 设计」类内容

---

## 四、Tier 3 阵地（只评论，不发帖）

这些社区规则严格禁止 vendor / AI 生成内容 / 商业自荐，**禁止发布原创帖推广，但是可以以普通用户身份在他人帖子下高质量评论，把自己的项目当作"参考案例"自然提及**：

| Sub | 关键禁区 |
|---|---|
| r/dataengineering | 禁 vendor / 禁 AI 生成内容 / 自荐 1 月 1 次 |
| r/BusinessIntelligence | **完全禁 vendor + 禁 Bot/AI 内容** |
| r/LLMDevs | **完全禁商业自荐** + 禁伪装求助 |
| r/analytics | 禁 blog spam，推广严控 |

> 但这几个 sub 里恰恰有最热的「data agent」相关讨论（见下方"黄金切入帖"），是评论区埋点的金矿。

---

## 五、黄金切入帖（可立即评论的现成讨论）

这些帖子是过去一年「data agent」语义的高赞讨论，**可立即跟评**（带具体经验/数据，不强推产品）：

| Subreddit | 标题（部分） | 热度 |
|---|---|---|
| r/dataengineering | Has anyone tried building their own AI/data agents for analytics workflows? | 66 pts / 49 cmts |
| r/dataengineering | Anyone here experimenting with AI agents for data engineering? Curious what people are using | 30 pts / 37 cmts |
| r/dataengineering | Agentic AI in data engineering | 11 pts / 28 cmts |
| r/datascience | Are you using any AI agent in your work in data science/analytics? | 55 pts / 63 cmts |
| r/datascience | Data Science Managers and Leaders - How are you prioritizing the insane number of requests | 59 pts / 28 cmts |
| r/BusinessIntelligence | Anyone got real world examples of using an AI Data Science agent? | 6 pts / 8 cmts |
| r/BusinessIntelligence | OpenAI's Data Agent and the S3 Gap | 0 pts / 8 cmts |
| r/AI_Agents | We built a data agent that saves our analyst team ~200 hrs/week. (Databricks, Omni, DBT...) | 4 pts / 13 cmts |
| r/SaaS | Agents and Automation connecting to internal data sources | 4 pts / 10 cmts |
| r/analytics | What data/data pipeline challenges come up when building AI agents for real business use? | 1 pts / 3 cmts |
| r/analytics | Semantic layer for ai agents requires way better data integration than the blog posts make | 21 pts / 19 cmts |
| r/LLMDevs | Giving AI agents direct access to production data feels like a disaster waiting to happen | 13 pts / 24 cmts |

---

## 六、首批行动建议（按周）

### 第 1-2 周：养号 + 评论

- 把 5 个常用账号注册/激活
- 在「黄金切入帖」清单里每日选 2-3 条，发布**高质量真实评论**（≥ 100 字、附数据/经验）
- 目标：每个核心账号 karma 攒到 100+

### 第 3-4 周：T1 首发

- 在 r/AI_Agents 发首篇长文（标题套 §5.2 公式四对比型）
- 在 r/LangChain 发首篇 build-in-public 短帖
- 在 r/LocalLLaMA 发首篇技术深度帖（明确披露身份）

### 第 5-8 周：T2 扩张 + T3 评论持续

- T2 每 sub 每月 1 篇深度长文
- T3 持续评论埋点
- 每周用「`according to Reddit` + data agent」类 prompt 在 ChatGPT 实测引用情况（对应 SOP §6.1 铁律）

---

## 七、监控 Prompt 候选（用于评估 GEO 效果）

> 用于在 ChatGPT 中定期测试，看 Reddit 内容是否被引用。

1. `What's the best AI data agent for analytics teams in 2026? According to Reddit users.`
2. `Best data agent vs traditional BI tools — what do Reddit data engineers actually say?`
3. `I'm a data engineer evaluating AI agents for our pipeline. What does Reddit recommend?`
4. `Compare popular AI data agents for SQL-heavy workflows according to Reddit discussions`
5. `What are the real production issues with AI data agents? Cite Reddit threads.`

---

## 附：原始侦察数据

- 调研 24 个 subreddit，订阅数全部通过 `reddit.com/r/{sub}/about.json` 获取（API 公开口径）
- 站内搜索 12 个 sub × Top 3 相关帖 = 36 条参考帖
- 抓取 10 个核心 sub 的完整规则（`about/rules.json`）
- 浏览器自动化执行：`~/.auto-coder/.autocodertools/agent-browser`
