"""Agent SDK 薄启动器：在本仓库起一次无头 Claude Code 会话，日志落盘 logs/。

用法：
    python run.py "<任务描述>"    # 运行一次会话；控制台打印进度摘要，完整日志存 logs/
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    Message,
    ResultMessage,
    ServerToolResultBlock,
    ServerToolUseBlock,
    SystemMessage,
    TextBlock,
    ThinkingBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    query,
)

REPO_ROOT = Path(__file__).resolve().parent
LOG_DIR = REPO_ROOT / "logs"

ALLOWED_TOOLS = ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "Skill", "Task", "Agent"]


def _setup_logging(workspace: Path | None) -> logging.Logger:
    """控制台只打一行摘要（INFO）；文件日志存完整内容（DEBUG），UTF-8 落盘。

    有工作区 → 落盘工作区/run.log（批量时日志跟着任务走）；无 → 落盘 logs/run_<ts>.log。
    """
    if workspace is not None:
        workspace.mkdir(parents=True, exist_ok=True)
        log_path = workspace / "run.log"
    else:
        LOG_DIR.mkdir(exist_ok=True)
        log_path = LOG_DIR / f"run_{time.strftime('%Y%m%d_%H%M%S')}.log"
    log = logging.getLogger("run")
    log.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(console_handler)
    return log


def _content_summary(content: str | list | None) -> str:
    """消息内容压成单行文本（兼容 str、dict 块、dataclass ContentBlock）。"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content.replace("\n", " ").strip()
    parts: list[str] = []
    for b in content:
        if isinstance(b, dict):
            btype = b.get("type")
            if btype == "text":
                parts.append(str(b.get("text", "")))
            elif btype == "tool_result":
                parts.append(f"[tool_result]{_content_summary(b.get('content'))}")
            else:
                parts.append(f"[{btype}]")
        elif isinstance(b, TextBlock):
            parts.append(b.text)
        elif isinstance(b, ThinkingBlock):
            parts.append("[thinking]")
        elif isinstance(b, (ToolUseBlock, ServerToolUseBlock)):
            parts.append(f"[tool:{b.name}]")
        elif isinstance(b, (ToolResultBlock, ServerToolResultBlock)):
            parts.append(f"[tool_result]{_content_summary(b.content)}")
        else:
            parts.append(repr(b))
    return " ".join(parts)


def _tool_detail(block: ToolUseBlock | ServerToolUseBlock) -> str:
    """工具输入摘要：常见字段取前 120 字符，其他取 JSON。"""
    inp = block.input or {}
    for key in ("file_path", "command", "pattern", "url", "prompt"):
        if isinstance(inp.get(key), str):
            return f" {key}={inp[key][:120]!r}"
    return f" {json.dumps(inp, ensure_ascii=False)[:120]}"


def _brief(msg: Message) -> str:
    """把一条 SDK 消息压成一行进度摘要。"""
    if isinstance(msg, ResultMessage):
        cost = f"${msg.total_cost_usd:.4f}" if msg.total_cost_usd is not None else "$?"
        return f"[result] error={msg.is_error} cost={cost} {(msg.result or '')[:120]}"
    if isinstance(msg, SystemMessage):
        return f"[system:{msg.subtype}] {json.dumps(msg.data, ensure_ascii=False)[:200]}"
    if isinstance(msg, UserMessage):
        return f"[user] {_content_summary(msg.content)[:500]}"
    if isinstance(msg, AssistantMessage):
        parts: list[str] = []
        for block in msg.content:
            if isinstance(block, TextBlock):
                parts.append(block.text[:500])
            elif isinstance(block, ThinkingBlock):
                parts.append("[thinking]")
            elif isinstance(block, (ToolUseBlock, ServerToolUseBlock)):
                detail = _tool_detail(block)
                parts.append(f"[tool:{block.name}]{detail}")
            elif isinstance(block, ToolResultBlock):
                parts.append(f"[tool_result]{_content_summary(block.content)[:300]}")
            elif isinstance(block, ServerToolResultBlock):
                parts.append(f"[tool_result]{json.dumps(block.content, ensure_ascii=False)[:300]}")
        return f"[assistant] {' '.join(parts)[:1000]}"
    return f"[{type(msg).__name__}]"


