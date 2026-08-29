"""Round 5: plan update + propose D1/D2 (full salt-transport formulation). t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

C1 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode porosity": 0.28,
    "Positive electrode active material volume fraction": 0.72,
    "Electrolyte conductivity [S.m-1]": 2.0,
    "Cation transference number": 0.6,
    "Electrolyte diffusivity [m2.s-1]": 3e-10,
    "Initial concentration in electrolyte [mol.m-3]": 2000.0,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}
D1 = dict(C1)
D1.update({
    "Initial concentration in electrolyte [mol.m-3]": 2500.0,
    "Cation transference number": 0.65,
    "Electrolyte diffusivity [m2.s-1]": 4e-10,
    "Positive electrode porosity": 0.30,
    "Positive electrode active material volume fraction": 0.70,
    "Negative electrode porosity": 0.27,
    "Negative electrode active material volume fraction": 0.73,
})
D2 = dict(C1)
D2.update({
    "Initial concentration in electrolyte [mol.m-3]": 2500.0,
    "Positive electrode porosity": 0.30,
    "Positive electrode active material volume fraction": 0.70,
    "Negative electrode porosity": 0.27,
    "Negative electrode active material volume fraction": 0.73,
})

plan_update = {
    "action": "plan",
    "update": True,
    "reason": (
        "R4 salt-depletion diagnosis confirmed and partially fixed (4C acceptance 0.048 -> 1.555 Ah, 32x) "
        "but still trips at 4.7 V with plating: total salt drop across the stack ~ "
        "sum (1-t+) i L_i / (F D eps_i^1.5) ~ 3200 mol/m3 > c0 2000 -> anode interface still depletes. "
        "Direction refinement: the binding constraint of the 4C contract is ELECTROLYTE SALT TRANSPORT "
        "(not solid diffusion / not surface pinning) -> architecture + electrolyte co-design: porosity "
        "rebalance (eps_p 0.30 / eps_n 0.27) + concentrated high-t+ low-viscosity formulation "
        "(c0 2.5 M, t+ 0.65, D 4e-10, kappa 2.0); particle size retained (nano electrodes still needed "
        "for surface-pinning avoidance)."
    ),
    "candidate_strategy": (
        "R5: D1 = full formulation (c0 2500, t+ 0.65, D 4e-10, eps 0.30/0.27); D2 = sensitivity with the "
        "milder R4 transport (t+ 0.6, D 3e-10) + porosity fix. Target: 4C charge runs full 900 s "
        "(4.5 Ah), anode potential stays positive, T_max <= 323.15, SEI <= 500, ED >= 950 (expected ~1070), "
        "midpoint >= 4.1 (~4.29). Then DFN verification (Stage 4) of the winner."
    ),
    "budget_allocation": "R5: 2 variants x 4 protocols (8 runs incl. 2 aging). R6: DFN 4C + DFN 1C "
                        "verification of winner + 1 robustness variant. R7: closing deliverables.",
}

propose = {
    "action": "propose",
    "round": 5,
    "candidates": [
        {
            "name": "D1_full_formulation",
            "base": LNMO_BASE,
            "struct": D1,
            "role": (
                "full salt-transport formulation: c0 1000->2500 mol/m3 (2.5 M concentrated), t+ 0.4->0.65 "
                "(high-transference), D 1.77e-10->4e-10 m2/s (low-viscosity DMC-rich blend, 45 C), "
                "kappa 1.6->2.0 S/m; porosity rebalance eps_p 0.28->0.30 (AM 0.72->0.70), eps_n 0.25->0.27 "
                "(AM 0.75->0.73). Estimated total salt drop ~1900 < c0 2500 -> anode-interface c_e ~1350 "
                "mol/m3 -> no depletion, no plating, full 900 s 4C charge."
            ),
        },
        {
            "name": "D2_mild_formulation",
            "base": LNMO_BASE,
            "struct": D2,
            "role": (
                "sensitivity: same porosity rebalance but milder transport claim (t+ 0.6, D 3e-10, "
                "kappa 2.0, c0 2500). Estimated drop ~2400 vs c0 2500 - tests the margin of the honest "
                "formulation envelope."
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (deltas vs C1_concentrated_electrolyte):\n"
        "  Initial concentration in electrolyte [mol.m-3] 2000 -> 2500 (2.5 M LiFSI/LiPF6 concentrated "
        "electrolyte; salt-formulation lever, literature 2-3 M)\n"
        "  Cation transference number 0.6 -> 0.65 (D1 only; high-t+ formulations literature 0.5-0.7)\n"
        "  Electrolyte diffusivity [m2.s-1] 3e-10 -> 4e-10 (D1 only; DMC-rich blend at 45 C)\n"
        "  Positive electrode porosity 0.28 -> 0.30 and Positive electrode active material volume fraction "
        "0.72 -> 0.70 (sum=1; D_eff transport gain; cathode capacity 9.51->8.88 mAh/cm2 still holds the "
        "5.1-5.3 mAh/cm2 discharge swing)\n"
        "  Negative electrode porosity 0.25 -> 0.27 and Negative electrode active material volume fraction "
        "0.75 -> 0.73 (Q_a 6.66->6.16 mAh/cm2 -> discharge ~5.14 mAh/cm2 -> ED ~1074 Wh/L, still >= 950)\n"
        "R4 verdicts: C1 fail (4C 1.555 Ah accepted then 4.7 V trip, plated -0.243, T 319.4 PASS, "
        "SEI 126.9 PASS, ED 1138.8 PASS, mid 4.2941 PASS); C2 identical except h 150 (T 319.8 PASS). "
        "Salt-drop arithmetic above in plan update."
    ),
}

for entry in (plan_update, propose):
    append_entry(ws, entry)
print("plan update + propose round 5 appended")

for name, params in (("D1", D1), ("D2", D2)):
    p = CELL / f"r5_{name}_params.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
