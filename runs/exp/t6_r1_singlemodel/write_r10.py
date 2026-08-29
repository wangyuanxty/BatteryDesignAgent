"""R10 propose: G-bracket - the early-trip razor (kappa 0.170-0.182 + h 400)."""
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
    "Total heat transfer coefficient [W.m-2.K-1]": 400.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}

CANDS = {
    "G1_kappa0182": 0.182,
    "G2_kappa0175": 0.175,
    "G3_kappa0170": 0.170,
}

roles = {
    "G1_kappa0182": "the shallowest of the razor: the eta_e = 0.06868/0.182 + 0.00546 = 0.3828 (the Delta-eta +0.0159 vs the F3). The V(t) peak ~4.686 + 0.0159 = 4.702 - the trip at the very peak (~t_ch 95-115); the anode_pot margin at the trip ~+11 mV (the algebra 0.9*Delta_eta - 1 mV). The lowest heat of the bracket (the T safest) but the thinnest anode-potential margin.",
    "G2_kappa0175": "the balanced razor: the eta_e 0.3979 (the Delta-eta +0.031). The trip on the V rising edge (~t_ch 85-95) at the anode_pot ~+25 mV. The middle of the margin/T trade.",
    "G3_kappa0170": "the deep razor: the eta_e 0.4094 (the Delta-eta +0.0425). The earliest trip (~t_ch 75-85), the anode_pot margin ~+32 mV (the margin grows ~0.9 mV per mV of the extra eta on the rising edge - the earlier the trip, the higher the OCP_n). The highest heat of the bracket (the T risk, the h 400 counters).",
}

propose = {
    "action": "propose",
    "round": 10,
    "candidates": [
        {
            "name": name,
            "base": BASE,
            "struct": {**BASE_PARAMS, "Electrolyte conductivity [S.m-1]": kappa},
            "role": roles[name],
        }
        for name, kappa in CANDS.items()
    ],
    "llm_reason": "Bridge listing (deltas vs F3_kappa0190):\n  Electrolyte conductivity [S.m-1] 0.190 -> 0.182 (G1) / 0.175 (G2) / 0.170 (G3); Total heat transfer coefficient 200 -> 400 (all three - the R9's T 324.1-324.5 K FAIL needs the thermal fix; the sanctioned thermal-management lever).\nR9 verdicts: F1/F2/F3 all fail (the plated TRUE with the anode_pot min -0.133/-0.133/-0.137; the T 324.14/324.26/324.52 FAIL). The diag_f3 trace resolved the TWO failure modes: (1) the dip-trip prediction failed - the measured eta_e = 0.06868/kappa + 0.00546 (0.3669 at the 0.19, NOT the 0.419 the linear 0.0796/kappa model predicted), so the eta_tot 0.374 < the 0.392 needed and the V peaked at only 4.641 in the OCP_c dip; the trip still fired at the anode kinetic saturation (the t_ch 1165-1214). (2) The deliberate IR pushed the anode surface potential NEGATIVE from the t_ch ~150 s (the anode_pot = OCP_n - 0.615*eta_e; the n crosses 0.26) - the low kappa makes the plating fire EARLIER, the opposite of the intent.\nThe algebra for the remaining window: the anode_pot at the trip = 0.385*OCP_n + 0.615*OCP_c - 2.8856 - positive only for the t_ch < ~110 s (the margin decays from +0.132 V at the t_ch 0 at ~-0.0012/s). The trip must therefore fire on the charge-start rising edge (the V(t) = 4.5515 + 0.00134*t + Delta_eta in the t_ch 0-100 window). The trip margin = 0.9*Delta_eta - 0.001 - i.e., the deeper the kappa, the EARLIER the trip and the LARGER the anode_pot margin. The G-bracket probes this razor: the expected trips at the t_ch ~75-115 with the margins +11 to +32 mV and the 4C fills ~1.5-2.5% (the honest consequence - the no-plating 4C charge terminates almost immediately at the 4.7 V limit; the criterion is the plating and the T, and the fill is reported honestly). The mid drops to ~4.205-4.21 (the plateau >= 4.1 PASS with the ~0.1 margin), the ED ~1104-1108 (PASS), the SEI ~130-132 (PASS). This is the LAST mechanism-consistent window: if the bracket fails, the case closes with the honest infeasibility conclusion (the 4C-to-4.7-V no-plating contract is at the edge of this OCP pair).",
}

with open("log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(propose, ensure_ascii=False) + "\n")
print("propose round 10 appended")

for name, kappa in CANDS.items():
    p = {**BASE_PARAMS, "Electrolyte conductivity [S.m-1]": kappa}
    (CELL / f"r10_{name.split('_')[0]}_params.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
    print(f"wrote r10_{name.split('_')[0]}_params.json (kappa={kappa}, h=400) ->", len(p), "keys")
