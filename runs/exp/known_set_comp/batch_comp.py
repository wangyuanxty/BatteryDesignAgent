"""Batch comp screen, verbose-unbuffered: per-candidate progress to stdout."""
import json
import sys
import time

sys.path.insert(0, "D:/research/degradation_prognostics/Battery_Design_Agent/.claude/skills/virtual-battery-factory/scripts")
from bda.simulators.comp_runner import run_composition_screen  # noqa: E402

data = json.load(open("runs/exp/known_set_comp/known_compositions.json", encoding="utf-8"))
print("total candidates:", len(data), flush=True)
t0 = time.time()
out = run_composition_screen({"candidates": data})
json.dump(out, open("runs/exp/known_set_comp/comp_out.json", "w"), indent=2)
cs = out.get("candidates", [])
ok = [c for c in cs if c.get("avg_voltage_v") is not None]
print("done %d with V / %d in %.0fs" % (len(ok), len(cs), time.time() - t0), flush=True)
for c in sorted(ok, key=lambda x: -x["avg_voltage_v"]):
    print("%-16s V=%.3f C=%.0f stab=%.2f conv=%s" % (
        c.get("name"), c["avg_voltage_v"] or 0, c.get("capacity_mah_g") or 0,
        c.get("rel_stability_ev_atom") or 0, c.get("converged")), flush=True)
for c in cs:
    if c.get("avg_voltage_v") is None:
        print("NONE:", c.get("name"), str(c.get("error"))[:120], flush=True)
