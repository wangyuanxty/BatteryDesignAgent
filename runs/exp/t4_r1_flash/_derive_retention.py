"""Mechanical retention computation: low_temperature_retention = capacity(lowT) / capacity(25C),
same params. Reads two run-pyamm outputs, writes derived JSON for log-evaluate.
Usage: python _derive_retention.py <lowt.json> <ref.json> <out.json> [--candidate NAME]
"""
import json
import sys
from pathlib import Path

lowt_path, ref_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
cand = ""
if "--candidate" in sys.argv:
    cand = sys.argv[sys.argv.index("--candidate") + 1]

lowt = json.loads(Path(lowt_path).read_text(encoding="utf-8"))
ref = json.loads(Path(ref_path).read_text(encoding="utf-8"))
c_lowt = lowt["capacity_ah"]
c_ref = ref["capacity_ah"]
retention = c_lowt / c_ref
derived = {
    "low_temperature_retention": retention,
    "capacity_ah_25c": c_ref,
    "capacity_ah_lowt": c_lowt,
    "retention_derivation": f"{c_lowt}/{c_ref} (same params)",
}
Path(out_path).write_text(json.dumps(derived, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(derived, indent=2))
