# WinClaw 接上 InfiniSynapse：让 AI 员工会查数据

- **来源**: 微信公众号
- **链接**: https://mp.weixin.qq.com/s/bIa-sEYcweAguY0ODXZ6vA
- **作者**: 祝威廉
- **发布日期**: 2026-05-07

---

## 概述

很多团队第一次搭 AI Native 协作系统时，先解决的是派活问题：人用自然语言说一句话，`winclaw` 负责理解意图，再把需求写进看板，交给本机的 AI 员工执行。

但这只是第一步。

真正进入业务场景以后，团队会很快遇到另一类需求：查数据、列数据集、做分析、回答经营问题。这时候，单靠「写需求」不够， AI 员工还需要接上专业的数据分析能力。

这篇文章只讲一件事：**如何把 winclaw 和 InfiniSynapse 的 agent_infini 打通，让同一个自然语言入口既能派活，也能查数据、跑分析**。

核心就一句：**agent_infini 配进 WinClaw 以后，同一句话既能派需求，也能在真实数据集上做查询与分析**。

---

## 这条链路是什么

可以先把三者的关系想清楚：

| 组件 | 作用 |
|---|---|
| `winclaw` | 自然语言入口和工具调度中枢 |
| `agent_infini` | winclaw 里调用 InfiniSynapse 能力的工具 |
| InfiniSynapse | 专业数据分析能力和数据集管理后台 |

打通以后，你可以在 winclaw 的同一个对话框里输入：

> 使用 agent_infini 列出我有哪些可用的数据集

winclaw 会理解你的意图，选择 `agent_infini`，再把请求交给 InfiniSynapse 。最终返回的不是一段泛泛的回答，而是你账号下真实可用的数据集列表。

这意味着 AI 员工不再只是「会接需求」。它开始具备一项专业能力：**围绕真实数据做查询和分析**。

---

## 准备条件

开始前确认三件事：

1. 你已经安装并登录了 `winclaw` 桌面客户端。下载地址是 winclaw.cn。
2. 你已经有 InfiniSynapse 账号，并能访问 app.infinisynapse.cn。
3. 你的 winclaw 工具商城里可以找到 `agent_infini`。如果你是在 Code Agent 生态里直接接 InfiniSynapse ，也可以到 www.infinisynapse.cn/tools 下载对应平台的二进制 Command Tool ，放进 `PATH` 后使用。它不需要 `pip install`，不需要 Node ，也不是一个常驻本机的 MCP 服务。

---

## 第一步：在 winclaw 安装 agent_infini

打开 winclaw 桌面客户端。

在左侧栏点击 **工具**，进入工具商城。搜索：

```
agent_infini
```

找到 `agent_infini` 后点击 **安装**。

如果你已经安装过，卡片上通常会显示「已安装」和「设置」。这说明工具已经进入 winclaw 的可调用工具列表，下一步只需要补上 InfiniSynapse 的访问凭证。

---

## 第二步：到 InfiniSynapse 获取 API Key

打开 InfiniSynapse 控制台：

https://app.infinisynapse.cn

登录后，点击左下角齿轮，进入 **API Key 管理** 页面。你也可以直接访问：

```
/ai/apikey
```

在页面右上角点击 **+ 创建 API Key**。

创建完成后，复制形如下面格式的密钥：

```
sk-xxxx
```

这个 API Key 是 `agent_infini` 访问 InfiniSynapse 的凭证。建议按团队、项目或用途分别创建，方便后续管理和吊销。

---

## 第三步：在 winclaw 里配置 agent_infini

回到 winclaw 。

进入左侧栏 **工具**，找到 `agent_infini` 卡片，点击 **设置**。

把刚才从 InfiniSynapse 复制的 API Key 粘贴进去，然后点击 **确认初始化**。

到这里，`winclaw` 已经知道该用哪一个 InfiniSynapse 账号来执行数据分析请求。之后用户在对话框里发起数据相关需求时， winclaw 就可以按需调用 `agent_infini`。

---

## 第四步：在 winclaw 首页验证连通

回到 winclaw **首页**。

在对话框输入：

```
使用 agent_infini 列出我有哪些可用的数据集
```

如果配置正确， winclaw 会开始思考，并调用类似下面的能力：

```
agent_infini db ls
```

成功后，你会看到 InfiniSynapse 返回的数据集列表。

这一步验证的是整条链路：

```
自然语言请求 -> winclaw -> agent_infini -> InfiniSynapse -> 数据集结果
```

一旦这里跑通，说明 winclaw 和 InfiniSynapse 已经打通。

---

## 打通以后能做什么

最直接的用法，是把 winclaw 当成一个自然语言数据入口。

比如：

```
使用 agent_infini 看一下我有哪些数据集
```

或者：

```
使用 agent_infini 帮我分析最近一周的销售数据，找出下滑最明显的品类
```

更进一步，如果你已经搭好了 auto-coder.chat 看板和本机 AI 员工，也可以把数据分析需求直接写进看板。 AI 员工在执行任务时，通过本机 winclaw 调用 `agent_infini`，再把分析结果回写到看板。

这时，看板不只是需求列表，而是统一指挥中心：

```
用户提问 -> winclaw / 看板 -> AI 员工 -> agent_infini -> InfiniSynapse -> 分析结果
```

---

## 常见问题

### 1. agent_infini 是什么？

`agent_infini` 是 winclaw 里连接 InfiniSynapse 能力的工具。你可以把它理解成 AI 员工的数据分析入口。

### 2. 它是不是 MCP ？

不是。 InfiniSynapse 面向 Code Agent 生态提供的是 Command Tools ：按需调起的二进制工具，不是 MCP Server ，也不需要为了接能力而在本机常驻一套独立服务。

### 3. 是否需要 pip install 或 npm install ？

不需要。推荐到 www.infinisynapse.cn/tools 下载对应平台的二进制，放进 `PATH` 后直接使用。

### 4. 为什么要放在 winclaw 里调用？

因为 winclaw 是自然语言入口和工具调度中枢。用户不需要记命令格式，也不需要知道背后有哪些工具。只要把需求说清楚， winclaw 就能选择合适的工具执行。

---

## 小结

这次打通以后，你得到的是一条新的能力链路：

```
winclaw -> agent_infini -> InfiniSynapse
```

它解决的不是「怎么聊天」，而是「怎么让 AI 员工接入真实数据能力」。

先安装 `agent_infini`，再拿到 InfiniSynapse API Key ，回到 winclaw 完成配置，最后用一句「列出我有哪些可用的数据集」验证。只要这一步成功，后续的数据查询、数据分析、看板任务联动，都可以从这条链路继续扩展。

---

## 相关链接

- WinClaw 官网：https://winclaw.cn
- InfiniSynapse 控制台：https://app.infinisynapse.cn
- Command Tools 下载：https://www.infinisynapse.cn/tools
- API Key 管理：https://app.infinisynapse.cn/ai/apikey
