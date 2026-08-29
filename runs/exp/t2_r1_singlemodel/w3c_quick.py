"""Final-params quick suite: 1C, lowT, 4C45, 4C25, calc-energy, derived retention."""
import json
import subprocess
import sys

CASE = "runs/exp/t2_r1_singlemodel"
CELL = f"{CASE}/cell"


def bda(*args):
    r = subprocess.run([sys.executable, "-m", "bda.cli", *args])
    if r.returncode != 0:
        print(f"FAILED: bda {' '.join(args)}")
        sys.exit(1)


# 1C discharge (DFN)
bda("run-pyamm", "--params", f"{CELL}/params_r3.json", "--protocol", "1C_discharge",
    "--mode", "dfn", "--out", f"{CELL}/r3_1c_dfn.json")
# lowT discharge (DFN)
bda("run-pyamm", "--params", f"{CELL}/params_r3_lowT.json", "--protocol", "lowT_discharge",
    "--mode", "dfn", "--out", f"{CELL}/r3_lowT.json")
# 4C charge 45C-start (DFN, plating)
bda("run-pyamm", "--params", f"{CELL}/params_r3_4c45.json", "--protocol", "4C_charge_45C",
    "--mode", "dfn", "--plating", "--out", f"{CELL}/r3_4c45.json")
# 4C charge conservative 25C-start (DFN, plating)
bda("run-pyamm", "--params", f"{CELL}/params_r3_4c25.json", "--protocol", "4C_charge_45C",
    "--mode", "dfn", "--plating", "--out", f"{CELL}/r3_4c25_conservative.json")
# contract-caliber energy density
bda("calc-energy", "--sim", f"{CELL}/r3_1c_dfn.json", "--params", f"{CELL}/params_r3.json",
    "--out", f"{CELL}/r3_energy.json")

# derived retention
lo = json.load(open(f"{CELL}/r3_lowT.json"))
ref = json.load(open(f"{CELL}/r3_1c_dfn.json"))
ret = lo["capacity_ah"] / ref["capacity_ah"] * 100
d = {
    "retention_lowT_pct": round(ret, 2),
    "capacity_lowT_ah": lo["capacity_ah"],
    "capacity_1C_ref_ah": ref["capacity_ah"],
    "source_files": ["cell/r3_lowT.json", "cell/r3_1c_dfn.json"],
    "formula": "capacity_lowT_ah / capacity_1C_ref_ah * 100",
}
json.dump(d, open(f"{CELL}/derived_retention_lowT_r3.json", "w"), indent=1)

e = json.load(open(f"{CELL}/r3_energy.json"))
c4 = json.load(open(f"{CELL}/r3_4c45.json"))
c4c = json.load(open(f"{CELL}/r3_4c25_conservative.json"))
print("R3 FINAL-PARAMS SUITE:")
print(f"  1C cap={ref['capacity_ah']:.4f} Ah | lowT cap={lo['capacity_ah']:.4f} Ah -> retention {ret:.2f}%")
print(f"  ED={e['energy_density_wh_kg']:.2f} Wh/kg mass={e['mass_kg']:.4f} kg")
print(f"  4C45 ap_min={min(c4['anode_potential_v']):.4f} T_max={c4.get('T_max_K', float('nan')):.1f}")
print(f"  4C25 ap_min={min(c4c['anode_potential_v']):.4f} T_max={c4c.get('T_max_K', float('nan')):.1f}")
