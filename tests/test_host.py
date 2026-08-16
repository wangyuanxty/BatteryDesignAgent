"""Task 20: Agent SDK thin launcher (run.py)."""

import asyncio
import importlib.util
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RUN_PATH = ROOT / "run.py"
SKILL_PATH = ROOT / ".claude" / "skills" / "virtual-battery-factory" / "SKILL.md"


def _has_api_route() -> bool:
    """True if a working API route exists (env vars or .env), without printing values."""
    if any(
        os.environ.get(k)
        for k in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY")
    ):
        return True
    dotenv_path = ROOT / ".env"
    if dotenv_path.exists():
        return "DEEPSEEK_API_KEY" in dotenv_path.read_text(encoding="utf-8")
    return False


@pytest.fixture(scope="module")
def run_mod():
    spec = importlib.util.spec_from_file_location("run", RUN_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_host_runs_minimal_query():
    """Smoke: the launcher boots the SDK and gets a text reply back."""
    if not _has_api_route():
        pytest.skip("no API route configured (no DEEPSEEK_API_KEY in .env)")
    r = subprocess.run(
        [sys.executable, str(RUN_PATH), "--smoke-test"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    assert r.returncode == 0, r.stderr
    assert "smoke" in (r.stdout or "").lower()


def test_resolve_session_none_when_missing(run_mod, tmp_path):
    assert run_mod._resolve_session(tmp_path) is None


def test_resolve_session_reads_id(run_mod, tmp_path):
    (tmp_path / "session_id").write_text("abc-123", encoding="utf-8")
    assert run_mod._resolve_session(tmp_path) == "abc-123"


def test_ensure_session_id_creates_and_persists(run_mod, tmp_path):
    sid = run_mod._ensure_session_id(tmp_path)
    assert sid
    assert (tmp_path / "session_id").read_text(encoding="utf-8") == sid
    # 幂等：已存在时返回同一 id，不重复生成
    assert run_mod._ensure_session_id(tmp_path) == sid


def test_build_system_injects_skill_and_case_context(run_mod, tmp_path):
    from bda.config import CaseConfig

    config_path = tmp_path / "fast_charge_v1.yaml"
    cfg = CaseConfig(goal="设计快充添加剂", system="EC/EMC+LiPF6", max_rounds=5)
    system = run_mod._build_system(config_path, cfg)
    # Full SKILL.md text is the protocol source of truth.
    assert "虚拟电池工厂协议" in system
    assert "goal" in system  # SKILL.md references the config schema
    # Case context injection.
    assert cfg.goal in system
    assert cfg.system in system
    assert "5 轮" in system
    assert str(config_path) in system  # actual config path, not a hardcoded name
    assert str(tmp_path) in system  # workspace = config's parent dir
    # Decision-log instruction appended.
    assert "log.jsonl" in system


class _DummyOptions:
    def __init__(self, **kwargs):
        pass


def _fake_sdk(query_gen):
    return types.SimpleNamespace(query=query_gen, ClaudeAgentOptions=_DummyOptions)


def test_smoke_raises_on_empty_stream(run_mod, monkeypatch):
    """Empty SDK stream (disconnect/zero messages) must raise, not AttributeError."""

    async def empty_query(**kwargs):
        if False:  # pragma: no cover - never yields
            yield None

    monkeypatch.setitem(sys.modules, "claude_agent_sdk", _fake_sdk(empty_query))
    with pytest.raises(RuntimeError, match="no result message"):
        asyncio.run(run_mod._smoke())


def test_run_honors_config_path(run_mod, monkeypatch, tmp_path):
    """--config loads the passed file (any name), not a hardcoded config.yaml."""
    config_path = tmp_path / "custom_case.yaml"
    config_path.write_text(
        "goal: 设计快充添加剂\nsystem: EC/EMC+LiPF6\nmax_rounds: 5\n",
        encoding="utf-8",
    )

    class _FakeResult:
        is_error = False
        session_id = "fake-session"
        result = "done"

    async def fake_query(**kwargs):
        yield _FakeResult()

    monkeypatch.setitem(sys.modules, "claude_agent_sdk", _fake_sdk(fake_query))
    rc = asyncio.run(run_mod._run(config_path, None))
    assert rc == 0
    assert (tmp_path / "session_id").read_text(encoding="utf-8") == "fake-session"
    assert (tmp_path / "candidates").is_dir()  # CaseWorkspace created in config dir


def _recording_sdk(options_capture, result):
    class _RecordingOptions:
        def __init__(self, **kwargs):
            options_capture.update(kwargs)

    async def fake_query(**kwargs):
        yield result

    return types.SimpleNamespace(
        query=fake_query, ClaudeAgentOptions=_RecordingOptions
    )


def _write_case(config_path, goal="g", system="s", max_rounds=1):
    config_path.write_text(
        f"goal: {goal}\nsystem: {system}\nmax_rounds: {max_rounds}\n",
        encoding="utf-8",
    )


def test_run_fresh_session_pins_session_id(run_mod, monkeypatch, tmp_path):
    """首跑：预生成 session id 并以 session_id= 传给 SDK（中断后可续跑）。"""
    config_path = tmp_path / "config.yaml"
    _write_case(config_path)
    captured = {}

    class _EchoResult:
        is_error = False
        result = "done"

        @property
        def session_id(self):
            # 真实 SDK 在首跑返回与 --session-id 相同的 id
            return captured["session_id"]

    monkeypatch.setitem(sys.modules, "claude_agent_sdk", _recording_sdk(captured, _EchoResult()))
    rc = asyncio.run(run_mod._run(config_path, None))
    assert rc == 0
    sid = captured.get("session_id")
    assert sid
    assert (tmp_path / "session_id").read_text(encoding="utf-8") == sid
    assert "resume" not in captured


def test_run_resume_rotates_session_id_and_prompts_recovery(run_mod, monkeypatch, tmp_path):
    """续跑：轮换 session id（新会话，工具白名单完整）并注入断点恢复提示词。

    回归依据（e2e 实测，CLI 2.1.233）：
    - --resume / --fork-session 均丢弃 --allowedTools（Bash 丢失，仅剩受限
      PowerShell，render 等命令无法执行）；
    - --session-id 对已存在的 id 报 "already in use"。
    因此续跑唯一可靠路径 = 新会话（session_id=<新 uuid>）+ 恢复提示词，
    断点状态以工作区产物为准（SKILL.md 准备节：log.jsonl/产物文件）。
    """
    config_path = tmp_path / "config.yaml"
    _write_case(config_path)
    (tmp_path / "session_id").write_text("old-session-id", encoding="utf-8")
    captured = {}
    prompts = []

    class _EchoResult:
        is_error = False
        result = "done"

        @property
        def session_id(self):
            return captured["session_id"]

    class _RecordingOptions:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    async def fake_query(**kwargs):
        prompts.append(kwargs.get("prompt", ""))
        yield _EchoResult()

    monkeypatch.setitem(
        sys.modules,
        "claude_agent_sdk",
        types.SimpleNamespace(query=fake_query, ClaudeAgentOptions=_RecordingOptions),
    )
    rc = asyncio.run(run_mod._run(config_path, "old-session-id"))
    assert rc == 0
    new_sid = captured.get("session_id")
    assert new_sid and new_sid != "old-session-id"
    assert (tmp_path / "session_id").read_text(encoding="utf-8") == new_sid
    assert "resume" not in captured
    assert prompts and "断点恢复" in prompts[0]


def test_bootstrap_env_uses_deepseek_defaults(run_mod, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "dummy-key")
    run_mod._bootstrap_env()
    assert os.environ["ANTHROPIC_AUTH_TOKEN"] == "dummy-key"
    assert os.environ["ANTHROPIC_BASE_URL"] == "https://api.deepseek.com/anthropic"
    assert os.environ["ANTHROPIC_MODEL"] == "deepseek-v4-pro"


def test_bootstrap_env_fails_fast_without_credentials(run_mod, monkeypatch, tmp_path):
    monkeypatch.setattr(run_mod, "load_dotenv", lambda *a, **k: None)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="DEEPSEEK_API_KEY"):
        run_mod._bootstrap_env()


def test_bootstrap_git_bash_sets_from_git_path(run_mod, monkeypatch, tmp_path):
    """Windows：从 git 路径反推 bash.exe 并写入 CLAUDE_CODE_GIT_BASH_PATH。

    回归依据（e2e 实测）：CLI 找不到 Git Bash 时 BashTool 不可用，SDK 会话
    只剩受限 PowerShell 工具，render 等命令被 guardrail 拦截无法执行。
    """
    if sys.platform != "win32":
        pytest.skip("windows-only CLI behavior")
    fake_bash = tmp_path / "bash.exe"
    fake_bash.write_text("", encoding="utf-8")
    monkeypatch.delenv("CLAUDE_CODE_GIT_BASH_PATH", raising=False)
    monkeypatch.setattr(run_mod.shutil, "which", lambda name: str(tmp_path / "git.exe"))
    run_mod._bootstrap_git_bash()
    assert os.environ["CLAUDE_CODE_GIT_BASH_PATH"] == str(fake_bash)


def test_bootstrap_git_bash_respects_existing(run_mod, monkeypatch):
    monkeypatch.setenv("CLAUDE_CODE_GIT_BASH_PATH", "C:/custom/bash.exe")
    run_mod._bootstrap_git_bash()
    assert os.environ["CLAUDE_CODE_GIT_BASH_PATH"] == "C:/custom/bash.exe"


def test_bootstrap_env_sets_git_bash_path(run_mod, monkeypatch):
    """_bootstrap_env 在凭证引导之外同时保证 Bash 工具可用。"""
    if sys.platform != "win32":
        pytest.skip("windows-only CLI behavior")
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("DEEPSEEK_API_KEY", "dummy-key")
    monkeypatch.delenv("CLAUDE_CODE_GIT_BASH_PATH", raising=False)
    called = []
    monkeypatch.setattr(run_mod, "_bootstrap_git_bash", lambda: called.append(True))
    run_mod._bootstrap_env()
    assert called


def test_skill_file_exists_for_host():
    assert SKILL_PATH.exists()
