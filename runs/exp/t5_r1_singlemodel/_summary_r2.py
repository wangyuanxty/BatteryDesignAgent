import json
from pathlib import Path

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
cell = WS / "cell"

rows = [("archD_combine", "archD"), ("archE_posPoro", "archE"), ("archF_npTrim", "archF"), ("archG_cool60", "archG")]
print(f"{'candidate':<16} {'ED Wh/kg':>9} {'cap Ah':>7} {'E Wh':>7} {'mass g':>7} {'Vmid':>6} {'DCR mOhm':>8} {'Tmax K':>7} {'anode min V':>11} {'model':>14}")
for disp, name in rows:
    en = json.loads((cell / f"r2_{name}_energy.json").read_text(encoding="utf-8"))
    c4 = json.loads((cell / f"r2_{name}_4c_dfn.json").read_text(encoding="utf-8"))
    ap = c4.get("anode_potential_v")
    apmin = min(ap) if ap else float("nan")
    print(f"{disp:<16} {en['energy_density_wh_kg']:9.1f} {en['capacity_ah']:7.3f} {en['energy_wh']:7.2f} "
          f"{en['mass_kg']*1000:7.2f} {en['midpoint_voltage_v']:6.3f} {en['dcr_ohm']*1000:8.2f} "
          f"{c4.get('T_max_K', float('nan')):7.2f} {apmin:11.4f} {c4.get('model_used', '-'):>14}")

# anode potential series around minimum (charge phase) for archD/archG to understand plating margin
import numpy as np
for name in ("archD", "archG"):
    c4 = json.loads((cell / f"r2_{name}_4c_dfn.json").read_text(encoding="utf-8"))
    ap = np.asarray(c4["anode_potential_v"])
    t = np.asarray(c4["time_s"])
    i = int(np.argmin(ap))
    print(f"[{name}] anode min {ap.min():.4f} V at t={t[i]:.0f} s (of {t[-1]:.0f}); "
          f"series head/tail: {ap[0]:.4f} -> {ap[-1]:.4f}; T series max {c4['T_max_K']:.2f} K")
