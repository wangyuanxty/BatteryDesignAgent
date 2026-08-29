"""Append one JSON entry file as a log.jsonl line via bda.store.append_entry (protocol-mandated writer).

Usage: python append_log.py <entry-file.json> [entry-file-2.json ...]
CaseWorkspace('t3_r2', 'runs/exp') -> repo-root/runs/exp/t3_r2/log.jsonl
"""
import json
import sys
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t3_r2", "runs/exp")
for arg in sys.argv[1:]:
    entry = json.loads(Path(arg).read_text(encoding="utf-8-sig"))
    append_entry(ws, entry)
    print(f"appended {arg}")
print(f"log.jsonl lines now: {sum(1 for _ in open(ws.path / 'log.jsonl', encoding='utf-8'))}")