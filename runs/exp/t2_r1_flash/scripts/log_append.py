"""Generic log entry appender: python log_append.py <entry.json> — uses bda.store.append_entry (official API)."""
import json
import sys
from pathlib import Path
from bda.store import append_entry, CaseWorkspace

entry = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ws = CaseWorkspace("t2_r1_flash", "runs/exp")
append_entry(ws, entry)
print("appended:", list(entry.keys())[0])
