"""Envelope adjudication for T10 (layer A): is the candidate inside the fixed
82-compound convex hull?  The same script also checks the documented-family gate
(layer B) added with the T10 v3 contract: a candidate that matches any of the
family-defining substructures of the documented additives is not "outside the
systems we have already screened".

The known set defaults to the 82-compound envelope the T10 v2 run was adjudicated
against (envelope_stats.json); the v3 contract points at envelope_stats_v2.json
(82 documented + the 5 candidates the v2 run found, folded in before the run), so
the v2 record stays replayable.

Usage:
    python envelope_check.py --smiles "SMILES"
    python envelope_check.py --funnel <mace_out.json,chgnet_out.json,xtb_out.json>
    python envelope_check.py --known-set envelope_stats_v2.json --smiles "SMILES"

Prints strictly machine-readable JSON: {"name", "in_envelope": bool,
"point_per_atom": [...], "hull_ref": "...", "in_documented_families": bool,
"families_matched": [...]}.
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

# Documented-family gate: each pattern is the mechanical definition of one family
# present in the 82-compound known set (self-checked: every documented molecule
# matches at least one pattern, and the known-set-external candidates of the
# feasibility probe match none).
FAMILY_GATE: dict[str, str] = {
    "nitrile": "C#N",
    "S=O (sulfoxide/sulfone/sulfite/sulfate/sulfonyl_F)": "[#16]=O",
    "ester": "[CX3](=O)[OX2][CX4,c]",
    "carbonate": "[CX3](=O)([OX2])[OX2]",
    "aromatic_ring": "a",
    "dialkyl_ether": "[OD2]([CX4])[CX4]",
    "boron": "[#5]",
    "silicon": "[#14]",
    "amide": "[CX3](=O)[NX3]",
    "nitro": "[$([NX3](=O)=O),$([N+](=O)[O-])]",
    "quinone": "O=C1C=CC(=O)C=C1",
    "phosphite_P3": "[PX3]",
    "phosphate_P5": "[PX4]=O",
}
_GATE_PATTERNS = {k: Chem.MolFromSmarts(v) for k, v in FAMILY_GATE.items()}


def families_matched(smiles: str) -> list[str]:
    """Names of the documented families the molecule belongs to (empty = outside)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    return [name for name, pat in _GATE_PATTERNS.items()
            if pat is not None and mol.HasSubstructMatch(pat)]


def load_tri(known_set: Path | None = None) -> Delaunay:
    env = json.loads((known_set or ENV).read_text(encoding="utf-8"))
    pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
    return Delaunay(pts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smiles")
    ap.add_argument("--funnel", help="same-schema mace+chgnet+xtb output JSON(s), comma-separated")
    ap.add_argument("--known-set", dest="known_set", default=None,
                    help="known-set JSON (default: envelope_stats.json, the v2 record)")
    args = ap.parse_args()

    known = Path(args.known_set) if args.known_set else ENV
    tri = load_tri(known)

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
        fams = families_matched(smiles)
        return {
            "name": "candidate",
            "smiles": smiles,
            "n_atoms": n,
            "mace": mace,
            "chgnet": chgnet,
            "xtb": xtb,
            "point_per_atom": pt,
            "in_envelope": in_hull,
            "hull_ref": known.name,
            "in_documented_families": bool(fams),
            "families_matched": fams,
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
        fams = families_matched(smi)
        print(json.dumps({
            "name": "candidate", "smiles": smi, "n_atoms": n,
            "point_per_atom": pt,
            "in_envelope": bool(tri.find_simplex(np.array(pt)) >= 0),
            "hull_ref": known.name,
            "in_documented_families": bool(fams),
            "families_matched": fams,
        }, ensure_ascii=False))
        return 0
    ap.error("one of --smiles / --funnel required")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
