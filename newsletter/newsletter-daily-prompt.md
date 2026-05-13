
# 每日 AI 资讯采集与分析任务

## 任务目标
每天晚上采集 Twitter/X 上与 InfiniSynapse 关注领域相关的最新 AI 资讯，整理后生成类似 https://aihot.virxact.com/ 风格的网页。

## 执行步骤

### 第一步：分析用户关注领域
1. 浏览 `/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/日常运营/` 目录下所有 .md 和 .pdf 文件名
2. 浏览 `/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/外部合作/` 目录内容
3. 提取关键词和关注领域，包括但不限于：
   - Data Agent / AI Agent
   - Claw / WinClaw / OpenClaw
   - Command Tools / MCP
   - InfiniSynapse
   - 数据分析 / AI 数据分析
   - DeepSeek / GPT / Claude
   - AI 工具生态
   - Code Agent
   - 其他从文件名中反映出的趋势话题

### 第二步：采集 Twitter 内容
使用 agent-browser 工具访问 Twitter/X，执行以下操作：

1. **搜索阶段**（至少覆盖 500 条推文）：
   - 针对每个关键领域关键词（data agent, claw/winclaw, command tools, AI data analysis, InfiniSynapse, DeepSeek, AI agent framework 等），在 Twitter 搜索中分别搜索
   - 每个关键词浏览至少 50-100 条搜索结果
   - 重点查看近 24-48 小时内的最新推文
   - 记录高互动量（点赞、转发、评论多）的内容

2. **Feed 流阶段**（至少覆盖 500 条推文）：
   - 浏览 Twitter 首页推荐 feed
   - 浏览 AI/技术领域的热门话题（Trending）
   - 关注以下账号的最新推文（如果可访问）：
     - @AnthropicAI, @OpenAI, @deepseek_ai
     - AI 领域知名 KOL 和研究者
     - AI 工具/开发相关账号
   - 滚动浏览至少 500 条以上内容

3. **总计至少浏览 1000 条以上 Twitter 内容**

### 第三步：边看边记录
在采集过程中，将发现的高质量内容实时记录到 newsletter 文件中：

存放路径：`/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/newsletter/`

文件命名格式：`YYYY-MM-DD-newsletter-raw.md`（如 `2026-05-11-newsletter-raw.md`）

每条记录包含：
```markdown
### [序号] 标题/概要
- **来源**: @Twitter用户名
- **时间**: 发布时间
- **链接**: 推文链接
- **互动**: 点赞数/转发数
- **分类**: [Data Agent/Claw/Command Tools/InfiniSynapse/AI工具/行业动态/...]
- **摘要**: 用中文简要总结内容（2-3句话）
- **相关性**: 高/中/低 — 与 InfiniSynapse 关注领域的相关度
```

至少记录 20-30 条高质量、高相关度的内容。

### 第四步：生成资讯网页
参考 https://aihot.virxact.com/ 的结构，生成一个 HTML 网页：

**网页存放路径**：`/Users/mengyuan/Documents/GitHub/InfiniSynapse-Growth/newsletter/YYYY-MM-DD-ai-news.html`

**网页要求**：
1. 页面标题："AI 每日资讯 — YYYY-MM-DD"
2. 顶部日期和简要统计（共采集多少条、高相关度多少条等）
3. 按分类组织内容，每个分类一个区块
4. 每条资讯卡片包含：头像/用户名、分类标签、中文摘要、原文链接
5. 响应式设计，手机和桌面端均可正常浏览
6. 简洁现代的视觉风格，类似 aihot.virxact.com
7. 支持暗色模式
8. 使用纯 HTML+CSS+JS（内联），无需任何构建工具
9. 页面底部注明生成时间和数据来源

**额外功能**：
- 顶部添加关键领域导航标签，点击可快速跳转到对应分类
- 添加"高相关度"筛选开关
- 统计今日各分类的资讯数量
