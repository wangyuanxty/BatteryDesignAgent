"""Diagnostic: replicate the bda 4C_charge_45C experiment and report the actual
applied current profile, step boundaries, and termination events.
Read-only analysis script (new file); does not modify the library or outputs."""
import json
import sys

import numpy as np
import pybamm

from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS, THERMAL_PARAM_DEFAULTS

params_file = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "spme"
out_path = sys.argv[3] if len(sys.argv) > 3 else None

params = json.load(open(params_file, encoding="utf-8"))
parameter_values = pybamm.ParameterValues("Chen2020")
parameter_values.update(params)
parameter_values.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
parameter_values.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)
for name, value in THERMAL_PARAM_DEFAULTS.items():
    if name not in parameter_values:
        parameter_values.update({name: value}, check_already_exists=False)
if "Cell volume [m3]" not in parameter_values:
    from bda.simulators.pybamm_runner import _cell_volume_default
    parameter_values.update({"Cell volume [m3]": _cell_volume_default(parameter_values)}, check_already_exists=False)

exp = pybamm.Experiment([
    "Discharge at 1C until 2.5 V",
    "Charge at 4C until 4.2 V",
])
options = {"thermal": "lumped", "lithium plating": "irreversible"}
model = pybamm.lithium_ion.DFN(options=options) if mode == "dfn" else pybamm.lithium_ion.SPMe(options=options)
sim = pybamm.Simulation(model, experiment=exp, parameter_values=parameter_values)
sol = sim.solve()

t = sol["Time [s]"].entries
cur = sol["Current [A]"].entries
v = sol["Terminal voltage [V]"].entries
print(f"termination: {sol.termination}")
print(f"n_pts={len(t)} t_end={t[-1]:.2f}")
# step detection: current sign changes / discontinuities
steps = []
prev = 0.0
for i in range(len(t)):
    if abs(cur[i] - prev) > 1e-6:
        steps.append((i, t[i], cur[i]))
        prev = cur[i]
for s in steps[:12]:
    print(f"  step start: idx={s[0]:4d} t={s[1]:9.3f} I={s[2]:9.4f} A")
# last current change
print(f"  last change: idx={steps[-1][0]:4d} t={steps[-1][1]:9.3f} I={steps[-1][2]:9.4f} A")
print("current stats per sign-segment:")
seg = []
for s in steps:
    seg.append(s)
for j in range(len(seg)):
    i0 = seg[j][0]
    i1 = seg[j + 1][0] if j + 1 < len(seg) else len(t)
    print(f"  seg {j}: t {seg[j][1]:9.3f} -> {t[i1-1]:9.3f} s, I={seg[j][2]:9.4f} A, dur={t[i1-1]-seg[j][1]:9.3f} s, Ah={(t[i1-1]-seg[j][1])*abs(seg[j][2])/3600:6.3f}")
# reference comparison if out file provided
if out_path:
    ref = json.load(open(out_path, encoding="utf-8"))
    print(f"reference file n={len(ref['time_s'])}, t_end={ref['time_s'][-1]:.2f}, V[0]={ref['voltage_v'][0]:.4f}")
    print(f"this run   V[0]={v[0]:.4f} (should match), T_max_K ref={ref.get('T_max_K')}")
    # compare T_max
    tmax = float(sol["Volume-averaged cell temperature [K]"].entries.max())
    print(f"this run T_max_K={tmax:.4f}")
