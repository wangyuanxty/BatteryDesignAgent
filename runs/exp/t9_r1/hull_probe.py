"""Map the known-set envelope: where is the outside region in (V, C, stab) space?"""
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
KS = json.loads((REPO / "runs/exp/known_set_comp/known_set.json").read_text(encoding="utf-8"))

pts = np.array([[p["V"], p["C"], p["stab"]] for p in KS["points"]])
names = [p["name"] for p in KS["points"]]
print("n points:", len(pts))
print("V  range: %.3f .. %.3f" % (pts[:, 0].min(), pts[:, 0].max()))
print("C  range: %.3f .. %.3f" % (pts[:, 1].min(), pts[:, 1].max()))
print("stab range: %.3f .. %.3f" % (pts[:, 2].min(), pts[:, 2].max()))
imax = int(np.argmax(pts[:, 2]))
print("max stab: %.4f at %s" % (pts[imax, 2], names[imax]))
imaxv = int(np.argmax(pts[:, 0]))
print("max V: %.4f at %s" % (pts[imaxv, 0], names[imaxv]))

from scipy.spatial import Delaunay
tri = Delaunay(pts)

def inside(v, c, s):
    return bool(tri.find_simplex(np.array([v, c, s])) >= 0)

# probe grid
print("\n-- probe: inside/outside over grid --")
print("V=5.5 (Ni-olivine band), C=117, stab from -2.5..-1.2:")
for s in (-2.5, -2.2, -2.0, -1.8, -1.5, -1.2):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(5.5, 117.0, s) else "OUTSIDE"))
print("V=6.5, C=115:")
for s in (-2.5, -2.2, -2.0, -1.8, -1.5, -1.2):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(6.5, 115.0, s) else "OUTSIDE"))
print("V=7.0, C=114:")
for s in (-2.5, -2.0, -1.5, -1.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(7.0, 114.0, s) else "OUTSIDE"))
print("spinel band V=8.3, C=103:")
for s in (-0.9, -0.5, -0.3, -0.1, 0.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(8.3, 103.0, s) else "OUTSIDE"))
print("spinel band V=8.5, C=105:")
for s in (-0.9, -0.5, -0.2, 0.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(8.5, 105.0, s) else "OUTSIDE"))
print("layered high-V V=4.5, C=190:")
for s in (-2.5, -1.5, -1.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(4.5, 190.0, s) else "OUTSIDE"))
print("mixed V=5.3, C=140:")
for s in (-2.5, -1.5, -1.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(5.3, 140.0, s) else "OUTSIDE"))
print("mixed V=5.3, C=160:")
for s in (-2.5, -1.5, -1.0):
    print("  stab %.1f -> %s" % (s, "INSIDE" if inside(5.3, 160.0, s) else "OUTSIDE"))
