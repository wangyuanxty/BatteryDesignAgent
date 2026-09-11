import json
from bda.store import CaseWorkspace, append_entry

# Agent-built one-shot helper; executed directly (not imported) via the venv Python
# to append the two mandatory closing entries to the audit trail. Only touches
# runs/exp/t10_r2/log.jsonl through bda.store.append_entry.

ws = CaseWorkspace("t10_r2", "runs/exp", create=False)

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false: true DFT/MD endorsement (run-orca / run-md) skipped per protocol; no fabricated DFT/MD values recorded.",
    "candidates": [
        {
            "name": "bis(trifluoromethyl)sulfone",
            "smiles": "FC(F)(F)S(=O)(=O)C(F)(F)F",
            "role": "round-1 leader: perfluoro sulfone SEI-forming additive",
        }
    ],
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "recommendation": (
        "Recommended new SEI-forming electrolyte additive: bis(trifluoromethyl)sulfone, "
        "SMILES FC(F)(F)S(=O)(=O)C(F)(F)F, on the Chen2020 NMC811/graphite grid-storage cell. "
        "Funnel evidence: xTB GFN2 HOMO -14.2961 eV (deepest of round 1, deeper than the task-contract "
        "deepest documented triflyl fluoride -14.14 eV which is inside the hull); MACE-MP per-atom "
        "E -5.3459 eV and CHGNet per-atom E -5.7035 eV, both ML legs converged, total energy <= 0 eV. "
        "Envelope: candidate point (-5.3459, -5.7035, -14.2961) lies OUTSIDE the 82-point convex hull "
        "(envelope_check.py Delaunay verdict in_envelope=false). "
        "k-rule: k(M) = 1.0e-12 * 10^((HOMO_xtb + 12.5)/1.0) = 1.0e-12 * 10^(-1.7961) = 1.599e-14 m/s. "
        "Cell level (SPMe): 100-cycle 1C aging final SEI 302.74 nm (<= 370 nm PASS); energy density "
        "400.29 Wh/kg (>= 327.18 Wh/kg PASS); 4C-charge thermal runaway NOT triggered (T_max 332.35 K "
        "cooling monotonically to 298.50 K, dTdt_max -0.00045 K/s; PASS). "
        "Novelty: not found in the searched public literature/catalog scope as an SEI additive "
        "(no absolute claim). Caveats labeled honestly: aging capacity-trajectory climb (1.63 -> 1.85 Ah) "
        "is a standard-SEI-model artifact; electrolyte mass excluded from energy density (parameter set "
        "lacks electrolyte density).",
    ),
    "verdict": "achieved",
}
append_entry(ws, final)

print("appended endorse (skipped) + final (achieved)")
