"""t5_r3 round-2 propose + funnel(baseline note) writer via bda.store.append_entry."""
from bda.store import CaseWorkspace, append_entry
ws = CaseWorkspace("t5_r3", "runs/exp")

# Round-1 baseline evaluation goes through bda log-evaluate (mechanical).
# Funnel log: start_stage=3 statement + base determination basis.
funnel = {
    "action": "funnel",
    "passed": 0,
    "rejected": 0,
    "disputed": 0,
    "detail": (
        "start_stage=3 (task names no materials) -> materials use system baseline; "
        "base=Chen2020 determined by anchor table: task names no electrode system -> default Chen2020 "
        "(discriminant dump: Lower/Upper cut-off 2.5/4.2 V, no SiOx keys, nominal 5 Ah). "
        "Props source=baseline (literature parameter set), no molecular funnel run this case-phase."
    ),
}
append_entry(ws, funnel)

propose = {
    "action": "propose",
    "round": 2,
    "candidates": [
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
            },
            "name": "V1 thin-overhead",
            "role": "halve Al/Cu foil thickness + 12->9um separator: cut inactive mass (contract ED lever)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
            },
            "name": "V2 thin-overhead+thick",
            "role": "V1 + electrodes 75.6->100um / 85.2->112um (N/P ratio kept): mass-dilution ED gain",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 100e-06,
                "Negative electrode thickness [m]": 112e-06,
                "Negative particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Cation transference number": 0.4,
                "Total heat transfer coefficient [W.m-2.K-1]": 30.0,
            },
            "name": "V3 V2+rate-mitigation",
            "role": "V2 + anode particles 5.86->3um + high-sigma/t+ electrolyte + liquid cooling h=30 (plating+T mitigation)",
        },
        {
            "struct": {
                "Positive current collector thickness [m]": 8e-06,
                "Negative current collector thickness [m]": 6e-06,
                "Separator thickness [m]": 9e-06,
                "Positive electrode thickness [m]": 85e-06,
                "Negative electrode thickness [m]": 96e-06,
                "Negative particle radius [m]": 3e-06,
                "Electrolyte conductivity [S.m-1]": 2.2,
                "Cation transference number": 0.4,
                "Total heat transfer coefficient [W.m-2.K-1]": 30.0,
            },
            "name": "V4 moderate-thick+mitigation",
            "role": "V3 but moderate thickness 85/96um: trade a little ED for plating margin at 4C",
        },
    ],
    "llm_reason": (
        "Baseline round-1: ED 400.29 Wh/kg (gap -100.65), 4C plated (anode_potential min -0.438V, baseline has no "
        "plating margin: charge clamps within ~30s), T_max 332.35K pass. CAUSE-SCALE DIAGNOSIS: ED gap = "
        "architecture (mass overhead 15 g of 43 g in Cu/Al foils + separator, dilutable by thicker electrodes); "
        "plating = architecture+transport (areal 4C-current density vs anode kinetics). Both same-scale (Stage 3) "
        "corrections -> no escalation yet; ceiling assessment (contract anatomy): thin foil+thick electrodes can "
        "reach ~515-540 Wh/kg, so 500.94 is architecture-reachable. Overrides: electrolyte sigma scalar 2.2 S/m "
        "= ~1.3x native Nyman2008 at 318K (estimate, high-conductivity formulation); t+=0.4 (estimate, "
        "concentrated/single-ion-class electrolyte); h=30 W/m2/K (liquid-cooled flagship thermal system, "
        "estimate). Particle radius 3um standard fine-anode grade. Porosity left at baseline (keep "
        "active-fraction+porosity complement physical)."
    ),
}
append_entry(ws, propose)
print("round-2 propose + funnel(baseline) appended")