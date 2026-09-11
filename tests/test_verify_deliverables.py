"""verify-deliverables 结构完整性测试。"""
from pathlib import Path

from bda.store import CaseWorkspace, append_entry
from bda.verify_deliverables import verify_deliverables


def _make_deliverable(d: Path, stem: str, suffix: str, content: str = "x") -> Path:
    p = d / f"{stem}{suffix}"
    p.write_text(content, encoding="utf-8")
    return p


def _make_deliverables(d: Path) -> None:
    for stem in ("design_spec", "bom", "datasheet", "calc", "dvpr", "dfmea", "delivery_index"):
        _make_deliverable(d, stem, ".md")
        _make_deliverable(d, stem, ".pdf", content="x" * 2000)
    (d / "delivery_index.md").write_text(
        "VBF-T1R1-DS-01\nVBF-T1R1-BOM-01\nVBF-T1R1-DSH-01\nVBF-T1R1-CALC-01\nVBF-T1R1-DVPR-01\nVBF-T1R1-DFMEA-01\n",
        encoding="utf-8",
    )


def _audit_check(report) -> dict:
    return next(c for c in report["checks"] if "audit chain" in c["check"])


def test_all_pass(tmp_path):
    d = tmp_path / "deliverables"
    d.mkdir()
    _make_deliverables(d)
    # 审计链完整：propose 轮均有同轮 evaluate（log-evaluate 协议前提）
    ws = CaseWorkspace(tmp_path.name, str(tmp_path.parent), create=False)
    append_entry(ws, {"criteria": {"stage2": {}, "stage3": {}}})
    for r in (1, 2):
        append_entry(ws, {"action": "propose", "round": r, "candidates": []})
        append_entry(ws, {"action": "evaluate", "round": r, "metrics": {}, "verdict": "pass"})
    append_entry(ws, {"action": "final", "recommendation": "R", "verdict": "pass"})
    report = verify_deliverables(tmp_path)
    assert report["all_pass"] is True


def test_missing_file_fails(tmp_path):
    d = tmp_path / "deliverables"
    d.mkdir()
    _make_deliverable(d, "bom", ".md")
    _make_deliverable(d, "bom", ".pdf", content="x" * 2000)
    report = verify_deliverables(tmp_path)
    assert report["all_pass"] is False
    assert any("design_spec" in c["detail"] or "design_spec" in c["check"] for c in report["checks"])


def test_empty_pdf_fails(tmp_path):
    d = tmp_path / "deliverables"
    d.mkdir()
    for stem in ("design_spec", "bom", "datasheet", "calc", "dvpr", "dfmea", "delivery_index"):
        _make_deliverable(d, stem, ".md")
        _make_deliverable(d, stem, ".pdf", content="x" * 500)  # <1KB
    report = verify_deliverables(tmp_path)
    assert report["all_pass"] is False
    assert any("PDFs non-empty" in c["check"] and not c["pass"] for c in report["checks"])


def test_index_without_ids_fails(tmp_path):
    d = tmp_path / "deliverables"
    d.mkdir()
    _make_deliverables(d)
    (d / "delivery_index.md").write_text("no ids here", encoding="utf-8")
    report = verify_deliverables(tmp_path)
    assert report["all_pass"] is False
    assert any("VBF" in c["check"] and not c["pass"] for c in report["checks"])


def test_propose_without_evaluate_fails(tmp_path):
    """v3 事故形态：round 1 只有 propose、评估只存在于散文 → 审计检查 FAIL。"""
    d = tmp_path / "deliverables"
    d.mkdir()
    _make_deliverables(d)
    ws = CaseWorkspace(tmp_path.name, str(tmp_path.parent), create=False)
    append_entry(ws, {"criteria": {"stage2": {}, "stage3": {}}})
    append_entry(ws, {"action": "propose", "round": 1, "candidates": []})
    append_entry(ws, {"action": "propose", "round": 2, "candidates": []})
    append_entry(ws, {"action": "evaluate", "round": 2, "metrics": {}, "verdict": "pass"})
    report = verify_deliverables(tmp_path)
    audit = _audit_check(report)
    assert audit["pass"] is False
    assert "R01" in audit["detail"]            # 指明缺失轮次


def test_missing_log_fails(tmp_path):
    """无 log.jsonl = 无审计记录 → 审计检查 FAIL（协议运行必须有日志）。"""
    d = tmp_path / "deliverables"
    d.mkdir()
    _make_deliverables(d)
    report = verify_deliverables(tmp_path)
    audit = _audit_check(report)
    assert audit["pass"] is False
    assert "log.jsonl" in audit["detail"]
