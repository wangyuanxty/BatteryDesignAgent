"""Composition envelope adjudication for T9 (single pre-registered file).

Layer A0 (membership): is the formula a documented cathode material?
Layer A1 (hull): does the computed point lie outside the documented-members' hull?

Usage:
    python comp_envelope_check.py --formula "LiNi0.5Mn0.5O2"
    python comp_envelope_check.py --point 4.2 190 -1.5
Prints machine-readable JSON verdict (replayable).
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

REPO = Path(__file__).resolve().parent
KNOWN_SET = REPO / "runs" / "exp" / "known_set_comp" / "known_set.json"


def _load() -> dict:
    return json.loads(KNOWN_SET.read_text(encoding="utf-8"))


def known_check(formula: str) -> bool:
    """Membership layer (A0): is the formula a documented cathode material?"""
    return any(c["formula"] == formula for c in _load()["membership"])


def load() -> tuple[Delaunay, dict]:
    ks = _load()
    pts = np.array([[p["V"], p["C"], p["stab"]] for p in ks["points"]])
    return Delaunay(pts), ks


def adjudicate(pt: list[float], name: str = "candidate") -> dict:
    tri, ks = load()
    inside = bool(tri.find_simplex(np.array(pt)) >= 0)
    return {
        "name": name,
        "point": pt,
        "in_envelope": inside,
        "verdict": "REJECT (known-set analogue)" if inside else "PASS (outside envelope)",
        "hull_ref": KNOWN_SET.name,
        "n_points": ks["n_points"],
        "n_membership": ks["n_membership"],
    }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--point":
        pt = [float(x) for x in sys.argv[2:5]]
        print(json.dumps(adjudicate(pt), ensure_ascii=False))
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "--formula":
        formula = sys.argv[2]
        if known_check(formula):
            ks = _load()
            print(json.dumps({"name": formula, "formula": formula, "in_known": True,
                              "in_envelope": None,
                              "verdict": "REJECT (known composition)",
                              "hull_ref": KNOWN_SET.name,
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
        res = adjudicate(pt, formula)
        res["computed"] = c
        print(json.dumps(res, ensure_ascii=False))
        return 0
    print("usage: --formula <f> | --point V C stab")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
