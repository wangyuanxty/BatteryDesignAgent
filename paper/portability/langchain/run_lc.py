"""run_lc.py — LangChain harness for the Virtual Battery Factory protocol.

Cross-harness portability experiment (§4.6), LangChain leg. Uses LangChain's
own on-demand skill idiom: the protocol (SKILL.md) is packaged as a skill the
agent loads via a load_skill tool (progressive disclosure), and the bda CLI
remains the shared tool library. Same task texts, same model, same budget
(recursion_limit) as the other legs.

Usage:
    .venv/Scripts/python.exe paper/portability/langchain/run_lc.py "TASK TEXT" \
        --workspace runs/portability/t1_lc --max-turns 300
"""
import argparse
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_MD = REPO_ROOT / ".claude" / "skills" / "virtual-battery-factory" / "SKILL.md"

from dotenv import load_dotenv

load_dotenv(REPO_ROOT / ".env")
_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not _API_KEY:
    print("bda error: DEEPSEEK_API_KEY not set in .env", file=sys.stderr)
    raise SystemExit(1)

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

WORKSPACE: Path = REPO_ROOT


# ---- tools (LangChain skill idiom + shell/files, same semantics as other legs) ----
@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt on demand.

    Available skills:
    - vbf_protocol: the Virtual Battery Factory operating protocol (five-stage
      funnel, evaluation/fallback, adjudication rules, bda CLI usage). This skill
      is MANDATORY for any battery design task; load it before doing anything else.

    Returns the skill's full prompt text."""
    if skill_name.strip().lower() == "vbf_protocol":
        return SKILL_MD.read_text(encoding="utf-8")
    return f"unknown skill '{skill_name}'; available: vbf_protocol"


@tool
def run_shell(command: str) -> str:
    """Run a shell command in the repository root and return stdout/stderr (truncated to 8000 chars).
    Use for ALL bda simulation/evaluation commands, e.g. `.venv/Scripts/python.exe -m bda run-pyamm ...`.
    Long simulations may take minutes; the command has a 30-minute timeout."""
    import subprocess

    try:
        r = subprocess.run(
            ["D:/software/Git/bin/bash.exe", "-c", command],
            shell=False,
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


@tool
def read_file(path: str) -> str:
    """Read a text file (relative to the workspace unless absolute) and return its content (truncated to 12000 chars)."""
    try:
        txt = _resolve(path).read_text(encoding="utf-8", errors="replace")
        return txt[-12000:] if len(txt) > 12000 else txt
    except Exception as e:
        return f"ERROR reading {path}: {e}"


@tool
def write_file(path: str, content: str) -> str:
    """Write a text file (relative to the workspace unless absolute). Returns the absolute path written."""
    try:
        p = _resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"written {p} ({len(content)} chars)"
    except Exception as e:
        return f"ERROR writing {path}: {e}"


@tool
def list_dir(path: str) -> str:
    """List a directory (relative to the workspace unless absolute)."""
    try:
        p = _resolve(path)
        return "\n".join(sorted(str(x.relative_to(p)) for x in p.iterdir()))
    except Exception as e:
        return f"ERROR listing {path}: {e}"


def build_system_prompt(workspace: Path) -> str:
    return (
        "You are a battery design agent.\n"
        "A skill named vbf_protocol contains your mandatory operating protocol "
        "(five-stage funnel, evaluation/fallback routing, mechanized adjudication, "
        "audit-chain rules, and the bda command reference). Load it FIRST with the "
        "load_skill tool and follow it exactly.\n"
        f"Your workspace (artifacts, log.jsonl, deliverables) is: {workspace}\n"
        "Shell commands execute in the repository root; use the read/write/list "
        "tools with workspace-relative paths. The bda tool library is invoked as "
        "`.venv/Scripts/python.exe -m bda <subcommand> ...`.\n"
        "Do everything yourself with the provided tools.\n"
    )


def main(argv=None) -> int:
    global WORKSPACE
    parser = argparse.ArgumentParser(prog="run_lc.py", description="LangChain harness (portability experiment)")
    parser.add_argument("task", help="Task text (natural-language contract)")
    parser.add_argument("--workspace", default=None, help="Workspace directory for artifacts/logs")
    parser.add_argument("--max-turns", type=int, default=300, help="Turn budget (LangChain recursion_limit)")
    parser.add_argument("--model", default="deepseek-v4-pro", help="Model name on the OpenAI-compatible endpoint")
    args = parser.parse_args(argv)

    ws = Path(args.workspace).resolve() if args.workspace else REPO_ROOT / "runs" / "portability" / "scratch_lc"
    ws.mkdir(parents=True, exist_ok=True)
    WORKSPACE = ws
    log_path = ws / "run.log"
    fh = open(log_path, "a", encoding="utf-8")
    fh.write(f"=== run_lc.py start {time.strftime('%Y-%m-%d %H:%M:%S')} | model={args.model} | max_turns={args.max_turns} | workspace={ws} ===\n")

    llm = ChatOpenAI(model=args.model, base_url="https://api.deepseek.com/v1", api_key=_API_KEY)
    agent = create_agent(
        model=llm,
        tools=[load_skill, run_shell, read_file, write_file, list_dir],
        system_prompt=build_system_prompt(ws),
    )
    prompt = (
        f"headless session: no user present, skip clarification questions (SKILL.md zero-interaction rule), "
        f"parse parameters from the task text, use defaults for unspecified ones, write to log.jsonl entry 0.\n"
        f"Task: {args.task}"
    )
    fh.write(f"[user] {prompt}\n")
    fh.flush()

    final_text = ""
    try:
        async def _run():
            nonlocal final_text
            async for ev in agent.astream_events(
                {"messages": [("user", prompt)]},
                config={"recursion_limit": args.max_turns},
                version="v2",
            ):
                kind = ev.get("event")
                if kind == "on_chat_model_stream":
                    chunk = ev["data"].get("chunk")
                    if chunk is not None and getattr(chunk, "content", None):
                        fh.write(f"[assistant] {chunk.content}\n")
                        final_text += str(chunk.content)
                elif kind == "on_tool_start":
                    fh.write(f"[tool_call] {ev['name']} {ev['data'].get('input', '')}\n")
                elif kind == "on_tool_end":
                    fh.write(f"[tool_result] {str(ev['data'].get('output', ''))[:500]}\n")
                fh.flush()

        import asyncio

        asyncio.run(_run())
    except Exception as exc:
        fh.write(f"[error] {exc}\n")
        fh.close()
        print(f"run_lc error: {exc}", file=sys.stderr)
        return 1
    fh.write(f"[final_output] {final_text[-2000:]}\n")
    (ws / "final_output.txt").write_text(final_text, encoding="utf-8")
    fh.write(f"=== done {time.strftime('%H:%M:%S')} ===\n")
    fh.close()
    print(f"run_lc finished: {ws} (final text {len(final_text)} chars)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
