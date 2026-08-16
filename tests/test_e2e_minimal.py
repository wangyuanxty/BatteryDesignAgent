"""Task 21: 最小案例端到端（协议验证）。

测试策略说明（本任务的选择）：
完整 e2e 需真实 Agent SDK + LLM 调用，实测约 30~60 分钟（3 轮预算、
真计算关闭、种子池 2 个已知分子），不适合常规测试运行。因此：

- 默认测试 `test_minimal_case_workspace_artifacts` 验证**已完成运行的产物**
  （`runs/minimal_smoke_e2e/`，与 e2e 完成标准一致：log.jsonl 第 0 条
  criteria、`final` 条目 verdict=达标、report.html 存在）。工作区不在
  （如全新克隆，runs/ 被 .gitignore 排除）时跳过并提示如何生成。
- 完整流程保留为 slow 测试 `test_minimal_case_end_to_end`（brief Step 1 的
  原始形式：复制 config 到 tmp 后真实运行），设置环境变量 `BDA_E2E_FULL=1`
  时执行。
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = ROOT / "runs" / "minimal_smoke_e2e"


def test_minimal_case_workspace_artifacts():
    """已完成 e2e 的产物验证（默认测试，即本任务完成的验收标准）。"""
    report = WORKSPACE / "report.html"
    log = WORKSPACE / "log.jsonl"
    if not report.exists() or not log.exists():
        pytest.skip(
            "e2e workspace missing: run "
            f"`python host/run.py --config {WORKSPACE / 'config.yaml'}` "
            "(~30-60 min, real Agent SDK) or set BDA_E2E_FULL=1"
        )
    lines = log.read_text(encoding="utf-8").splitlines()
    assert lines
    # 第 0 条 = 达标标准审计
    criteria = json.loads(lines[0]).get("criteria")
    assert criteria
    assert criteria["capacity_ah"]["min"] == 2.0
    assert criteria["max_rounds"] == 3
    # final 条目存在且如实记录（铁律：不得虚构达标）
    actions = [json.loads(line).get("action") for line in lines]
    assert "final" in actions
    final = json.loads(lines[actions.index("final")])
    assert final.get("verdict") == "达标"
    assert final.get("recommendation")
    # report.html 已生成
    assert report.is_file() and report.stat().st_size > 0


@pytest.mark.slow
def test_minimal_case_end_to_end(tmp_path):
    """完整 e2e（brief 原始形式）：复制 config 到 tmp 后真实运行。

    需真实 API 凭证（.env DEEPSEEK_API_KEY）与约 30~60 分钟。
    设置 BDA_E2E_FULL=1 执行。
    """
    if os.environ.get("BDA_E2E_FULL") != "1":
        pytest.skip("set BDA_E2E_FULL=1 to run the full e2e (~30-60 min)")
    case_dir = tmp_path / "minimal_smoke"
    case_dir.mkdir()
    shutil.copy(ROOT / ".claude" / "skills" / "virtual-battery-factory" / "assets" / "cases" / "minimal_smoke.yaml", case_dir / "config.yaml")
    r = subprocess.run(
        [sys.executable, str(ROOT / "host" / "run.py"), "--config", str(case_dir / "config.yaml")],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=2700,
    )
    assert r.returncode == 0, r.stderr[-1000:]
    log_lines = (case_dir / "log.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(log_lines) >= 2
    assert json.loads(log_lines[0])["criteria"]  # 第 0 条 = 达标标准审计
    assert (case_dir / "report.html").exists()
