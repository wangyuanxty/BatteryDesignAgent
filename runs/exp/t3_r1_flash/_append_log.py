import json
import sys
from bda.store import append_entry, CaseWorkspace

ws = CaseWorkspace("t3_r1_flash", "runs/exp")
for path in sys.argv[1:]:
    with open(path, encoding="utf-8-sig") as f:
        entry = json.load(f)
    append_entry(ws, entry)
    print("appended:", path, "| keys:", list(entry.keys()))
