# Read 4C plating metric (min anode_potential_v) for r3 E/F/G/H vs baseline and r2 refs.
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

d = Path("runs/exp/t2_r1_noceiling/cell")
refs = [("base", "r1_baseline_4c45.json"), ("r2A", "r2_A_4c45.json"),
        ("r2B", "r2_B_4c45.json"), ("r2C", "r2_C_4c45.json"), ("r2D", "r2_D_4c45.json")]
for name, f in refs:
    if (d / f).exists():
        p = json.loads((d / f).read_text(encoding="utf-8-sig"))
        a = p["anode_potential_v"]
        t = p["time_s"]
        print(f"{name:5s}: anode_min={min(a):+.4f}  t_end={t[-1]:.1f}s  cap={p['capacity_ah']:.4f}Ah  Tmax={p['T_max_K']:.1f}K")
print()
for c in "EFGH":
    p = json.loads((d / f"r3_{c}_4c45.json").read_text(encoding="utf-8-sig"))
    a = p["anode_potential_v"]
    t = p["time_s"]
    i = min(range(len(a)), key=lambda j: a[j])
    print(f"r3_{c}: anode_min={min(a):+.4f} @t={t[i]:.2f}s  t_end={t[-1]:.1f}s  cap={p['capacity_ah']:.4f}Ah  Tmax={p['T_max_K']:.1f}K")
