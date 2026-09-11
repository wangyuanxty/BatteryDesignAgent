import json
from pathlib import Path
from bda.store import CaseWorkspace, append_entry

ws = CaseWorkspace("t1_oa", "runs/portability")

endorse = {
    "action": "endorse",
    "skipped": True,
    "reason": "real_compute=false: true DFT/MD endorsement (run-orca/run-cp2k/run-md) skipped per protocol. No fabricated DFT/MD values. The design's material/electrolyte/architecture choices are parameter-bridge design values (electrolyte transport sigma/t+/D and particle size), not molecular candidates requiring first-principles endorsement.",
}

final = {
    "action": "final",
    "recommendation": (
        "T10-final: OKane2022 (NMC811/graphite+SiOx) base + liquid cooling h=80 W/m2/K + advanced electrolyte "
        "(sigma=3.0 S/m, t+=0.6, D=4e-10 m2/s) + nanostructured anode (negative particle 0.8 um, positive 2.0 um). "
        "Achieved: ED 426.89 Wh/kg (>=392.61); 4C charge no plating (anode min +0.0341 V); T_max 324.55 K (<=333.15 K=60 C); "
        "overcharge to 4.70 V no thermal runaway (triggered=false). "
        "Design logic: graphite anode (Chen2020) plates fundamentally at 4C (anode -0.438 V, transport-insensitive); SiOx anode (OKane2022) does not plate but overheats at default cooling (T_max 368 K); liquid cooling caps T_max and advanced electrolyte transport + nanostructured anode restore the no-plating margin at the cooler operating temperature. All values DFN-verified (SPMe used only for screening)."
    ),
    "verdict": "achieved",
}

for e in (endorse, final):
    append_entry(ws, e)
print("endorse + final appended")
