import json, sys
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t9_r1", "runs/exp", create=True)
with open(sys.argv[1], encoding="utf-8") as f:
    entry = json.load(f)
append_entry(ws, entry)
print("appended entry, action=", entry.get("action"), "keys=", list(entry.keys()))
