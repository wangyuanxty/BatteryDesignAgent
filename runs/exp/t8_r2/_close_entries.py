# -*- coding: utf-8 -*-
"""Write closing entries: endorse (skipped, real_compute=false) + final (achieved)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t8_r2", "runs/exp")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false (entry-0 meta; headless session, no true-compute request): no run-orca/run-cp2k/run-qe/run-md endorsement executed for V_G; no DFT/MD values fabricated. True-compute endorsement is the only skipped item; Stage-3/4 verdicts are mechanically evidenced by bda log-evaluate rounds 1-3.",
}
append_entry(ws, endorse)
print("endorse written")

final = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "Recommend V_G on Chen2020 NMC811/graphite: electrolyte D=4.2e-10 m2/s, t+=0.40, sigma=1.2 S/m; "
        "positive/negative particle radii 3.0/3.5 um; positive 60 um / negative 67.62 um (width 1.9908 m x height 0.065 m, area-scaled to preserve 5 Ah); "
        "separator 9 um; current collectors 8 um Al / 6 um Cu. "
        "Contract evidence = round-3 evaluate V_VG (mechanically judged by bda log-evaluate, entry evidence chain quoted below): "
        "energy_density_wh_kg 483.37 >= 446.18 PASS; retention_5c 0.9631 >= 0.90 PASS; mass_kg 0.03771 <= 0.04 PASS; "
        "plated False (4C charge 45C, anode_potential_v min 0.02148 V > 0) PASS. "
        "Margins vs contract: ED +37.19 Wh/kg, retention +0.0631, mass slack 2.287 g, plating margin +21.5 mV. "
        "4C-charge T_max 351.93 K honest record (no contract threshold). "
        "V_G preferred over V_E/V_F: same mass as V_E with larger electrolyte margin (t+ 0.40 / D 4.2e-10) and larger plating margin (21.5 mV vs 17.6 mV); "
        "superior ED/mass slack vs V_F (483.4/37.71 vs 459.6/39.71)."
    ),
    "evidence": [
        {"metric": "energy_density_wh_kg", "value": 483.3667003671966, "threshold": {"min": 446.18}, "verdict": "pass", "source": "cell/r3_VG_energy.json:energy_density_wh_kg"},
        {"metric": "retention_5c", "value": 0.9630686588433051, "threshold": {"min": 0.9}, "verdict": "pass", "source": "cell/r3_VG_retention.json:retention_5c"},
        {"metric": "mass_kg", "value": 0.03771305623098, "threshold": {"max": 0.04}, "verdict": "pass", "source": "cell/r3_VG_energy.json:mass_kg"},
        {"metric": "plated", "value": False, "threshold": False, "verdict": "pass", "source": "cell/r3_VG_safety.json:anode_potential_v (min=0.02148V>0)"},
    ],
    "comparison": [
        {"name": "V_E smallP", "metrics": {"energy_density_wh_kg": 483.24250174995285, "retention_5c": 0.9627182299544768, "mass_kg": 0.03771305623098, "plated": False, "anode_min_v": 0.01756, "T_max_K": 352.83}, "verdict": "pass"},
        {"name": "V_F smallP+thinPos", "metrics": {"energy_density_wh_kg": 459.63432570369184, "retention_5c": 0.9640140597142708, "mass_kg": 0.039712412629655996, "plated": False, "anode_min_v": 0.02444, "T_max_K": 348.64}, "verdict": "pass"},
        {"name": "V_G smallP+tplus (SELECTED)", "metrics": {"energy_density_wh_kg": 483.3667003671966, "retention_5c": 0.9630686588433051, "mass_kg": 0.03771305623098, "plated": False, "anode_min_v": 0.02148, "T_max_K": 351.93}, "verdict": "pass"},
    ],
    "limits": [
        "max_energy_ev / max_homo_ev unchecked: real_compute=false, no Stage-1 DFT/MD material screening executed (task required no material invention; all rounds were Stage-3 architecture/formulation)",
        "cycle life not simulated: contract has no durability criterion; aging model not exercised in this loop",
        "electrolyte mass excluded from contract-caliber mass (calc-energy note: parameter set lacks electrolyte density); BOM lists it as an annotated estimate with literature-default density",
        "overcharge/nail/crush/thermal-runaway abuse items N/A (beyond pure simulation boundary)",
        "CAD structural model skipped: optional deliverable that per protocol requires user choice of form/expression (zero-interaction session)",
    ],
    "todo": None,
}
append_entry(ws, final)
print("final written")