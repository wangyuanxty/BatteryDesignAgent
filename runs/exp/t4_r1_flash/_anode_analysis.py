"""Analyze anode potential series: where does the min occur (discharge vs charge leg)?
Also print voltage vs time around the min and the crossing points below 0 V."""
import json, sys
import numpy as np

f = sys.argv[1]
d = json.load(open(f, encoding="utf-8"))
t = np.array(d["time_s"])
v = np.array(d["voltage_v"])
ap = np.array(d["anode_potential_v"])
imin = int(np.argmin(ap))
print(f"{f}: len={len(t)}, t_end={t[-1]:.1f} s")
print(f"  anode min = {ap[imin]:.4f} V at t={t[imin]:.1f} s, V={v[imin]:.3f} V")
# below-zero crossings
below = ap < 0
if below.any():
    idx = np.where(below)[0]
    print(f"  below 0 V: {len(idx)} pts, t range {t[idx[0]]:.1f}..{t[idx[-1]]:.1f} s")
    # voltage at first and last below-zero
    print(f"  V at first below-0: {v[idx[0]]:.3f} V (t={t[idx[0]]:.1f}s), V at last below-0: {v[idx[-1]]:.3f} V (t={t[idx[-1]]:.1f}s)")
    # where is the first below-zero relative to end of discharge leg (~ last time before charge)?
    # charge leg starts when voltage rises again after reaching ~2.5V; find min voltage index
    ivmin = int(np.argmin(v))
    print(f"  cell V min = {v[ivmin]:.3f} V at t={t[ivmin]:.1f} s -> discharge leg ends ~ t={t[ivmin]:.1f}s")
    print(f"  first below-0 at t={t[idx[0]]:.1f}s vs discharge-end t={t[ivmin]:.1f}s -> {'CHARGE leg' if t[idx[0]] > t[ivmin] else 'DISCHARGE leg'}")
else:
    print("  never below 0")
