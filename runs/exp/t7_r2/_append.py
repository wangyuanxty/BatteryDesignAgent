# -*- coding: utf-8 -*-
"""Append one log entry from a JSON file (library API). Usage: python _append.py <entry.json>"""
import json
import sys

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r2", "runs")
with open(sys.argv[1], encoding="utf-8") as f:
    entry = json.load(f)
append_entry(ws, entry)
print("appended:", json.dumps(entry, ensure_ascii=False)[:160])