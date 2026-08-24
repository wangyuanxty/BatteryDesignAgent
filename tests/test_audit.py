"""log-evaluate 确定性判定测试：verdict 机械计算、plated 推导、evidence 溯源、CLI 端到端。

背景：t1_r1_v3 事故——agent 对话内评估 V1-V3 但不落日志，报告轮卡片
propose-only 却引用"第 1 轮结论"。本测试保证：评估条目由代码写入，
verdict/evidence 全部机械生成，agent 只传候选与输出文件。
"""
import json
import subprocess
import sys

from bda.audit import _threshold_ok, extract_metrics
from bda.cli import main
from bda.store import CaseWorkspace, append_entry

CRITERIA = {
    "stage1": {},
    "stage2": {"energy_density_wh_kg": {"min": 446.18}},
    "stage3": {"T_max_K": {"max": 333.15}, "plated": False},
    "meta": {},
}


def _make_case(tmp_path, criteria=None):
    case = tmp_path / "case"
    ws = CaseWorkspace(case.name, str(tmp_path), create=True)
    append_entry(ws, {"criteria": criteria or CRITERIA})
    return case, ws


def _write_output(case, rel: str, data: dict):
    p = case / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data), encoding="utf-8")
    return rel


def _run(case, round_no, outputs, candidate="", note=""):
    argv = ["log-evaluate", "--case-dir", str(case), "--round", str(round_no),
            "--outputs", *outputs]
    if candidate:
        argv += ["--candidate", candidate]
    if note:
        argv += ["--note", note]
    return main(argv)


def _last_entry(ws) -> dict:
    lines = [l for l in (ws.path / "log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return json.loads(lines[-1])


# ---------------------------------------------------------------------------
# 阈值判定
# ---------------------------------------------------------------------------

def test_threshold_min_max_bool_scalar():
    assert _threshold_ok(450.0, {"min": 446.18}) is True
    assert _threshold_ok(440.0, {"min": 446.18}) is False
    assert _threshold_ok(332.0, {"max": 333.15}) is True
    assert _threshold_ok(334.0, {"max": 333.15}) is False
    assert _threshold_ok(False, False) is True
    assert _threshold_ok(True, False) is False
    assert _threshold_ok(3.0, 2.0) is True      # 标量视为 min
    assert _threshold_ok(1.0, 2.0) is False
    assert _threshold_ok("abc", {"min": 1}) is False  # 不可判形态 → 不过


# ---------------------------------------------------------------------------
# plated 推导（输出文件无 plated 键，由 anode_potential_v 时序 min<0 判定）
# ---------------------------------------------------------------------------

def test_extract_metrics_derives_plated_from_potential(tmp_path):
    f = tmp_path / "4c.json"
    f.write_text(json.dumps({"T_max_K": 330.0, "anode_potential_v": [0.13, 0.02, 0.09]}), encoding="utf-8")
    m = extract_metrics([f])
    assert m["plated"] == (False, f)        # min=0.02 > 0 → 无析锂
    assert m["_plated_note"][0].startswith("anode_potential_v (min=0.02V>0")


def test_extract_metrics_plated_flagged_when_potential_dips_below_zero(tmp_path):
    f = tmp_path / "4c.json"
    f.write_text(json.dumps({"anode_potential_v": [0.1, -0.005, 0.2]}), encoding="utf-8")
    m = extract_metrics([f])
    assert m["plated"] == (True, f)         # min=-0.005 < 0 → 析锂风险


def test_extract_metrics_keeps_scalars_only(tmp_path):
    f = tmp_path / "out.json"
    f.write_text(json.dumps({"energy_density_wh_kg": 461.2, "voltage_v": [4.2, 3.5]}), encoding="utf-8")
    m = extract_metrics([f])
    assert m["energy_density_wh_kg"][0] == 461.2
    assert "voltage_v" not in m


# ---------------------------------------------------------------------------
# CLI 端到端
# ---------------------------------------------------------------------------

def test_log_evaluate_pass_with_evidence(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 468.1, "capacity_ah": 4.7})
    _write_output(case, "cell/v1_4c.json",
                  {"T_max_K": 332.25, "anode_potential_v": [0.13, 0.015, 0.09]})
    rc = _run(case, 1, ["cell/v1_energy.json", "cell/v1_4c.json"], candidate="V1")
    assert rc == 0
    e = _last_entry(ws)
    assert e["action"] == "evaluate" and e["round"] == 1 and e["candidate"] == "V1"
    assert e["verdict"] == "pass"
    assert e["metrics"]["plated"] is False        # 推导值进入条目
    assert len(e["evidence"]) == 3                # ED / T_max / plated 各一条
    src = {ev["metric"]: ev for ev in e["evidence"]}
    assert src["energy_density_wh_kg"]["source"].endswith("cell/v1_energy.json:energy_density_wh_kg")
    assert "anode_potential_v (min=0.015V>0 推导)" in src["plated"]["source"]


def test_log_evaluate_fail_when_ed_below_min(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 440.0})
    _write_output(case, "cell/v1_4c.json", {"T_max_K": 320.0, "anode_potential_v": [0.1]})
    rc = _run(case, 1, ["cell/v1_energy.json", "cell/v1_4c.json"])
    assert rc == 0
    e = _last_entry(ws)
    assert e["verdict"] == "fail"
    assert [ev["metric"] for ev in e["evidence"] if ev["verdict"] == "fail"] == ["energy_density_wh_kg"]


