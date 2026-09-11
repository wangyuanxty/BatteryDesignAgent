import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("portability/t6_oa", "runs")

propose = {
    "action": "propose",
    "round": 1,
    "candidates": [
        {
            "base": ".claude/skills/virtual-battery-factory/scripts/bda/simulators/data/LNMO.json",
            "name": "LNMO",
            "role": "high-voltage spinel cathode (4.7V class) baseline system to meet plateau>=4.1V",
        }
    ],
    "llm_reason": (
        "Task plateau>=4.1V forces a high-voltage cathode: NMC811 cell midpoint~3.61V cannot meet it. "
        "LNMO (LiNi0.5Mn1.5O4) spinel is the matching system (4.7V class OCP, cell midpoint~4.17V). "
        "Round 1 = baseline characterization of LNMO to measure the gap to each threshold "
        "(volumetric ED, plateau, T_max@4C, plating, SEI after 100cyc) before proposing architecture variants."
    ),
}

funnel = {
    "action": "funnel",
    "passed": 1,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "System candidate (LNMO) skips molecular screening (ML potentials/xtb are unreliable for full "
        "electrode systems); goes directly to Stage 3 cell simulation. Chosen base = LNMO.json "
        "(4.7V-class spinel positive-electrode override over Chen2020 base). Matching basis (anchor table): "
        "task plateau>=4.1V + smartphone high-voltage -> LNMO high-voltage cathode/spinel; "
        "discriminant anchor verified: Positive electrode OCP [V] = lnmo_ocp (4.7V class), molar mass 0.1503 kg/mol, "
        "Nominal cell capacity 4.5 Ah. props source: baseline (Chen2020 negative/electrolyte/SEI inherited)."
    ),
}

append_entry(ws, propose)
append_entry(ws, funnel)
print("propose+funnel entries written")
