import json, os, sys
ws = os.path.dirname(os.path.abspath(__file__))
fn = sys.argv[1] if len(sys.argv) > 1 else "cell/r8_lnmo_r5_4c45_dfn.json"
tag = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(fn)
d = json.load(open(os.path.join(ws, fn), encoding="utf-8"))
t, v, a = d["time_s"], d["voltage_v"], d["anode_potential_v"]
mn = min(range(len(a)), key=a.__getitem__)
print(tag, "n_points", len(t), "t_end %.0f" % t[-1], "v_end %.3f" % v[-1])
print(tag, "min anode %.4f V at t=%.0f s, cell V=%.3f" % (a[mn], t[mn], v[mn]))
for i in range(max(0, mn - 3), min(len(t), mn + 4)):
    print("   t=%8.0f  V=%.3f  anode=%.4f" % (t[i], v[i], a[i]))
neg = [(t[i], v[i], a[i]) for i in range(len(a)) if a[i] < 0]
if neg:
    print("below-zero: %d pts, first t=%.0f (V=%.3f), last t=%.0f (V=%.3f)"
          % (len(neg), neg[0][0], neg[0][1], neg[-1][0], neg[-1][1]))
print("max V reached: %.3f" % max(v))
