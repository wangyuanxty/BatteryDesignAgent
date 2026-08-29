"""Mechanical derivation files for log-evaluate (baseline, round 1).
- derived_sei_500cyc_base.json: renames the 500-cycle aging output key
  sei_thickness_nm_end -> sei_thickness_nm_end_500cyc so the 550 nm threshold
  is judged against its own criteria key (raw file is NOT passed to
  log-evaluate: its sei_thickness_nm_end would be judged against the
  100-cycle 500 nm threshold).
- derived_retention_lowT_base.json: lowT retention = -20C capacity / 25C
  1C capacity * 100.
"""
import json
from pathlib import Path

CELL = Path("runs/exp/t2_r1_singlemodel/cell")

def load(name):
    return json.loads((CELL / name).read_text(encoding="utf-8-sig"))

# --- 500-cycle SEI rename (pure key copy, no arithmetic) ---
aging500 = load("base_aging500.json")
sei500 = float(aging500["sei_thickness_nm_end"])
(CELL / "derived_sei_500cyc_base.json").write_text(
    json.dumps({
        "sei_thickness_nm_end_500cyc": sei500,
        "derived_from": "cell/base_aging500.json:sei_thickness_nm_end",
        "formula": "key copy (rename only, no arithmetic)",
    }, indent=2),
    encoding="utf-8",
)

# --- lowT retention (mechanical division) ---
lowT = load("base_lowT_cold.json")
ref = load("base_1c_spme.json")
cap_lowT = float(lowT["capacity_ah"])
cap_25C = float(ref["capacity_ah"])
retention = cap_lowT / cap_25C * 100.0
(CELL / "derived_retention_lowT_base.json").write_text(
    json.dumps({
        "retention_lowT_pct": retention,
        "capacity_ah_lowT": cap_lowT,
        "capacity_ah_25C": cap_25C,
        "derived_from": "cell/base_lowT_cold.json:capacity_ah / "
                        "cell/base_1c_spme.json:capacity_ah * 100",
        "formula": "lowT_capacity / 25C_capacity * 100",
    }, indent=2),
    encoding="utf-8",
)
print(f"sei500 = {sei500} nm; retention = {retention:.2f}%")
