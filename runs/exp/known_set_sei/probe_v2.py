"""Probe candidate SEI additives against the pre-registered 82-compound hull (T10 v2).

Runs the same three-model funnel (MACE medium CUDA / CHGNet CUDA / xTB GFN2)
as batch_funnel.py on a batch of candidate SMILES and reports, per candidate,
the per-atom MACE/CHGNet energies, xTB HOMO/LUMO/total, and the Delaunay
inside/outside verdict vs the known-set envelope. Outside + HOMO <= -13.74 eV
is the layer-A + layer-B target.
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
spec.loader.exec_module(bf)  # noqa: S404 - local trusted script

import numpy as np
from rdkit import Chem
from scipy.spatial import Delaunay

ENV = REPO / "runs" / "exp" / "known_set_sei" / "envelope_stats.json"
env = json.loads(ENV.read_text(encoding="utf-8"))
pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
tri = Delaunay(pts)

CANDIDATES = [
    # inorganic / perfluorinated electron-poor small molecules
    {"name": "sulfuryl fluoride", "smiles": "O=S(=O)(F)F"},
    {"name": "carbonyl fluoride", "smiles": "O=C(F)F"},
    {"name": "nitrogen trifluoride", "smiles": "FN(F)F"},
    {"name": "sulfur hexafluoride", "smiles": "FS(F)(F)(F)(F)F"},
    {"name": "phosphoryl fluoride", "smiles": "O=P(F)(F)F"},
    {"name": "carbon tetrafluoride", "smiles": "FC(F)(F)F"},
    {"name": "trifluoroacetyl fluoride", "smiles": "O=C(F)C(F)(F)F"},
    {"name": "pentafluoroethylsulfonyl fluoride", "smiles": "FS(=O)(=O)C(F)(F)C(F)(F)F"},
    {"name": "triflyl fluoride", "smiles": "FC(F)(F)S(=O)(=O)F"},
    {"name": "pyrosulfuryl fluoride", "smiles": "O=S(=O)(F)OS(=O)(=O)F"},
    {"name": "fluorosulfonyl isocyanate", "smiles": "O=C=NS(=O)(=O)F"},
    {"name": "sulfuryl chloride fluoride", "smiles": "O=S(=O)(Cl)F"},
    {"name": "difluorophosphate", "smiles": "O=P(F)(F)O"},
    {"name": "nitrosyl fluoride", "smiles": "FN=O"},
    {"name": "nitryl fluoride", "smiles": "O=[N+]([O-])F"},
    {"name": "perchloryl fluoride", "smiles": "O=Cl(=O)(=O)F"},
    {"name": "carbonyl sulfide", "smiles": "O=C=S"},
    {"name": "sulfuryl isocyanate fluoride", "smiles": "O=C=NS(=O)(=O)F"},
]


def main() -> int:
    out_path = REPO / "runs" / "exp" / "known_set_sei" / "probe_v2_out.jsonl"
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
