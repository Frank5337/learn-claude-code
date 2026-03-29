# Learn Claude Code 总结笔记（Java 开发者版）

这份文档是对 `s01-s12` 的一份压缩总结，目标不是替代原文档，而是帮你快速建立整个仓库的心智模型。

如果你是 Java 开发者，可以把这个仓库理解成：

`一个 coding agent harness 是如何从最小循环，一步步长成多 agent 并行执行系统的。`

---

## 先记住一句话

这个仓库最核心的观点是：

- `Agent` 是模型本身
- `Harness` 是围绕模型搭出来的工作环境

也就是说：

- 模型负责感知、推理、决定下一步
- Harness 负责提供工具、知识、上下文管理、任务系统和隔离边界

你不是在“写智能”，你是在“给智能搭工作台”。

---

## 一张总图

`s01-s12` 不是 12 个平行知识点，而是一条连续演进路线：

1. 先让模型能形成最小闭环
2. 再让它拥有更多可控工具
3. 再让它会规划、会拆任务、会加载知识
4. 再让它能管理记忆和外部状态
5. 再让它能异步执行、团队协作、自主认领
6. 最后让它真正并行改代码而不互相踩目录

你可以把整个仓库压成一句话：

`从“会调工具的单 agent”演化到“有任务系统、有团队协议、有 worktree 隔离的多 agent runtime”。`

---

## 高频术语

### Agent

模型本身，不是外面那层 if-else 流程。

### Harness

围绕模型提供的工作环境，包括：

- tools
- skills / knowledge
- context management
- task persistence
- background execution
- team protocols
- worktree isolation

### Tool

一个具体动作，能被模型调用。

例如：

- `bash`
- `read_file`
- `write_file`

可以类比成 Java 里的一个可注册方法。

### Skill

一份按需加载的专业知识包，不是动作本身。

例如：

- `code-review`
- `pdf`
- `mcp-builder`

一句话：

`tool` 让 agent 能做，`skill` 让 agent 更懂怎么做。

### MCP

`Model Context Protocol`

不是 tool，也不是 skill，而是一套把外部能力标准化接给模型的协议。

可以粗略类比成：

- JDBC
- LSP
- 插件协议

### Dispatch

分发 / 路由。

意思是：

根据工具名，把调用转给正确的 handler。

很像：

- `Map<String, Handler>`
- `switch-case`

### Summary

摘要、压缩结果。

在 subagent 场景里，指子 agent 做完活后，不把完整内部历史带回来，只带回一段压缩后的结论说明。

### Docstring

文档字符串。

写在模块、类、函数开头的三引号字符串，用来解释这段代码是干什么的。

可以类比成 Python 里的运行时版本 Javadoc。

---

## 分阶段理解 s01-s12

### 第一阶段：让单个 Agent 活起来

#### s01 Agent Loop

最小闭环。

核心模式：

- 用户发消息
- 模型决定是否调工具
- Harness 执行工具
- 把 `tool_result` 喂回模型
- 循环直到模型不再调用工具

一句话：

`LLM + tools + while 循环 = 最小 agent`

Java 类比：

- 控制循环
- 工具执行器
- 请求-响应反馈闭环

#### s02 Tool Use

重点不是改 loop，而是把工具做成可扩展分发系统。

核心增加：

- 多工具注册
- `tool_name -> handler` 映射
- 路径沙箱

一句话：

`加工具，不改 loop，只加 handler。`

Java 类比：

- Handler registry
- Strategy map

#### s03 TodoWrite

解决多步任务中 agent 跑偏的问题。

核心增加：

- TodoManager
- `pending / in_progress / completed`
- nag reminder

一句话：

`让 agent 会管理自己的短期执行计划。`

和 `s07 task system` 的区别：

- `todo` 管当前会话里的短期步骤
- `task` 管系统级的长期持久状态

#### s04 Subagent

解决复杂任务把主上下文污染掉的问题。

核心增加：

- 子 agent
- 独立 `messages=[]`
- summary 回传

一句话：

`任务可以拆出去做，但不要把全部噪音带回来。`

Java 类比：

- 子任务执行器
- 独立上下文 worker

#### s05 Skill Loading

解决“领域知识不能全塞 system prompt”的问题。

两层注入：

- Layer 1：system prompt 里只放 skill 名称和简介
- Layer 2：真正需要时通过 `load_skill(...)` 加载完整内容

一句话：

`让知识按需加载，而不是启动时全量灌入。`

Java 类比：

- 插件目录
- 延迟加载知识库
- 运行时说明书注入

#### s06 Context Compact

解决长会话上下文一定会爆的问题。

三层压缩：

- `microcompact`
- `auto_compact`
- `compact tool`

一句话：

`不是保留全部历史，而是保留继续工作真正需要的记忆。`

Java 类比：

- 缓存淘汰
- 日志归档
- checkpoint / 阶段总结

---

### 第二阶段：把关键状态搬出对话

#### s07 Task System

这是一条非常关键的分水岭。

核心变化：

- 任务状态不再只放在 `messages` 里
- 改为持久化到 `.tasks/*.json`
- 任务之间可以有依赖关系

核心字段：

