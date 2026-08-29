"""Scratch: dissect the 4C protocol time series (charge phase dynamics)."""
import json

d = json.load(open("runs/exp/t5_r1/cell/r1_chen2020_4c_dfn.json", encoding="utf-8-sig"))
t = d["time_s"]; v = d["voltage_v"]; ap = d["anode_potential_v"]

# end of discharge = global voltage minimum (before charge rises)
imin = v.index(min(v))
print(f"end of discharge: t={t[imin]:.1f}s v={v[imin]:.4f}V anode_pot={ap[imin]:.4f}V")
print(f"charge segment duration: {t[-1]-t[imin]:.1f}s  capacity@4C={(t[-1]-t[imin])*20/3600:.3f}Ah")
print(f"voltage at charge start (+0s): {v[imin]:.4f}")
for k in (5, 10, 20, 30):
    idx = min(len(t)-1, imin + k)
    print(f"  charge +{t[idx]-t[imin]:.0f}s: V={v[idx]:.4f} anode_pot={ap[idx]:.4f}")
print(f"charge end: V={v[-1]:.4f} anode_pot={ap[-1]:.4f}")
# when does anode potential first go negative?
neg = [i for i, x in enumerate(ap) if x < 0]
print(f"first negative anode potential at t={t[neg[0]]:.1f}s" if neg else "anode never negative")
print(f"negative during charge phase: {sum(1 for i in neg if i > imin)} points of {len(neg)}")
# discharge-phase heat picture: T rise during 1C discharge at 45C amb
print(f"T_max_K={d['T_max_K']:.2f}")
print(f"ambient=318.15 -> dT_max={d['T_max_K']-318.15:.2f}K")
