"""Append a JSON entry to the case log.jsonl via the bda store API (protocol rule:
all log writes except evaluate go through append_entry). Usage:
  python _append.py <entry.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

entry_path = Path(sys.argv[1])
entry = json.loads(entry_path.read_text(encoding="utf-8"))
ws = CaseWorkspace("t4_r1_flash", "runs/exp")
append_entry(ws, entry)
print("appended:", entry_path.name)
