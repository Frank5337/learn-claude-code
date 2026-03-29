#!/usr/bin/env python3
# Harness: the loop -- the model's first connection to the real world.
# 上面这一行 shebang 可以理解成：
# “如果在 Unix/macOS 里把这个脚本当成可执行文件运行，请用 python3 来解释它。”
"""
s01_agent_loop.py - The Agent Loop

The entire secret of an AI coding agent in one pattern:

    while stop_reason == "tool_use":
        response = LLM(messages, tools)
        execute tools
        append results

    +----------+      +-------+      +---------+
    |   User   | ---> |  LLM  | ---> |  Tool   |
    |  prompt  |      |       |      | execute |
    +----------+      +---+---+      +----+----+
                          ^               |
                          |   tool_result |
                          +---------------+
                          (loop continues)

This is the core loop: feed tool results back to the model
until the model decides to stop. Production agents layer
policy, hooks, and lifecycle controls on top.
"""

# `os` 模块：拿环境变量、当前目录等系统信息。
# 你可以把它粗略理解成 Java 里一组和 `System.getenv`、工作目录有关的工具方法。
import os

# `subprocess` 模块：启动外部进程，类似 Java 的 `ProcessBuilder`。
import subprocess

# Anthropic SDK 客户端类，用来向模型发消息。
from anthropic import Anthropic

# dotenv：把 `.env` 文件中的配置加载到环境变量。
from dotenv import load_dotenv

# 读取项目根目录下的 `.env` 文件。
# `override=True` 表示即使某些环境变量已经存在，也允许被 `.env` 里的值覆盖。
load_dotenv(override=True)

# 如果用户配置了兼容 Anthropic 协议的第三方网关地址，
# 就主动移除一个可能冲突的认证变量，避免 SDK 走错认证逻辑。
if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

# 创建 API 客户端。
# 可以类比成 Java 里的 `new AnthropicClient(baseUrl)`。
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))

# 从环境变量里读取模型 ID。
# 这里故意用 `os.environ["MODEL_ID"]` 而不是 `get`：
# 如果没配，会立刻报错，提醒你环境变量缺失。
MODEL = os.environ["MODEL_ID"]

# 系统提示词。
# `f"..."` 是 Python 的格式化字符串，和 Java 的模板插值 / String.format 很像。
# `os.getcwd()` 会返回当前工作目录。
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

# 声明工具列表。
# 这里目前只给模型暴露了一个工具：`bash`。
# Python 的 list 可以理解成 Java 的 `List`，
# Python 的 dict 可以理解成 Java 的 `Map<String, Object>`。
TOOLS = [{
    # 工具名。模型发起工具调用时会引用这个名字。
    "name": "bash",
    # 工具描述，主要是给模型看的。
    "description": "Run a shell command.",
    # 工具参数的 JSON Schema。
    "input_schema": {
        # 表示这个工具接收一个 JSON 对象作为参数。
        "type": "object",
        # 对象里允许有哪些字段。
        "properties": {
            # `command` 参数要求是字符串。
            "command": {"type": "string"}
        },
        # 哪些字段是必填。
        "required": ["command"],
    },
}]


def run_bash(command: str) -> str:
    # 函数签名解释：
    # `command: str` 表示参数 command 是字符串。
    # `-> str` 表示返回值也是字符串。
    # 可以类比成 Java：
    #   String runBash(String command)

    # 一个极简的危险命令黑名单。
    # 这里只是教学示例，不是生产级安全策略。
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]

    # `any(...)` 的意思是：
    # 只要生成器里的任意一个表达式为 True，结果就为 True。
    # 这里就是“只要命令里包含任意一个危险片段，就拒绝执行”。
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"

    try:
        # 真正执行 shell 命令。
        # `shell=True`：让 shell 来解释命令字符串，例如 `ls -la`。
        # `cwd=os.getcwd()`：在当前工作目录执行。
        # `capture_output=True`：抓取 stdout/stderr，而不是直接打印到终端。
        # `text=True`：把输出当作字符串处理，而不是 bytes。
        # `timeout=120`：最多等 120 秒。
        r = subprocess.run(
            command,
            shell=True,
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=120,
        )

        # 把标准输出和标准错误合并起来。
        out = (r.stdout + r.stderr).strip()

        # 工具返回给模型的结果不宜无限长，所以这里做一个字符级截断。
        # 如果命令完全没有输出，则返回一个占位字符串。
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        # 如果 shell 命令超时，不让整个程序崩掉，而是把错误文本返回给模型。
        return "Error: Timeout (120s)"


# -- The core pattern: a while loop that calls tools until the model stops --
def agent_loop(messages: list):
    # `messages` 就是完整对话历史。
    # 你可以把它想成：
    #   List<Map<String, Object>> messages
    # 里面按顺序保存 user / assistant / tool_result 等消息。
    while True:
        # 向模型发起一次请求。
        # 每一轮都把“完整历史 + 可用工具”一起发过去，
        # 让模型自己决定是继续调用工具，还是直接给最终文本回复。
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )

        # 把模型刚刚这一轮的回复追加到历史中。
        # 如果你不做这一步，下一轮模型就看不到自己上一轮说过什么。
        messages.append({"role": "assistant", "content": response.content})

        # `stop_reason != "tool_use"` 表示模型这轮没有继续请求工具。
        # 这通常意味着：它准备好直接结束本次推理了。
        if response.stop_reason != "tool_use":
            return

        # 用来收集这一轮所有工具调用的执行结果。
        results = []

        # `response.content` 里可能同时包含文本块和 tool_use 块，
        # 所以需要逐块遍历。
        for block in response.content:
            # 只处理工具调用块。
            if block.type == "tool_use":
                # 在本地终端打印出模型想执行的命令，方便人类观察。
                print(f"\033[33m$ {block.input['command']}\033[0m")

                # 真正执行命令。
                output = run_bash(block.input["command"])

                # 只预览前 200 个字符，避免终端输出过长。
                print(output[:200])

                # 组装成 Anthropic 规定的 `tool_result` 结构。
                # `tool_use_id` 非常重要，它用来标识“这是对哪次工具调用的响应”。
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        # 把工具结果整体作为一条新的 user 消息塞回历史。
        # 这一步就是 agent loop 的核心闭环：
        # 模型提工具请求 -> Harness 执行 -> 结果再喂给模型。
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    # 只有直接运行这个脚本时，这个 REPL 循环才会生效。
    history = []

    while True:
        try:
            # 从终端读取用户输入。
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D 或 Ctrl+C 时优雅退出。
            break

        # 这些输入都视为“结束程序”。
        if query.strip().lower() in ("q", "exit", ""):
            break

        # 把当前用户问题追加进对话历史。
        history.append({"role": "user", "content": query})

        # 执行 agent loop，直到模型不再调用工具。
        agent_loop(history)

        # 取最后一条消息的 content。
        # `history[-1]` 是 Python 的“倒数第 1 个元素”写法。
        response_content = history[-1]["content"]

        # 如果 content 是列表，就尝试把其中的文本块打印出来。
        if isinstance(response_content, list):
            for block in response_content:
                # 并不是所有 block 都有 `.text` 属性。
                # 文本块有，tool_result 这种字典通常没有。
                if hasattr(block, "text"):
                    print(block.text)

        # 单纯为了终端输出更易读，额外空一行。
        print()
