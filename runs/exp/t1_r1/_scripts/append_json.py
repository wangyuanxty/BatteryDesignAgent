"""Generic log appender: append a JSON file's content as one log.jsonl entry.
Usage: python append_json.py <entry-json-file>
Uses bda.store.append_entry (protocol rule)."""
import json
import sys
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_r1", "runs/exp")
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
append_entry(ws, data)
print("appended entry:", json.dumps(data, ensure_ascii=False)[:120])
