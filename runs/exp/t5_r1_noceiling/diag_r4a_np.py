# Diagnostic: R4A charge-window stoichiometry endpoints for the N/P ratio (design_spec).
import sys, json
import numpy as np
import pybamm

sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.simulators import pybamm_runner as R

params = json.load(open("runs/exp/t5_r1_noceiling/candidates/r4_A_params.json", encoding="utf-8"))
p = dict(R.PROTOCOLS["4C_charge_45C"])
pv0 = pybamm.ParameterValues("Chen2020")
pv0.update(params)
pv0.update({"Ambient temperature [K]": p["T_amb_K"]}, check_already_exists=False)
pv0.update(R.PLATING_PARAM_DEFAULTS, check_already_exists=False)
for name, value in R.THERMAL_PARAM_DEFAULTS.items():
    if name not in pv0:
        pv0.update({name: value}, check_already_exists=False)
if "Cell volume [m3]" not in pv0:
    pv0.update({"Cell volume [m3]": R._cell_volume_default(pv0)}, check_already_exists=False)

options = {"thermal": "lumped", "lithium plating": "irreversible"}
v_min = float(pv0["Lower voltage cut-off [V]"])
v_max = float(pv0["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", f"Charge at 4C until {v_max} V"])
model = pybamm.lithium_ion.DFN(options=options)
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv0)
sol = sim.solve()

t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
i_end = int(np.argmin(V))
t_c0 = float(t[i_end])
t_c1 = float(t[-1])

def val(name, tt):
    s = sol[name]
    return float(np.asarray(s(tt)).flatten()[0])

c_max_n = float(pv0["Maximum concentration in negative electrode [mol.m-3]"])
c_max_p = float(pv0["Maximum concentration in positive electrode [mol.m-3]"])
c0_n = val("X-averaged negative particle concentration [mol.m-3]", t_c0)
c1_n = val("X-averaged negative particle concentration [mol.m-3]", t_c1)
c0_p = val("X-averaged positive particle concentration [mol.m-3]", t_c0)
c1_p = val("X-averaged positive particle concentration [mol.m-3]", t_c1)
x0_n, x1_n = c0_n / c_max_n, c1_n / c_max_n
x0_p, x1_p = c0_p / c_max_p, c1_p / c_max_p

eps_p = float(pv0["Positive electrode porosity"])
eps_n = float(pv0["Negative electrode porosity"])
L_p = float(pv0["Positive electrode thickness [m]"])
L_n = float(pv0["Negative electrode thickness [m]"])
F = 96485.3329
Qp = c_max_p * (x0_p - x1_p) * (1 - eps_p) * L_p * F / 3600.0   # Ah/m2, discharge direction
Qn = c_max_n * (x1_n - x0_n) * (1 - eps_n) * L_n * F / 3600.0
print(f"charge start t={t_c0:.1f}s (V={float(V[i_end]):.3f})  charge end t={t_c1:.1f}s (V={float(V[-1]):.3f})")
print(f"x_n: {x0_n:.4f} -> {x1_n:.4f}   x_p: {x0_p:.4f} -> {x1_p:.4f}")
print(f"Q_neg areal = {Qn:.3f} Ah/m2   Q_pos areal = {Qp:.3f} Ah/m2   N/P = {Qn/Qp:.4f}")
print(f"L_n={L_n*1e6:.1f} um  L_p={L_p*1e6:.1f} um  eps_n={eps_n}  eps_p={eps_p}")
