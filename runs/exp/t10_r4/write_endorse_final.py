"""T10 v4 (t10_r4): append endorse (real_compute=false skip) + final entries to log.jsonl."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"D:/research/degradation_prognostics/Battery_Design_Agent/.claude/skills/virtual-battery-factory/scripts")))
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("exp/t10_r4", root="runs")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false (contract default): no run-orca/run-cp2k/run-md true-compute endorsement; all funnel numbers are MACE-MP medium + CHGNet + GFN2-xTB proxies",
    "candidates": [
        {
            "smiles": "O=C(OC(=O)C(F)(F)F)C(F)(F)F",
            "name": "trifluoroacetic anhydride",
            "endorsement": {
                "note": "proxy-level only (no fabricated DFT/MD values)",
                "envelope_check_v2": "in_envelope=false, families_matched=[] (official CLI record finalist_envelope_check.txt)",
            },
        }
    ],
}
append_entry(ws, endorse)

final = {
    "action": "final",
    "verdict": "achieved",
    "recommendation": (
        "trifluoroacetic anhydride (TFAA), SMILES O=C(OC(=O)C(F)(F)F)C(F)(F)F, CAS 407-25-0 (cataloged, liquid). "
        "Funnel: xTB HOMO -14.1603 eV (<= -13.74), LUMO -10.9558 eV (<= -7.0, reduction-first), MACE -80.376 eV / "
        "CHGNet -84.479 eV both converged, envelope_check v2: in_envelope=false (outside 87-point hull), "
        "families_matched=[] (no banned family). Mapping: k = k0*10^((HOMO+12.5)/1.0) = 1e-12*10^(-1.6603) = "
        "2.1863e-14 m/s (factor 0.021863, mapping.py). Cell: SEI 322.636 nm after 100x1C (<= 370, passes with 47 nm "
        "margin), ED 400.293 Wh/kg (>= 327.18, calc-energy), 4C/45C run-tr triggered=false (T_max 354.289 K). "
        "Honest caveats: (1) factor 0.0219 lies below the mapping's 0.1x-1x calibration range (449.12/385.10 nm) - "
        "the mapped k is an extrapolation assumption, reported as such; (2) lithium plating still occurs at 4C "
        "(anode min -0.192 V), same as baseline - not a contract criterion, no non-molecular fix allowed; "
        "(3) k-sweep check: SEI(k) 449.12/384.96/366.87/322.74/274.35 nm at k0/0.1x/5.754e-14/2.19e-14/1.1e-14 - "
        "even the window-edge HOMO (-13.74 -> k=5.754e-14) passes 370 nm, so the result does not depend on "
        "extrapolation fragility alone."
    ),
    "cataloged": True,
    "cataloged_ref": "CAS 407-25-0, trifluoroacetic anhydride (liquid, commercial)",
    "assumption_notes": [
        "mapping k(M) calibrated on 449.12 nm (k0) and 385.10 nm (0.1x); finalist factor 0.0219x is below range -> extrapolation",
        "molecular levers only: geometry/transport/kinetic overrides/system switches all prohibited (entry-0 meta.freedoms)",
    ],
}
append_entry(ws, final)
print("endorse + final appended")
