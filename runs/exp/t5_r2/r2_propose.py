"""Round-2 propose entry (t5_r2): 1 system candidate + 3 architecture candidates.

All overridden parameters listed with units and source BEFORE running (protocol rule):
  arch_A_slim:  Positive current collector thickness 16->8 um; Negative 12->6 um;
                Separator thickness 12->8 um. Source: design choices in architecture freedom
                (ultra-thin foil / separator), values are cell-design decisions.
  arch_B_slim_thick1.3: arch_A + uniform electrode scale x1.3 (pos 75.6->98.28 um,
                neg 85.2->110.76 um) + Nominal cell capacity 5->6.5 Ah (consistent areal
                loading, larger cell format). Source: design choices.
  arch_C_slim_thick1.5: arch_A + x1.5 (pos 113.4 um, neg 127.8 um) + nominal 7.5 Ah.
  systemLNMO_default: base = skill library LNMO.json (4.7 V-class spinel, nominal 4.5 Ah);
                no overrides. Source: bda library (baseline literature parameterization).
"""
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t5_r2", "runs/exp")

append_entry(ws, {
    "action": "propose",
    "round": 2,
    "candidates": [
        {"name": "systemLNMO_default", "role": "system candidate: 4.7V-class LNMO spinel (skill library LNMO.json), measured evidence arm for the voltage-lever hypothesis (ceiling assessment estimated it non-competitive on contract ED; measured to settle)"},
        {"name": "arch_A_slim", "role": "architecture: overhead-mass cut (Al 8um / Cu 6um collectors, 8um separator), ED lever #1"},
        {"name": "arch_B_slim_thick1.3", "role": "architecture: arch_A + uniform thickness x1.3 + nominal capacity 6.5 Ah; first variant estimated to pass 500.94 (est 509)"},
        {"name": "arch_C_slim_thick1.5", "role": "architecture: arch_A + x1.5 + nominal 7.5 Ah; higher ED margin (est 516), watches 4C plating penalty of thicker electrodes"},
    ],
    "llm_reason": (
        "Ceiling assessment: overhead cut + thickness scaling with nominal capacity are the two "
        "contract-ED levers (measured baseline 400.29 -> est 488 -> est ~509-516); LNMO included as "
        "measured system-screening arm. Params shown above with units; sources: design choices "
        "(architecture freedom) + bda library baseline for LNMO. Every candidate runs the full triad "
        "(1C discharge -> calc-energy -> 4C_charge_45C DFN lumped+plating) and is mechanically evaluated."
    ),
})
print("propose round 2 appended")