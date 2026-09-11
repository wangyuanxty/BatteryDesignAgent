"""Probe batch 2: deeper-HOMO / better-additive-story candidates.

Focus: perfluoro sulfonyl fluorides (chain extension of triflyl fluoride),
perfluoro sulfones, and other extremely electron-poor small molecules.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "bf", REPO / "runs" / "exp" / "known_set_sei" / "batch_funnel.py"
)
bf = importlib.util.module_from_spec(spec)
sys.modules["bf"] = bf
spec.loader.exec_module(bf)  # noqa: S404

import numpy as np
from rdkit import Chem
from scipy.spatial import Delaunay

ENV = REPO / "runs" / "exp" / "known_set_sei" / "envelope_stats.json"
env = json.loads(ENV.read_text(encoding="utf-8"))
pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
tri = Delaunay(pts)
HOMO_MIN = min(p["homo"] for p in env["points"])  # hull's minimum HOMO = triflyl vertex

CANDIDATES = [
    {"name": "pentafluoroethylsulfonyl fluoride", "smiles": "FS(=O)(=O)C(F)(F)C(F)(F)F"},
    {"name": "perfluoropropanesulfonyl fluoride", "smiles": "FS(=O)(=O)C(F)(F)C(F)(F)C(F)(F)F"},
    {"name": "nonafluorobutanesulfonyl fluoride", "smiles": "FS(=O)(=O)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F"},
    {"name": "bis(trifluoromethyl)sulfone", "smiles": "O=S(=O)(C(F)(F)F)C(F)(F)F"},
    {"name": "triflyl chloride", "smiles": "O=S(=O)(Cl)C(F)(F)F"},
    {"name": "trifluoromethyl sulfur pentafluoride", "smiles": "FC(F)(F)S(F)(F)(F)(F)F"},
    {"name": "hexafluoroethane", "smiles": "FC(F)(F)C(F)(F)F"},
    {"name": "trifluoromethyl hypofluorite", "smiles": "FOC(F)(F)F"},
    {"name": "1,1,2,2-tetrafluoroethanesulfonyl fluoride", "smiles": "FS(=O)(=O)C(F)(F)C(F)F"},
    {"name": "2,2,2-trifluoroethylsulfonyl fluoride", "smiles": "FS(=O)(=O)CC(F)(F)F"},
    {"name": "fluorosulfonyl difluoromethanesulfonyl fluoride", "smiles": "O=S(=O)(F)C(F)(F)S(=O)(=O)F"},
    {"name": "carbonyl fluoride", "smiles": "O=C(F)F"},
    {"name": "trifluoroacetyl fluoride", "smiles": "O=C(F)C(F)(F)F"},
    {"name": "nitryl fluoride", "smiles": "O=[N+]([O-])F"},
]


def main() -> int:
    out_path = REPO / "runs" / "exp" / "known_set_sei" / "probe_v3_out.jsonl"
    results = []
    for i, c in enumerate(CANDIDATES, 1):
        smiles = c["smiles"]
        rec = {"name": c["name"], "smiles": smiles}
        t0 = time.time()
        try:
            m = Chem.MolFromSmiles(smiles)
            n = m.GetNumAtoms()
            rec["n_atoms"] = n
            rec["mace"] = bf.relax_ml(smiles, "mace")
            rec["chgnet"] = bf.relax_ml(smiles, "chgnet")
            rec["xtb"] = bf.xtb_run(smiles)
            e_mace = rec["mace"]["energy_ev"] / n
            e_chg = rec["chgnet"]["energy_ev"] / n
            homo = rec["xtb"]["homo_ev"]
            rec["point_per_atom"] = [e_mace, e_chg, homo]
            rec["in_envelope"] = bool(tri.find_simplex(np.array([e_mace, e_chg, homo])) >= 0)
            # geometric guarantee: HOMO strictly below hull minimum -> outside regardless of energies
            rec["homo_below_hull_min"] = homo < HOMO_MIN
            rec["window_ok"] = (not rec["in_envelope"]) and (homo <= -13.74)
        except Exception as ex:  # noqa: BLE001
            rec["error"] = f"{type(ex).__name__}: {str(ex)[:300]}"
        rec["elapsed_s"] = round(time.time() - t0, 1)
        results.append(rec)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
    out_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in results) + "\n",
        encoding="utf-8",
    )
    print("HULL_MIN_HOMO =", HOMO_MIN, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
