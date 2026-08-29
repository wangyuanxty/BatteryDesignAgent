"""Write Round 3 propose entry + params file."""
import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t7_r1_noforce", "D:/research/degradation_prognostics/Battery_Design_Agent/runs")
struct = {
    "Positive current collector thickness [m]": 1.0e-05,
    "Negative current collector thickness [m]": 6.0e-06,
    "Separator thickness [m]": 1.0e-05,
    "Electrolyte conductivity [S.m-1]": 2.5,
    "Electrolyte diffusivity [m2.s-1]": 5.0e-10,
    "Cation transference number": 0.5,
    "Total heat transfer coefficient [W.m-2.K-1]": 100.0,
    "Negative particle radius [m]": 4.0e-06,
    "Negative electrode thickness [m]": 9.2e-05,
}
propose = {
    "action": "propose",
    "round": 3,
    "candidates": [
        {
            "struct": struct,
            "name": "Cooled h100 + Rate-Ready Anode",
            "role": "recover 4C anode-potential margin under liquid cooling: smaller graphite particles (5.86->4.0 um, solid-diffusion polarization ~-2.1x) + thicker negative (85.2->92 um, N/P 1.19->1.29, shallower end-of-charge lithiation)",
        }
    ],
    "llm_reason": (
        "R2 mechanical verdict: only plating fails (anode min -0.008 V, plated=true). Symptom-to-scale: anode "
        "polarization at 4C under cooler operation = architecture/electrode-structure cause -> Stage 3 fallback. "
        "Two rate-capability levers, both standard fast-charge design practice: (1) particle radius 4.0 um cuts "
        "solid-diffusion time constant by ~2.1x (r^2 scaling; smaller-particle rate benefit = domain experience, "
        "skill-measured T1 precedent +14.6%); (2) negative thickness 92 um raises N/P 1.19->1.29 so end-of-charge "
        "lithiation is shallower (graphite OCP drops steeply near full lithiation). Costs: neg mass +8% -> ED "
        "484->~473 Wh/kg (still >> 327.18); SEI risk: smaller particles increase specific surface area -> SEI "
        "growth may rise (aging re-simulated; if sei > 550 nm, next lever = SEI kinetic rate constant via "
        "negative coating, same-system comparison). Nail coupling unchanged (hA=0.531 W/K, t_init = candidate's "
        "own 4C T_max_K, mass from candidate calc-energy)."
    ),
}
append_entry(ws, propose)
(ws.path / "cell" / "params_r3_anode.json").write_text(json.dumps(struct, indent=2), encoding="utf-8")
print("propose R3 appended; params_r3_anode.json written")
