"""Stage 1 log entries: entry 0 (criteria). Agent-built scratch, uses bda.store.append_entry."""
import json
from pathlib import Path
from bda.store import append_entry, CaseWorkspace

WS_ROOT = Path(__file__).resolve().parent.parent
ws = CaseWorkspace("t2_r1_flash", "runs/exp")  # path = runs/exp/t2_r1_flash (root/case_id)

entry0 = json.loads((WS_ROOT / "stage1_entry0.json").read_text(encoding="utf-8"))
append_entry(ws, entry0)
print("entry 0 written:", ws.path / "log.jsonl")
