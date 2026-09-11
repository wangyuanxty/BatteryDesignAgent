"""Composition envelope adjudication for T9 (single pre-registered file).

Layer A0 (membership): is the formula a documented cathode material?
Layer A1 (hull): does the computed point lie outside the documented-members' hull?

Usage:
    python comp_envelope_check.py --formula "LiNi0.5Mn0.5O2"
    python comp_envelope_check.py --point 4.2 190 -1.5
    python comp_envelope_check.py --known-set runs/exp/known_set_comp/known_set_v2.json --formula "..."
Prints machine-readable JSON verdict (replayable).

The known set defaults to the v1 file (which the v8 arm was adjudicated against); the v9
contract points at known_set_v2.json explicitly, so the v8 record stays replayable.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

REPO = Path(__file__).resolve().parent
KNOWN_SET = REPO / "runs" / "exp" / "known_set_comp" / "known_set.json"


def _resolve(path: "str | Path | None") -> Path:
    return Path(path) if path else KNOWN_SET


def _load(path: "str | Path | None" = None) -> dict:
    return json.loads(_resolve(path).read_text(encoding="utf-8"))


def known_check(formula: str, path: "str | Path | None" = None) -> bool:
    """Membership layer (A0): is the formula a documented cathode material?"""
    return any(c["formula"] == formula for c in _load(path)["membership"])


def load(path: "str | Path | None" = None) -> tuple[Delaunay, dict]:
    ks = _load(path)
    pts = np.array([[p["V"], p["C"], p["stab"]] for p in ks["points"]])
    return Delaunay(pts), ks


def adjudicate(pt: list[float], name: str = "candidate",
               path: "str | Path | None" = None) -> dict:
    tri, ks = load(path)
    inside = bool(tri.find_simplex(np.array(pt)) >= 0)
    return {
        "name": name,
        "point": pt,
        "in_envelope": inside,
        "verdict": "REJECT (known-set analogue)" if inside else "PASS (outside envelope)",
        "hull_ref": _resolve(path).name,
        "n_points": ks["n_points"],
        "n_membership": ks["n_membership"],
    }


def main() -> int:
    argv = sys.argv[1:]
    known_set = None
    if "--known-set" in argv:
        i = argv.index("--known-set")
        known_set = argv[i + 1]
        del argv[i:i + 2]

    if argv and argv[0] == "--point":
        pt = [float(x) for x in argv[1:4]]
        print(json.dumps(adjudicate(pt, path=known_set), ensure_ascii=False))
        return 0
    if argv and argv[0] == "--formula":
        formula = argv[1]
        ks = _load(known_set)
        if known_check(formula, known_set):
            print(json.dumps({"name": formula, "formula": formula, "in_known": True,
                              "in_envelope": None,
                              "verdict": "REJECT (known composition)",
                              "hull_ref": _resolve(known_set).name,
                              "n_points": ks["n_points"],
                              "n_membership": ks["n_membership"],
                              "replayable": f'python comp_envelope_check.py --formula "{formula}"'},
                             ensure_ascii=False))
            return 0
        sys.path.insert(0, str(REPO / ".claude" / "skills" / "virtual-battery-factory" / "scripts"))
        from bda.simulators.comp_runner import run_composition_screen

        out = run_composition_screen({"candidates": [{"name": "candidate", "formula": formula}]})
        c = out["candidates"][0]
        if c.get("avg_voltage_v") is None:
            print(json.dumps({"error": c.get("error", "no voltage")}, ensure_ascii=False))
            return 1
        pt = [c["avg_voltage_v"], c.get("capacity_mah_g", 0), c.get("rel_stability_ev_atom", 0)]
        res = adjudicate(pt, formula, path=known_set)
        res["computed"] = c
        print(json.dumps(res, ensure_ascii=False))
        return 0
    print("usage: [--known-set PATH] --formula <f> | --point V C stab")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
