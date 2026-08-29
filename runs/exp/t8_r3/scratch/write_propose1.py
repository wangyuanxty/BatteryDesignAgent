"""Propose entry (round 1) + candidate params files."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)

# Round 1 candidates (architecture scale, Stage 3)
C0 = {}  # baseline characterization, Chen2020 defaults
V1 = {
    "Negative current collector thickness [m]": 8e-6,   # Cu 12 -> 8 um (thin-foil grade)
    "Positive current collector thickness [m]": 10e-6,  # Al 16 -> 10 um (thin-foil grade)
    "Separator thickness [m]": 9e-6,                    # 12 -> 9 um
}
V2 = dict(V1)
V2["Positive electrode thickness [m]"] = 80.6e-6   # 75.6 -> 80.6 um (+6.6%, N/P-ratio-preserving)
V2["Negative electrode thickness [m]"] = 90.8e-6   # 85.2 -> 90.8 um (+6.6%)
V3 = dict(V1)
V3["Negative particle radius [m]"] = 4.0e-6        # 5.86 -> 4.0 um (rate margin)

cands = {
    "C0 baseline": C0,
    "V1 massfit": V1,
    "V2 activeboost": V2,
    "V3 ratemargin": V3,
}

for name, struct in cands.items():
    p = Path("runs/exp/t8_r3/cell") / f"params_r1_{name.replace(' ', '_')}.json"
    p.write_text(json.dumps(struct, indent=2), encoding="utf-8")
    print("wrote", p)

propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": C0,
            "name": "C0 baseline",
            "role": "Chen2020 NMC811/graphite baseline characterization (full-width geometry, ~43.5 g stack); anchor for every target-facing metric",
        },
        {
            "struct": V1,
            "name": "V1 massfit",
            "role": "thin inactive layers (Cu 8 um / Al 10 um / separator 9 um) at full electrode area -> stack mass ~38 g <= 40 g; dead-mass thickness overrides only, capacity untouched",
        },
        {
            "struct": V2,
            "name": "V2 activeboost",
            "role": "V1 + both electrodes +6.6% thickness (N/P ratio preserved) -> more active mass inside the 40 g budget (~39.9 g), higher 1C capacity; probes the ED side of the ED-vs-rate frontier",
        },
        {
            "struct": V3,
            "name": "V3 ratemargin",
            "role": "V1 + negative particle radius 5.86 -> 4.0 um -> better graphite kinetics at 5C discharge; probes the rate side of the frontier",
        },
    ],
    "llm_reason": (
        "Chen2020 default stack mass ~43.5 g exceeds the 40 g cap, so Round 1 must re-partition mass. "
        "V1 thins only dead layers (collectors/separator) to <=40 g at full area and nominal 5 Ah class. "
        "V2 probes thicker electrodes (more 1C energy) inside the same mass cap; V3 probes rate capability "
        "via smaller negative particles. All parameter keys verified present in Chen2020 (dump). "
        "All overrides listed before running; sources: thin-foil/small-particle values are design "
        "choices from commercial practice (domain experience), recorded as architecture design parameters."
    ),
}
append_entry(ws, propose)
print("propose entry appended")