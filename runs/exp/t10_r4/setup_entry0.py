"""T10 v4 (t10_r4): write log entry 0 (criteria) + plan entry into runs/exp/t10_r4/log.jsonl.

Uses bda.store.append_entry (protocol-mandated log writer).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/.claude/skills/virtual-battery-factory/scripts")))
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t10_r4", root="runs")

entry0 = {
    "criteria": {
        "stage1": {
            # molecular gates (funnel outputs): property window + reduction-first + envelope/family + ML sanity
            "homo_ev": {"max": -13.74},
            "lumo_ev": {"max": -7.0},
            "in_envelope": False,
            "in_documented_families": False,
            "converged": True,
            "energy_ev": {"max": 0.0},
        },
        "stage2": {
            # cell performance (contract verbatim)
            "sei_thickness_nm_end": {"max": 370.0},
            "energy_density_wh_kg": {"min": 327.18},
        },
        "stage3": {
            # safety (contract verbatim: no thermal-runaway trigger under 4C charge at 45 C)
            "triggered": False,
        },
        "meta": {
            "case": "t10_r4",
            "contract": "T10 v4 (reduction-first arm)",
            "base": "Chen2020",
            "real_compute": False,
            "ablation": {"exploration_force": "off", "ceiling_escalation": "off", "funnel_voting": "on"},
            "freedoms": {
                "electrode_system": "locked (Chen2020)",
                "electrolyte_transport": "locked",
                "electrode_modification": "locked except declared additive SEI-kinetics mapping",
                "cell_architecture": "locked",
                "thermal_management": "locked (h=10 default)",
            },
            "mapping": {
                "rule": "k(M) = k0 * 10^((HOMO_xTB(M) + 12.5)/1.0)",
                "k0_m_s": 1e-12,
                "k0_source": "Chen2020 'SEI kinetic rate constant [m.s-1]' (pybamm ParameterValues dump)",
                "calibration": [{"factor": 1.0, "homo_ev": -12.5, "sei_nm": 449.12}, {"factor": 0.1, "homo_ev": -13.5, "sei_nm": 385.10}],
                "extrapolation_note": "mapping calibrated over 0.1x-1x; beyond that range is an assumption, reported as such",
            },
            "known_set": "runs/exp/known_set_sei/envelope_stats_v2.json (87 points: 82 documented + 5 folded candidates)",
            "adjudication": "runs/exp/known_set_sei/envelope_check.py --known-set runs/exp/known_set_sei/envelope_stats_v2.json --smiles <SMILES>",
            "solvent_lumo_ref_ev": {"EC": -6.7171, "EMC": -6.1581, "PC": -6.620, "FEC": -7.1960, "VC": -7.0894},
            "homo_calibration_refs_ev": {"triflyl_fluoride_documented_deepest": -14.14, "known_set_deepest_bis(trifluoromethyl)sulfone": -14.30},
            "energy_density_definition": "calc-energy contract convention (active layers + collectors + separator, electrolyte excluded)",
        },
    }
}
append_entry(ws, entry0)

plan = {
    "action": "plan",
    "objective_breakdown": (
        "stage1 molecular: xTB HOMO <= -13.74 eV (SEI window), xTB LUMO <= -7.0 eV (reduction-first vs "
        "solvent LUMOs EC -6.7171/EMC -6.1581/PC -6.620; known film-formers FEC -7.1960/VC -7.0894), "
        "family gate empty, outside 87-point hull. stage2 cell: SEI <= 370 nm after 100x1C, ED >= 327.18 Wh/kg "
        "(calc-energy). stage3 safety: no TR trigger at 4C/45C. Trade-off: deeper HOMO -> smaller k -> thinner SEI "
        "(only lever); ED and 4C thermal behavior are baseline properties (non-molecular levers prohibited)."
    ),
    "candidate_strategy": (
        "S=O chemistry (the natural deep-HOMO/deep-LUMO space) is family-banned; target electron-poor non-gate "
        "motifs: acyl fluorides, alpha-dicarbonyls, anhydrides, ketenes, isocyanates/isothiocyanates, thiocarbonyls, "
        "S-F hypervalent (SF4/SF5/SF6/S2F10), N-F (NF3/N2F4/R-NF2), hypofluorites, thioesters, imines, perfluoro "
        "aliphatic rings/alkenes, ClO3F/IF7. Round 1: ~60 xTB probes; survivors go to MACE/CHGNet + envelope_check."
    ),
    "budget_allocation": "r1: ~60 xtb probes + ~5-10 envelope adjudications; r2-3 refinements ~15 probes each; cell: baseline 3 runs + 3 runs per finalist.",
    "risk_and_fallback": (
        "R1 no molecule clears both windows -> stronger EWG stacks or honest negative. R2 survivors inside hull -> "
        "per-atom-energy offset or HOMO < -14.2961. R3 SEI > 370 at window edge -> deeper-HOMO variant. "
        "R4 baseline ED/TR fail -> negative result (no molecular fix allowed)."
    ),
    "detail": "design_plan.md",
}
append_entry(ws, plan)

print("entries written; log now has:")
for line in (ws.path / "log.jsonl").read_text(encoding="utf-8").splitlines():
    print(" ", line[:160])
