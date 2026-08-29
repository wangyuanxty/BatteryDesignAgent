"""Generate round-2 variant parameter files (workspace-internal helper, t3_r3).

Fixed platform (all variants): electrolyte formulation overrides (sigma=1.5 S/m,
t+=0.35, D=5e-10 m2/s, literature-class estimate), ultrathin collectors
(Al 16->8 um, Cu 12->6 um). Loading scale s=0.46 of baseline electrode loading,
negative loading x1.05 vs baseline N/P ratio.
"""
import json
from pathlib import Path

CELL = Path("runs/exp/t3_r3/cell")

RHO_P = 3262.0  # positive density kg/m3
RHO_N = 1657.0  # negative density kg/m3
L_P0 = 75.6e-6  # baseline positive thickness
EPS_P0 = 0.335
L_N0 = 85.2e-6
EPS_N0 = 0.25
S = 0.46  # loading scale factor (targets ~2.28 Ah at baseline utilization)
N_P_FAC = 1.05  # +5% negative loading for plating margin

base_pos_loading = L_P0 * (1 - EPS_P0) * RHO_P  # 0.16399 kg/m2
base_neg_loading = L_N0 * (1 - EPS_N0) * RHO_N  # 0.10588 kg/m2

common = {
    "Electrolyte conductivity [S.m-1]": 1.5,
    "Cation transference number": 0.35,
    "Electrolyte diffusivity [m2.s-1]": 5e-10,
    "Positive current collector thickness [m]": 8e-6,
    "Negative current collector thickness [m]": 6e-6,
    "Separator porosity": 0.5,
}

def thicknesses(eps_p, eps_n):
    lp = S * base_pos_loading / (RHO_P * (1 - eps_p))
    ln = S * base_neg_loading * N_P_FAC / (RHO_N * (1 - eps_n))
    return lp, ln

variants = {
    "V1_HP_A": {"eps_p": 0.50, "eps_n": 0.45, "r_p": 2.0e-6, "r_n": 2.5e-6},
    "V2_HP_B": {"eps_p": 0.55, "eps_n": 0.50, "r_p": 2.0e-6, "r_n": 2.5e-6},
    "V3_HP_C": {"eps_p": 0.50, "eps_n": 0.45, "r_p": 1.2e-6, "r_n": 1.5e-6},
}

for name, v in variants.items():
    lp, ln = thicknesses(v["eps_p"], v["eps_n"])
    p = dict(common)
    p.update({
        "Positive electrode thickness [m]": round(lp, 10),
        "Negative electrode thickness [m]": round(ln, 10),
        "Positive electrode porosity": v["eps_p"],
        "Negative electrode porosity": v["eps_n"],
        "Positive particle radius [m]": v["r_p"],
        "Negative particle radius [m]": v["r_n"],
    })
    out = CELL / f"r2_{name.lower()}_params.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    print(out.name)
    for k, val in sorted(p.items()):
        print(f"  {k} = {val}")