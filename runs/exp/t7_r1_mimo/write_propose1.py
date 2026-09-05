"""Write propose entry for Round 1 architecture variants."""
import os, sys, json
os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent")
from bda.store import append_entry, CaseWorkspace

ws = CaseWorkspace("t7_r1_mimo", "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")

# Architecture variants targeting 4C plating reduction
# Key insight: reduce electrode thickness + increase porosity to improve Li+ transport
# Also try thinner separator and optimized particle size
propose_entry = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "struct": {
                "Positive electrode thickness [m]": 70e-6,
                "Negative electrode thickness [m]": 75e-6
            },
            "name": "Variant B - Thinner electrodes",
            "role": "Reduce electrode thickness by ~30% to improve Li+ transport and reduce plating risk at 4C; trade-off: lower ED"
        },
        {
            "struct": {
                "Positive electrode porosity": 0.35,
                "Negative electrode porosity": 0.35,
                "Separator porosity": 0.55
            },
            "name": "Variant C - Higher porosity",
            "role": "Increase electrode porosity from default to 0.35 and separator to 0.55 for better electrolyte transport at 4C; trade-off: lower active material fraction"
        },
        {
            "struct": {
                "Separator thickness [m]": 12e-6,
                "Positive particle radius [m]": 3.5e-6,
                "Negative particle radius [m]": 3.5e-6
            },
            "name": "Variant D - Thin separator + small particles",
            "role": "Thinner separator reduces resistance and inactive mass; smaller particles reduce diffusion path length for better rate capability"
        },
        {
            "struct": {
                "Positive electrode thickness [m]": 80e-6,
                "Negative electrode thickness [m]": 85e-6,
                "Positive electrode porosity": 0.33,
                "Negative electrode porosity": 0.33,
                "Positive particle radius [m]": 3.5e-6,
                "Negative particle radius [m]": 5e-6
            },
            "name": "Variant E - Balanced moderate",
            "role": "Moderate thickness reduction + slightly higher porosity + smaller positive particles; balance ED and rate capability"
        }
    ],
    "llm_reason": "Baseline shows ED=400 Wh/kg (exceeds target) but 4C plating occurs (anode_potential_v min=-0.438V). Primary failure mode is Li+ transport limitation at 4C. Architecture levers: (1) thinner electrodes reduce transport distance, (2) higher porosity improves electrolyte diffusivity, (3) smaller particles reduce solid-state diffusion, (4) thinner separator reduces total resistance. Four variants exploring these directions systematically."
}

append_entry(ws, propose_entry)
print("Propose entry written for Round 1")
