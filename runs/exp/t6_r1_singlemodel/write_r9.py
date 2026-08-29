"""R9 propose: deliberate-IR candidates F1/F2/F3 (kappa bracket) + param files."""
import json
from pathlib import Path

CELL = Path("cell")
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

BASE_PARAMS = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1.0e-04,
    "Positive electrode thickness [m]": 6.1e-05,
    "Positive electrode porosity": 0.3,
    "Positive electrode active material volume fraction": 0.7,
    "Negative electrode porosity": 0.27,
    "Negative electrode active material volume fraction": 0.73,
    "Cation transference number": 0.65,
    "Electrolyte diffusivity [m2.s-1]": 4e-10,
    "Initial concentration in electrolyte [mol.m-3]": 2500.0,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}

CANDS = {
    "F1_kappa0205": 0.205,
    "F2_kappa0200": 0.200,
    "F3_kappa0190": 0.190,
}

roles = {
    "F1_kappa0205": "near the trip boundary: the eta_tot(4C) = 0.0796/kappa + 0.012 = 0.400 V. The V = 4.70 crossing fires when the OCP_n(n) = 4.40 + eta - 4.70 = 0.100-0.108, i.e., the anode sto ~0.62-0.65 (the OCP_n 0.119 at 0.6, 0.092 at 0.7) -> the charge swing ~3.5-3.7 mAh/cm2, the anode at the trip ~0.62-0.65 (the margin ~0.3 Q_a = ~440 s to the saturation), the 4C fill ~65-70%. The highest fill of the bracket; probes the boundary (the kappa > ~0.2095 stalls at V 4.699 - no clean trip).",
    "F2_kappa0200": "the balanced center: the eta_tot 0.410 V -> the crossing at the OCP_n 0.110 -> the anode ~0.62 -> the swing ~3.45 mAh/cm2, the fill ~65%, the margin ~440 s. Expected no-plating with the comfortable margin.",
    "F3_kappa0190": "the deep-IR safety: the eta_tot 0.431 V -> the crossing at the OCP_n 0.131 -> the anode ~0.49 -> the swing ~2.6 mAh/cm2, the fill ~49%, the margin enormous. The max-margin variant if F1/F2 land too close to the boundary.",
}

propose = {
    "action": "propose",
    "round": 9,
    "candidates": [
        {
            "name": name,
            "base": BASE,
            "struct": {**BASE_PARAMS, "Electrolyte conductivity [S.m-1]": kappa},
            "role": roles[name],
        }
        for name, kappa in CANDS.items()
    ],
    "llm_reason": "Bridge listing (deltas vs E1_cathode_61um):\n  Electrolyte conductivity [S.m-1] 2.0 -> 0.205 (F1) / 0.200 (F2) / 0.190 (F3). The sanctioned electrolyte-formulation lever, used here deliberately as the charge-end IR.\nR8 verdicts: E5/E6 both fail (the 4C charge 1079.0/985.5 s, plated -0.234/-0.236; T 319.53/319.09 PASS, SEI 112.1/111.9 PASS, ED 975.3/962.9 PASS, mid 4.2976/4.2980 PASS). The diag_e5 trace resolved the mechanism definitively: the discharge ends by the cathode KINETIC saturation (the positive reaction overpotential -0.93 V at the sto 1.0); the charge's total overpotential is only ~0.05 V (the eta_e 0.0398 at the kappa 2.0), so the clean V ceiling 4.696-0.092+0.05 = 4.654 < 4.70 - the trip requires the anode kinetic saturation + the plunge. The fix: the deliberate IR - the eta_tot = 0.0796/kappa + 0.012 must clear 4.70 - 4.40 (the OCP_c dip floor) + 0.092 = 0.392 V, i.e., the kappa <= ~0.209; then the 4.7 trip fires inside the OCP_c flat dip with the anode at 0.5-0.7 and a huge no-plating margin. The cost: the 1C midpoint drops ~0.10 V (the eta_e 0.10 at the 1C) to ~4.20 (the plateau >= 4.1 still PASS with the ~0.1 margin), the ED ~1165-1175, and the 4C fill ~50-70% of the full capacity (the honest datasheet note). The 4C IR heat adds ~6-7 W -> the T ~319.8 (PASS).",
}

with open("log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(propose, ensure_ascii=False) + "\n")
print("propose round 9 appended")

for name, kappa in CANDS.items():
    p = {**BASE_PARAMS, "Electrolyte conductivity [S.m-1]": kappa}
    (CELL / f"r9_{name.split('_')[0]}_params.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
    print(f"wrote r9_{name.split('_')[0]}_params.json (kappa={kappa}) ->", len(p), "keys")
