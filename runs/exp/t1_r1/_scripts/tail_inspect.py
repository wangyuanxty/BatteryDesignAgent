"""Print the last N (t, V, anode_potential) triples of a 4C output; flag negative points."""
import json
import sys

path = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 45
d = json.load(open(path, encoding="utf-8"))
t = d["time_s"]
v = d["voltage_v"]
p = d.get("anode_potential_v", [])
print(f"{path}: {len(t)} points, t_end={t[-1]:.2f} s")
neg = [(tt, vv, pp) for tt, vv, pp in zip(t, v, p) if pp < 0]
print(f"negative points: {len(neg)}; first negative at t={neg[0][0]:.3f} s" if neg else "no negative points")
for i in range(max(0, len(t) - n), len(t)):
    flag = " <-- NEG" if p and p[i] < 0 else ""
    print(f"  t={t[i]:10.3f}  V={v[i]:8.4f}  phi={p[i]:8.4f}{flag}" if p else f"  t={t[i]:10.3f}  V={v[i]:8.4f}")
