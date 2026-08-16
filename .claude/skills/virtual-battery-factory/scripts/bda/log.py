import json

from bda.store import CaseWorkspace


def append_entry(ws: CaseWorkspace, entry: dict) -> None:
    with open(ws.path / "log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
