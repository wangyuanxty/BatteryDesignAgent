"""Generate round-4 variant parameter files (workspace-internal helper, t3_r3)."""
import json
from pathlib import Path

CELL = Path("runs/exp/t3_r3/cell")

BASE = {
    "Electrolyte conductivity [S.m-1]": 1.5,
    "Cation transference number": 0.35,
    "Positive current collector thickness [m]": 8e-6,
    "Negative current collector thickness [m]": 6e-6,
    "Separator porosity": 0.5,
    "Positive electrode thickness [m]": 4.62521e-05,
    "Positive electrode porosity": 0.5,
    "Negative electrode thickness [m]": 6.94764e-05,
    "Negative electrode porosity": 0.45,
}

def mk(r_p, r_n, D, h):
    p = dict(BASE)
    p.update({
        "Positive particle radius [m]": r_p,
        "Negative particle radius [m]": r_n,
        "Electrolyte diffusivity [m2.s-1]": D,
        "Total heat transfer coefficient [W.m-2.K-1]": h,
    })
    return p

variants = {
    "r4_v8_finecath": mk(0.8e-6, 1.0e-6, 5.0e-10, 20.0),
    "r4_v9_fastd": mk(1.2e-6, 1.5e-6, 8.0e-10, 20.0),
    "r4_v10_h25": mk(1.2e-6, 1.5e-6, 5.0e-10, 25.0),
    "r4_v11_combo": mk(0.8e-6, 1.0e-6, 8.0e-10, 25.0),
}

for name, p in variants.items():
    out = CELL / f"{name}_params.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    print(out.name, "| rp", p["Positive particle radius [m]"], "| rn", p["Negative particle radius [m]"], "| D", p["Electrolyte diffusivity [m2.s-1]"], "| h", p["Total heat transfer coefficient [W.m-2.K-1]"])