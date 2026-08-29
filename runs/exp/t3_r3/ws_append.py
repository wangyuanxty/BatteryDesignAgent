"""Append prepared log entries to t3_r3/log.jsonl in order (workspace-internal helper)."""
import json
import sys

from bda.store import CaseWorkspace, append_entry

WS = CaseWorkspace("exp/t3_r3", "runs")
for path in sys.argv[1:]:
    entry = json.load(open(path, encoding="utf-8"))
    append_entry(WS, entry)
    print(f"appended {path} -> {entry.get('action', 'criteria-meta')}")