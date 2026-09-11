"""Write the t10_r3 audit log (entries 0 + plan + propose + funnel + final).

Evaluate entries go through `bda log-evaluate` (mechanical verdicts), not here.
"""
import json
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t10_r3", root="runs", create=False)

append_entry(ws, {"criteria": {
    "stage1": {"homo_ev": {"max": -13.74},
               "envelope": "in_envelope=false vs envelope_stats_v2.json (87 pts)",
               "family_gate": "families_matched=[]"},
    "stage2": {"sei_thickness_nm_end": {"max": 370.0},
               "energy_density_wh_kg": {"min": 327.18}},
    "stage3": {"triggered": False},
    "meta": {"contract": "T10 v3 (t10_r3)", "base": "Chen2020",
             "mapping": "k(M) = k0 * 10**((HOMO_xTB+12.5)/1.0), k0=1e-12",
             "real_compute": False, "funnel_voting": "off",
             "exploration_force": "off", "ceiling_escalation": "off",
             "freedoms": {"additive_molecule_only": True},
             "known_set": "envelope_stats_v2.json (82 documented + 5 prior-run)"}}})

append_entry(ws, {"action": "plan",
    "objective_breakdown": "C1 envelope out of hull (87 pts) / C2 family gate empty / "
                          "C3 xTB HOMO <= -13.74 / C4 SEI<=370nm, ED>=327.18 Wh/kg, "
                          "no TR trigger at 4C 45C; mapping k=k0*10^(HOMO+12.5) fixed",
    "candidate_strategy": "perfluorinated chemistry outside the 13 screened families "
                          "(perfluoroamines/perfluoroalkanes); HOMO < -14.2961 (hull min) "
                          "guarantees out-of-hull; deepest = max SEI margin",
    "budget_allocation": "1 funnel round (6 candidates), 1 cell-window round for the "
                        "chosen primary (pfta) + panel aging for all 5 passers",
    "risk_and_fallback": "risk: --funnel branch of envelope_check.py defective (top-level "
                         "model key) -> adjudicate via --smiles + mechanical crosscheck from "
                         "bda outputs; risk: deep extrapolation below 0.1x calibration floor "
                         "-> flag in report; fallback: shallower perfluoro panel members",
    "detail": "notes.md"})

append_entry(ws, {"action": "propose", "round": 1,
    "candidates": [
        {"smiles": "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)N(C(F)(F)C(F)(F)C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F",
         "name": "perfluorotributylamine (FC-43, CAS 311-89-7)",
         "role": "deep-HOMO perfluoroamine additive (liquid, industrial fluorinert)"},
        {"smiles": "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F",
         "name": "perfluorohexane (CAS 355-42-0)", "role": "perfluoroalkane additive (liquid)"},
        {"smiles": "FC(F)(F)C(F)(F)N(C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)F",
         "name": "perfluorotriethylamine (CAS 359-70-6)", "role": "perfluoroamine additive (liquid)"},
        {"smiles": "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F",
         "name": "perfluoropentane (CAS 678-26-2)", "role": "perfluoroalkane additive (liquid)"},
        {"smiles": "FC(F)(F)N(C(F)(F)F)C(F)(F)F",
         "name": "tris(trifluoromethyl)amine (CAS 432-03-1)", "role": "deepest-HOMO probe (gas at RT)"},
        {"smiles": "FS(F)(F)(F)(F)F", "name": "sulfur hexafluoride", "role": "probe (S without S=O)"}],
    "llm_reason": "Pre-run feasibility (notes a-c) identifies perfluorinated chemistry as the "
                  "deepest family outside the 13 screened families; panel spans perfluoroamines "
                  "and perfluoroalkanes of varying size plus one S-probe; all expected to be "
                  "family-gate-clean and HOMO < hull min (-14.2961 eV)"})

append_entry(ws, {"action": "funnel", "passed": 5, "rejected": 1, "disputed": 0,
    "detail": "5 perfluoro candidates pass HOMO<=-13.74, out-of-envelope, family gate clean; "
              "sf6 rejected (HOMO -9.2861 fails window)",
    "dispositions": [
        {"name": "perfluorotributylamine", "status": "passed", "reason": "HOMO -14.9642, out-of-hull, families []"},
        {"name": "perfluorohexane", "status": "passed", "reason": "HOMO -14.9147, out-of-hull, families []"},
        {"name": "perfluorotriethylamine", "status": "passed", "reason": "HOMO -14.8818, out-of-hull, families []"},
        {"name": "perfluoropentane", "status": "passed", "reason": "HOMO -15.0496, out-of-hull, families []"},
        {"name": "tris(trifluoromethyl)amine", "status": "passed", "reason": "HOMO -15.7893, out-of-hull, families []"},
        {"name": "sulfur hexafluoride", "status": "rejected", "reason": "HOMO -9.2861 > -13.74 (window fail)"}]})

print("log entries 0/plan/propose/funnel written")
