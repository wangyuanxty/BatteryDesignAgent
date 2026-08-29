"""Propose round 3 + params files: cooling x anode-margin intersection variants."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

import pybamm

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)

V1 = {
    "Negative current collector thickness [m]": 8e-6,
    "Positive current collector thickness [m]": 10e-6,
    "Separator thickness [m]": 9e-6,
}
TRANSPORT = {
    "Electrolyte conductivity [S.m-1]": 2.0,
    "Electrolyte diffusivity [m2.s-1]": 6e-10,
    "Cation transference number": 0.4,
}
V4 = dict(V1); V4.update(TRANSPORT)
V4["Positive particle radius [m]"] = 1.5e-6
V4["Negative particle radius [m]"] = 2.5e-6

V8 = dict(V4)
V8["Total heat transfer coefficient [W.m-2.K-1]"] = 60.0   # forced-air ducted cooling
V8["Negative particle radius [m]"] = 1.5e-6                # rebuild anode kinetics at low T

V9 = dict(V4)
V9["Total heat transfer coefficient [W.m-2.K-1]"] = 60.0
V9["Negative electrode thickness [m]"] = 100e-6            # anode capacity margin -> shallower end-of-charge anode

V10 = dict(V4)
V10["Total heat transfer coefficient [W.m-2.K-1]"] = 40.0  # mid cooling: probe trade-off curve
V10["Negative particle radius [m]"] = 1.5e-6

V11 = dict(V4)
V11["Total heat transfer coefficient [W.m-2.K-1]"] = 60.0
V11["Negative particle radius [m]"] = 1.5e-6
V11["Negative electrode thickness [m]"] = 100e-6           # both anode margins combined

# --- pre-verify expected stack mass against the 40 g cap (same formula as calc-energy) ---
pv = pybamm.ParameterValues("Chen2020")
H = float(pv["Electrode height [m]"])
W = float(pv["Electrode width [m]"])

def stack_mass_g(struct):
    p = pv.copy()
    for k, v in struct.items():
        p.update({k: v}, check_already_exists=False)
    area = float(p["Electrode width [m]"]) * float(p["Electrode height [m]"])
    layers = [
        (float(p["Negative current collector thickness [m]"]), 0.0, float(pv["Negative current collector density [kg.m-3]"])),
        (float(p["Separator thickness [m]"]), 0.0, float(pv["Separator density [kg.m-3]"])),
        (float(p["Positive current collector thickness [m]"]), 0.0, float(pv["Positive current collector density [kg.m-3]"])),
        (float(p["Positive electrode thickness [m]"]), float(pv["Positive electrode porosity"]), float(pv["Positive electrode density [kg.m-3]"])),
        (float(p["Negative electrode thickness [m]"]), float(pv["Negative electrode porosity"]), float(pv["Negative electrode density [kg.m-3]"])),
    ]
    return sum(t * (1 - por) * rho * area for t, por, rho in layers) * 1000.0

cands = {
    "V8 cooled_anodefast": V8,
    "V9 cooled_thickneg": V9,
    "V10 midcool_anodefast": V10,
    "V11 cooled_bigmargin": V11,
}
for name, struct in cands.items():
    m = stack_mass_g(struct)
    print(f"{name}: expected stack mass = {m:.2f} g {'OK' if m <= 40 else 'OVER'}")
    p = Path("runs/exp/t8_r3/cell") / f"params_r3_{name.replace(' ', '_')}.json"
    p.write_text(json.dumps(struct, indent=2), encoding="utf-8")

propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {"struct": V8, "name": "V8 cooled_anodefast",
         "role": "V4 + h=60 W/m2K forced-air cooling (=V7, T_max 328.5 K pass) + negative particle 2.5->1.5 um: rebuild anode surface kinetics at the lower operating temperature that lost 22 mV of anode margin in V7 (anode_min +0.0126 -> -0.0102 V)"},
        {"struct": V9, "name": "V9 cooled_thickneg",
         "role": "V4 + h=60 + negative electrode 85.2->100 um (N/P ratio up ~17%): shallower end-of-charge anode lithiation keeps anode potential positive during 4C/45C charge; capacity stays cathode-limited"},
        {"struct": V10, "name": "V10 midcool_anodefast",
         "role": "probe on the trade-off curve: h=40 W/m2K (thermal-lumped estimate T_max ~332 K, just under 333.15) + negative particle 1.5 um; tests whether less cooling preserves enough anode margin without the full h=60"},
        {"struct": V11, "name": "V11 cooled_bigmargin",
         "role": "kitchen sink: V4 + h=60 + negative particle 1.5 um + negative 100 um - combines kinetic-area margin and capacity margin at full cooling"},
    ],
    "llm_reason": (
        "Round 2 (corrected mechanical evaluation): rate problem SOLVED - positive/negative particle "
        "downsizing + high-transport electrolyte move 5C retention 8.7% -> 98.0% (V4: 0.9805, V6: 0.9808); "
        "ED 454-501 Wh/kg and mass 38.0-39.5 g all pass Stage 2. Remaining frontier is Stage 3 safety: "
        "4C/45C charge thermal-plating intersection. V4/V5/V6 (h=10) show T_max 352.5/354.0/356.4 K > 333.15 K; "
        "V7 (h=60) cools to 328.5 K (pass) but the colder cell slows anode kinetics and plates "
        "(anode_min -0.0102 V). Round 3 strikes the intersection from the anode side at full or mid cooling: "
        "negative particle 1.5 um (surface-area/kinetics, same architecture lever family as Round 2), negative "
        "electrode 100 um (loading/N-P capacity margin), combined in V11; V10 maps the h-T curve midpoint. "
        "All material keys identical to V4 (which passed rate+energy+mass); all values are architecture/design "
        "levers per the SKILL.md mapping (particle size architecture, electrode thickness loading, heat "
        "transfer coefficient = thermal management system design); expected stack masses pre-verified "
        "in-script against the calc-energy layer formula (printed above, must be <= 40 g)."
    ),
}
append_entry(ws, propose)
print("propose round 3 appended")