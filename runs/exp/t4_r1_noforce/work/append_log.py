"""Append a log entry from a JSON file via bda.store.append_entry (all log writes except evaluate)."""
import json
import sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t4_r1_noforce", "runs/exp")
entry = json.loads(open(sys.argv[1], encoding="utf-8-sig").read())
append_entry(ws, entry)
print("appended:", json.dumps(entry, ensure_ascii=False)[:200])
