import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
ws = CaseWorkspace("exp/t5_r1_singlemodel", "runs")
e = json.loads((WS / "_entry0.json").read_text(encoding="utf-8"))
append_entry(ws, e)
print("entry 0 written ->", ws.path / "log.jsonl")
