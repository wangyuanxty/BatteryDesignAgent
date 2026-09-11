"""Sanity-check the 82-point envelope Delaunay for degeneracy (self-containment test).

- Importers/callers: invoked manually from this workspace (headless session); no module imports it.
- Affected API: none. Reads envelope_stats.json; prints diagnostics to stdout only.
- Data schemas: input = runs/exp/known_set_sei/envelope_stats.json {"points":[{"name","smiles","E_mace_per_atom","E_chgnet_per_atom","homo"}], "hull_vertices_idx":[...], "n":82}.
- Verbatim instruction: "candidate computed point must lie OUTSIDE the 82-point convex hull ...
  adjudicated by envelope_check.py, Delaunay outside test, machine-readable verdict".
"""
import json
import numpy as np
from scipy.spatial import Delaunay
from pathlib import Path

env = json.loads(Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\known_set_sei\envelope_stats.json").read_text(encoding="utf-8"))
pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
tri = Delaunay(pts)
s = tri.find_simplex(pts)
inside = int(np.sum(s >= 0))
print("n_points", len(pts))
print("n_inside_own_hull", inside)
print("n_outside_own_hull", int(len(pts) - inside))
for i in range(len(pts)):
    if s[i] < 0:
        p = env["points"][i]
        print("OUTLIER idx", i, p["name"], p["smiles"], "simplex", int(s[i]))
print("hull_vertices_idx", env["hull_vertices_idx"])
print("n_hull_vertices", len(env["hull_vertices_idx"]))
print("mace_range", float(pts[:, 0].min()), float(pts[:, 0].max()))
print("chgnet_range", float(pts[:, 1].min()), float(pts[:, 1].max()))
print("homo_range", float(pts[:, 2].min()), float(pts[:, 2].max()))
