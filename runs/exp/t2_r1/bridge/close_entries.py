"""Closing entries: endorse (honest skip) + final (verdict achieved)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (case default, task originator did not request true compute). Additionally this case "
        "started at stage 3 (start_stage=3: task names no new materials, baseline Chen2020 chemistry) so no "
        "molecular-scale candidates were generated in the funnel and there is no Top-N to endorse at the molecular "
        "level; the design levers used (electrolyte transport constants, particle radii, porosity, SEI kinetic "
        "rate constant) are cell-scale parameter representations. No DFT/MD values are fabricated; Stage 5 true "
        "compute remains as future work if the originator enables real_compute."
    ),
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "GridStore-D3: Chen2020 NMC811/graphite baseline with neg r 2.0 um, pos r 2.5 um, constant electrolyte "
        "transport (sigma 3.0 S/m, D 2.5e-9 m2/s, t+ 0.35), neg/pos porosity 0.40/0.40, SEI kinetic rate constant "
        "1e-16 m/s. All five contracts pass with margin: ED 465.62 Wh/kg >= 327.18; 4C charge plating-free "
        "(anode potential min +0.0498 V); SEI 9.087 nm @100cyc <= 500 and 25.317 nm @500cyc <= 550; -20 C "
        "discharge retention 99.571% >= 90% (protocol 99.571%, true-soak probe 99.571% at 266.7 K cell temperature)."
    ),
    "evidence": [
        {"metric": "energy_density_wh_kg", "value": 465.622, "threshold": {"min": 327.18},
         "source": "cell/r6_d3_energy.json:energy_density_wh_kg", "sourced": True},
        {"metric": "plated", "value": False, "threshold": False,
         "source": "cell/r6_d3_4c.json:anode_potential_v (min=+0.049796 V >= 0, derived)", "sourced": True},
        {"metric": "sei_100cyc_nm", "value": 9.087, "threshold": {"max": 500.0},
         "source": "cell/r6_d3_sei100.json:sei_100cyc_nm (bridge of cell/r6_d3_aging100.json:sei_thickness_nm_end)", "sourced": True},
        {"metric": "sei_500cyc_nm", "value": 25.317, "threshold": {"max": 550.0},
         "source": "cell/r6_d3_sei500.json:sei_500cyc_nm (bridge of cell/r6_d3_aging500.json:sei_thickness_nm_end)", "sourced": True},
        {"metric": "lowT_retention_pct", "value": 99.571, "threshold": {"min": 90.0},
         "source": "cell/r6_d3_lowT_ret.json:lowT_retention_pct (100 x 5.04452/5.06626 Ah; true-soak probe 5.04452 Ah, T_max 266.71 K)", "inferred": "mechanical: 100*capa_lowT/capa_1C"},
    ],
    "note": (
        "Pre-closing self-check (7 failure modes) all clear: no simulation failure repackaged; every value read from "
        "tool output on disk; unfavorable conditions tested (true -20 C soak, 45 C 4C charge, 500-cycle aging); "
        "known artifacts labeled as artifacts (aging per-cycle-capacity variable freezes at first-discharge value "
        "while real steps are full 1C swings - probe-grounded; calc-energy midpoint/DCR are solver-step-density "
        "index artifacts; part of the porosity ED gain is contract-caliber since electrolyte mass is excluded); "
        "entry-0 thresholds untouched; units mechanically converted; final design changed across R3->R6 driven by "
        "data. Endorsement skipped honestly (real_compute=false). Rounds R1-R6 each carry propose+evaluate pairs."
    ),
}
append_entry(ws, final)
print("endorse + final appended")
