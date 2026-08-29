import json
import sys

sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r1_noceiling", "runs/exp")
for name in ["endorse.json", "final.json"]:
    entry = json.load(open(f"runs/exp/t5_r1_noceiling/{name}", encoding="utf-8"))
    append_entry(ws, entry)
    print("appended", name, entry.get("action"))
