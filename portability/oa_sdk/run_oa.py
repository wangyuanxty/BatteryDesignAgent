"""run_oa.py — OpenAI Agents SDK harness for the Virtual Battery Factory protocol.

Cross-harness portability experiment (§4.6): the SAME declarative protocol
(SKILL.md as agent instructions), the SAME tool library (bda CLI), the SAME
headless prompt format, and the SAME task texts as the primary harness.
The only variable under test is the orchestration substrate (OpenAI Agents SDK
instead of the Claude agent SDK).

Usage:
    .venv/Scripts/python.exe paper/portability/oa_sdk/run_oa.py "TASK TEXT" \
        --workspace runs/portability/t1_oa --max-turns 300
"""
import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_MD = REPO_ROOT / ".claude" / "skills" / "virtual-battery-factory" / "SKILL.md"

# ---- environment / client setup (before agents import) ----
from dotenv import load_dotenv

load_dotenv(REPO_ROOT / ".env")
_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not _API_KEY:
    print("bda error: DEEPSEEK_API_KEY not set in .env", file=sys.stderr)
    raise SystemExit(1)

from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_client,
    set_tracing_disabled,
)

set_tracing_disabled(True)
set_default_openai_client(
    AsyncOpenAI(base_url="https://api.deepseek.com/v1", api_key=_API_KEY),
    use_for_tracing=False,
)

WORKSPACE: Path = REPO_ROOT  # set in main


# ---- tools (same toolset semantics as the primary harness: shell + files) ----
@function_tool
def run_shell(command: str) -> str:
    """Run a shell command in the repository root and return stdout/stderr (truncated to 8000 chars).
    Use for ALL bda simulation/evaluation commands, e.g. `.venv/Scripts/python.exe -m bda run-pyamm ...`.
    Long simulations may take minutes; the command has a 30-minute timeout."""
    import subprocess

    try:
        r = subprocess.run(
            command,
            shell=True,
            executable="D:/software/Git/bin/bash.exe",
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=1800,
        )
        out = (r.stdout or "") + (("\n[stderr] " + r.stderr) if r.stderr else "")
        return out[-8000:] if out else f"(exit {r.returncode}, no output)"
    except subprocess.TimeoutExpired:
        return "TIMEOUT after 30 minutes"
    except Exception as e:
        return f"ERROR: {e}"


def _resolve(path: str) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = WORKSPACE / p
    return p


@function_tool
def read_file(path: str) -> str:
    """Read a text file (relative to the workspace unless absolute) and return its content (truncated to 12000 chars)."""
    try:
        txt = _resolve(path).read_text(encoding="utf-8", errors="replace")
        return txt[-12000:] if len(txt) > 12000 else txt
    except Exception as e:
        return f"ERROR reading {path}: {e}"


@function_tool
def write_file(path: str, content: str) -> str:
    """Write a text file (relative to the workspace unless absolute). Returns the absolute path written."""
    try:
        p = _resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"written {p} ({len(content)} chars)"
    except Exception as e:
        return f"ERROR writing {path}: {e}"


@function_tool
def list_dir(path: str) -> str:
    """List a directory (relative to the workspace unless absolute)."""
    try:
        p = _resolve(path)
        return "\n".join(sorted(str(x.relative_to(p)) for x in p.iterdir()))
    except Exception as e:
        return f"ERROR listing {path}: {e}"


# ---- event logger ----
def log_event(fh, ev) -> None:
    et = getattr(ev, "type", "?")
    if et == "run_item_stream_event":
        item = ev.item
        it = getattr(item, "type", "?")
        if it == "message_output_item":
            txt = getattr(item, "content", "")
            for b in txt:
                if getattr(b, "type", "") == "output_text":
                    fh.write(f"[assistant] {b.text}\n")
        elif it == "reasoning_item":
            fh.write("[thinking]\n")
        elif it == "tool_call_item":
            _name = getattr(item, "name", None) or getattr(getattr(item, "raw_item", None), "name", "?")
            _args = getattr(item, "arguments", "") or getattr(getattr(item, "raw_item", None), "arguments", "")
            fh.write(f"[tool_call] {_name} {_args}\n")
        elif it == "tool_call_output_item":
            fh.write(f"[tool_result] {str(item.output)[:500]}\n")


def build_instructions(workspace: Path) -> str:
    skill = SKILL_MD.read_text(encoding="utf-8")
    note = (
        "\n\n===== PORTABILITY HARNESS NOTES (read carefully) =====\n"
        f"- You are running under a different agent harness than usual; the protocol rules above are unchanged and fully binding.\n"
        f"- Your workspace (artifacts, log.jsonl, deliverables) is: {workspace}\n"
        "- Shell commands execute in the repository root; use the read/write/list tools with workspace-relative paths.\n"
        "- The bda tool library is invoked exactly as the protocol says: `.venv/Scripts/python.exe -m bda <subcommand> ...`\n"
        "- You may not delegate to other agents; do everything yourself with the four tools provided.\n"
    )
    return skill + note


async def main(argv=None) -> int:
    global WORKSPACE
    parser = argparse.ArgumentParser(prog="run_oa.py", description="OpenAI Agents SDK harness (portability experiment)")
    parser.add_argument("task", help="Task text (natural-language contract)")
    parser.add_argument("--workspace", default=None, help="Workspace directory for artifacts/logs")
    parser.add_argument("--max-turns", type=int, default=300, help="Turn budget (SDK max_turns)")
    parser.add_argument("--model", default="deepseek-v4-pro", help="Model name on the OpenAI-compatible endpoint")
    args = parser.parse_args(argv)

    ws = Path(args.workspace).resolve() if args.workspace else REPO_ROOT / "runs" / "portability" / "scratch"
    ws.mkdir(parents=True, exist_ok=True)
    WORKSPACE = ws
    log_path = ws / "run.log"
    fh = open(log_path, "a", encoding="utf-8")
    fh.write(f"=== run_oa.py start {time.strftime('%Y-%m-%d %H:%M:%S')} | model={args.model} | max_turns={args.max_turns} | workspace={ws} ===\n")

    agent = Agent(
        name="vbf_agent",
        instructions=build_instructions(ws),
        model=args.model,
        tools=[run_shell, read_file, write_file, list_dir],
    )
    prompt = (
        f"headless session: no user present, skip clarification questions (SKILL.md zero-interaction rule), "
        f"parse parameters from the task text, use defaults for unspecified ones, write to log.jsonl entry 0.\n"
        f"Task: {args.task}"
    )
    fh.write(f"[user] {prompt}\n")
    fh.flush()

    result = None
    try:
        result = Runner.run_streamed(agent, prompt, max_turns=args.max_turns)
        async for ev in result.stream_events():
            log_event(fh, ev)
            fh.flush()
    except Exception as exc:
        fh.write(f"[error] {exc}\n")
        fh.close()
        print(f"run_oa error: {exc}", file=sys.stderr)
        return 1
    final = result.final_output if result is not None else "(no result)"
    fh.write(f"[final_output] {final}\n")
    (ws / "final_output.txt").write_text(str(final), encoding="utf-8")
    fh.write(f"=== done {time.strftime('%H:%M:%S')} ===\n")
    fh.close()
    print(f"run_oa finished: {ws} (final output {len(str(final))} chars)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(asyncio.run(main()))
