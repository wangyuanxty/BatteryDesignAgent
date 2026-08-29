"""t5_r2 close-out (a): endorse + final audit entries into log.jsonl."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

# ---- Stage 5, Step B: true-compute endorsement -------------------------------
append_entry(ws, {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false in entry 0 contract; no DFT/MD compute gateway was used",
    "note": ("Design decisions therefore rest on the contractual mechanical simulators "
             "(pybamm-runner DFN/SPMe, calc-energy, log-evaluate). Electrolyte transport "
             "properties (conductivity 1.5 S/m, cation transference 0.6, EC-phase diffusivity "
             "5.0e-10 m2/s) are literature-class ADJUSTABLE-FREEDOM estimates, explicitly "
             "marked 'estimate' - they are parameter-bridge values, NOT endorsed by "
             "true-compute methods. This is recorded as an honest limitation, not a defect."),
})

# ---- Stage 5, Step C: final case entry --------------------------------------
append_entry(ws, {
    "action": "final",
    "verdict": "achieved",
    "score_summary": {
        "energy_density_wh_kg": {"measured": 666.2984629492356, "threshold": 500.94, "pass": True},
        "T_max_K": {"measured": 330.9840728321742, "threshold": 333.15, "pass": True},
        "plated": {"measured": False, "anode_potential_min_v": 0.0506, "pass": True},
    },
    "recommendation": {
        "name": "f2_h70_C (VBF-T5R2 finalist)",
        "params": "bridge/p_r6_f2.json (overrides on Chen2020 base)",
        "key_numbers": {
            "energy_density_wh_kg": 666.30,
            "volumetric_wh_l": 1020.47,
            "capacity_ah_1c_dfn": 7.171,
            "energy_wh": 25.375,
            "mass_g_contract_caliber": 38.083,
            "thickness_um": 242.12,
            "area_m2": 0.1027,
            "T_max_degC_at_4C": 57.83,
            "ap_min_v": 0.0506,
            "midpoint_v": 3.7798,
            "dcr_mohm": 2.538,
        },
        "rationale": (
            "Energy density achieved by architecture-on-Chen2020 (x1.3 uniform thickness "
            "scaling with nominal capacity 6.5 Ah -> overhead amortization), thin "
            "current collectors (8/6 um) and separator (8 um) for the mass caliber, "
            "plus porosity 0.43/0.45. Plating margin built FIRST via anode-side transport "
            "(t+ 0.6, D 5e-10, neg porosity 0.45, neg particle 3 um) and an N/P anode buffer "
            "(121.84 um negative, ~5% headroom beyond full charge); only then was cooling "
            "(h = 70 W/m2/K channel-cooling class) applied for the T_max criterion - "
            "cooling alone re-plates the cell (measured h-sweep, rounds 4-5), so the "
            "order of levers matters."
        ),
    },
    "design_path": [
        "baseline Chen2020: ED 400.29, plated, T_max 354.29 K - all three criteria fail",
        "ceiling assessment: ED reachable via overhead cut + thickness/nominal scaling; LNMO 4.7V lever measured and eliminated (420.27, still plated)",
        "r2 architecture arms a1/a2/a3: 488.61 / 509.06 / 512.23 - ED criterion becomes solvable",
        "r3 transport (sigma 1.5, t+ 0.45, D 3.5e-10) + porosity: first plating-free cell (e2, ap +0.0138 V) but T 367.45 K",
        "r4-r5: cooling h-sweep re-plates (T down => ap down); decoupled via t+ 0.6, D 5e-10, neg por 0.45, particle 3 um, N/P buffer; rounds 5 B/C/D all-pass",
        "r6: thermal margin consolidation h=70 (f2_h70_C: ED 665.4 spme-grade, T 330.98 K, ap +0.0506)",
        "r7: finalist verification at DFN precision - ED 666.30, T 330.98 K, no plating (mechanical PASS on all criteria)",
    ],
    "honest_caveats": [
        "Contract energy-density caliber excludes electrolyte and casing (parameter set lacks their densities); BOM-caliber value with literature electrolyte fill (1.2 g/cm3) is ~502 Wh/kg - packaging reality is lower than the 666.3 evaluated number.",
        "'Supports 4C' is protocol-defined: 1C discharge then 4C CC charge to 4.2 V (no CV hold). Charge acceptance in that step is 0.51 Ah before cut-off; anode potential min +0.0506 V => no plating over the evaluated profile. Real packs would use a tapered fast-charge profile.",
        "Electrolyte transport properties are literature estimates, not true-compute-endorsed (real_compute=false).",
        "Informational 100-cycle aging run (SPMe, SEI ec-reaction-limited) produced a per-cycle capacity series inconsistent with the contract 1C capacity (runner protocol definition); reported only as raw SEI-trend signal (end SEI 520.3 nm), no cycle-life rating claimed.",
        "No three-strike questioning event occurred; ceiling assessment resolved the only open question in round 1, so no escalation object is attached.",
        "cell_model.stl not requested by the task, therefore not provided.",
    ],
})
print("endorse + final appended")