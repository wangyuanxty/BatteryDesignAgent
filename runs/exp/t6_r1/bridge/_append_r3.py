import json, sys
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("exp/t6_r1", "runs")
with open(ws.path / "bridge" / "propose_r3.json", encoding="utf-8") as fh:
    append_entry(ws, json.load(fh))
print("appended propose_r3")