def _full(msg: Message) -> str:
    """消息完整内容（仅文件日志，不截断）。"""
    if isinstance(msg, ResultMessage):
        return f"[result] error={msg.is_error} session={msg.session_id} result:\n{msg.result or ''}"
    if isinstance(msg, SystemMessage):
        return f"[system:{msg.subtype}] {json.dumps(msg.data, ensure_ascii=False)}"
    if isinstance(msg, UserMessage):
        return f"[user]\n{_content_summary(msg.content)}"
    if isinstance(msg, AssistantMessage):
        blocks: list[str] = []
        for block in msg.content:
            if isinstance(block, TextBlock):
                blocks.append(f"<text>\n{block.text}\n</text>")
            elif isinstance(block, ThinkingBlock):
                blocks.append(f"<thinking>\n{block.thinking}\n</thinking>")
            elif isinstance(block, (ToolUseBlock, ServerToolUseBlock)):
                blocks.append(f"<tool_use name={block.name}>\n{json.dumps(block.input, ensure_ascii=False)}\n</tool_use>")
            elif isinstance(block, ToolResultBlock):
                blocks.append(f"<tool_result error={block.is_error}>\n{block.content}\n</tool_result>")
            elif isinstance(block, ServerToolResultBlock):
                blocks.append(f"<server_tool_result>\n{json.dumps(block.content, ensure_ascii=False)}\n</server_tool_result>")
        return "[assistant]\n" + "\n".join(blocks)
    return f"[{type(msg).__name__}]"


def _usage_summary(result: ResultMessage) -> str:
    """按模型汇总 token 用量，返回一行文本。"""
    parts: list[str] = []
    for name, usage in (result.model_usage or {}).items():
        parts.append(
            f"{name}: in={usage.get('inputTokens', 0)} out={usage.get('outputTokens', 0)} "
            f"cache_read={usage.get('cacheReadInputTokens', 0)} cache_write={usage.get('cacheCreationInputTokens', 0)}"
        )
    if not parts and result.usage:
        parts.append(str(result.usage))
    return " | ".join(parts) or "no usage data"


async def _query(log: logging.Logger, options: ClaudeAgentOptions, prompt: str) -> ResultMessage | None:
    """运行一次 query，流式记录进度，返回最终结果消息。"""
    final: Message | None = None
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, SystemMessage) and msg.subtype == "thinking_tokens":
                continue  # 思考 token 计数元数据，无信息量
            log.debug(_full(msg))  # 文件日志：完整内容
            log.info(_brief(msg))  # 控制台：一行摘要
            final = msg
    except Exception as exc:
        # SDK 在 max_turns 耗尽时抛异常而非返回 ResultMessage；预算耗尽=设计内终止
        if "maximum number of turns" in str(exc):
            log.info("turns exhausted (max_turns reached)")
            return None
        raise
    return final if isinstance(final, ResultMessage) else None


def _disable_auto_memory() -> None:
    """禁用 SDK 会话的 auto-memory：领域事实已固化进 skill references/facts.md，
    实验会话不得加载会话外记忆（可复现性 + C1 对照纯净性）。"""
    os.environ["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"


# C1 bare 模式禁读的协议文件（SKILL.md / assets 示例），cli-commands.md（工具用法）放行
_BLOCKED_PROTOCOL = ("SKILL.md", "examples.md")


async def _bare_guard(input: dict, tool_use_id: str | None, context) -> dict:
    """PreToolUse 回调：C1 裸 LLM 模式下拦截对 skill 协议文件的读取（Read/Bash/Grep/Glob）。"""
    probe = " ".join(str(v) for v in (input.get("tool_input") or {}).values())
    for blocked in _BLOCKED_PROTOCOL:
        if blocked in probe:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"C1 裸 LLM 对照模式禁止读取协议文件（{blocked}）",
                }
            }
    return {}


