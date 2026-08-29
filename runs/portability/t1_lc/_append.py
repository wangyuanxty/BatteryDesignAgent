import json, sys
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t1_lc", "runs")
entry = json.loads(open(sys.argv[1], encoding="utf-8").read())
append_entry(ws, entry)
print("appended:", entry.get("action", entry.get("criteria", "?"))[:1])
