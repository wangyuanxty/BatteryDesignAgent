"""Task 20: Agent SDK thin launcher (host/run.py)."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
RUN_PATH = ROOT / "host" / "run.py"
SKILL_PATH = ROOT / "skills" / "virtual-battery-factory" / "SKILL.md"


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
        timeout=300,
    )
    assert r.returncode == 0, r.stderr
    assert "smoke" in r.stdout.lower()


def test_resolve_session_none_when_missing(run_mod, tmp_path):
    assert run_mod._resolve_session(tmp_path) is None


def test_resolve_session_reads_id(run_mod, tmp_path):
    (tmp_path / "session_id").write_text("abc-123", encoding="utf-8")
    assert run_mod._resolve_session(tmp_path) == "abc-123"


def test_build_system_injects_skill_and_case_context(run_mod, tmp_path):
    from bda.config import CaseConfig

    cfg = CaseConfig(goal="设计快充添加剂", system="EC/EMC+LiPF6", max_rounds=5)
    system = run_mod._build_system(tmp_path, cfg)
    # Full SKILL.md text is the protocol source of truth.
    assert "虚拟电池工厂协议" in system
    assert "goal" in system  # SKILL.md references the config schema
    # Case context injection.
    assert cfg.goal in system
    assert cfg.system in system
    assert "5 轮" in system
    assert str(tmp_path) in system
    # Decision-log instruction appended.
    assert "log.jsonl" in system


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


def test_skill_file_exists_for_host():
    assert SKILL_PATH.exists()
