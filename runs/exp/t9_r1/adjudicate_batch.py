"""Mechanical adjudication of a run-comp output against the known-set layers.

Usage: python adjudicate_batch.py <screen_output.json> [B_threshold]
Prints per-candidate: A0 membership (exact formula), A1 hull verdict, B window verdict.
"""
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
KS = json.loads((REPO / "runs/exp/known_set_comp/known_set.json").read_text(encoding="utf-8"))
MEMBERSHIP = {c["formula"] for c in KS["membership"]}
from scipy.spatial import Delaunay
PTS = np.array([[p["V"], p["C"], p["stab"]] for p in KS["points"]])
TRI = Delaunay(PTS)

B_TH = float(sys.argv[2]) if len(sys.argv) > 2 else 5.3

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(f"{'candidate':<28} {'A0':<4} {'V':>8} {'C':>7} {'stab':>7} {'A1':<8} {'B':<3}")
for c in data["candidates"]:
    if c.get("error") or c.get("avg_voltage_v") is None:
        print(f"{c.get('name','?'):<28} ERR {c.get('error','')}")
        continue
    f = c["formula"]
    a0 = "REJ" if f in MEMBERSHIP else "ok "
    v, cap, s = c["avg_voltage_v"], c["capacity_mah_g"], c["rel_stability_ev_atom"]
    inside = bool(TRI.find_simplex(np.array([v, cap, s])) >= 0)
    a1 = "INSIDE" if inside else "OUTSIDE"
    b = "ok" if v >= B_TH else "no "
    flag = "  <== passes A0+A1+B" if (a0 == "ok " and not inside and v >= B_TH) else ""
    print(f"{c['name']:<28} {a0:<4} {v:>8.3f} {cap:>7.1f} {s:>7.3f} {a1:<8} {b:<3}{flag}")
