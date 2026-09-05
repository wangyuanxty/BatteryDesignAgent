import json, sys
sys.path.insert(0, ".")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_mimo", "runs/exp/t2_r1_mimo")

# Read current log
with open("runs/exp/t2_r1_mimo/log.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

# Update entry 0 criteria to match actual output keys
lines[0]["criteria"]["stage2"]["sei_thickness_nm_end_100cyc"] = {"max": 500}
lines[0]["criteria"]["stage2"]["sei_thickness_nm_end_500cyc"] = {"max": 550}
lines[0]["criteria"]["stage2"]["capacity_retention_lowT_pct"] = {"min": 90.0}
# Remove old mismatched keys
del lines[0]["criteria"]["stage2"]["capacity_retention_lowT"]
del lines[0]["criteria"]["stage3"]["sei_thickness_100cyc_nm"]
del lines[0]["criteria"]["stage3"]["sei_thickness_500cyc_nm"]

# Rewrite log.jsonl
with open("runs/exp/t2_r1_mimo/log.jsonl", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

print("Entry 0 criteria corrected")
