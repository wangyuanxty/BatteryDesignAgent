import os

import pytest

from bda.store import append_entry
from bda.store import CaseWorkspace
from bda.report import render_report, export_csv

def _make_case(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    append_entry(ws, {"round": 0, "criteria": {"T_max_C": 60, "plating_free": True}})
    append_entry(ws, {"round": 1, "action": "propose", "candidates": ["FEC"], "llm_reason": "seed"})
    append_entry(ws, {"round": 1, "action": "evaluate", "metrics": {"T_max_K": 325.0, "plated": False}, "verdict": "pass"})
    return ws

@pytest.fixture
def full_case(tmp_path):
    """含 funnel/evaluate/endorse/final 四类条目的完整日志案例。"""
    ws = _make_case(tmp_path)
    append_entry(ws, {"action": "funnel", "passed": 3, "rejected": 2, "disputed": 1})
    append_entry(ws, {"action": "funnel", "passed": 1, "rejected": 0, "disputed": 1})
    append_entry(ws, {
        "round": 2, "action": "evaluate",
        "metrics": {"T_max_K": 318.0, "plated": False, "energy_density_Wh_kg": 500},
        "verdict": "pass",
    })
    append_entry(ws, {
        "action": "endorse",
        "candidates": [{"smiles": "CCOC(=O)O",
                        "endorsement": {"level": "ORCA-PBE0", "E_hartree": -343.12, "note": "stable"}}],
    })
    append_entry(ws, {"action": "final", "recommendation": "FEC 2wt%", "verdict": "达标"})
    return ws

def test_render_produces_self_contained_html(tmp_path):
    ws = _make_case(tmp_path)
    html_path = render_report(str(ws.path))
    html = open(html_path, encoding="utf-8").read()
    assert "<html" in html
    assert "60" in html
    assert "FEC" in html

def test_render_all_six_sections(tmp_path, full_case):
    ws = full_case
    html_path = render_report(str(ws.path))
    html = open(html_path, encoding="utf-8").read()
    for heading in ("漏斗统计", "阶段 2/3 结果", "收尾背书", "最终推荐"):
        assert heading in html
    assert "ORCA-PBE0" in html  # 收尾背书中的 endorsement 值
    assert "energy_density_Wh_kg" in html  # 阶段 2/3 表格渲染全部 metrics 键
    assert "<td>4</td>" in html  # 漏斗计数跨条目求和（3+1）

def test_render_missing_sections_show_placeholders(tmp_path):
    ws = _make_case(tmp_path)
    html_path = render_report(str(ws.path))
    html = open(html_path, encoding="utf-8").read()
    assert "暂无数据" in html
    assert "暂无推荐（预算耗尽或未达标）" in html

def test_export_csv(tmp_path):
    ws = _make_case(tmp_path)
    out_dir = str(ws.path / "csv")
    export_csv(str(ws.path), out_dir)
    files = os.listdir(out_dir)
    assert any(f.endswith(".csv") for f in files)
