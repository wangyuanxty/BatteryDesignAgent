"""t4_r3: closing log entries — endorse (honest real_compute=false skip) + final (verdict achieved)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

endorse_entry = {
    "action": "endorse",
    "skipped": True,
    "reason": (
        "real_compute=false (entry-0 meta): closing skips true-compute endorsement per protocol "
        "(no run-orca/run-cp2k/run-qe/run-md executed; no fabricated DFT/MD values recorded). "
        "Conclusion-grade values in this case are sourced (run-pyamm / calc-energy / log-evaluate "
        "output files) or inferred (bridge lowT_retention_1C_pct = 100*cap_lowT/cap_25C, mechanical). "
        "Electrolyte transport values sigma=2.2 S/m, D=6.0e-10 m2/s, t+=0.5 are category 'estimated' "
        "(formulation-direction estimates mapped via the parameter bridge), not true-compute output "
        "and not endpoint measurements."
    ),
    "candidates": [
        {"name": "V18_ok_h50_elx_plus_DFN"},
        {"name": "V17_ok_h60_elx_plus_DFN"},
    ],
}

final_entry = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "FINAL DESIGN (VBF-T4R3): OKane2022 base, 8um Al CC / 6um Cu CC / 8um separator, "
        "h=50 W/m2/K, radii neg 2.0um / pos 2.5um, electrolyte direction sigma=2.2 S/m, "
        "D=6.0e-10 m2/s, t+=0.5 (category 'estimated', see endorse). DFN-verified (round 7, "
        "evaluate pass both candidates): V18: retention 97.97% (>=95), ED_kg 514.8 (>=327.18), "
        "ED_L 977.0 (>=880), T_max 330.45K (<=333.15), plating false (anode min +0.0155V). "
        "V17 twin (h=60): same dimensions, T_max 328.63K, anode +0.0138V — deeper thermal margin, "
        "thinner plating margin; recommend V18 (h=50) as primary for the wider plating margin, "
        "V17 as the conservative-cooling alternate. Sources: cell/r7_V18_*.json, cell/r7_V17_*.json, "
        "bridge/r7_V18_lowT_retention.json (all values tool-output; verdicts mechanical via "
        "bda log-evaluate rounds 1-7). Trajectory: Chen2020 baseline failed ED_L 843.5<880 and "
        "plated at 4C45 (round 1-4: T-independent kinetics wall) -> platform switch to OKane2022 "
        "(round 4/5) -> h-retention coupling resolved by combined cooling+kinetics design (round 6 "
        "V17 SPMe pass) -> DFN confirmation + margin variant (round 7). Honest caveats: (1) lowT "
        "protocol uses identical params incl. initial temperature — no cold-soak equilibrium is "
        "simulated (warm-start artifact); true cold-soak retention may be lower, physical test "
        "required; (2) plating margin is thin (~15mV) and coupled to cooling derate (h=40 territory "
        "fails, round 5 data); (3) electrolyte excluded from mass/volume (calc-energy contract "
        "caliber, electrolyte_included:false); (4) casing/tabs not modeled (ED_L is layer-stack "
        "caliber); (5) cycle life not simulated (aging protocol not run).",
    ),
}

append_entry(ws, endorse_entry)
append_entry(ws, final_entry)
print("closing entries written: endorse (skipped), final (achieved)")