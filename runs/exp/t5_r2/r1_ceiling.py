"""Ceiling assessment (funnel entry) + plan update (direction refinement) for t5_r2 round 1->2."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

# --- Opening ceiling assessment (executed during baseline characterization) ---
append_entry(ws, {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "OPENING CEILING ASSESSMENT (Chen2020 NMC811/graphite, ceiling_escalation ON). "
        "Measured baseline: ED 400.29 Wh/kg, energy 17.395 Wh, mass 43.455 g, "
        "layer kg/m2 pos_el 0.16399 / neg_el 0.10588 / pos_cc 0.04320 / neg_cc 0.10752 / sep 0.00252 "
        "(sourced: cell/r1_base_chen2020_energy.json). "
        "Contract-ED levers: (a) overhead cut estimated - Al 16->8um Cu 12->6um sep 12->8um "
        "=> ED est 488.3 Wh/kg (estimated, formula: E/A / (0.16399+0.10588+0.0216+0.05376+0.00168)); "
        "(b) uniform thickness x1.3 + nominal capacity 5->6.5 Ah x1.3 (same areal loading, larger cell) "
        "=> ED est 509.3 Wh/kg (estimated); x1.4=>516.2. So 500.94 IS within NMC811/graphite ceiling "
        "via architecture alone. System-switch estimate: LNMO 4.7V-class at same geometry loses ED "
        "(pos-layer capacity per mass est ~0.53x NMC811 from stoich limits; voltage midpoint only "
        "+1.15x; estimated) -> voltage lever not the primary ED driver; measured cross-check "
        "planned round 2. BINDING RISK: 4C plating at scaled thickness (through-plane polarization ~ L) "
        "plus T_max baseline already 354.29 K. ESCALATION DECISION: objective exceeds the baseline "
        "architecture-space point but NOT the system ED ceiling; therefore escalate the FORMULATION "
        "dimension (electrolyte transport sigma/t+/D - Stage 2 bridge, addressed via electrolyte-"
        "formulation candidates, literature values marked estimate) + architecture scaling + thermal h, "
        "NOT a cathode-system switch (est non-competitive). LNMO still measured once for evidence."
    ),
})

# --- Plan update (direction refined by measured baseline; not overwritten) ---
append_entry(ws, {
    "action": "plan",
    "update": True,
    "reason": (
        "trigger 3 (key assumption overturned by simulation): measured baseline layer-mass "
        "decomposition + contract ED formula show the primary ED lever is overhead-mass reduction "
        "and uniform thickness scaling with nominal capacity (bigger cell), not a cathode-system / "
        "voltage switch; and the primary 4C-safety lever is electrolyte transport + thermal h. "
        "Original plan favored LNMO system switch as the ED lever."
    ),
    "candidate_strategy": (
        "R2 measured screening (4 candidates): systemLNMO_default (voltage-lever evidence arm), "
        "arch_A_slim (cc 8/6um + sep 8um), arch_B_slim_x1.3 (slim + uniform thickness x1.3, nominal "
        "6.5 Ah) - first estimated ED pass, arch_C_slim_x1.5 (nominal 7.5 Ah). R3+: formulation "
        "overrides (sigma/t+/D literature estimates) + N/P + neg particle size + cooling h tuned "
        "on the surviving architecture until 4C plating-free with T_max_K <= 333.15."
    ),
    "budget_allocation": "R2 system+architecture screening (4 candidates, full triad each); R3-R5 formulation+thermal tuning; R6 safety fine-tune; unchanged closing plan.",
})
print("funnel(ceiling) + plan-update appended")