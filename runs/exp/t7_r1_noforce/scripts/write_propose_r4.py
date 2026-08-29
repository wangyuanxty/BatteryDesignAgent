"""Write Round 4 propose entry + params file."""
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
    "Negative electrode thickness [m]": 9.5e-05,
    "SEI kinetic rate constant [m.s-1]": 7.5e-13,
}
propose = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "struct": struct,
            "name": "R3 + Al2O3 ALD Negative Coating + N/P 1.35",
            "role": "margin round: Al2O3 ALD coating on graphite (SEI kinetic rate constant x0.75) widens SEI margin; negative 95 um (N/P ~1.35) widens 4C anode-potential margin",
        }
    ],
    "llm_reason": (
        "R3 passes all four criteria mechanically (verdict=pass) but with thin margins: SEI 547.58 nm vs 550 "
        "(+2.4 nm) and anode min +0.0126 V (+12.6 mV). For a deliverable design these margins are fragile "
        "(simulation/process variability), so one margin round with two monotone levers: "
        "(1) Electrode modification (Stage 2 candidate type, judged in Stage 3 aging): Al2O3 ALD coating on graphite "
        "- inorganic ionic solid, molecular funnel SKIPPED per protocol (ML potentials unreliable on charged/ionic "
        "solids); bridge value SEI kinetic rate constant 1e-12 -> 7.5e-13 m/s (x0.75) marked ESTIMATE "
        "(literature: ALD Al2O3 passivation suppresses SEI growth ~25%+, domain experience); "
        "(2) N/P 1.29 -> ~1.35 (negative 95 um): shallower end-of-charge lithiation -> higher anode potential; "
        "ED cost ~1% (still >> 327.18); SEI max-thickness growth is separator-interface dominated, expected "
        "~unchanged - aging re-simulated to confirm. SEI coating comparison stays on the SAME system (Chen2020). "
        "Nail coupling: hA=0.531 W/K, t_init = candidate's own 4C T_max_K, mass from candidate calc-energy."
    ),
}
append_entry(ws, propose)
(ws.path / "cell" / "params_r4_margin.json").write_text(json.dumps(struct, indent=2), encoding="utf-8")
print("propose R4 appended; params_r4_margin.json written")
