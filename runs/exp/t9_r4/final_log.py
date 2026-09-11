"""The final log entry (negative result) - appended AFTER the round-4 evaluate entries,
so it is the LAST write to log.jsonl."""
from bda import store

ws = store.CaseWorkspace("t9_r4", root="runs/exp")

final = {
    "action": "final",
    "verdict": "negative",
    "recommendation": (
        "No cathode composition satisfies the contract within the six supported families. The binding result is the "
        "charging-potential gate: the ONLY candidate in 42 screened that cleared the 4.6 V computed window (AlB55, "
        "LiAl0.5B0.5O2, avg 4.641 V) charges its last Li (x: 0.4 -> 0.3) at 7.41 V - 2.6 V above the 4.8 V anodic "
        "limit of the fixed electrolyte. Its window pass was an artifact of a pathological x=0.3 endpoint, and the "
        "mechanism condemns the entire d0/d10 O-redox layered line. The TM-redox layered band caps at ~4.0 V "
        "(measured: NiFe55 3.990, known-set max ~4.03), and every non-layered family is energy-density-infeasible "
        "under the contract's 0.9-capacity mapping rule (even an olivine at 4.8 V / 128 mAh/g yields ~322 < 327.18 "
        "Wh/kg). Honest negative result: the window [4.6, 4.8] V on CHGNet-computed layered voltage is empty when "
        "the charging potential must stay <= 4.8 V. No candidate is reported as passing."
    ),
    "evidence": {
        "screened": "42 layered candidates in 3 run-comp batches + known-set layered references (LiNiO2 3.890, NMC811 3.803, LiNi0.5Mn0.5O2 3.701, LiCrO2 3.558, LiCoO2 3.361, LiMnO2 3.143)",
        "tm_redox_layered_band": "2.56-3.99 V (round 1; NiFe55 3.990 max) - below 4.6 V",
        "d0d10_oredox_line": "LiScO2 4.298, LiGaO2 4.479, LiZnO2 4.492, LiAlO2 4.598, AlB55 4.641, BGa55 4.504, GaAl55 4.494, AlB95 4.488, LiBO2 4.253 - the line reaches the window only via a pathological x=0.3 endpoint",
        "charging_gate_alB55": "charging_potential_v 7.410 V (gate_out.json: E(0.4) -295.256 eV, E(0.3) -285.968 eV from the same batch machinery, n=1, e_li -1.878 eV) vs limit 4.8 V -> FAIL",
        "envelope_alB55": "comp_envelope_check.py PASS on both modes (outside the 102-point hull; not among the 115 catalogue members); the --formula mode independently re-computed avg 4.6354 V - the screening value reproduces within 6 mV",
        "ed_infeasibility_non_layered": "decisive plan analysis: olivine/spinel/tavorite/NASICON under the 0.9-capacity rule give ED <= ~322 Wh/kg even at 4.8 V (LiNiPO4 at its true 5.1 V ~ 317) -> only layered can reach 327.18",
        "true_voltage_guard_status": "not needed for a rejected candidate; noted that the known real >4.6 V materials (LiCoMnO4, LiCoPO4, LNMO) are all non-layered (ED-infeasible under the 0.9 rule) or overestimate-prone computed (LiNiPO4 computes 7.016 vs true 5.1)",
    },
    "escalation_questioning": [
        "(1) Window premise: within the layered LiMO2 family, is a CHGNet-computed average of >= 4.6 V achievable by "
        "any chemistry whose top-of-charge incremental potential stays <= 4.8 V? Evidence says no: TM-redox caps at "
        "~4.0 V and the only >4.6 V mechanism (d0 O-redox) intrinsically ends with a >4.8 V final step.",
        "(2) Family boundary: real 4.6-4.8 V cycling materials are olivine (LiCoPO4), spinel (LiCoMnO4, LNMO) - all "
        "excluded from the ED window by the 0.9-capacity mapping rule. If the six-family constraint is a proxy for "
        "supported prototypes, the [4.6, 4.8] V x ED>=327.18 region is unreachable within it.",
        "(3) Mapping rule: the plateau-OCP fixed cell delivers ~5.1 Ah anode-limited (LNMO.json precedent) at "
        "~4.4-4.5 V mid-voltage for any candidate, i.e. ED ~470-500 Wh/kg regardless of the rule capacity - the "
        "0.9 x C rule (not the delivered cell) is what excludes the non-layered high-voltage families. Is that the "
        "intended reading of the contract?",
    ],
    "close_loop": {
        "runcomp_replay": "comp_envelope_check.py --formula mode re-computed AlB55 independently (avg 4.6354 V, capacity 324.38, stab -2.390) - within 6 mV of the batch value; verdict PASS (outside envelope)",
        "public_catalogue_search": "web search for LiAl0.5B0.5O2 / LiAlO2 as lithium-battery cathode materials returned no results - recorded as 'not found in the searched scope'",
        "qe_status": "run-qe not performed: no candidate survived the stage-1 co-gates to reach Stage 5 (the QE pseudopotential map was extended with Al and B in preparation, recorded honestly); the d0-line mechanism basis (Li2MnO3-class O-redox plateau ~4.5 V) was checked against literature instead",
    },
    "conclusion": (
        "Honest negative result. No candidate passes the window without breaking compatibility, and no candidate "
        "passing compatibility reaches the window. The two decisive walls: (i) TM-redox layered voltage caps at "
        "~4.0 V; (ii) the only mechanism reaching 4.6 V - d0/d10 O-redox - fails the 4.8 V charging-potential gate "
        "catastrophically (7.41 V measured). Nothing is reported as passing."
    ),
}
store.append_entry(ws, final)
print("final appended (last log entry)")
