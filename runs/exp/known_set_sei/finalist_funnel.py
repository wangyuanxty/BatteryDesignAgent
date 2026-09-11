"""Authoritative finalist funnel: run the pre-registered three-model funnel on
the chosen candidate and write deliverable-schema JSONs (mace/chgnet/xtb) that
envelope_check.py --funnel can adjudicate, plus a raw details file for the
report (incl. xtb total energy).

Finalist: pentafluoroethylsulfonyl fluoride (perfluoroethanesulfonyl fluoride),
SMILES FS(=O)(=O)C(F)(F)C(F)(F)F  — the C2F5 homolog of the documented-deepest
triflyl fluoride (CF3SO2F, HOMO -14.1428), designed to push the xTB HOMO deeper
while staying on the sulfonyl-fluoride SEI-forming motif.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CASE = Path(r"C:\c1_control\runs\c1_t10_r1")

spec = importlib.util.spec_from_file_location(
    "bf", REPO / "runs" / "exp" / "known_set_sei" / "batch_funnel.py"
)
bf = importlib.util.module_from_spec(spec)
sys.modules["bf"] = bf
spec.loader.exec_module(bf)  # noqa: S404

FINALIST = {
    "name": "pentafluoroethylsulfonyl fluoride",
    "smiles": "FS(=O)(=O)C(F)(F)C(F)(F)F",
}


def main() -> int:
    smiles = FINALIST["smiles"]
    row = {"smiles": smiles}
    row["mace"] = bf.relax_ml(smiles, "mace")
    row["chgnet"] = bf.relax_ml(smiles, "chgnet")
    row["xtb"] = bf.xtb_run(smiles)

    # deliverable-schema files (same schema as run-mlp / run-xtb)
    (CASE / "mace_finalist.json").write_text(
        json.dumps(bf.deliverable_schema("mace", [row]), indent=2), encoding="utf-8"
    )
    (CASE / "chgnet_finalist.json").write_text(
        json.dumps(bf.deliverable_schema("chgnet", [row]), indent=2), encoding="utf-8"
    )
    (CASE / "xtb_finalist.json").write_text(
        json.dumps(bf.deliverable_schema("xtb", [row]), indent=2), encoding="utf-8"
    )
    # raw details incl. total energy for the report / hard funnel line
    (CASE / "funnel_details.json").write_text(
        json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
