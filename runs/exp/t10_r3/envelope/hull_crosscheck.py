"""Cross-check: adjudicate hull + family gate from the bda funnel OUTPUTS.

The shipped envelope_check.py --funnel branch reads a top-level "model" key that
current bda run-mlp outputs do not carry (model is per-candidate; the branch fails
even on the pre-registered mace_out.json/chgnet_out.json/xtb_out.json - verified
verbatim). This script performs the mechanically identical adjudication on the
funnel outputs produced by the contract's commands (run-mlp mace/chgnet + run-xtb),
using the fixed script's own hull loader (load_tri) and family-gate function
(families_matched). Verdicts must agree with the --smiles path.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "runs" / "exp" / "known_set_sei"))

from envelope_check import load_tri, families_matched  # noqa: E402

KNOWN_SET = REPO / "runs" / "exp" / "known_set_sei" / "envelope_stats_v2.json"
FUNNEL = REPO / "runs" / "exp" / "t10_r3" / "funnel"

tri = load_tri(KNOWN_SET)
hull_pts = json.loads(KNOWN_SET.read_text(encoding="utf-8"))["points"]
print("known-set points:", len(hull_pts),
      "| min HOMO over known set:", min(p["homo"] for p in hull_pts))
print("known-set deepest:", max(hull_pts, key=lambda p: -p["homo"])["name"],
      min(p["homo"] for p in hull_pts))

CANDIDATES = ["pfta", "pfhex", "pftea", "pfpent", "ncf3"]
results = []
for k in CANDIDATES:
    mace = json.loads((FUNNEL / f"{k}_mace.json").read_text(encoding="utf-8"))["candidates"][0]
    chgnet = json.loads((FUNNEL / f"{k}_chgnet.json").read_text(encoding="utf-8"))["candidates"][0]
    xtb = json.loads((FUNNEL / f"{k}_xtb.json").read_text(encoding="utf-8"))["candidates"][0]
    smi = mace["smiles"]
    n_atoms = len(smi) and None
    from rdkit import Chem
    n = Chem.MolFromSmiles(smi).GetNumAtoms()
    pt = [mace["metrics"]["energy_ev"] / n, chgnet["metrics"]["energy_ev"] / n,
          xtb["metrics"]["homo_ev"]]
    in_hull = bool(tri.find_simplex(pt) >= 0)
    fams = families_matched(smi)
    results.append({"candidate": k, "smiles": smi, "n_atoms": n,
                    "point_per_atom": pt, "in_envelope": in_hull,
                    "in_documented_families": bool(fams), "families_matched": fams,
                    "hull_ref": KNOWN_SET.name})
    print(k, "| in_envelope=", in_hull, "| families_matched=", fams,
          "| point_per_atom=", [round(x, 5) for x in pt])

out = REPO / "runs" / "exp" / "t10_r3" / "envelope" / "crosscheck_from_bda_outputs.json"
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", out.name)
