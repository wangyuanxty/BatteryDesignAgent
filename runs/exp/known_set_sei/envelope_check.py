"""Envelope adjudication for T10 v2 (layer A): is the candidate inside the
pre-registered 82-compound convex hull?  Pre-registered 2026-09-09 with the
contract; the same script adjudicates the run (agent evidence + replay).

Usage:
    python envelope_check.py --smiles "SMILES"
    python envelope_check.py --funnel <mace_out.json,chgnet_out.json,xtb_out.json>

Prints strictly machine-readable JSON: {"name", "in_envelope": bool,
"point_per_atom": [...], "hull_ref": "envelope_stats.json"}.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from rdkit import Chem
from scipy.spatial import Delaunay

REPO = Path(__file__).resolve().parents[3]
ENV = REPO / "runs" / "exp" / "known_set_sei" / "envelope_stats.json"


def load_tri() -> Delaunay:
    env = json.loads(ENV.read_text(encoding="utf-8"))
    pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
    return Delaunay(pts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smiles")
    ap.add_argument("--funnel", help="same-schema mace+chgnet+xtb output JSON(s), comma-separated")
    args = ap.parse_args()

    tri = load_tri()

    def compute(smiles: str) -> dict:
        from importlib.util import spec_from_file_location, module_from_spec

        spec = spec_from_file_location("bf", REPO / "runs" / "exp" / "known_set_sei" / "batch_funnel.py")
        bf = module_from_spec(spec)
        sys.modules["bf"] = bf
        spec.loader.exec_module(bf)
        m = Chem.MolFromSmiles(smiles)
        n = m.GetNumAtoms()
        mace = bf.relax_ml(smiles, "mace")
        chgnet = bf.relax_ml(smiles, "chgnet")
        xtb = bf.xtb_run(smiles)
        pt = [mace["energy_ev"] / n, chgnet["energy_ev"] / n, xtb["homo_ev"]]
        in_hull = bool(tri.find_simplex(np.array(pt)) >= 0)
        return {
            "name": "candidate",
            "smiles": smiles,
            "n_atoms": n,
            "mace": mace,
            "chgnet": chgnet,
            "xtb": xtb,
            "point_per_atom": pt,
            "in_envelope": in_hull,
            "hull_ref": ENV.name,
        }

    if args.smiles:
        print(json.dumps(compute(args.smiles), ensure_ascii=False))
        return 0
    if args.funnel:
        files = [Path(p.strip()) for p in args.funnel.split(",")]
        mace = chgnet = xtb = None
        for f in files:
            d = json.loads(f.read_text(encoding="utf-8"))
            for c in d.get("candidates", []):
                if d.get("model") == "mace" and mace is None:
                    mace = c
                elif d.get("model") == "chgnet" and chgnet is None:
                    chgnet = c
                elif "homo_ev" in c.get("metrics", {}) and xtb is None:
                    xtb = c
        if not (mace and chgnet and xtb):
            raise SystemExit("need mace+chgnet+xtb candidate outputs; check schemas")
        smi = mace["smiles"]
        n = Chem.MolFromSmiles(smi).GetNumAtoms()
        pt = [mace["metrics"]["energy_ev"] / n, chgnet["metrics"]["energy_ev"] / n, xtb["metrics"]["homo_ev"]]
        print(json.dumps({
            "name": "candidate", "smiles": smi, "n_atoms": n,
            "point_per_atom": pt,
            "in_envelope": bool(tri.find_simplex(np.array(pt)) >= 0),
            "hull_ref": ENV.name,
        }, ensure_ascii=False))
        return 0
    ap.error("one of --smiles / --funnel required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