async def _run(
    log: logging.Logger,
    prompt: str,
    max_turns: int | None,
    system: str | None = None,
    skills: list[str] | None = None,
    hooks: dict | None = None,
    model: str | None = None,
) -> int:
    """跑一次会话，返回进程退出码。"""
    options = ClaudeAgentOptions(
        system_prompt=system,
        skills=skills,
        hooks=hooks,
        permission_mode="bypassPermissions",
        effort="max",
        enable_file_checkpointing=True,
        allowed_tools=ALLOWED_TOOLS,
        setting_sources=["project"],
        max_turns=max_turns,
        cwd=str(REPO_ROOT),
        model=model or None,
    )
    result = await _query(log, options, prompt)
    if result is None:
        # 正常终止（含 max_turns 预算耗尽）：agent 已按协议写 log.jsonl，退出码 0
        log.info("session finished")
        return 0
    if result.is_error:
        log.error("error: %s", getattr(result, "errors", "unknown error"))
        return 1
    log.info("tokens: %s", _usage_summary(result))
    log.info("result:\n%s", result.result or "")
    return 0


def main(argv: list[str] | None = None) -> int:
    _disable_auto_memory()
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="无头 Claude Code 会话（本仓库，项目 settings，bypassPermissions）",
    )
    parser.add_argument("prompt", nargs="?", help="任务描述，例如：python run.py \"设计一款能量密度提升20%%的电池…\"")
    parser.add_argument("--max-turns", type=int, default=300, help="最大对话轮数（默认 1000）")
    parser.add_argument("--workspace", default=None, help="工作区目录（产物落点）；不传=agent 自行决定")
    parser.add_argument("--model", default=os.environ.get("ANTHROPIC_MODEL") or "", help="模型覆盖（鲁棒性实验用，如 deepseek-v4-pro；默认=ANTHROPIC_MODEL 或会话默认）")
    parser.add_argument(
        "--bare",
        action="store_true",
        help="C1 裸 LLM 对照：不加载 skill、无协议规则，只给工具说明与目标",
    )
    parser.add_argument(
        "--override",
        default=None,
        help="system prompt 覆盖（消融 B 用：如 '结构变体数量不做强制要求'）——系统层指令，覆盖 skill 规则",
    )
    args = parser.parse_args(argv)
    if not args.prompt:
        parser.error('需要任务描述，例如：python run.py "设计一款能量密度提升20%的电池…"')
    if args.max_turns is not None and args.max_turns <= 0:
        parser.error("--max-turns 必须为正整数")
    ws = Path(args.workspace).resolve() if args.workspace else None
    if args.bare:
        # C1 裸 LLM：工具说明 + 目标，无协议规则（不含漏斗/回退/criteria/审计要求）；
        # 真 DFT/MD 代码禁用（背书是协议流程的一部分，C1 无协议不需要）
        os.environ["BDA_DISABLE_TRUE_COMPUTE"] = "1"
        system = (
            "你是电池设计智能体。可用工具：Bash/Read/Write/Edit/Grep/Glob。\n"
            "仿真工具库 bda：`.venv\\Scripts\\python.exe -m bda <子命令>`"
            "（子命令见 `-m bda --help`，完整用法参考 "
            ".claude/skills/virtual-battery-factory/references/cli-commands.md）。\n"
            f"目标：{args.prompt}"
        )
        if ws:
            system += f"\n工作区：{ws}"
        from claude_agent_sdk import HookMatcher

        log = _setup_logging(ws)
        return asyncio.run(
            _run(
                log,
                "",
                args.max_turns,
                system=system,
                skills=[],
                hooks={"PreToolUse": [HookMatcher(matcher="Read|Bash|Grep|Glob", hooks=[_bare_guard])]},
                model=args.model or None,
            )
        )
    prompt = f"headless 会话：无用户在场，跳过澄清提问（SKILL.md 零交互执行规则），参数从任务文本解析、缺省用默认值，写入 log.jsonl 第 0 条。\n任务：{args.prompt}"
    if ws:
        prompt = f"工作区：{ws}\n" + prompt
    system = f"你是电池设计智能体。本任务中：{args.override}" if args.override else None
    log = _setup_logging(ws)
    return asyncio.run(_run(log, prompt, args.max_turns, system=system, model=args.model or None))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
