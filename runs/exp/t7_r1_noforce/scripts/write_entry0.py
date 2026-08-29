"""Write entry 0 (criteria+meta) to log.jsonl via bda.store.append_entry (protocol-mandated writer)."""
import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS_DIR = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")
ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")
entry = json.loads((WS_DIR / "criteria_entry0.json").read_text(encoding="utf-8"))
append_entry(ws, entry)
lines = (ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()
print("log.jsonl entries:", len(lines))
print("entry0 stage2:", json.loads(lines[0])["criteria"]["stage2"])
print("entry0 stage3:", json.loads(lines[0])["criteria"]["stage3"])
