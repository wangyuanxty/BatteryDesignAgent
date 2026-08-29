"""Scratch: compact summary table over candidates x systems. Usage: scratch_summary.py <glob>"""
import json, sys, glob

pat = sys.argv[1] if len(sys.argv) > 1 else "runs/exp/t5_r1/cell/r3*_energy.json"

print(f"{'candidate':34s} {'ED_wh/kg':>10s} {'E_wh':>8s} {'mass_g':>8s} {'cap_Ah':>7s} {'Tmax_K':>8s} {'anode_min':>9s} {'plated':>7s} {'model':>14s}")
for e in sorted(glob.glob(pat)):
    norm = e.replace("\\", "/")
    tag = norm.split("_energy")[0].split("cell/")[1]
    d = json.load(open(e, encoding="utf-8-sig"))
    f4 = e.replace("_energy.json", "_4c_dfn.json")
    d4 = json.load(open(f4, encoding="utf-8-sig"))
    amin = min(d4["anode_potential_v"]) if "anode_potential_v" in d4 else float("nan")
    print(f"{tag:34s} {d['energy_density_wh_kg']:10.2f} {d['energy_wh']:8.3f} {d['mass_kg']*1000:8.2f} {d['capacity_ah']:7.3f} {d4['T_max_K']:8.2f} {amin:9.4f} {str(amin<0):>7s} {d4['model_used']:>14s}")
    t = d4["time_s"]; v = d4["voltage_v"]
    imin = v.index(min(v))
    print(f"    charge seg {t[-1]-t[imin]:.1f}s -> accepted {(t[-1]-t[imin])*20/3600:.2f} Ah (physical)")