- `id`
- `subject`
- `status`
- `blockedBy`
- `blocks`

一句话：

`任务不再靠 agent 记住，而由系统持久化保存。`

Java 类比：

- `Task` 实体
- `TaskRepository`
- 最小依赖图 / 状态机

#### s08 Background Tasks

解决慢操作会阻塞主 loop 的问题。

核心变化：

- 耗时命令放到后台线程执行
- 完成后通过通知队列把结果送回主 agent
- 主 loop 不需要傻等

一句话：

`慢活后台跑，主 agent 继续思考。`

Java 类比：

- 线程池
- 异步任务执行器
- 完成通知队列

---

### 第三阶段：从单人走向团队

#### s09 Agent Teams

从临时 subagent 升级到长期存在的 teammate。

核心增加：

- `.team/config.json`
- 每个 agent 的 `inbox/*.jsonl`
- 长期身份
- `work -> idle -> work` 生命周期

一句话：

`不只是临时分身，而是有长期队友了。`

Java 类比：

- Actor model
- Mailbox worker
- 持久成员注册表

和 `s04` 的区别：

- `s04`：一次性子任务执行器
- `s09`：长期存在的正式队友

#### s10 Team Protocols

团队有了，还要有沟通规矩。

核心增加：

- `request_id`
- request-response 配对
- shutdown protocol
- plan approval protocol

一句话：

`队友之间不只是发消息，而是按协议协作。`

Java 类比：

- correlation id
- handshake protocol
- 审批流 / 状态机

#### s11 Autonomous Agents

让 agent 不再永远等 lead 派活，而是空闲时自己看任务板找活做。

核心增加：

- idle polling
- 自动检查 inbox
- 自动扫描任务板
- 自动 claim task
- identity re-injection

一句话：

`队友开始具备自驱调度能力。`

Java 类比：

- worker polling
- task claiming
- 长生命周期 worker

---

### 第四阶段：真正并行执行而不互相踩

#### s12 Worktree Task Isolation

这是整个仓库最工程落地的一课。

它解决的问题是：

`多个 agent 就算逻辑上分工明确，如果都在同一个目录里改代码，仍然会互相踩。`

核心设计：

- task system 管“做什么”
- worktree system 管“在哪做”

核心结构：

- `.tasks/`
- `.worktrees/index.json`
- `.worktrees/events.jsonl`
- 每个任务绑定一个独立 git worktree

一句话：

`任务板负责协调，worktree 负责隔离执行。`

Java 类比：

- 任务控制平面
- 工作空间注册表
- 生命周期事件流
- 每任务独立执行沙箱

---

## 用一句话串起 s01-s12

你可以把这 12 节课记成下面这条链：

1. `s01` 让模型能通过工具形成闭环
2. `s02` 让工具调用变成可扩展分发系统
3. `s03` 让 agent 会规划当前步骤
4. `s04` 让复杂任务能拆给子 agent
5. `s05` 让知识按需加载
6. `s06` 让长会话能持续工作
7. `s07` 让任务状态持久化到磁盘
8. `s08` 让慢操作后台执行
9. `s09` 让系统拥有长期存在的队友
10. `s10` 让队友之间有正式协议
11. `s11` 让队友主动认领任务
12. `s12` 让并行任务在独立 worktree 中执行

---

## 如果你只想记住每课一句话

| 章节 | 一句话总结 |
|------|------------|
| `s01` | 一个 loop + 一个工具，就能形成最小 agent |
| `s02` | 加工具不改 loop，只加 dispatch handler |
| `s03` | agent 需要显式计划，否则多步任务容易跑偏 |
| `s04` | 子任务要隔离上下文，结果只带 summary 回来 |
| `s05` | 知识不要全塞 prompt，按需加载就够了 |
| `s06` | 上下文总会满，必须学会压缩记忆 |
| `s07` | 关键任务状态要放到对话外持久化保存 |
| `s08` | 慢操作要后台执行，别阻塞主思考链路 |
| `s09` | 临时 subagent 不够，要有长期存在的队友 |
| `s10` | 团队通信必须协议化，不能只靠自然语言 |
| `s11` | 队友不应永远等派活，要能主动认领任务 |
| `s12` | 多任务并行执行时，目录必须物理隔离 |

---

## 站在 Java 开发者角度，你已经建立了什么映射

你现在其实不是在“学 Python”，而是在学一个 agent runtime 的设计。

可以这样映射：

- `agent loop` = 控制循环
- `tool dispatch` = handler registry
- `todo` = 短期执行状态
- `subagent` = 隔离上下文的子任务执行器
- `skill` = 按需加载的知识插件
- `compact` = 记忆治理 / checkpoint
- `task system` = 外部持久化状态层
- `background task` = 异步执行器
- `agent teams` = 多 worker 协作系统
- `protocols` = 带 request id 的正式通信机制
- `autonomy` = 主动拉取任务的 worker
- `worktree isolation` = 每任务独立工作空间

---

## 最后一句

如果把整个仓库压成一句最实用的话，那就是：

`最好的 agent 系统，不是把智能硬编码出来，而是给模型提供一个足够好的工作环境。`

这个工作环境，就是 harness。
