"""Adjudicate every round-1 candidate through envelope_check.py (Delaunay
outside test) verbatim, one candidate per file triple, and collect the
machine-readable verdicts.

This script does NOT re-run any simulation: it slices the already-computed
round1_mace/chgnet/xtb.json outputs into the single-candidate schema that
runs/exp/known_set_sei/envelope_check.py --funnel expects, and shells out to
that exact adjudicator for each candidate.

- Importers/callers: invoked manually from this workspace (headless session,
  no other module imports it).
- Affected API: none. Reads round1_*.json in candidates/; writes
  envelope_verdicts.json in this workspace; shells out to the pre-registered
  envelope_check.py.
- Data schemas: input = the bda run-mlp / run-xtb output schema
  ({"model", "candidates":[{"smiles","metrics"}]}); output =
  {"verdicts":[{"smiles","point_per_atom","in_envelope","hull_ref",...}]}.
- Verbatim instruction: "candidate computed point ... must lie OUTSIDE the
  82-point convex hull ... adjudicated by runs/exp/known_set_sei/
  envelope_check.py, Delaunay outside test, machine-readable verdict".
"""
import json
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent
REPO = WS.parents[2]
ENV_CHECK = REPO / "runs" / "exp" / "known_set_sei" / "envelope_check.py"
PY = sys.executable


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def by_smiles(d):
    return {c["smiles"]: c for c in d["candidates"]}


mace = load(WS / "candidates" / "round1_mace.json")
chgnet = load(WS / "candidates" / "round1_chgnet.json")
xtb = load(WS / "candidates" / "round1_xtb.json")

M = by_smiles(mace)
C = by_smiles(chgnet)
X = by_smiles(xtb)

tmp = WS / "envelope_tmp"
tmp.mkdir(exist_ok=True)

results = []
for i, smi in enumerate(M, 1):
    fm = tmp / f"{i}_mace.json"
    fc = tmp / f"{i}_chgnet.json"
    fx = tmp / f"{i}_xtb.json"
    fm.write_text(json.dumps({"model": "mace", "candidates": [M[smi]]}), encoding="utf-8")
    fc.write_text(json.dumps({"model": "chgnet", "candidates": [C[smi]]}), encoding="utf-8")
    fx.write_text(json.dumps({"candidates": [X[smi]]}), encoding="utf-8")
    out = subprocess.run(
        [PY, str(ENV_CHECK), "--funnel", f"{fm},{fc},{fx}"],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        results.append({"smiles": smi, "error": out.stderr.strip()})
        continue
    verdict = json.loads(out.stdout.strip())
    results.append(verdict)

(WS / "envelope_verdicts.json").write_text(
    json.dumps({"verdicts": results}, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({"verdicts": results}, ensure_ascii=False, indent=2))