def test_log_evaluate_fail_when_plating_detected(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 468.0})
    _write_output(case, "cell/v1_4c.json", {"T_max_K": 320.0, "anode_potential_v": [0.1, -0.01]})
    rc = _run(case, 1, ["cell/v1_energy.json", "cell/v1_4c.json"])
    assert rc == 0
    e = _last_entry(ws)
    assert e["verdict"] == "fail"
    assert e["metrics"]["plated"] is True


def test_log_evaluate_unchecked_criteria_recorded(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 468.1})
    rc = _run(case, 1, ["cell/v1_energy.json"], note="诊断一句话")
    assert rc == 0
    e = _last_entry(ws)
    assert e["verdict"] == "pass"                 # 已检查指标全过
    assert e["unchecked"] == ["T_max_K", "plated"]
    assert "未检查 criteria: T_max_K, plated" in e["note"]


def test_log_evaluate_round_zero_baseline_allowed(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/base_energy.json", {"energy_density_wh_kg": 405.62})
    _write_output(case, "cell/base_4c.json", {"T_max_K": 367.42, "anode_potential_v": [0.016]})
    rc = _run(case, 0, ["cell/base_energy.json", "cell/base_4c.json"])
    assert rc == 0
    assert _last_entry(ws)["round"] == 0          # 基线评估（无 propose）合法


def test_log_evaluate_missing_criteria_entry_fails(tmp_path):
    case = tmp_path / "case"                      # 无第 0 条 criteria
    ws = CaseWorkspace(case.name, str(tmp_path), create=True)
    append_entry(ws, {"action": "propose", "round": 1, "candidates": []})
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 468.1})
    rc = _run(case, 1, ["cell/v1_energy.json"])
    assert rc == 1                                # criteria 未预注册 = 不可判定


def test_log_evaluate_nonexistent_output_fails(tmp_path):
    case, ws = _make_case(tmp_path)
    rc = _run(case, 1, ["cell/nope.json"])
    assert rc == 1


def test_log_evaluate_no_criteria_metrics_fails(tmp_path):
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1.json", {"capacity_ah": 4.7})   # 无任何 criteria 指标
    rc = _run(case, 1, ["cell/v1.json"])
    assert rc == 1


def test_cli_module_entrypoint_runs(tmp_path):
    """进程级入口：`python -m bda.cli` 必须真正执行命令并写条目。
    回归防护——cli.py 曾缺 `if __name__ == "__main__"`，-m 静默空转 exit 0，
    而单元测试直接调 main() 全部通过，进程入口缺陷逃过测试。"""
    case, ws = _make_case(tmp_path)
    _write_output(case, "cell/v1_energy.json", {"energy_density_wh_kg": 468.1})
    _write_output(case, "cell/v1_4c.json",
                  {"T_max_K": 332.25, "anode_potential_v": [0.13, 0.015, 0.09]})
    proc = subprocess.run(
        [sys.executable, "-m", "bda.cli", "log-evaluate",
         "--case-dir", str(case), "--round", "1",
         "--outputs", "cell/v1_energy.json", "cell/v1_4c.json"],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    assert "已记录" in proc.stdout                # 进程真实执行了命令
    e = _last_entry(ws)
    assert e["action"] == "evaluate" and e["verdict"] == "pass"
