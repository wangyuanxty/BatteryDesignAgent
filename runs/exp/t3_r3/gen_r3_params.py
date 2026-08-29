"""Generate round-3 variant parameter files (workspace-internal helper, t3_r3)."""
import json
from pathlib import Path

CELL = Path("runs/exp/t3_r3/cell")

RHO_P = 3262.0
RHO_N = 1657.0
S = 0.46

COMMON_POS = {
    "Positive electrode thickness [m]": 4.62521e-05,
    "Positive electrode porosity": 0.5,
}

def mk(eps_p, lp, eps_n, neg_fac, h):
    p = {
        "Electrolyte conductivity [S.m-1]": 1.5,
        "Cation transference number": 0.35,
        "Electrolyte diffusivity [m2.s-1]": 5e-10,
        "Positive current collector thickness [m]": 8e-6,
        "Negative current collector thickness [m]": 6e-6,
        "Separator porosity": 0.5,
        "Positive particle radius [m]": 1.2e-6,
        "Negative particle radius [m]": 1.5e-6,
        "Total heat transfer coefficient [W.m-2.K-1]": h,
    }
    p["Positive electrode thickness [m]"] = lp
    p["Positive electrode porosity"] = eps_p
    p["Negative electrode porosity"] = eps_n
    ln = S * 0.105881827 * neg_fac / (RHO_N * (1 - eps_n))
    p["Negative electrode thickness [m]"] = round(ln, 10)
    return p

L45 = 4.62521e-05  # eps_p 0.50
L55 = 5.13912e-05  # eps_p 0.55

variants = {
    "r3_v4_npup": mk(0.50, L45, 0.45, 1.3, 10.0),
    "r3_v5_cool": mk(0.50, L45, 0.45, 1.05, 20.0),
    "r3_v6_npup_cool": mk(0.50, L45, 0.45, 1.3, 20.0),
    "r3_v7_hip_npup_cool": mk(0.55, L55, 0.50, 1.3, 20.0),
}

for name, p in variants.items():
    out = CELL / f"{name}_params.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)
    print(out.name)
    for k in ("Positive electrode thickness [m]", "Positive electrode porosity",
              "Negative electrode thickness [m]", "Negative electrode porosity",
              "Total heat transfer coefficient [W.m-2.K-1]"):
        print(f"  {k} = {p[k]}")