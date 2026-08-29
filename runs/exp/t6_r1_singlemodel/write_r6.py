"""Round 6: propose E1/E2 (cathode-anode balance so 4C charge trips before anode saturation). t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

D1 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode porosity": 0.30,
    "Positive electrode active material volume fraction": 0.70,
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
E1 = dict(D1)
E1.update({"Positive electrode thickness [m]": 6.1e-05})
E2 = dict(E1)
E2.update({
    "Positive electrode porosity": 0.28,
    "Positive electrode active material volume fraction": 0.72,
})

propose = {
    "action": "propose",
    "round": 6,
    "candidates": [
        {
            "name": "E1_cathode_61um",
            "base": LNMO_BASE,
            "struct": E1,
            "role": (
                "charge-end rebalance: D1 4C trace shows the charge runs 1323 s at 18 A with the anode "
                "surface potential positive (min +0.026 V), but the experiment charge step is 'until 4.7 V' "
                "with no time cap -> the charge overshoots past anode-full (~1230 s, bulk sto 1.0) into the "
                "over-charge regime -> plating (-0.237) and 4.7 V trip at 1386 s. Fix: thinner cathode "
                "75->61 um (Q_c 8.88->7.22 mAh/cm2) so the cathode surface strips to its 4.7 V OCP at "
                "~1090 s (swing 0.73 x 7.22 = 5.3 mAh/cm2), BEFORE the anode fills (~1183 s). The 4.7 V "
                "trip then fires while the anode surface is still at sto ~0.99 / OCP ~0.045 V (positive) "
                "-> no plating. Discharge stays anode-limited (5.14 mAh/cm2; cathode ends 0.976 < 1) -> "
                "ED ~1137 Wh/L (thinner stack, same energy)."
            ),
        },
        {
            "name": "E2_am072_sensitivity",
            "base": LNMO_BASE,
            "struct": E2,
            "role": (
                "sensitivity: AM 0.70->0.72 (porosity 0.30->0.28) on the 61 um cathode (Q_c 7.43): trip "
                "margin vs anode-full narrows to ~68 s. Tests the balance-margin robustness."
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (deltas vs D1_full_formulation):\n"
        "  Positive electrode thickness [m] 75e-6 -> 61e-6 (E1/E2; charge-end balance, Q_c 8.88 -> "
        "7.22/7.43 mAh/cm2; discharge remains anode-limited, cathode end-sto 0.976/0.953 < 1)\n"
        "  (E2 only: Positive electrode porosity 0.30 -> 0.28 and Positive electrode active material "
        "volume fraction 0.70 -> 0.72, sum=1)\n"
        "R5 verdicts: D1 fail (4C: charge 1386 s, cap metric 1.54 Ah per runner formula (duration x 4 / "
        "3600; true charge = 18 A x 1386 s = 6.93 Ah), plated -0.237, T 319.2 PASS, SEI 126.9 PASS, "
        "ED 1138.8 PASS, mid 4.2941 PASS); D2 same (plated -0.240). D1 trace: anode potential positive "
        "for the first 1323 s (min +0.026); plating only in the over-charge tail after the anode "
        "saturates. Balance fix above."
    ),
}

append_entry(ws, propose)
print("propose round 6 appended")

for name, params in (("E1", E1), ("E2", E2)):
    p = CELL / f"r6_{name}_params.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
