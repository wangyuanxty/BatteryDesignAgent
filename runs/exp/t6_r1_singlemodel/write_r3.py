"""Round 3: propose B1/B2 (transient-pinning fix) + params files. t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

A4 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode porosity": 0.28,
    "Positive electrode active material volume fraction": 0.72,
    "Electrolyte conductivity [S.m-1]": 1.6,
    "Cation transference number": 0.4,
    "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
}
B1 = dict(A4)
B1.update({
    "Positive particle radius [m]": 1e-07,
    "Negative particle radius [m]": 2e-07,
    "Total heat transfer coefficient [W.m-2.K-1]": 200.0,
})
B2 = dict(B1)
B2.update({"Negative particle radius [m]": 3e-07})

propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "name": "B1_nano_100_200",
            "base": LNMO_BASE,
            "struct": B1,
            "role": (
                "transient-pinning fix: R2 data show the 4C charge dies in ~10 s in A1-A4 even at R_p 0.2 um. "
                "Diagnosis: transient surface strip time ~ pi*D/4*(F*dc/j)^2 is radius-independent; with "
                "D_p=4e-15 m2/s the cathode surface strips in ~3 s and the anode surface saturates in ~8 s at "
                "18 A; then V = OCP_c(0) - OCP_a(1) + eta ~ 4.67 + eta > 4.7 V for any eta > 30 mV -> trip. "
                "Fix: quasi-steady overshoot jR/(5FD) must stay below stoich headroom so the surface never "
                "pins: R_p 0.1 um -> overshoot 0.21*c_max (headroom 0.21: bulk 0.89 -> surface 0.08 at end), "
                "R_n 0.2 um -> overshoot 0.066*c_max (end surface sto 0.74, OCP ~0.09-0.12 V > 0 -> no "
                "plating). h 150->200 W/m2K for thermal margin over the full 900-s charge."
            ),
        },
        {
            "name": "B2_nano_100_300",
            "base": LNMO_BASE,
            "struct": B2,
            "role": (
                "sensitivity on the anode radius (0.2 -> 0.3 um): overshoot 0.10*c_max, end surface sto 0.78 "
                "(OCP ~0.10-0.13 V). Tests how much anode-surface pinning margin B1 actually has; otherwise "
                "identical to B1."
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (deltas vs A4_plus_coating_cooling, which itself = A1 stack + sigma 1.6/t+ 0.4 + "
        "k_SEI 1e-13/j0_SEI 1.5e-8 + h):\n"
        "  Positive particle radius [m] 2e-7 -> 1e-7 (100 nm nano-LNMO spinel, literature 50-200 nm; "
        "Santhanam & Rambabu J. Power Sources 195 (2010) 5442; radius is the sanctioned diffusion lever - "
        "solid diffusivity override forbidden)\n"
        "  Negative particle radius [m] 5e-7 -> 2e-7 (200 nm nano-graphite, high-power anode; B2 tests 3e-7)\n"
        "  Total heat transfer coefficient [W.m-2.K-1] 150 -> 200 (hA ~1.0 W/K; full 900-s 18-A charge heat "
        "est. 2-3 W -> deltaT ~2-3 K; active-cooling phone design note)\n"
        "R2 verdicts: A1 fail (T 330.2, plated, SEI 810, 4C dead 0.035 Ah); A2 fail (328.9, plated, 826, 0.045); "
        "A3 fail (324.1, plated, SEI 310 PASS, 0.048); A4 fail (320.5 PASS, plated, SEI 295 PASS, 0.048). "
        "ED 1115-1156 PASS all; midpoint 4.16-4.27 PASS all. Mechanism above -> B1/B2 expected to clear "
        "4C acceptance + plating; then DFN verification of the winner (Stage 4)."
    ),
}

append_entry(ws, propose)
print("propose round 3 appended")

for name, params in (("B1", B1), ("B2", B2)):
    p = CELL / f"r3_{name}_params.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
