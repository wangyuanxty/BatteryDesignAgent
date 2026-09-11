"""Adjudicate all round-1 both-window passers with envelope_check (v2 known set).

Same code path as the CLI `envelope_check.py --known-set envelope_stats_v2.json --smiles S`
(imports batch_funnel, runs mace/chgnet on CUDA + xtb, Delaunay hull test, family gate).
Writes one JSON record per candidate to adjudication_r1.jsonl.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
from rdkit import Chem

REPO = Path(r"D:/research/degradation_prognostics/Battery_Design_Agent")
sys.path.insert(0, str(REPO / "runs/exp/known_set_sei"))
from envelope_check import families_matched, load_tri
from batch_funnel import relax_ml, xtb_run

KNOWN = REPO / "runs/exp/known_set_sei/envelope_stats_v2.json"
tri = load_tri(KNOWN)


def compute(smiles: str) -> dict:
    """Identical code path to envelope_check.py --smiles (load_tri + batch_funnel + Delaunay + gate)."""
    m = Chem.MolFromSmiles(smiles)
    n = m.GetNumAtoms()
    mace = relax_ml(smiles, "mace")
    chgnet = relax_ml(smiles, "chgnet")
    xtb = xtb_run(smiles)
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
        "hull_ref": KNOWN.name,
        "in_documented_families": bool(fams),
        "families_matched": fams,
    }

PASSERS = [
    ("trifluoromethyl hypofluorite", "FOC(F)(F)F"),
    ("hexafluoro-2-butyne", "FC(F)(F)C#CC(F)(F)F"),
    ("perfluorosuccinyl difluoride", "O=C(F)C(F)(F)C(F)(F)C(=O)F"),
    ("pentafluoropropionyl fluoride", "O=C(F)C(F)(F)C(F)(F)F"),
    ("carbonyl difluoride", "O=C(F)F"),
    ("trifluoroacetyl fluoride", "O=C(F)C(F)(F)F"),
    ("hexafluoroacetone N-(trifluoromethyl)imine", "FC(F)(F)C(=NC(F)(F)F)C(F)(F)F"),
    ("perfluoroglutaric anhydride", "O=C1OC(=O)C(F)(F)C(F)(F)C1(F)F"),
    ("perfluoro-2-butanone", "O=C(C(F)(F)F)C(F)(F)F"),
    ("difluoromalonyl difluoride", "O=C(F)C(F)(F)C(=O)F"),
    ("trifluoromethyl isocyanate", "O=C=NC(F)(F)F"),
    ("trifluoroacetic anhydride", "O=C(OC(=O)C(F)(F)F)C(F)(F)F"),
    ("bis(trifluoromethyl)maleic anhydride", "O=C1OC(=O)C(C(F)(F)F)=C1C(F)(F)F"),
    ("fluoroformic anhydride", "O=C(F)OC(=O)F"),
    ("perfluorosuccinic anhydride", "O=C1OC(=O)C(F)(F)C1(F)F"),
    ("perfluorocyclobutene", "FC1=C(F)C(F)(F)C1(F)F"),
]

out_path = REPO / "runs/exp/t10_r4/adjudication_r1.jsonl"
out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open("a", encoding="utf-8") as fh:
    for name, smi in PASSERS:
        t0 = time.time()
        try:
            rec = compute(smi)
            rec["proposed_name"] = name
            line = json.dumps(rec, ensure_ascii=False)
        except Exception as e:
            rec = {"proposed_name": name, "smiles": smi, "error": f"{type(e).__name__}: {str(e)[:300]}"}
            line = json.dumps(rec, ensure_ascii=False)
        fh.write(line + "\n")
        fh.flush()
        ok = "error" not in rec
        if ok:
            print(f"{name:44s} in_env={rec['in_envelope']} fams={rec['families_matched']} "
                  f"homo={rec['xtb']['homo_ev']:.4f} lumo={rec['xtb']['lumo_ev']:.4f} "
                  f"mace={rec['mace'].get('energy_ev','?'):.3f} chg={rec['chgnet'].get('energy_ev','?'):.3f} "
                  f"mace_conv={rec['mace'].get('converged')} chg_conv={rec['chgnet'].get('converged')} "
                  f"{time.time()-t0:.1f}s", flush=True)
        else:
            print(f"{name:44s} ERROR: {rec['error'][:120]}", flush=True)
print("done", flush=True)
