"""Append the Stage-1 plan entry to the audit ledger (t5_r2)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

entry = {
    "action": "plan",
    "objective_breakdown": (
        "stage2 ED >= 500.94 Wh/kg (contract caliber, electrolyte-excluded); "
        "stage3 4C fast charge without plating (plated=false) and T_max_K <= 333.15 "
        "(<=15 K rise over 318.15 K start). Expected Pareto tension: ED vs 4C plating "
        "(thick/dense electrodes), ED vs T_max (mass cuts raise per-mass heat). "
        "Voltage lever (system switch) and electrolyte transport raise ED/plating "
        "margin simultaneously; cooling h attacks T_max only."
    ),
    "candidate_strategy": (
        "R1 baseline Chen2020 (1C discharge -> calc-energy -> 4C_charge_45C lumped+plating) "
        "with opening ceiling assessment; expected escalation to Stage 2 system design; "
        "R2 system candidates (LNMO 4.7V-class from skill library, Chen2020 reference arm); "
        "R3+ architecture x electrolyte x thermal tuning on surviving system "
        "(thickness scaling, thin collectors/separator, porosity, negative particle size/N-P, "
        "sigma/t+/D transport overrides (literature estimates), cooling h); safety fine-tune last."
    ),
    "budget_allocation": (
        "R1 baseline+ceiling 1 round; system screening 1-2 rounds; architecture/electrolyte/"
        "thermal tuning ~8 rounds (2-4 variants each, exploration_force ON); safety fine-tune "
        "~3 rounds; closing endorse+deliverables. No fixed round cap; three-strike per cause."
    ),
    "risk_and_fallback": (
        "ED gap -> material/system escalation; 4C plating persists -> electrolyte transport + "
        "N/P + particle size; T_max misses -> cooling h + reduced ohmic heat; LNMO insufficient "
        "-> thickness re-scaling then NMC811 arm; overall unreachable -> three-strike questioning "
        "then honest negative result with quantified nearest-feasible relaxation."
    ),
    "detail": "design_plan.md",
}

append_entry(ws, entry)
print("plan entry appended")