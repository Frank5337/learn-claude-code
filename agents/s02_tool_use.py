#!/usr/bin/env python3
# Harness: tool dispatch -- expanding what the model can reach.
# 这一课的重点是：
# s01 里只有一个 bash 工具；
# s02 开始把工具变成“声明 + handler 分发”的模式。
"""
s02_tool_use.py - Tools

The agent loop from s01 didn't change. We just added tools to the array
and a dispatch map to route calls.

    +----------+      +-------+      +------------------+
    |   User   | ---> |  LLM  | ---> | Tool Dispatch    |
    |  prompt  |      |       |      | {                |
    +----------+      +---+---+      |   bash: run_bash |
                          ^          |   read: run_read |
                          |          |   write: run_wr  |
                          +----------+   edit: run_edit |
                          tool_result| }                |
                                     +------------------+

Key insight: "The loop didn't change at all. I just added tools."
"""

# 操作系统相关工具。
import os

# 启动子进程，类似 Java 的 ProcessBuilder。
import subprocess

# Path 比直接拼字符串路径更安全。
# 可以类比 Java NIO 里的 Path。
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# 读取 `.env`。
load_dotenv(override=True)

# 兼容第三方 Anthropic 协议网关时，清理可能冲突的认证变量。
if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

# 当前工作目录。
WORKDIR = Path.cwd()

# Anthropic 客户端。
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))

# 使用哪个模型。
MODEL = os.environ["MODEL_ID"]

# 系统提示词。
SYSTEM = f"You are a coding agent at {WORKDIR}. Use tools to solve tasks. Act, don't explain."


def safe_path(p: str) -> Path:
    # 这个函数的作用是做“路径沙箱”。
    # 防止模型传入 `../../secret.txt` 之类的路径跳出项目目录。

    # `(WORKDIR / p)`：把相对路径拼到当前工作目录下。
    # `.resolve()`：转成规范化后的绝对路径。
    path = (WORKDIR / p).resolve()

    # `is_relative_to` 用来检查规范化后的路径是否仍然位于工作区内部。
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")

    return path


def run_bash(command: str) -> str:
    # 和 s01 一样，保留一个最简单的 bash 工具。
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]

    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"

    try:
        r = subprocess.run(
            command,
            shell=True,
            cwd=WORKDIR,
            capture_output=True,
            text=True,
            timeout=120,
        )
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"


def run_read(path: str, limit: int = None) -> str:
    # 一个专用“读文件”工具。
    # 相比让模型自己调用 `cat`，这个工具更稳定，也更容易加沙箱控制。
    try:
        text = safe_path(path).read_text()

        # `splitlines()` 会按行拆分文本。
        lines = text.splitlines()

        # 如果用户/模型指定了 limit，就只返回前若干行。
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]

        return "\n".join(lines)[:50000]
    except Exception as e:
        return f"Error: {e}"


def run_write(path: str, content: str) -> str:
    # 一个专用“写文件”工具。
    try:
        fp = safe_path(path)

        # 如果父目录不存在，先创建父目录。
        fp.parent.mkdir(parents=True, exist_ok=True)

        # 直接把内容写入文件。
        fp.write_text(content)

        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    # 一个最小可用的“文本替换式编辑”工具。
    # 它不是 AST 编辑器，也不是 diff 编辑器，
    # 就是把 old_text 替换成 new_text，一次。
    try:
        fp = safe_path(path)
        content = fp.read_text()

        if old_text not in content:
            return f"Error: Text not found in {path}"

        # 第三个参数 `1` 表示只替换第一次出现的位置。
        fp.write_text(content.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


# -- The dispatch map: {tool_name: handler} --
# 这就是本课的核心结构：
# 工具名 -> 真正执行它的 Python 函数。
# 以后加新工具时，不需要改 agent loop；
# 只要扩展 TOOLS 和 TOOL_HANDLERS 就够了。
TOOL_HANDLERS = {
    "bash":       lambda **kw: run_bash(kw["command"]),
    "read_file":  lambda **kw: run_read(kw["path"], kw.get("limit")),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file":  lambda **kw: run_edit(kw["path"], kw["old_text"], kw["new_text"]),
}

# 给模型声明“有哪些工具可用”。
# 注意：这里的名字必须和 TOOL_HANDLERS 里的 key 对上。
TOOLS = [
    {
        "name": "bash",
        "description": "Run a shell command.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
    {
        "name": "read_file",
        "description": "Read file contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "limit": {"type": "integer"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "edit_file",
        "description": "Replace exact text in file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
]


def agent_loop(messages: list):
    # 注意：这个循环和 s01 的结构几乎没变。
    # 这正是该文件想传达的设计原则：
    # “加工具，只加注册和 handler，不动核心 loop。”
    while True:
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=8000,
        )

        # 保存 assistant 回复到历史里。
        messages.append({"role": "assistant", "content": response.content})

        # 如果这轮模型没有继续调用工具，说明它打算结束。
        if response.stop_reason != "tool_use":
            return

        results = []

        for block in response.content:
            if block.type == "tool_use":
                # 根据工具名找到对应的 handler。
                handler = TOOL_HANDLERS.get(block.name)

                # 如果找不到 handler，就返回错误文本，而不是直接抛异常。
                output = handler(**block.input) if handler else f"Unknown tool: {block.name}"

                # 控制台打印一部分结果，方便你观察 agent 在干什么。
                print(f"> {block.name}: {output[:200]}")

                # 把执行结果包装成 tool_result。
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        # 把所有工具结果再喂回模型，开始下一轮思考。
        messages.append({"role": "user", "content": results})


if __name__ == "__main__":
    # 最小命令行交互模式。
    history = []

    while True:
        try:
            query = input("\033[36ms02 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break

        if query.strip().lower() in ("q", "exit", ""):
            break

        history.append({"role": "user", "content": query})
        agent_loop(history)

        # 尝试打印模型最终文本回复。
        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if hasattr(block, "text"):
                    print(block.text)

        print()
