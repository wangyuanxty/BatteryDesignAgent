import json, sys
sys.path.insert(0, ".")
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t2_r1_mimo", "runs/exp/t2_r1_mimo")

# Round 2 propose
propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"name": "Variant A (thin electrodes)", "role": "Reduce electrode thickness to lower transport resistance"},
        {"name": "Variant B (thin + high porosity + small particles)", "role": "Aggressive rate-capable architecture"},
        {"name": "Variant C (thin optimal)", "role": "Maximum rate optimization"},
        {"name": "Variant D (thin + high N/P)", "role": "Thin electrodes with 1.5x N/P ratio"},
        {"name": "Variant E (moderate + high N/P)", "role": "Moderate thickness with 1.5x N/P ratio"},
    ],
    "llm_reason": "Architecture exploration: all5 variants fail plating (min anode V ranges -0.039 to -0.439). Variants B/C/D closest to no-plating (min V ~-0.04 to -0.05). ED trade-off: thinner electrodes reduce ED. Chen2020 electrolyte transport is the bottleneck for 4C plating."
}
append_entry(ws, propose)

# Round 2 evaluate (batch for all5 variants)
eval_entry = {
    "action": "evaluate",
    "round": 2,
    "metrics": {
        "A": {"ed": 324.63, "plated": True, "min_v": -0.422, "tmax": 330.5},
        "B": {"ed": 318.29, "plated": True, "min_v": -0.049, "tmax": 350.2, "sei_100": 355.3, "sei_500": 613.5},
        "C": {"ed": 297.07, "plated": True, "min_v": -0.039, "tmax": 349.5},
        "D": {"ed": 377.52, "plated": True, "min_v": -0.048, "tmax": 360.1, "sei_100": 442.4, "sei_500": 796.6},
        "E": {"ed": 419.70, "plated": True, "min_v": -0.082, "tmax": 373.8},
    },
    "comparison": [
        {"name": "Variant A", "metrics": {"ed": 324.63, "plated": True, "min_v": -0.422}, "verdict": "fail"},
        {"name": "Variant B", "metrics": {"ed": 318.29, "plated": True, "min_v": -0.049, "sei_100": 355.3, "sei_500": 613.5}, "verdict": "fail"},
        {"name": "Variant C", "metrics": {"ed": 297.07, "plated": True, "min_v": -0.039}, "verdict": "fail"},
        {"name": "Variant D", "metrics": {"ed": 377.52, "plated": True, "min_v": -0.048, "sei_100": 442.4, "sei_500": 796.6}, "verdict": "fail"},
        {"name": "Variant E", "metrics": {"ed": 419.70, "plated": True, "min_v": -0.082}, "verdict": "fail"},
    ],
    "verdict": "fail",
    "note": "All architecture variants fail plating. B/C/D closest to no-plating (~-0.04V). SEI@500 also fails for tested variants (B:614nm, D:797nm). Material-property bottleneck identified: electrolyte transport and SEI kinetics.",
    "candidate": "architecture variants A-E"
}
append_entry(ws, eval_entry)

# Plan update
plan_update = {
    "action": "plan",
    "update": True,
    "reason": "Three-strike on architecture: all5 variants fail plating despite reducing electrode thickness. Root cause is electrolyte transport limitation in Chen2020 baseline. SEI@500 also fails (material limitation). Escalating to electrolyte formulation (sigma, D) and SEI modification.",
    "candidate_strategy": "R3: electrolyte transport enhancement variants (increased sigma, D). R4: SEI suppression candidates. R5: combined optimization.",
    "budget_allocation": "Remaining ~10 rounds: 4 electrolyte, 3 SEI, 3 combined"
}
append_entry(ws, plan_update)

print("Round 2 entries and plan update written")
