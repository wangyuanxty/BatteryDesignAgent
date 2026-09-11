import json
import numpy as np
from scipy.spatial import Delaunay

env = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\known_set_sei\envelope_stats.json"))
pts = np.array([[p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]] for p in env["points"]])
tri = Delaunay(pts)
print("hull has", tri.nsimplex, "simplices; points:", len(pts))
inside = 0
outsiders = []
for i, p in enumerate(env["points"]):
    q = np.array([p["E_mace_per_atom"], p["E_chgnet_per_atom"], p["homo"]])
    s = tri.find_simplex(q)
    if s >= 0:
        inside += 1
    else:
        outsiders.append((p["name"], s))
print(f"self-test: {inside}/{len(pts)} of stored points are find_simplex>=0 (inside own hull)")
print("stored points reported OUTSIDE their own hull:")
for n, s in outsiders:
    print("  ", n, "-> simplex", s)

# explicit re-test of triflyl fluoride vertex
tf = [p for p in env["points"] if p["name"] == "triflyl fluoride"][0]
q = np.array([tf["E_mace_per_atom"], tf["E_chgnet_per_atom"], tf["homo"]])
print("triflyl find_simplex:", tri.find_simplex(q))

# also test tiny perturbation inward/outward
import itertools
for eps in (1e-9, 1e-6, 1e-4, 1e-3):
    q2 = q + np.array([eps, 0.0, 0.0])
    print(f"triflyl +[{eps},0,0] (higher energy):", tri.find_simplex(q2))
for eps in (1e-9, 1e-6, 1e-4, 1e-3):
    q2 = q - np.array([eps, 0.0, 0.0])
    print(f"triflyl -[{eps},0,0] (lower energy):", tri.find_simplex(q2))
