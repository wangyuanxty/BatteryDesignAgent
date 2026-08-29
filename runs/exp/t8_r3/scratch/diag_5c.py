"""Diagnose 5C discharge: curve shape + quick 2C/3C rate map."""
import json
from pathlib import Path

cell = Path("runs/exp/t8_r3/cell")

d = json.loads((cell / "r1_C0_5c_dfn.json").read_text(encoding="utf-8"))
t, v = d["time_s"], d["voltage_v"]
print(f"5C C0: n={len(t)}, t_end={t[-1]:.1f} s, v_start={v[0]:.3f}, v_end={v[-1]:.3f}")
step = max(1, len(t) // 60)
print("  sample (t, V):")
for i in range(0, len(t), step):
    print(f"    {t[i]:8.1f}  {v[i]:.4f}")
print("  last 6:", [(round(t[i],1), round(v[i],4)) for i in range(-6, 0)])