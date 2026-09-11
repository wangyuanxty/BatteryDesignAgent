"""Flatten the official envelope_check CLI record for the finalist into a top-level-scalar
file consumed by `bda log-evaluate` (which extracts only top-level scalar keys).

All values are mechanically copied from:
  - runs/exp/t10_r4/finalist_envelope.json  (exact record of the CLI adjudication run)
  - AND-of-two-tool-outputs for the single `converged` criteria key.
No hand-derived chemistry numbers.
"""
import json
import io
from pathlib import Path

WS = Path("runs/exp/t10_r4")
rec = json.load(io.open(WS / "finalist_envelope.json", encoding="utf-8"))

flat = {
    "provenance": (
        "top-level scalars from finalist_envelope.json (official envelope_check v2 CLI record, "
        "batch_funnel mace+chgnet CUDA + xtb GFN2 + Delaunay hull over envelope_stats_v2.json + family gate); "
        "converged = mace.converged AND chgnet.converged; energy_ev = mace energy_ev (funnel energy elimination line; "
        "chgnet energy_ev also negative, see chgnet_energy_ev)"
    ),
    "smiles": rec["smiles"],
    "homo_ev": rec["xtb"]["homo_ev"],
    "lumo_ev": rec["xtb"]["lumo_ev"],
    "energy_ev": rec["mace"]["energy_ev"],
    "converged": bool(rec["mace"]["converged"] and rec["chgnet"]["converged"]),
    "mace_energy_ev": rec["mace"]["energy_ev"],
    "mace_converged": rec["mace"]["converged"],
    "chgnet_energy_ev": rec["chgnet"]["energy_ev"],
    "chgnet_converged": rec["chgnet"]["converged"],
    "in_envelope": rec["in_envelope"],
    "in_documented_families": rec["in_documented_families"],
}
(WS / "cell/adjud_finalist_eval.json").write_text(json.dumps(flat, indent=2), encoding="utf-8")
print(json.dumps(flat, indent=2))
