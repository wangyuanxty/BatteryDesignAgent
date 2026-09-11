"""Flatten adjudication records into per-candidate JSON files for bda log-evaluate.

Each output file has TOP-LEVEL scalar keys (log-evaluate extracts only top-level
scalars; the adjudication records nest homo/lumo under 'xtb' etc.). Mechanically
derived from adjudication_r1.jsonl (provenance recorded inside each file).
"""
import json
from pathlib import Path

REPO = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent")
WS = REPO / "runs/exp/t10_r4"
src = WS / "adjudication_r1.jsonl"
out_dir = WS / "cell"
out_dir.mkdir(parents=True, exist_ok=True)

if not src.exists():
    raise SystemExit("adjudication_r1.jsonl not found yet")

for line in src.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    r = json.loads(line)
    if "error" in r:
        continue
    flat = {
        "provenance": "flattened from adjudication_r1.jsonl (envelope_check v2 pipeline: batch_funnel mace+chgnet CUDA + xtb GFN2 + Delaunay hull + family gate)",
        "name": r["proposed_name"],
        "smiles": r["smiles"],
        "n_atoms": r["n_atoms"],
        "homo_ev": r["xtb"]["homo_ev"],
        "lumo_ev": r["xtb"]["lumo_ev"],
        "mace_energy_ev": r["mace"]["energy_ev"],
        "mace_converged": r["mace"]["converged"],
        "chgnet_energy_ev": r["chgnet"]["energy_ev"],
        "chgnet_converged": r["chgnet"]["converged"],
        "in_envelope": r["in_envelope"],
        "in_documented_families": r["in_documented_families"],
    }
    fname = "adjud_" + r["proposed_name"].replace(" ", "_").replace("-", "_") + ".json"
    (out_dir / fname).write_text(json.dumps(flat, indent=2), encoding="utf-8")
    print("wrote", fname, "| in_env:", flat["in_envelope"], "| fams:", flat["in_documented_families"],
          "| homo:", round(flat["homo_ev"], 4), "| lumo:", round(flat["lumo_ev"], 4))
