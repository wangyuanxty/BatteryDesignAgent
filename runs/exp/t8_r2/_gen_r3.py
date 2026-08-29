# -*- coding: utf-8 -*-
"""Generate R3 params from V_D (mechanical) + propose entry."""
import json

from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t8_r2", "runs/exp")
cell = ws.path / "cell"

base = json.load(open(cell / "params_r2_VD.json", encoding="utf-8"))
Lp = base["Positive electrode thickness [m]"]  # 60 um
Ln = base["Negative electrode thickness [m]"]  # 67.6 um
W = base["Electrode width [m]"]  # 1.9908 m

VE = dict(base)
VE["Positive particle radius [m]"] = 3.0e-6
VE["Negative particle radius [m]"] = 3.5e-6

VF = dict(VE)
VF["Positive electrode thickness [m]"] = 50.0e-6
VF["Negative electrode thickness [m]"] = Ln * 50.0e-6 / Lp
VF["Electrode width [m]"] = W * Lp / 50.0e-6  # area-scaled: capacity preserved

VG = dict(VE)
VG["Cation transference number"] = 0.40
VG["Electrolyte diffusivity [m2.s-1]"] = 4.2e-10

for key, struct in [("VE", VE), ("VF", VF), ("VG", VG)]:
    (cell / f"params_r3_{key}.json").write_text(json.dumps(struct, ensure_ascii=False, indent=2), encoding="utf-8")
    print(key, "written:", json.dumps(struct, ensure_ascii=False))

propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "name": "V_E smallP",
            "role": "V_D + positive particle radius 5.22->3.0 um and negative 5.86->3.5 um (microstructure lever): tau_diff 6812->2250 s, 5C surface access depth fraction 1.7um/3um=57%; primary attack on positive solid-phase surface depletion",
            "struct": VE,
        },
        {
            "name": "V_F smallP+thinPos",
            "role": "V_E + positive 50 um (area-scaled 2.389 m width to preserve 5 Ah): lower areal loading lowers 5C areal current density on top of the particle-shrink",
            "struct": VF,
        },
        {
            "name": "V_G smallP+tplus",
            "role": "V_E + t+ 0.36->0.40 and D 4.0->4.2e-10: further reduce electrolyte-side salt polarization (buffer for the 4C-charge plating exam too)",
            "struct": VG,
        },
    ],
    "llm_reason": "R2 conclusion (mechanical): retention plateau 0.722 with electrolyte depletion resolved (c_e pos 355 mol/m3); diagnosed limiter = positive solid-phase surface depletion at 5C (sep-face pos stoich 0.312 at t=515.5 s; eta_pos -0.283 V; D_s=4e-15 excluded lever, tau_diff=6812 s >> 720 s). Particle radius is the sanctioned microstructure lever for exactly this limit. V_E = attacked directly; V_F = plus loading reduction; V_G = plus electrolyte margin. All keep V_D's ED/mass gains (467 Wh/kg / 37.7 g) by construction. Full Stage-4 safety exam (4C charge 45C, lumped thermal + plating) runs for all three this round - plating is the co-objective for the fast-charge exam.",
}

append_entry(ws, propose)
print("propose R3 written")