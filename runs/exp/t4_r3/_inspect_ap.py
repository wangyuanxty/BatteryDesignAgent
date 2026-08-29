"""t4_r3: inspect 4C_45C anode potential trajectory — locate the dip and its context."""
import json

from bda.store import CaseWorkspace

ws = CaseWorkspace("exp/t4_r3", root="runs")

for name in ("r1_base_4C_45C_spme", "r2_V4_4C_45C_spme", "r3_V6_4C_45C_spme"):
    d = json.loads((ws.path / f"cell/{name}.json").read_text(encoding="utf-8-sig"))
    ap = d["anode_potential_v"]
    t = d["time_s"]
    vv = d["voltage_v"]
    mn, mi = min(ap), ap.index(min(ap))
    print(f"== {name}: anode_min={mn:+.4f}V at t={t[mi]:7.1f}s (idx {mi}/{len(ap)})  V(t)={vv[mi]:.3f}  t_end={t[-1]:.1f}  V_end={vv[-1]:.3f}")
    print("   ap around min:", " ".join(f"{x:+.3f}" for x in ap[max(0, mi - 4):mi + 5]))
    print(f"   ap start={ap[0]:+.3f}  ap end={ap[-1]:+.3f}")
    neg_start = next((i for i, x in enumerate(ap) if x < 0), None)
    print(f"   first negative at t={t[neg_start]:.1f}s V={vv[neg_start]:.3f}" if neg_start is not None else "   never negative")
    # discharge/charge boundary: discharge step ends when voltage hits 2.5 V
    dis_end = next((i for i, x in enumerate(vv) if x <= 2.51), None)
    print(f"   discharge reached 2.5V at t={t[dis_end]:.1f}s (idx {dis_end})" if dis_end is not None else "   no 2.5V crossing")