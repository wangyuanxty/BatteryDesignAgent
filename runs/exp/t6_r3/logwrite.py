"""Append one log.jsonl entry from a JSON file via bda.store.append_entry (protocol-sanctioned path).

Usage: .venv\\Scripts\\python.exe runs/exp/t6_r3/logwrite.py <entry-json-file>
"""
import json
import sys

from bda.store import CaseWorkspace, append_entry

CASE_ID = "t6_r3"
ROOT = "runs/exp"

entry_path = sys.argv[1]
with open(entry_path, "r", encoding="utf-8") as f:
    entry = json.load(f)

ws = CaseWorkspace(CASE_ID, ROOT)
append_entry(ws, entry)
print("appended ->", ws.path / "log.jsonl", "| entry keys:", sorted(entry.keys()))
