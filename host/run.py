"""Agent SDK 薄启动器：加载虚拟电池工厂协议（SKILL.md）并运行案例。

用法：
    python host/run.py --config <case_dir>/config.yaml   # 运行/续跑案例
    python host/run.py --smoke-test                      # 连通性冒烟

环境引导（_bootstrap_env，密钥永不打印/落盘）：
    - ANTHROPIC_BASE_URL 缺省指向 DeepSeek Anthropic 兼容端点
      https://api.deepseek.com/anthropic（可用环境变量覆盖指向其他代理）
    - 凭证取 ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY，否则读 .env 的
      DEEPSEEK_API_KEY 作为 ANTHROPIC_AUTH_TOKEN
    - ANTHROPIC_MODEL 缺省 deepseek-v4-pro

会话恢复：session id 存于工作区（--config 所在目录）的 session_id 文件，
重跑同命令自动 resume。
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from bda.config import CaseConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / "skills" / "virtual-battery-factory" / "SKILL.md"
SESSION_FILE = "session_id"

DEFAULT_BASE_URL = "https://api.deepseek.com/anthropic"
DEFAULT_MODEL = "deepseek-v4-pro"
ALLOWED_TOOLS = ["Bash", "Read", "Write", "Edit", "Grep", "Glob"]

SYSTEM_EXTRA = """
你是虚拟电池工厂协议的执行者。当前案例配置与工作区：
{case_context}
每次运行结束时把本轮决策追加写入工作区 log.jsonl（第 0 条为达标标准）。
"""


def _bootstrap_env() -> None:
    """确保 ANTHROPIC_* 环境变量就绪；密钥只在进程环境内传递。"""
    os.environ.setdefault("ANTHROPIC_BASE_URL", DEFAULT_BASE_URL)
    os.environ.setdefault("ANTHROPIC_MODEL", DEFAULT_MODEL)
    if os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY"):
        return
    for env_file in (REPO_ROOT / ".env", Path.cwd() / ".env"):
        if env_file.exists():
            load_dotenv(env_file)
            break
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        os.environ["ANTHROPIC_AUTH_TOKEN"] = key
        return
    raise RuntimeError(
        "未找到 API 凭证：请在 .env 设置 DEEPSEEK_API_KEY，"
        "或设置 ANTHROPIC_AUTH_TOKEN / ANTHROPIC_API_KEY 环境变量"
    )


def _resolve_session(case_dir: Path) -> str | None:
    p = case_dir / SESSION_FILE
    return p.read_text(encoding="utf-8").strip() if p.exists() else None


def _build_system(case_dir: Path, cfg: "CaseConfig") -> str:
    case_context = (
        f"目标: {cfg.goal}\n"
        f"体系: {cfg.system}\n"
        f"预算: {cfg.max_rounds} 轮\n"
        f"参数集: {cfg.base_params}\n"
        f"配置: {case_dir / 'config.yaml'}\n"
        f"工作区: {case_dir}"
    )
    return SKILL_PATH.read_text(encoding="utf-8") + SYSTEM_EXTRA.format(case_context=case_context)


async def _run(case_dir: Path, resume_session: str | None) -> int:
    from claude_agent_sdk import ClaudeAgentOptions, query
    from bda.config import load_case_config
    from bda.store import CaseWorkspace

    CaseWorkspace(case_dir.name, str(case_dir.parent))
    cfg = load_case_config(str(case_dir / "config.yaml"))
    system = _build_system(case_dir, cfg)
    options = ClaudeAgentOptions(
        system_prompt=system,
        permission_mode="acceptEdits",
        allowed_tools=ALLOWED_TOOLS,
        resume=resume_session,
        cwd=str(REPO_ROOT),
    )
    final = None
    async for msg in query(prompt=f"开始执行设计任务：{cfg.goal}", options=options):
        final = msg
    if final is None or final.is_error:
        print(f"error: {getattr(final, 'errors', 'no result message')}", file=sys.stderr)
        print(getattr(final, "result", "") or "", file=sys.stderr)
        return 1
    (case_dir / SESSION_FILE).write_text(final.session_id, encoding="utf-8")
    print(f"session_id: {final.session_id}")
    print(final.result or "")
    return 0


async def _smoke() -> str:
    from claude_agent_sdk import ClaudeAgentOptions, query

    system = SKILL_PATH.read_text(encoding="utf-8")
    options = ClaudeAgentOptions(
        system_prompt=system,
        permission_mode="acceptEdits",
        cwd=str(REPO_ROOT),
    )
    final = None
    async for msg in query(prompt="回复 smoke ok", options=options):
        final = msg
    if final.is_error:
        raise RuntimeError(f"smoke query failed: {final.errors}")
    return final.result or ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="host/run.py",
        description="虚拟电池工厂 Agent SDK 薄启动器",
    )
    parser.add_argument("--config", help="案例配置 YAML 路径（工作区为其所在目录）")
    parser.add_argument("--smoke-test", action="store_true", help="连通性冒烟测试")
    args = parser.parse_args(argv)
    _bootstrap_env()
    if args.smoke_test:
        print(asyncio.run(_smoke()))
        return 0
    if not args.config:
        parser.error("--config is required (or use --smoke-test)")
    case_dir = Path(args.config).resolve().parent
    if not (case_dir / "config.yaml").exists():
        print(f"config not found: {case_dir / 'config.yaml'}", file=sys.stderr)
        return 1
    return asyncio.run(_run(case_dir, _resolve_session(case_dir)))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())
