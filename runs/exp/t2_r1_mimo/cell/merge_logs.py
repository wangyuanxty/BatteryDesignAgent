import json, sys, os
sys.path.insert(0, ".")
from bda.store import CaseWorkspace, append_entry

# Read the nested log (where append_entry wrote)
nested_log = "runs/exp/t2_r1_mimo/t2_r1_mimo/log.jsonl"
main_log = "runs/exp/t2_r1_mimo/log.jsonl"

# Read entries from nested log
nested_entries = []
with open(nested_log, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            nested_entries.append(json.loads(line))

print(f"Nested log has {len(nested_entries)} entries")
for e in nested_entries:
    print(f"  action={e.get('action','?')}, round={e.get('round','-')}")

# Read entry0 from main log
with open(main_log, encoding="utf-8") as f:
    entry0 = json.loads(f.readline().strip())

# Rewrite main log with entry0 + all nested entries
with open(main_log, "w", encoding="utf-8") as f:
    f.write(json.dumps(entry0, ensure_ascii=False) + "\n")
    for e in nested_entries:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

# Count lines
with open(main_log, encoding="utf-8") as f:
    count = sum(1 for line in f if line.strip())
print(f"\nMain log now has {count} entries")
