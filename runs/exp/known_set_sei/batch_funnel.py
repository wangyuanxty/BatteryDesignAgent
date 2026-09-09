"""Batch funnel over the pre-registered known SEI-additive set (T10 v2).

Runs the SAME three-model screening as the protocol's molecular funnel
(run-mlp mace / run-mlp chgnet / run-xtb) over every compound in
known_additives.json, with identical algorithms (RDKit embed seed 42 +
MMFF pre-optimization, BFGS fmax=0.05 steps=50) but on CUDA for the two
ML potentials. Outputs are written in the run-mlp / run-xtb schema so the
known set and future candidates are judged in exactly one口径.

Usage:
    python batch_funnel.py --smoke 2     # time-check on first N molecules
    python batch_funnel.py               # full batch, resumable
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
XTB_DIR = Path("D:/research/tools/xtb/xtb-6.6.1/bin")

# xtb is resolved via shutil.which inside xtb_runner; patch PATH first.
os.environ["PATH"] = str(XTB_DIR) + os.pathsep + os.environ.get("PATH", "")
sys.path.insert(
    0, str(REPO / ".claude" / "skills" / "virtual-battery-factory" / "scripts")
)


def relax_ml(smiles: str, model: str) -> dict[str, Any]:
    from rdkit import Chem
    from rdkit.Chem import AllChem

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"invalid SMILES: {smiles!r}")
    mol = Chem.AddHs(mol)
    if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
        raise RuntimeError(f"failed to embed 3D structure for {smiles}")
    AllChem.MMFFOptimizeMolecule(mol)
    from ase import Atoms
    from ase.io import read as ase_read
    from io import StringIO

    xyz = Chem.MolToXYZBlock(mol)
    atoms = ase_read(StringIO(xyz), format="xyz")
    if model == "mace":
        from mace.calculators import mace_mp

        calc = mace_mp(model="medium", device="cuda")
    else:
        atoms.cell = [20.0, 20.0, 20.0]
        atoms.pbc = True
        atoms.center()
        from chgnet.model.dynamics import CHGNetCalculator

        try:
            calc = CHGNetCalculator(device="cuda")
        except TypeError:  # very old chgnet: no device kwarg
            calc = CHGNetCalculator()
    atoms.calc = calc
    from ase.optimize import BFGS

    opt = BFGS(atoms)
    converged = bool(opt.run(fmax=0.05, steps=50))
    return {
        "energy_ev": float(atoms.get_potential_energy()),
        "converged": converged,
    }


def xtb_run(smiles: str) -> dict[str, Any]:
    from bda.simulators.xtb_runner import xtb_single_point

    return xtb_single_point(smiles)


def deliverable_schema(model: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Match run-mlp / run-xtb output schema."""
    out = {"candidates": []}
    for row in rows:
        if model == "xtb":
            entry = {
                "smiles": row["smiles"],
                "metrics": {
                    "homo_ev": row["xtb"]["homo_ev"],
                    "lumo_ev": row["xtb"]["lumo_ev"],
                },
            }
        else:
            entry = {
                "smiles": row["smiles"],
                "metrics": {
                    "energy_ev": row[model]["energy_ev"],
                    "converged": row[model]["converged"],
                },
                "model": model,
            }
        out["candidates"].append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", type=int, default=0)
    args = ap.parse_args()

    work = REPO / "runs" / "exp" / "known_set_sei"
    entries = json.loads((work / "known_additives.json").read_text(encoding="utf-8"))
    prog_path = work / "progress.jsonl"
    done: dict[str, dict[str, Any]] = {}
    if prog_path.exists():
        for line in prog_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["name"]] = r

    if args.smoke:
        entries = entries[: args.smoke]
    print(f"known additives: {len(entries)} (fresh={sum(1 for e in entries if e['name'] not in done)})",
          flush=True)

    for i, e in enumerate(entries, 1):
        name, smiles = e["name"], e["smiles"]
        if name in done and not args.smoke:
            continue
        t0 = time.time()
        rec: dict[str, Any] = {"name": name, "smiles": smiles}
        try:
            rec["mace"] = relax_ml(smiles, "mace")
        except Exception as ex:  # noqa: BLE001 - batch must not die on one molecule
            rec["mace"] = {"error": f"{type(ex).__name__}: {str(ex)[:200]}"}
        try:
            rec["chgnet"] = relax_ml(smiles, "chgnet")
        except Exception as ex:  # noqa: BLE001
            rec["chgnet"] = {"error": f"{type(ex).__name__}: {str(ex)[:200]}"}
        try:
            rec["xtb"] = xtb_run(smiles)
        except Exception as ex:  # noqa: BLE001
            rec["xtb"] = {"error": f"{type(ex).__name__}: {str(ex)[:200]}"}
        rec["elapsed_s"] = round(time.time() - t0, 1)
        with prog_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok = all(isinstance(rec[k], dict) and "error" not in rec[k] for k in ("mace", "chgnet", "xtb"))
        print(f"[{i}/{len(entries)}] {name}: {'OK' if ok else 'ERRORS'} "
              f"(mace={rec['mace'].get('energy_ev', '?')}, "
              f"chgnet={rec['chgnet'].get('energy_ev', '?')}, "
              f"xtb-homo={rec['xtb'].get('homo_ev', '?')}, {rec['elapsed_s']}s)", flush=True)

    prog = [
        json.loads(l)
        for l in prog_path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ] if prog_path.exists() else []
    complete = [p for p in prog if all(isinstance(p.get(k), dict) and "error" not in p[k]
                                       for k in ("mace", "chgnet", "xtb"))]
    (work / "mace_out.json").write_text(
        json.dumps(deliverable_schema("mace", complete), indent=2), encoding="utf-8")
    (work / "chgnet_out.json").write_text(
        json.dumps(deliverable_schema("chgnet", complete), indent=2), encoding="utf-8")
    (work / "xtb_out.json").write_text(
        json.dumps(deliverable_schema("xtb", complete), indent=2), encoding="utf-8")
    print(f"DONE: {len(complete)}/{len(prog)} complete; elapsed total via progress.jsonl", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
