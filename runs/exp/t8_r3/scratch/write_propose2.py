"""Propose round 2 + params files: rate-transport variants."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r".claude\skills\virtual-battery-factory\scripts")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t8_r3", root="runs", create=False)

V1 = {
    "Negative current collector thickness [m]": 8e-6,
    "Positive current collector thickness [m]": 10e-6,
    "Separator thickness [m]": 9e-6,
}
TRANSPORT = {
    "Electrolyte conductivity [S.m-1]": 2.0,      # estimate: formulated high-conductivity carbonate blend
    "Electrolyte diffusivity [m2.s-1]": 6e-10,    # estimate: low-viscosity dilute-solvent formulation
    "Cation transference number": 0.4,            # estimate: low-solvating LiFSI-based pair blend
}
V4 = dict(V1); V4.update(TRANSPORT)
V4["Positive particle radius [m]"] = 1.5e-6      # 5.22 -> 1.5 um single-crystal NMC
V4["Negative particle radius [m]"] = 2.5e-6      # 5.86 -> 2.5 um fine synthetic graphite

V5 = dict(V4)
V5["Positive electrode thickness [m]"] = 90e-6   # 75.6 -> 90 um (lower per-particle cathode flux)
V5["Electrode width [m]"] = 1.509                # mass fit <= 40 g

V6 = dict(V4)
V6["Positive electrode thickness [m]"] = 85.5e-6
V6["Negative electrode thickness [m]"] = 96.3e-6  # balanced loading, N/P ratio preserved
V6["Electrode width [m]"] = 1.498                 # mass fit <= 40 g

V7 = dict(V4)
V7["Total heat transfer coefficient [W.m-2.K-1]"] = 60.0  # propwash forced-air cooling design

cands = {"V4 ratemax": V4, "V5 thickcathode": V5, "V6 thickboth": V6, "V7 ratemax+cooling": V7}
for name, struct in cands.items():
    p = Path("runs/exp/t8_r3/cell") / f"params_r2_{name.replace(' ', '_')}.json"
    p.write_text(json.dumps(struct, indent=2), encoding="utf-8")
    print("wrote", p)

propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"struct": V4, "name": "V4 ratemax",
         "role": "rate-bottleneck fix: cathode/anode particle downsizing (a_s up, solid-diffusion path down) + high-transport electrolyte formulation (kappa 2.0 S/m, D 6e-10, t+ 0.4) on V1 mass base"},
        {"struct": V5, "name": "V5 thickcathode",
         "role": "V4 + positive electrode 75.6->90 um: lower per-particle cathode surface flux at 5C (diagnosed saturation), width shrunk to keep mass <=40 g"},
        {"struct": V6, "name": "V6 thickboth",
         "role": "V4 + both electrodes scaled (85.5/96.3 um, N/P preserved): more active mass at equal 40 g, checks whether thicker loading survives 5C after particle fix"},
        {"struct": V7, "name": "V7 ratemax+cooling",
         "role": "V4 + cooling coefficient h 10->60 W/m2K (propwash forced-air pack design): targets the 4C/45C T_max failure seen at baseline (354 K vs 333.15 K cap)"},
    ],
    "llm_reason": (
        "Round-1 diagnosis (scratch/diag_physics.py, direct DFN solve): at 5C discharge the positive particle "
        "surface concentration saturates (63081 of 63104 mol/m3 at 62 s, ~96% of c_max) while the negative stays "
        "mid-range; t=0 terminal voltage already sags 4.2->3.821 V (kinetics+ohmic). Bottleneck scale = positive "
        "solid-phase surface kinetics/diffusion area -> architecture lever is particle size (a_s = 3*eps_s/R), "
        "plus electrolyte transport for the ohmic/kinetic floor. Solid-phase diffusivity itself is a forbidden "
        "lever (no formulation mapping), so the allowed fix is surface-area via smaller particles + thinner-formulation "
        "transport. Parameter list (all keys tool-verified in Chen2020): Positive/Negative particle radius [m] "
        "(architecture, commercial nano/single-crystal NMC & fine synthetic graphite practice - domain estimate); "
        "Electrolyte conductivity 2.0 S/m, diffusivity 6e-10 m2/s, t+ 0.4 (formulation estimates marked estimate, "
        "not simulation output); collector/separator thicknesses as Round 1; Electrode width shrink = pure mass-fit "
        "arithmetic; h=60 W/m2K = forced-convection cooling design choice for the V7 thermal variant."
    ),
}
append_entry(ws, propose)
print("propose round 2 appended")