"""Trace X1 4C: where does min_ap happen?"""
import json

s = json.load(open(r"runs\exp\t5_r3\cell\r4_x1_4c_45c.json", encoding="utf-8"))
t, v, ap = s["time_s"], s["voltage_v"], s["anode_potential_v"]
jumps = [i for i in range(1, len(v)) if v[i] - v[i - 1] > 0.05]
i0 = jumps[-1]
print("charge start idx", i0, "t", round(t[i0], 1), "v", round(v[i0], 3))
imin = ap.index(min(ap))
print("min_ap", round(min(ap), 4), "at idx", imin, "t", round(t[imin], 1),
      "rel-to-charge-start", round(t[imin] - t[i0], 1), "v", round(v[imin], 3))
# sample ap at a few points through the charge
for frac in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
    idx = i0 + int((len(t) - 1 - i0) * frac)
    print(f"  frac {frac:.2f}: t_rel {t[idx]-t[i0]:7.1f}s v {v[idx]:.3f} ap {ap[idx]:+.4f}")