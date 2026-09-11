"""T10 v4 mapping executor: k(M) = k0 * 10^((HOMO_xTB(M) + 12.5)/1.0).

Declared screening rule, executed by code from the funnel outputs (no free parameters).
k0 = 1e-12 m/s = Chen2020 baseline 'SEI kinetic rate constant [m.s-1]' (pybamm dump).

Usage:
    python mapping.py --xtb <xtb_out.json> --name <candidate_name>   # run-xtb schema
    python mapping.py --env <envelope_check_output.json>             # envelope_check schema (point_per_atom[2]=homo)
"""
import argparse
import json
import sys
from pathlib import Path

K0 = 1e-12  # m/s, Chen2020 baseline
HOMO_0 = -12.5
SLOPE = 1.0  # per eV


def factor(homo_ev: float) -> float:
    return 10.0 ** ((homo_ev - HOMO_0) / SLOPE)


def k_m_s(homo_ev: float) -> float:
    return K0 * factor(homo_ev)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--xtb", help="run-xtb output JSON")
    ap.add_argument("--env", help="envelope_check output JSON")
    ap.add_argument("--name", default=None, help="candidate name filter (xtb mode)")
    args = ap.parse_args()

    if args.env:
        d = json.loads(Path(args.env).read_text(encoding="utf-8"))
        homo = d["point_per_atom"][2]
        name = d.get("name", "candidate")
        smiles = d.get("smiles", "")
    elif args.xtb:
        d = json.loads(Path(args.xtb).read_text(encoding="utf-8"))
        rows = [c for c in d["candidates"] if args.name is None or c.get("name") == args.name or c["smiles"] == args.name]
        if not rows:
            print("no matching candidate", file=sys.stderr)
            return 2
        row = rows[0]
        homo = row["metrics"]["homo_ev"]
        name = row.get("name", row["smiles"])
        smiles = row["smiles"]
    else:
        ap.error("one of --xtb / --env required")
        return 2

    f = factor(homo)
    k = k_m_s(homo)
    out = {
        "name": name,
        "smiles": smiles,
        "homo_ev": homo,
        "mapping": {
            "rule": "k(M) = k0 * 10^((HOMO_xTB(M) + 12.5)/1.0)",
            "k0_m_s": K0,
            "factor": f,
            "k_m_s": k,
            "param": {"SEI kinetic rate constant [m.s-1]": k},
            "calibration": [
                {"homo_ev": -12.5, "factor": factor(-12.5), "sei_nm": 449.12},
                {"homo_ev": -13.5, "factor": factor(-13.5), "sei_nm": 385.10},
            ],
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
