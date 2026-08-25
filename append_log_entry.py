"""Append a JSON entry (from a file) to a log.jsonl (UTF-8, no BOM issues)."""
import json
import sys

entry_file, log_file = sys.argv[1], sys.argv[2]
entry = json.load(open(entry_file, encoding="utf-8-sig"))
with open(log_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print("appended", entry.get("action"), "round", entry.get("round"))
