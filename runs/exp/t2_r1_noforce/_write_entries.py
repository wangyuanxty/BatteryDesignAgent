"""Write log.jsonl entry 0 (criteria) and the Stage-1 plan entry via bda.store.append_entry.

All log writes go through bda.store.append_entry (protocol rule); this script is only
a thin caller so the PowerShell quoting layer cannot mangle the JSON payloads.
"""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

WS = Path("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t2_r1_noforce")
ws = CaseWorkspace("exp/t2_r1_noforce", "runs")
log = ws.path / "log.jsonl"
n_before = 0
if log.exists():
    n_before = sum(1 for _ in log.open(encoding="utf-8"))

entry0 = json.loads((WS / "entry0_input.json").read_text(encoding="utf-8"))
plan = json.loads((WS / "plan_entry.json").read_text(encoding="utf-8"))
append_entry(ws, entry0)
append_entry(ws, plan)
n_after = sum(1 for _ in log.open(encoding="utf-8"))
print("log.jsonl entries:", n_before, "->", n_after)
