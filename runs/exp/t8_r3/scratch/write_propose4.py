"""Propose round 4 + params files: anode-margin confirmation on the V8 winner."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)

with open("runs/exp/t8_r3/cell/params_r3_V8_cooled_anodefast.json", encoding="utf-8") as f:
    V8 = json.load(f)

V12 = dict(V8)
V12["Negative particle radius [m]"] = 1.2e-6   # extra anode surface margin (fine graphite grade)

V13 = dict(V8)
V13["Negative electrode porosity"] = 0.30       # relax anode coating density -> electrolyte transport/margin

cands = {"V12 cooled_anodefast2": V12, "V13 porousanode": V13}
for name, struct in cands.items():
    p = Path("runs/exp/t8_r3/cell") / f"params_r4_{name.replace(' ', '_')}.json"
    p.write_text(json.dumps(struct, indent=2), encoding="utf-8")

propose = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {"struct": V12, "name": "V12 cooled_anodefast2",
         "role": "V8 winner + negative particle 1.5->1.2 um: widen the thinnest remaining margin (anode_min +7.3 mV at 4C/45C) via extra anode surface area at the same h=60 cooling"},
        {"struct": V13, "name": "V13 porousanode",
         "role": "V8 winner + negative electrode porosity 0.25->0.30: relax anode coating density to cut anode-side electrolyte polarization at end of 4C charge (transport margin route instead of particle route)"},
    ],
    "llm_reason": (
        "Round 3 mechanical evaluation: V8 (h=60, neg particle 1.5 um) and V10 (h=40, neg particle 1.5 um) "
        "PASS all five entry-0 criteria; V9/V11 (negative 100 um, both h=60) fail plating - the capacity-margin "
        "route through a thicker negative electrode is empirically a plating liability at 4C/45C in this system "
        "(electrolyte polarization through the thicker anode overrides the shallower end-of-charge state), and "
        "the particle-size route (V7->V8: -10.2 -> +7.3 mV) is the effective anode-margin lever. Round 4 confirms "
        "the winner branch and widens its thinnest margin (V8 anode_min +7.3 mV): V12 pushes the same lever "
        "further (1.2 um fine graphite, architecture freedom), V13 tests a coating-density route (negative "
        "porosity 0.30, architecture freedom) that also drops stack mass. Thermal stays h=60 forced-air (V8 "
        "T_max 327.27 K, 5.9 K margin). V10 remains the fallback pick with its +10.7 mV anode margin (2.1 K "
        "thermal margin). This is the confirmation round; winner => Stage 4 abuse check => closing."
    ),
}
append_entry(ws, propose)
print("propose round 4 appended")