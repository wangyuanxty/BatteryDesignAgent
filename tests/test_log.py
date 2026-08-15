import json

from bda.log import append_entry
from bda.store import CaseWorkspace


def test_append_entries(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    append_entry(ws, {"round": 0, "criteria": {"T_max_C": 60}})
    append_entry(ws, {"round": 1, "action": "propose"})
    lines = (ws.path / "log.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["round"] == 0
    assert first["criteria"]["T_max_C"] == 60
