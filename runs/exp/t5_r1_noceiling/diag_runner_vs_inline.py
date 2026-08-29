# Compare: direct run_simulation call vs inline replication, same params (R3C, 4C).
import sys, json
import numpy as np

sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.simulators import pybamm_runner as R

params = json.load(open("runs/exp/t5_r1_noceiling/candidates/r3_C_params.json", encoding="utf-8"))

print("=== direct R.run_simulation ===")
out = R.run_simulation(dict(params), protocol="4C_charge_45C", base="Chen2020",
                       mode="spme", thermal="lumped", plating=True)
t = out["time_s"]; v = out["voltage_v"]
an = out["anode_potential_v"]
print(f"model={out['model_used']} t_end={t[-1]:.1f} cap={out['capacity_ah']:.4f} V_end={v[-1]:.4f} T_max={out['T_max_K']:.2f} anode_min={min(an):.4f}")
i_min = int(np.argmin(v))
print(f"charge start t={t[i_min]:.1f} V={v[i_min]:.3f}; charge len={t[-1]-t[i_min]:.1f} s")
# where does V first reach 4.2?
first42 = next((tt for tt, vv in zip(t, v) if vv >= 4.199), None)
print(f"first V>=4.199 at t={first42} (charge +{first42-t[i_min]:.1f} s)")
