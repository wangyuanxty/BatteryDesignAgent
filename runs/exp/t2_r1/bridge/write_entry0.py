"""Write log.jsonl entry 0 (criteria + meta) for case t2_r1 via bda.store.append_entry."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t2_r1", "runs")

entry = {
    "criteria": {
        # Decision layer 1 (molecular goals / elimination lines): inactive — case starts
        # at Stage 3 (cell design); materials use system baseline (see funnel log entry).
        "stage1": {},
        # Decision layer 2 (cell performance), thresholds verbatim from task text.
        # sei_100cyc_nm / sei_500cyc_nm / lowT_retention_pct are evaluated from
        # mechanically derived bridge JSONs (values copied / ratioed from run-pyamm
        # outputs by bridge scripts; bridge files document formula + source file:key),
        # because the log-evaluate flat criteria supports one threshold per key name
        # while the raw aging output key `sei_thickness_nm_end` carries two distinct
        # cycle-count contracts in the task text.
        "stage2": {
            "energy_density_wh_kg": {"min": 327.18},
            "sei_100cyc_nm": {"max": 500.0},
            "sei_500cyc_nm": {"max": 550.0},
            "lowT_retention_pct": {"min": 90.0},
        },
        # Decision layer 3 (safety): 4C fast charge with no lithium plating.
        # plated derived mechanically from anode_potential_v min < 0 (run-pyamm 4C output).
        # T_max_K: no red line in task text -> monitored only (auto-extracted to metrics), not judged.
        "stage3": {
            "plated": False,
        },
        "meta": {
            "case_id": "t2_r1",
            "task": "Design a battery for grid energy storage: energy density >= 327.18 Wh/kg, support 4C fast charge (no lithium plating), anode SEI thickness <= 500 nm after 100 cycles of 1C cycling, discharge capacity retention >= 90% at -20C, SEI <= 550 nm after 500 cycles.",
            "base": "Chen2020",
            "base_reason": "task text names no electrode system -> anchor table default Chen2020 (NMC811/graphite baseline teaching parameterization, aging-capable SEI parameters). Discriminant anchor verified by parameter-set dump (bridge/dump_base.py output) before this entry.",
            "start_stage": 3,
            "start_stage_reason": "task text specifies performance metrics only; no new materials/additives/electrolyte/coating design named -> start at Stage 3 cell design with system baseline materials; material fallback (Stage 2) remains available via evaluation routing if cell-scale levers hit a material ceiling.",
            "real_compute": False,
            "real_compute_reason": "headless default (task text does not request true DFT/MD endorsement)",
            "freedoms": {
                "electrode_system": "adjustable — task silent -> widest interpretation; base parameter-set switch allowed if ED ceiling requires (anchor table candidates OKane2022/ORegan2022/LNMO etc.)",
                "electrolyte_formulation": "adjustable — transport-parameter overrides allowed (Electrolyte conductivity/diffusivity, Cation transference number) as formulation candidates (t1_r1 lesson: widest, not narrowest)",
                "electrode_modification": "adjustable — SEI-kinetics coating overrides allowed (SEI kinetic rate constant / SEI reaction exchange current density; inorganic coating candidates skip molecular funnel)",
                "cell_architecture": "adjustable — electrode thickness/porosity/N-P/separator/current-collector/particle-size overrides allowed",
                "thermal_management": "adjustable — Total heat transfer coefficient overridable (contract has no T_max red line; temperature monitored only)",
            },
            "criteria_mechanics": "stage2 keys sei_100cyc_nm/sei_500cyc_nm/lowT_retention_pct are matched against mechanically derived bridge JSONs passed alongside simulation outputs to log-evaluate (unique key names per threshold; raw output keys land in metrics unchanged). Derived values are verbatim copies or ratios of run-pyamm output values; bridge files record formula + source file:key for audit replay.",
        },
    }
}

append_entry(ws, entry)
print("entry 0 written:", ws.path / "log.jsonl")
