"""Diagnose the F3 4C charge: actual eta_e and V through the dip region."""
import json
from pathlib import Path

import numpy as np
import pybamm

from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS, THERMAL_PARAM_DEFAULTS
from bda.simulators.lnmo_parameters import lnmo_ocp

CELL = Path("cell")
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

params = json.loads((CELL / "r9_F3_params.json").read_text(encoding="utf-8"))
extra = json.loads(Path(BASE).read_text(encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)
pv.update(params)
pv.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
pv.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)
for name, value in THERMAL_PARAM_DEFAULTS.items():
    if name not in pv:
        pv.update({name: value}, check_already_exists=False)

print("kappa override:", pv.get("Electrolyte conductivity [S.m-1]"))
print("Chen2020 default conductivity function?", type(pv.get("Electrolyte conductivity [S.m-1]")))

c_max_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
c_max_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])

options = {"thermal": "lumped", "lithium plating": "irreversible"}
model = pybamm.lithium_ion.SPMe(options=options)
v_min = float(pv["Lower voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", "Charge at 4C until 4.7 V"])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
ap = sol["Negative electrode surface potential difference at separator interface [V]"].entries
i0 = int(min(range(len(V)), key=lambda i: V[i]))


def arr(key):
    return np.asarray(sol[key].entries, dtype=float).reshape(-1)


def try_arr(key):
    try:
        return arr(key)
    except Exception:
        return None


def tof(x):
    v = getattr(x, "value", x)
    return float(v)


c_avg = arr("Average positive particle concentration [mol.m-3]")
n_avg = arr("Average negative particle concentration [mol.m-3]")
eta_e = try_arr("X-averaged electrolyte overpotential [V]")
eta_n = try_arr("X-averaged negative electrode reaction overpotential [V]")

print(f"charge start: t={t[i0]:.1f}s  c={c_avg[i0]/c_max_p:.4f}  n={n_avg[i0]/c_max_n:.4f}")
print(f"{'t_ch':>7} {'V':>7} {'anode_pot':>9} {'c_sto':>7} {'n_sto':>7} {'OCP_c':>7} {'OCP_n':>7} "
      f"{'eta_tot':>8} {'eta_e':>8} {'eta_n':>7}")
for tch in (0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1150, 1165, 1170, 1180, 1200):
    target = t[i0] + tch
    i = min(range(len(t)), key=lambda k: abs(t[k] - target))
    c_sto = tof(c_avg[i]) / c_max_p
    n_sto = tof(n_avg[i]) / c_max_n
    ocp_c = tof(lnmo_ocp(c_sto, 0))
    ocp_n = tof(pv["Negative electrode OCP [V]"](n_sto))
    eta_tot = float(V[i]) - ocp_c + ocp_n
    row = f"{tch:>7} {float(V[i]):>7.4f} {float(ap[i]):>9.4f} {c_sto:>7.4f} {n_sto:>7.4f} {ocp_c:>7.4f} {ocp_n:>7.4f} {eta_tot:>8.4f}"
    for name, a in (("eta_e", eta_e), ("eta_n", eta_n)):
        row += f" {tof(a[i]):>8.4f}" if a is not None else "       NA"
    print(row)
