"""Generate per-candidate funnel input files for the t10_r3 candidate panel.

One candidate per input file so that envelope_check.py --funnel (which reads the
FIRST candidate of each mace/chgnet/xtb output) adjudicates exactly one molecule.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

CANDIDATES = [
    ("pfta", "perfluorotributylamine",
     "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)N(C(F)(F)C(F)(F)C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F"),
    ("pfhex", "perfluorohexane",
     "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F"),
    ("pftea", "tris(pentafluoroethyl)amine (perfluorotriethylamine)",
     "FC(F)(F)C(F)(F)N(C(F)(F)C(F)(F)F)C(F)(F)C(F)(F)F"),
    ("pfpent", "perfluoropentane",
     "FC(F)(F)C(F)(F)C(F)(F)C(F)(F)C(F)(F)F"),
    ("ncf3", "tris(trifluoromethyl)amine",
     "FC(F)(F)N(C(F)(F)F)C(F)(F)F"),
    ("sf6", "sulfur hexafluoride",
     "FS(F)(F)(F)(F)F"),
]

for key, name, smiles in CANDIDATES:
    out = HERE / f"{key}_in.json"
    out.write_text(json.dumps({"candidates": [{"smiles": smiles, "name": name}]}, indent=2),
                   encoding="utf-8")
    print(f"wrote {out.name}")
