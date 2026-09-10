"""Extend known_set_comp with documented high-voltage spinel cathodes (envelope sealing, v8 T9).

Runs run_composition_screen (CHGNet, py312 CUDA env) on the documented spinel family
so their computed points enter the pre-registered hull: known members must be
measured by the same machine as candidates (T10-style closure).

Usage: D:/anaconda/envs/py312/python.exe extend_spinels_screen.py
"""
import json
import sys

sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent/.claude/skills/virtual-battery-factory/scripts")
from bda.simulators.comp_runner import run_composition_screen  # noqa: E402

SPINELS = [
    {"name": "LMO",       "formula": "LiMn2O4"},
    {"name": "LNMO",      "formula": "LiNi0.5Mn1.5O4"},
    {"name": "LCMO",      "formula": "LiCoMnO4"},
    {"name": "LiCrMnO4",  "formula": "LiCrMnO4"},
    {"name": "LiNiVO4",   "formula": "LiNiVO4"},
    {"name": "LiCuMn",    "formula": "LiCu0.5Mn1.5O4"},
]

out = run_composition_screen({"candidates": SPINELS})
json.dump(out, open("runs/exp/known_set_comp/comp_out_spinels.json", "w"), indent=2)
for c in out.get("candidates", []):
    if c.get("avg_voltage_v") is not None:
        print("%-12s V=%.3f C=%.0f stab=%.3f conv=%s" % (
            c.get("name"), c["avg_voltage_v"], c.get("capacity_mah_g") or 0,
            c.get("rel_stability_ev_atom") or 0, c.get("converged")), flush=True)
    else:
        print("NONE:", c.get("name"), str(c.get("error"))[:120], flush=True)
