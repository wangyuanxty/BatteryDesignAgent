# -*- coding: utf-8 -*-
"""t1_r3 — closing entries: endorse (skip, real_compute=false) + final."""
import sys

from bda.store import CaseWorkspace, append_entry


def main() -> int:
    ws = CaseWorkspace("exp/t1_r3")

    append_entry(ws, {
        "action": "endorse",
        "skipped": True,
        "reason": (
            "real_compute=false: Stage 5 true-compute endorsement (run-orca/run-md/run-qe) skipped by "
            "protocol; no DFT/MD values fabricated. All closing numbers carry simulation/parameter-set "
            "source annotations (r5_v11_*.json outputs, Chen2020 parameter set)."
        ),
    })

    append_entry(ws, {
        "action": "final",
        "recommendation": (
            "Finalist V11 (Chen2020 NMC811/graphite, cell-level design): electrode thicknesses 75.6/85.2 um, "
            "porosities 0.45/0.42, 0.8 um particles (both electrodes), electrolyte sigma=1.8 S/m "
            "(Nyman2008-function base, conductivity ceiling flagged), D=6.0e-10 m2/s, t+=0.55, separator "
            "8 um/porosity 0.6, current collectors 10 um Al / 6 um Cu, h=120 W/m2/K, nominal capacity 5.085 Ah "
            "calibrated to measured 1C capacity. Verified: ED 605.33 Wh/kg >= 392.61 (cell/r5_v11_energy.json); "
            "true-4C charge 20.34 A accepted 4.677 Ah = 92.0% of 1C capacity in 13.8 min with anode potential "
            "min +0.0425 V -> plated=false (cell/r5_v11_4c.json); T_max 321.2 K <= 333.15 K; overcharge 0.5C "
            "DFN to 4.70 V -> T_max 298.57 K, run-tr triggered=false (cell/r5_v11_oc.json + r5_v11_tr.json). "
            "Units note (R5 diagnosis): runner charge capacity_ah is C-rate-normalized duration; true Ah = "
            "reported x nominal — earlier '~46% acceptance plateau' was a units artifact; V11 is a genuine "
            "4C fast charge. Residual risks documented in deliverables: no aging/cycle-life model, lumped "
            "thermal only, no molecular-level electrolyte oxidation endorsement (real_compute=false), "
            "geometric N/P 0.624 per template formula with Chen2020 OCP fit-domain caveat."
        ),
        "verdict": "achieved",
    })
    print("endorse + final entries appended")
    return 0


if __name__ == "__main__":
    sys.exit(main())
