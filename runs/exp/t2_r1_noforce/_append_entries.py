"""Append a batch of entry JSON files (in order) to this case's log.jsonl via bda.store.append_entry."""
import json
import sys
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

WS = Path("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t2_r1_noforce")
ws = CaseWorkspace("exp/t2_r1_noforce", "runs")
for name in sys.argv[1:]:
    entry = json.loads((WS / name).read_text(encoding="utf-8"))
    append_entry(ws, entry)
    print("appended:", name, "->", entry.get("action"), entry.get("round", ""))
print("total entries:", sum(1 for _ in (ws.path / "log.jsonl").open(encoding="utf-8")))
