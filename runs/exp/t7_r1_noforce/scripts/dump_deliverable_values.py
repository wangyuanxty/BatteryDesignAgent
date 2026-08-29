"""Dump all values needed for deliverables + check lib availability + verify-deliverables expectations."""
import json, sys
from pathlib import Path

ws = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_noforce")

print("=== R5 energy output (full) ===")
d = json.loads((ws / "cell/r5_slim_energy.json").read_text(encoding="utf-8-sig"))
print(json.dumps(d, indent=2, ensure_ascii=False)[:3000])

print("\n=== R5 1C DFN scalars ===")
d = json.loads((ws / "cell/r5_slim_1c_dfn.json").read_text(encoding="utf-8-sig"))
for k, v in d.items():
    if isinstance(v, (int, float, bool)):
        print(f"  {k}: {v}")

print("\n=== R5 4C45 scalars ===")
d = json.loads((ws / "cell/r5_slim_4c45.json").read_text(encoding="utf-8-sig"))
for k, v in d.items():
    if isinstance(v, (int, float, bool)):
        print(f"  {k}: {v}")

print("\n=== R5 aging45 scalars ===")
d = json.loads((ws / "cell/r5_slim_aging45.json").read_text(encoding="utf-8-sig"))
for k, v in d.items():
    if isinstance(v, (int, float, bool)):
        print(f"  {k}: {v}")

print("\n=== R5 nail scalars ===")
d = json.loads((ws / "validation/r5_slim_nail.json").read_text(encoding="utf-8-sig"))
for k, v in d.items():
    if isinstance(v, (int, float, bool)):
        print(f"  {k}: {v}")

print("\n=== params_r5_slim ===")
print((ws / "cell/params_r5_slim.json").read_text(encoding="utf-8"))

print("\n=== libs ===")
for m in ("openpyxl", "reportlab", "docx"):
    try:
        __import__(m)
        print(f"  {m}: OK")
    except ImportError as e:
        print(f"  {m}: MISSING ({e})")
