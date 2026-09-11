"""Thin Agent SDK launcher: start one headless Claude Code session in this repo, logs written to disk.

Usage:
    python run.py "<task description>"    # run one session; console prints progress summary, full log in logs/
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
    """Console prints one-line summaries (INFO); file log stores full content (DEBUG), UTF-8.

    With workspace → write to workspace/run.log (logs follow the task in batches); without → logs/run_<ts>.log.
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
    """Compress message content into a single line (handles str, dict blocks, dataclass ContentBlocks)."""
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
    """Tool input summary: common fields truncated to 120 chars, others as JSON."""
    inp = block.input or {}
    for key in ("file_path", "command", "pattern", "url", "prompt"):
        if isinstance(inp.get(key), str):
            return f" {key}={inp[key][:120]!r}"
    return f" {json.dumps(inp, ensure_ascii=False)[:120]}"


def _brief(msg: Message) -> str:
    """Compress one SDK message into a one-line progress summary."""
    if isinstance(msg, ResultMessage):
        cost = f"${msg.total_cost_usd:.4f}" if msg.total_cost_usd is not None else "$?"
        turns = getattr(msg, "num_turns", "?")
        dur = getattr(msg, "duration_ms", "?")
        return (f"[result] error={msg.is_error} turns={turns} duration_ms={dur} cost={cost} "
                f"{(msg.result or '')[:120]}")
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
    """Full message content (file log only, no truncation)."""
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
    """Summarize token usage per model into one text line."""
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
    """Run one query, stream progress to log, return the final result message."""
    final: Message | None = None
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, SystemMessage) and msg.subtype == "thinking_tokens":
                continue  # thinking-token counter metadata only; not informative
            log.debug(_full(msg))  # file log: full content
            log.info(_brief(msg))  # console: one-line summary
            final = msg
    except Exception as exc:
        # SDK raises instead of returning ResultMessage when max_turns exhausted; budget exhaustion = in-design termination
        if "maximum number of turns" in str(exc):
            log.info("turns exhausted (max_turns reached)")
            return None
        raise
    return final if isinstance(final, ResultMessage) else None


def _disable_auto_memory() -> None:
    """Disable SDK session auto-memory: domain facts are already fixed in the skill's references;
    experiment sessions must not load out-of-session memory (reproducibility + C1 control purity)."""
    os.environ["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"


def _plugin_off_settings() -> str | None:
    """Highest-priority settings layer disabling every plugin enabled by project settings.

    Governed sessions must load no plugin skills/hooks/MCP servers; the protocol skills
    (virtual-battery-factory, cad-skill) are repo skills, not plugins, and stay available.
    MCP servers are additionally blocked by strict_mcp_config.
    """
    path = REPO_ROOT / ".claude" / "settings.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    disabled = {name: False for name in (data.get("enabledPlugins") or {})}
    return json.dumps({"enabledPlugins": disabled}) if disabled else None


async def _run(
    log: logging.Logger,
    prompt: str,
    max_turns: int | None,
    system: str | None = None,
    skills: list[str] | None = None,
    model: str | None = None,
    plugins: list[str] | None = None,
    allowed_tools: list[str] | None = None,
    tools: list[str] | None = None,
    resume: str | None = None,
) -> int:
    """Run one session, return the process exit code. With `resume`, continue an
    interrupted session (by id) from its own transcript."""
    if resume:
        log.info("resuming session %s", resume)
    options = ClaudeAgentOptions(
        system_prompt=system,
        skills=skills,
        resume=resume,
        permission_mode="bypassPermissions",
        effort="max",
        enable_file_checkpointing=True,
        allowed_tools=allowed_tools or ALLOWED_TOOLS,
        tools=tools or None,
        setting_sources=["project"],
        plugins=plugins,
        settings=_plugin_off_settings(),
        strict_mcp_config=True,
        max_turns=max_turns,
        cwd=str(REPO_ROOT),
        model=model or None,
    )
    result = await _query(log, options, prompt)
    if result is None:
        # Normal termination (incl. max_turns budget exhaustion): agent already wrote log.jsonl per protocol; exit 0
        log.info("session finished")
        return 0
    if result.is_error:
        log.error("error: %s", getattr(result, "errors", "unknown error"))
        return 1
    log.info("tokens: %s", _usage_summary(result))
    log.info("sdk_turns: %s | sdk_duration_ms: %s | api_duration_ms: %s",
             getattr(result, "num_turns", "?"), getattr(result, "duration_ms", "?"),
             getattr(result, "duration_api_ms", "?"))
    log.info("result:\n%s", result.result or "")
    return 0


def main(argv: list[str] | None = None) -> int:
    _disable_auto_memory()
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Headless Claude Code session (this repo, project settings, bypassPermissions)",
    )
    parser.add_argument("prompt", nargs="?", help="Task description, e.g.: python run.py \"design a battery with 20%% higher energy density...\"")
    parser.add_argument("--max-turns", type=int, default=300, help="Maximum conversation turns (default 1000)")
    parser.add_argument("--workspace", default=None, help="Workspace directory (artifact destination); unset = agent decides")
    parser.add_argument("--model", default=os.environ.get("ANTHROPIC_MODEL") or "", help="Model override (robustness experiments, e.g. official-deepseek-v4-pro; default = ANTHROPIC_MODEL or session default)")
    parser.add_argument(
        "--override",
        default=None,
        help="system prompt override (ablation B, e.g. 'architecture variant count not enforced') — system-level instruction, overrides skill rules",
    )
    parser.add_argument("--resume", default=None, help="Resume an interrupted session by its session id (continues that conversation); the prompt is treated as a continuation nudge")
    parser.add_argument(
        "--bare",
        action="store_true",
        help="protocol-free control: initial prompt carries no protocol sentence (no zero-interaction rule, no log.jsonl entry-0 instruction, no SKILL.md reference); role statement kept",
    )
    args = parser.parse_args(argv)
    if args.model in ("deepseek-v4-pro", "official-deepseek-v4-pro"):
        args.model = "official-deepseek-v4-pro"  # official channel (same model, stable/fast)
    if not args.prompt:
        parser.error('Task description required, e.g.: python run.py "design a battery with 20% higher energy density..."')
    if args.max_turns is not None and args.max_turns <= 0:
        parser.error("--max-turns must be a positive integer")
    ws = Path(args.workspace).resolve() if args.workspace else None
    if args.bare:
        prompt = (
            "Headless session: no user present. "
            "WORKSPACE DISCIPLINE: read/write only your own workspace and the task text; do not read "
            "other runs' workspaces or the skill/protocol files.\n"
            f"Task: {args.prompt}"
        )
    else:
        prompt = f"Headless task: no user present. Parse the design target, explore the available simulation tools, and produce your best battery design. Keep notes in the workspace.\nTask: {args.prompt}"
    if ws:
        prompt = f"Workspace: {ws}\n" + prompt
    system = f"You are a battery design agent. In this task: {args.override}" if args.override else None

    allowed_tools = ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "PowerShell"] if args.bare else ALLOWED_TOOLS
    bare_tools = ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "PowerShell"] if args.bare else None
    log = _setup_logging(ws)
    return asyncio.run(_run(log, prompt, args.max_turns, system=system, model=args.model or None, allowed_tools=allowed_tools, tools=bare_tools, resume=args.resume))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
