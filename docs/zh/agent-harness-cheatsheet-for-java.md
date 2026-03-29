# Learn Claude Code 精简速查表（Java 开发者版）

这是一份面向快速回顾的速查表。  
如果你想看完整解释，请结合
[agent-harness-summary-for-java.md](/Users/mac/develop/vscode/learn-claude-code/docs/zh/agent-harness-summary-for-java.md)
一起看。

---

## 一句话总纲

`s01-s12 = 从最小 agent loop，演进到带任务系统、团队协议、自治认领和 worktree 隔离的多 agent harness。`

---

## 三组最容易混的概念

| 概念 | 最短解释 | Java/工程类比 |
|------|----------|----------------|
| `tool` | 一个具体动作 | 一个可注册方法 / handler |
| `skill` | 一份按需加载的知识包 | 插件说明书 / 最佳实践文档 |
| `MCP` | 把外部能力接给模型的标准协议 | JDBC / LSP / 插件协议 |

| 概念 | 最短解释 | Java/工程类比 |
|------|----------|----------------|
| `dispatch` | 按名字把请求路由到正确处理逻辑 | `Map<String, Handler>` / `switch-case` |
| `summary` | 子流程返回的压缩结果 | 子任务 Result / 摘要 DTO |
| `docstring` | 写在模块/类/函数开头的文档字符串 | 运行时可读的 Javadoc 风格说明 |

---

## s01-s12 一页速记

| 章节 | 主题 | 一句话记忆 | Java/后端类比 |
|------|------|------------|----------------|
| `s01` | Agent Loop | 模型调工具，结果回喂，形成最小闭环 | 控制循环 |
| `s02` | Tool Use | 加工具不改 loop，只加 dispatch handler | Handler registry |
| `s03` | TodoWrite | 用 todo 管当前步骤，防止多步任务跑偏 | 运行时 checklist |
| `s04` | Subagent | 子任务独立上下文执行，只回传 summary | 子任务执行器 |
| `s05` | Skill Loading | 知识按需加载，不全塞 prompt | 延迟加载知识库 |
| `s06` | Context Compact | 上下文会爆，要分层压缩记忆 | 缓存淘汰 + checkpoint |
| `s07` | Task System | 关键任务状态持久化到磁盘 | Repository + 状态机 |
| `s08` | Background Tasks | 慢操作丢后台，主 loop 不阻塞 | 异步执行器 |
| `s09` | Agent Teams | 有长期存在的队友和 mailbox | Actor / worker team |
| `s10` | Team Protocols | 团队通信必须带协议和 request_id | correlation id + handshake |
| `s11` | Autonomous Agents | 队友自己看任务板、自己认领活 | polling worker + task claim |
| `s12` | Worktree Isolation | 每个任务一个独立 worktree，互不打架 | 每任务独立工作空间 |

---

## 四阶段总览

| 阶段 | 覆盖章节 | 核心问题 | 最短答案 |
|------|----------|----------|----------|
| 1 | `s01-s06` | 单个 agent 怎么更会干活 | 会调工具、会规划、会用知识、会管理记忆 |
| 2 | `s07-s08` | 状态和慢任务怎么放到对话外 | 任务持久化 + 后台执行 |
| 3 | `s09-s11` | 多个 agent 怎么协作和主动找活 | team + protocol + autonomy |
| 4 | `s12` | 并行改代码怎么避免互相踩 | task 管目标，worktree 管目录 |

---

## 最值得记住的五句话

1. `Agent 是模型，Harness 是工作环境。`
2. `最小 agent 的本质是 tool_use -> tool_result -> loop。`
3. `知识不要全塞 prompt，任务不要全靠上下文记。`
4. `有队友之后，要有协议；有协议之后，才谈自治。`
5. `task 决定做什么，worktree 决定在哪做。`
