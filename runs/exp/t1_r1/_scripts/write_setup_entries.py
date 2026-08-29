"""t1_r1 setup: log.jsonl entry 0 (criteria+meta), plan entry, funnel entry.
All log writes go through bda.store.append_entry (protocol rule)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_r1", "runs/exp")

entry0 = {
    "criteria": {
        "stage1": {"max_energy_ev": 0.0, "max_homo_ev": -6.0},
        "stage2": {"energy_density_wh_kg": {"min": 392.61}},
        "stage3": {"T_max_K": {"max": 333.15}, "plated": False, "triggered": False},
        "meta": {
            "case": "t1_r1",
            "task": "Design a battery for a next-generation pure electric sedan: energy density >= 392.61 Wh/kg, support 4C fast charge (no lithium plating), maximum temperature <= 60 C, overcharge to 4.7 V without triggering thermal runaway",
            "real_compute": False,
            "start_stage": 3,
            "base_params": "Chen2020",
            "base_determination": "task text names no electrode system -> anchor table default row: Chen2020 (recorded); electrode-system DOF adjustable (widest interpretation) allows base switching as a design candidate",
            "freedoms": {
                "electrode_system": "adjustable",
                "electrolyte_formulation": "adjustable",
                "electrode_modification": "adjustable",
                "cell_architecture": "adjustable",
                "thermal_management": "adjustable"
            },
            "freedom_notes": [
                "headless zero-interaction run: no clarification; undeclared degrees of freedom take the WIDEST interpretation, recorded here for audit (t1_r1 lesson)",
                "60 C converted mechanically to 333.15 K (60 + 273.15)",
                "overcharge 4.7 V maps mechanically to bda overcharge protocol on a 4.2 V upper-cut-off base (4.2 + 0.5 = 4.7 V); a base with 4.7 V cut-off (e.g. LNMO) would overcharge beyond 4.7 V and is not task-compliant for this metric",
                "4C fast-charge plating/Tmax judged on 4C_charge_45C protocol (318.15 K ambient, 900 s, coupled lumped thermal, plating module)",
                "ED judged by calc-energy contract formula (stack mass: electrodes + current collectors + separator; electrolyte and casing excluded, annotated in report)"
            ]
        }
    }
}

plan = {
    "action": "plan",
    "objective_breakdown": "Four metrics: ED>=392.61 Wh/kg (stage2, calc-energy contract); 4C no plating (stage3, plated=false on 4C_charge_45C); T_max<=333.15 K (stage3, 60 C converted); overcharge to 4.7 V no TR (stage3, triggered=false; overcharge protocol 4.2 V cut-off +0.5 V -> run-tr ODE). Trade-offs: ED vs 4C (thicker/compacted electrodes raise ED but worsen plating/heat); plating and Tmax both benefit from transport improvement (sigma_e, small particles) and cooling h; TR levers: overcharge heat (impedance), cell thermal mass (mass from calc-energy), heat rejection (hA).",
    "candidate_strategy": "R0 baseline Chen2020 defaults on all four protocols (anchor). Then ceiling probe: best-architecture Chen2020 (thin current collectors, thin separator, moderate electrode thickening, small anode particles, higher-h cooling) to test ED>=392.61 with 4C-safe simultaneously. If ceiling insufficient or plating persists -> escalate to Stage 2 material design: system candidate OKane2022 (SiOx anode, plating/cracking parameterization) and/or electrolyte formulation candidates (conductivity/transference/diffusivity overrides). Safety fine-tuning last (h, N/P, particle size, hA for TR).",
    "budget_allocation": "R0 baseline 1 round; architecture exploration 3-5 rounds; Stage-2 escalation (system/formulation) 2-3 rounds if needed; safety fine-tuning 2 rounds; deliverables + closing fixed.",
    "risk_and_fallback": "Risk A: ED ceiling of Chen2020 below 392.61 with 4C-safe architecture -> escalate system switch (OKane2022 SiOx). Risk B: 4C plating -> raise N/P, smaller anode particles, higher electrolyte conductivity (formulation), higher anode porosity. Risk C: T_max>333.15 -> raise Total heat transfer coefficient (liquid cooling), reduce impedance. Risk D: TR triggered at 4.7 V -> reduce overcharge heat (impedance), raise hA in run-tr (thermal-management DOF), larger cell mass; material escalation (high-voltage-stable chemistry) only if architecture+formulation space exhausted. Three-strike rule: same failure cause 3 consecutive rounds -> question model/system, task-boundary, and metric assumptions layer by layer, record in final escalation.",
    "detail": "design_plan.md"
}

funnel = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": "start_stage=3: case starts at Stage 3; materials use system baseline (no molecular candidates, no molecular screening). Base determination (deterministic, anchor table): task text names no electrode system -> default Chen2020 with record. Anchor verification (parameter dump, pybamm.ParameterValues(Chen2020)): upper cut-off 4.2 V -> overcharge target 4.7 V = 4.2+0.5 matches task verbatim; NMC811/graphite class (positive density 3262 kg/m3, negative 1657 kg/m3); complete thermal/geometry keys present (Total heat transfer coefficient 10 W/m2K; Cu CC 12 um, Al CC 16 um; separator 12 um porosity 0.47; positive 75.6 um porosity 0.335; negative 85.2 um porosity 0.25; electrode height 0.065 m x width 1.58 m; nominal capacity 5 Ah). props source: baseline (Chen2020 literature parameter set).",
    "note": "molecular funnel skipped at start_stage=3; stage1 elimination lines (max_energy_ev 0.0 eV, max_homo_ev -6.0 eV) apply only if Stage 2 molecular candidates are proposed later"
}

for entry in (entry0, plan, funnel):
    append_entry(ws, entry)

print("wrote 3 setup entries to", ws.path / "log.jsonl")
