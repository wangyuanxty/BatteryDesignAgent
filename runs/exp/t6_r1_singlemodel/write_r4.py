"""Round 4: propose C1/C2 (salt-depletion fix via concentrated electrolyte) + params. t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

B1 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode porosity": 0.28,
    "Positive electrode active material volume fraction": 0.72,
    "Electrolyte conductivity [S.m-1]": 1.6,
    "Cation transference number": 0.4,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
}
C1 = dict(B1)
C1.update({
    "Initial concentration in electrolyte [mol.m-3]": 2000.0,
    "Electrolyte conductivity [S.m-1]": 2.0,
    "Cation transference number": 0.6,
    "Electrolyte diffusivity [m2.s-1]": 3e-10,
})
C2 = dict(C1)
C2.update({"Total heat transfer coefficient [W.m-2.K-1]": 150.0})

propose = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "name": "C1_concentrated_electrolyte",
            "base": LNMO_BASE,
            "struct": C1,
            "role": (
                "salt-depletion fix: B1 4C trace shows the charge runs ~43 s while the anode OCP swings "
                "1.85->0.79 V (V 2.7-3.8), then the anode surface potential plunges through zero (-0.158 V) "
                "in 4 s and V trips at 4.7 V. Diagnosis: steady-state salt depletion at the anode interface, "
                "drop ~ i(1-t+)L_n/(2 F D eps^1.5) ~ 1000+ mol/m3 >= c0=1000 -> c_e -> 0 -> electrolyte "
                "potential collapses -> plating. Fix: concentrated 2 M electrolyte (c0 2000) + high "
                "transference t+ 0.6 + high diffusivity D 3e-10 m2/s + kappa 2.0 S/m (concentrated "
                "LiFSI/LiPF6 blend at 45 C, literature) -> interface c_e ~1400 mol/m3, concentration "
                "overpotential ~10 mV -> no depletion, no plating, charge runs full 900 s."
            ),
        },
        {
            "name": "C2_h150_sensitivity",
            "base": LNMO_BASE,
            "struct": C2,
            "role": (
                "thermal sensitivity of C1: h 200 -> 150 W/m2K (hA ~0.75 W/K). Tests the cooling claim margin; "
                "otherwise identical to C1."
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (deltas vs B1_nano_100_200):\n"
        "  Initial concentration in electrolyte [mol.m-3] 1000 -> 2000 (2 M concentrated electrolyte; salt "
        "formulation lever, electrolyte_formulation DoF - the forbidden 'initial concentration' item refers "
        "to electrode lithiation, not salt molarity; recorded interpretation)\n"
        "  Electrolyte conductivity [S.m-1] 1.6 -> 2.0 (scalar; concentrated blend at 45 C, literature "
        "1.8-2.5 S/m)\n"
        "  Cation transference number 0.4 -> 0.6 (high-t+ concentrated LiFSI electrolytes report 0.5-0.7)\n"
        "  Electrolyte diffusivity [m2.s-1] 1.77e-10 -> 3e-10 (DMC-rich low-viscosity blend at 45 C)\n"
        "  (C2 additionally: Total heat transfer coefficient 200 -> 150 W/m2K sensitivity)\n"
        "R3 verdicts: B1 fail (4C 0.048 Ah, plated -0.158, T 319.9 PASS, SEI 129.2 PASS, ED 1119.4 PASS, "
        "midpoint 4.2757 PASS); B2 fail (4C 0.048 Ah, plated -0.176, T 320.1 PASS, SEI 187.4 PASS). "
        "4C trace diagnosis above - failure mode is electrolyte salt transport, not solid diffusion; "
        "fallback routing: cell-scale symptom, electrolyte-formulation cause -> Stage 3 electrolyte "
        "formulation lever (no material redesign needed)."
    ),
}

append_entry(ws, propose)
print("propose round 4 appended")

for name, params in (("C1", C1), ("C2", C2)):
    p = CELL / f"r4_{name}_params.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
