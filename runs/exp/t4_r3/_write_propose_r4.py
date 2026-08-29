"""t4_r3: propose entry round 4 — electrode-system switch candidates (DoF: electrode system, adjustable)."""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t4_r3", root="runs")

propose_r4 = {
    "action": "propose",
    "round": 4,
    "candidates": [
        {
            "base": "ORegan2022",
            "name": "V8_sys_ORegan2022",
            "role": "system switch: NMC811/graphite LG M50 (ORegan2022) with empty overrides — Arrhenius-type T-dependent kinetics/transport; tests 4C@45C plating and true cold-discharge behavior",
        },
        {
            "base": "OKane2022",
            "name": "V9_sys_OKane2022",
            "role": "system switch: NMC811/graphite+SiOx (OKane2022, cracking model) with empty overrides — alternative anode chemistry for 4C plating margin and density",
        },
    ],
    "llm_reason": (
        "Round 3 diagnosis: anode-potential dive at the 4C charge-cutoff frame (-0.43 to -0.45 V) is "
        "insensitive to electrolyte transport (V4) and to particle radii 5.86->2.5 um (V5-V7) -> in "
        "Chen2020 the binding term is the temperature-INDEPENDENT charge-transfer kinetics at high C-rate, "
        "which has no sanctioned architecture/formulation lever. Degrees of freedom recorded in entry 0 "
        "make the electrode system adjustable; the anchor table (SKILL 1.5) maps NMC811/graphite to "
        "ORegan2022 (LG M50, pure graphite) and NMC811/graphite+SiOx to OKane2022. System candidates skip "
        "molecular screening and go straight to Stage 3 simulation. Expected mechanism: ORegan2022's "
        "Arrhenius T-dependence raises charge-transfer rate at 45 C and makes -20C retention a genuine "
        "cold-transport test (Chen2020 baseline 'cold' retention 99.4% is a warm-start artifact of "
        "T-independent params). Both evaluated on their own parameter sets (calc-energy per-set mass)."
    ),
}
append_entry(ws, propose_r4)
print("propose r4 written")