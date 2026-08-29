import json
import sys

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r1_flash", root="runs/exp")
for p in sys.argv[1:]:
    with open(p, encoding="utf-8") as f:
        entry = json.load(f)
    append_entry(ws, entry)
    print("appended:", p, "->", ws.path / "log.jsonl")
