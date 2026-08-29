"""Round 2: propose entry (A1-A4) + params JSON files. t6_r1_singlemodel."""
import json
from pathlib import Path

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t6_r1_singlemodel", "runs/exp")
CELL = ws.path / "cell"
CELL.mkdir(exist_ok=True)

LNMO_BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

# --- candidate parameter deltas (vs LNMO.json base = Chen2020 geometry/electrolyte/SEI + LNMO positive) ---
A1 = {
    "Separator thickness [m]": 1e-05,
    "Negative electrode thickness [m]": 1e-04,
    "Positive electrode porosity": 0.28,
    "Positive electrode active material volume fraction": 0.72,
}
A2 = dict(A1)
A2.update({
    "Electrolyte conductivity [S.m-1]": 1.6,
    "Cation transference number": 0.4,
})
A3 = dict(A2)
A3.update({
    "Positive particle radius [m]": 2e-07,
    "Negative particle radius [m]": 5e-07,
})
A4 = dict(A3)
A4.update({
    "Total heat transfer coefficient [W.m-2.K-1]": 150.0,
    "SEI kinetic rate constant [m.s-1]": 1e-13,
    "SEI reaction exchange current density [A.m-2]": 1.5e-08,
})

cands = [
    ("A1_anode_rebalance", A1),
    ("A2_plus_electrolyte", A2),
    ("A3_plus_nanoparticles", A3),
    ("A4_plus_coating_cooling", A4),
]

propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "name": "A1_anode_rebalance",
            "base": LNMO_BASE,
            "struct": A1,
            "role": (
                "architecture rebalance: thinner separator (25->10 um) cuts ionic resistance; thicker anode "
                "(85->100 um) raises anode areal capacity 5.66->6.66 mAh/cm2 -> discharge delivers ~5.9-6.0 mAh/cm2 "
                "(anode-surface-depletion cliff at 2.5 V limits baseline to 4.98) -> ED and plateau margin up; "
                "cathode porosity 0.25->0.28 (AM 0.75->0.72) for 4C electrolyte transport"
            ),
        },
        {
            "name": "A2_plus_electrolyte",
            "base": LNMO_BASE,
            "struct": A2,
            "role": (
                "electrolyte formulation on A1: sigma 1.6 S/m (baseline Nyman2008 function gives 0.949 S/m at "
                "c=1000, temperature-independent -> scalar override is the formulation lever) with cation "
                "transference number kept at 0.4 (Chen2020 baseline value; the A-series therefore isolates the "
                "conductivity effect). Lowers ohmic drop and anode-interface electrolyte potential rise at 18 A "
                "-> plating margin and heat"
            ),
        },
        {
            "name": "A3_plus_nanoparticles",
            "base": LNMO_BASE,
            "struct": A3,
            "role": (
                "nano electrodes on A2: cathode particle radius 5.22->0.2 um (LNMO nano-spinel, literature "
                "50-200 nm particles; solid diffusivity fixed at Chen2020 4e-15 m2/s - LNMO.json 1e-12 override is "
                "dead under PyBaMM 26.7 key rename, forbidden lever anyway -> radius is the sanctioned diffusion "
                "lever) -> cathode surface sto excursion at 18 A shrinks ~26x -> OCP stays on 4.4-4.53 V plateau "
                "instead of spiking to 4.66-4.70 V -> 4C charge sustains instead of dying in seconds. "
                "Anode radius 5.86->0.5 um -> surface overshoot ~0.17 (vs ~1.9) -> anode surface sto at 4C charge "
                "end ~0.73-0.84, OCP ~0.10-0.14 V -> surface potential stays positive (no plating)"
            ),
        },
        {
            "name": "A4_plus_coating_cooling",
            "base": LNMO_BASE,
            "struct": A4,
            "role": (
                "SEI suppression + thermal management on A3: k_SEI 1e-12 -> 1e-13 (x0.1, Al2O3 ALD coating) and "
                "SEI exchange current density 1.5e-7 -> 1.5e-8 (x0.1, coating suppresses SEI growth). "
                "Total heat transfer coefficient 10 -> 150 W/m2K (lumped cooling area ~0.005 m2 -> hA "
                "0.05 -> 0.75 W/K; 4C charge heat est. 2.5-3.5 W -> deltaT ~3.5-4.7 K above 45 C ambient; "
                "vapor-chamber/heat-spreader phone-class cooling estimate)"
            ),
        },
    ],
    "llm_reason": (
        "Bridge listing (all overrides vs LNMO.json base; every key verified live in PyBaMM 26.7 model):\n"
        "  Separator thickness [m] 25e-6 -> 1e-5 (thin ceramic-coated separator, domain experience: 10-16 um "
        "high-power separators; ionic resistance cut)\n"
        "  Negative electrode thickness [m] 85e-6 -> 1e-4 (thicker anode rebalance; baseline discharge is "
        "anode-limited - measured 4.976 mAh/cm2 of 5.66 available; thicker anode -> ~5.9+ mAh/cm2 -> ED > 1100)\n"
        "  Positive electrode porosity 0.25 -> 0.28 and Positive electrode active material volume fraction "
        "0.75 -> 0.72 (sum=1 conserved; +transport for 18 A charge)\n"
        "  Electrolyte conductivity [S.m-1] 0.949 -> 1.6 (scalar replaces Nyman2008 function, optimized "
        "high-conductivity carbonate blend, +68%; ref: design_plan.md electrolyte formulation)\n"
        "  Cation transference number 0.4 (baseline 0.4 -> asserted formulation control; no change) -> NOT in "
        "A2..A4 structs, recorded here for trace\n"
        "  Positive particle radius [m] 5.22e-6 -> 2e-7 (nano-LNMO; Santhanam & Rambabu J. Power Sources 195 "
        "(2010) 5442 nano-spinel synthesis; solid diffusivity NOT overridden - forbidden lever)\n"
        "  Negative particle radius [m] 5.86e-6 -> 5e-7 (nano-graphite, high-power anode)\n"
        "  Total heat transfer coefficient [W.m-2.K-1] 10 -> 150 (vapor chamber + spreader; hA = 0.75 W/K)\n"
        "  SEI kinetic rate constant [m.s-1] 1e-12 -> 1e-13 (Al2O3 ALD coating x0.1)\n"
        "  SEI reaction exchange current density [A.m-2] 1.5e-7 -> 1.5e-8 (x0.1; note: may be inert under "
        "ec-reaction-limited SEI model - run will show)\n"
        "R1 baseline: ED 1005 PASS, midpoint 4.166 PASS, 4C charge dead in ~6 s (cathode surface OCP spike, "
        "D=4e-15 dead override), T_max 328.86 FAIL, plated FAIL (-0.176 V), SEI 753 nm FAIL. "
        "R2 mechanism-informed ladder: A1 = architecture (ED+ionic), A2 = +electrolyte (plating+heat), "
        "A3 = +nano electrodes (4C acceptance: cathode surface stays off the 4.66-4.70 V ramp; anode surface "
        "overshoot 0.17 -> no saturation -> no plating), A4 = +coating (SEI) + cooling (T_max). "
        "All four simulated on 1C_discharge spme + calc-energy + 4C_charge_45C spme/lumped/plating + "
        "aging_1C_100cyc spme; batch log-evaluate round 2."
    ),
}

append_entry(ws, propose)
print("propose round 2 appended")

for name, params in cands:
    p = CELL / f"r2_{name}.json"
    p.write_text(json.dumps(params, indent=2), encoding="utf-8")
    print("wrote", p.name, "->", len(params), "keys")
