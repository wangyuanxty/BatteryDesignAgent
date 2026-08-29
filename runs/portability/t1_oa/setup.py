import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_oa", "runs/portability")
here = Path(__file__).resolve().parent
entry0 = json.loads((here / "entry0.json").read_text(encoding="utf-8"))

# Append entry 0 only if log.jsonl does not already have a criteria entry
log_path = ws.path / "log.jsonl"
has_criteria = False
if log_path.exists():
    for line in log_path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if isinstance(e.get("criteria"), dict):
            has_criteria = True
            break
if not has_criteria:
    append_entry(ws, entry0)
    print("entry0 appended")
else:
    print("entry0 already present, skipped")

print("log path:", log_path)
