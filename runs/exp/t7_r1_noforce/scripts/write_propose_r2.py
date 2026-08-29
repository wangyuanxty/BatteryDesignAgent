"""Write Round 2 propose entry."""
import json
from pathlib import Path
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
}
propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": struct,
            "name": "Probe A + Liquid Cooling h100",
            "role": "Ceiling Probe A architecture + high-transport electrolyte + active liquid cooling (h=100 W/m2/K) to pass the 10 W nail test without thermal runaway",
        }
    ],
    "llm_reason": (
        "R1 mechanical verdicts: Probe A passes ED (486.38)/SEI (507.94)/plating (+25.4 mV), fails ONLY the nail "
        "criterion (triggered at 72.0 s under near-adiabatic hA=0.05 W/K). Symptom-to-scale: heat dissipation -> "
        "thermal management freedom (Total heat transfer coefficient), a Stage 3 lever, not a material cause. "
        "h=100 W/m2/K = liquid-cooling-plate value, automotive HEV standard (domain estimate). "
        "run-tr coupling (mechanical): hA = h x Cell cooling surface area 0.00531 m2 (Chen2020) = 0.531 W/K "
        "- same cooling-area convention as the cell lumped thermal model; t_init = candidate's own 4C_charge_45C "
        "T_max_K (entry-0 pre-registration); mass-kg = candidate's calc-energy mass_kg. "
        "4C charge re-simulated because cooler operation lowers electrolyte transport - plating margin must be "
        "re-verified (risk: Probe A's +25.4 mV margin may shrink)."
    ),
}
append_entry(ws, propose)
print("propose R2 appended; entries:", len((ws.path / "log.jsonl").read_text(encoding="utf-8").strip().splitlines()))
# also write the params file for the run
out = (ws.path / "cell" / "params_r2_cool1.json")
out.write_text(json.dumps(struct, indent=2), encoding="utf-8")
print("params_r2_cool1.json written")
