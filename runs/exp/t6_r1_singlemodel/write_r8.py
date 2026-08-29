"""R8 propose: bulk-capacity balance candidates E5/E6 + param files."""
import json
from pathlib import Path

CELL = Path("cell")
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

E5 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1.1e-04,
    "Positive electrode thickness [m]": 5.25e-05,
    "Positive electrode porosity": 0.3,
    "Positive electrode active material volume fraction": 0.7,
    "Negative electrode porosity": 0.27,
    "Negative electrode active material volume fraction": 0.73,
    "Electrolyte conductivity [S.m-1]": 2.0,
    "Cation transference number": 0.65,
    "Electrolyte diffusivity [m2.s-1]": 4e-10,
    "Initial concentration in electrolyte [mol.m-3]": 2500.0,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}
E6 = dict(E5)
E6["Negative electrode thickness [m]"] = 1.0e-04
E6["Positive electrode thickness [m]"] = 4.8e-05

propose = {
    "action": "propose",
    "round": 8,
    "candidates": [
        {
            "name": "E5_anode110_cath52",
            "base": BASE,
            "struct": E5,
            "role": "bulk-capacity balance (the R7-diagnosed mechanism): anode 100->110 um (Q_a 6.48->7.13 mAh/cm2) + cathode 61->52.5 um (Q_c 7.22->6.22). The 4C charge trips at 4.7 V when the cathode BULK strips to ~0.01-0.03 (the OCP_c caps at 4.696 < 4.7; the trip swing ~0.97-0.99 Q_c = 6.03-6.16 mAh/cm2 -> ~1241-1267 s). The anode charge-room = (1-n_start)xQ_a with the clamp-tail discharge (S_dis ~0.82 Q_a = 5.85, the anode ends ~0.08 like the E3/D1 traces) -> the room ~0.92 Q_a = 6.56 mAh/cm2 -> the anode-full at ~1349 s. The margin ~80-110 s positive -> no plating expected. Discharge stays the anode-depletion-limited clamp-tail ~5.8-5.9 mAh/cm2 (~5.97 Ah) -> ED ~1310-1320 Wh/L (>=950 PASS with margin). All other keys inherit the passing E-lineage (electrolyte c0 2500 / t+ 0.65 / D 4e-10 / kappa 2.0, porosity 0.30/0.27, SEI 1e-13/1.5e-8, h 200).",
        },
        {
            "name": "E6_anode100_cath48",
            "base": BASE,
            "struct": E6,
            "role": "sensitivity, thinner cathode 48 um (Q_c 5.68) on the D1 anode 100 um (Q_a 6.48). Trip swing ~0.97-0.99 Q_c = 5.51-5.62 -> ~1133-1157 s; the anode room with the clamp-tail discharge (the end-anode ~0.08 like the E3 trace) ~0.92 Q_a = 5.96 -> the anode-full at ~1226 s: margin ~69-93 s positive. Discharge ~5.3-5.5 mAh/cm2 -> ED ~1290-1300. Tests whether the thinner cathode (less charge-time to the trip) further widens the no-plating margin at the cost of the ED.",
        },
    ],
    "llm_reason": "Bridge listing (deltas vs E1_cathode_61um):\n  E5: Negative electrode thickness 1.0e-4 -> 1.1e-4; Positive electrode thickness 6.1e-5 -> 5.25e-5 (R_p back to 1e-7, the empirically dead lever).\n  E6: Positive electrode thickness 6.1e-5 -> 4.8e-5 (the anode unchanged).\nR7 verdicts: E3/E4 both fail (the 4C charge 1245.3/1245.5 s, plated min -0.237; T 319.14 PASS, SEI 118.8 PASS, ED 1130.7 PASS, mid 4.2973 PASS). The R7 diagnostics resolved the mechanism: the anode saturates at the swing 0.913 Q_a (1217 s) -> the plunge -> the plating -> the trip, while the clean 4.7 V trip needs the cathode BULK to strip to ~0.01-0.03 (the OCP_c cap 4.696 < 4.7) - with the Q_c 7.22 that is 1438+ s, far past the anode-full. The quasi-steady surface-overshoot theory is overturned (the c_surf == c_avg in this SPMe; the R_p change moved the trip < 1 s) and the salt-depletion theory is overturned (the frozen profile, min 2045 mol/m3). The balance constraint: 0.97-0.99 Q_c + margin <= the anode charge-room 0.10 Q_a + S_dis (the clamp-tail discharge S_dis ~ 0.82 Q_a, evidenced by the D1's 5.80 mAh/cm2 past the 5.27 cathode-room point). E5 = the main balance candidate; E6 = the margin sensitivity.",
}

with open("log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(propose, ensure_ascii=False) + "\n")
print("propose round 8 appended")

(CELL / "r8_E5_params.json").write_text(json.dumps(E5, indent=2), encoding="utf-8")
(CELL / "r8_E6_params.json").write_text(json.dumps(E6, indent=2), encoding="utf-8")
print("wrote r8_E5_params.json ->", len(E5), "keys")
print("wrote r8_E6_params.json ->", len(E6), "keys")
