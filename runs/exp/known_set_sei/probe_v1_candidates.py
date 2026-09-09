"""Probe the three T10-v1 analog candidates against the known-set envelope.

Runs the same funnel on the v1 candidates (which the loosened v1 contract
produced) and tests whether their computed points fall INSIDE the
82-compound envelope hull — the demonstration that the envelope catches
substituted analogues of documented families.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "bf", REPO / "runs" / "exp" / "known_set_sei" / "batch_funnel.py"
)
bf = importlib.util.module_from_spec(spec)
sys.modules["bf"] = bf
spec.loader.exec_module(bf)  # noqa: S404 - local trusted script

PROBES = [
    {"name": "F-VEC", "smiles": "C=CC1(F)COC(=O)O1"},
    {"name": "2-fluoroethanesulfonyl fluoride", "smiles": "FS(=O)(=O)CCF"},
    {"name": "3-fluoropropanesulfonyl fluoride", "smiles": "FS(=O)(=O)CCCF"},
]

try:
    import numpy as np
    from scipy.spatial import Delaunay

    env = json.loads((REPO / "runs" / "exp" / "known_set_sei" / "envelope_stats.json").read_text(encoding="utf-8"))
    pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
    tri = Delaunay(pts)

    def inside(e_mace, e_chgnet, homo, n_atoms: int) -> bool:
        return bool(tri.find_simplex(np.array([e_mace / n_atoms, e_chgnet / n_atoms, homo])) >= 0)

    for probe in PROBES:
        from rdkit import Chem

        n_atoms = Chem.MolFromSmiles(probe["smiles"]).GetNumAtoms()
        rec = {"name": probe["name"], "smiles": probe["smiles"]}
        rec["mace"] = bf.relax_ml(probe["smiles"], "mace")
        rec["chgnet"] = bf.relax_ml(probe["smiles"], "chgnet")
        rec["xtb"] = bf.xtb_run(probe["smiles"])
        rec["in_envelope"] = inside(rec["mace"]["energy_ev"], rec["chgnet"]["energy_ev"], rec["xtb"]["homo_ev"], n_atoms)
        rec["n_atoms"] = n_atoms
        print(json.dumps(rec, ensure_ascii=False), flush=True)
except Exception as ex:  # noqa: BLE001
    print(f"PROBE ERROR: {type(ex).__name__}: {ex}", flush=True)
