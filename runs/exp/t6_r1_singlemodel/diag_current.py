"""Diagnose the actual 4C charge current and the anode-side current split in E3."""
import json
from pathlib import Path

import pybamm

from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS, THERMAL_PARAM_DEFAULTS
from bda.simulators.lnmo_parameters import lnmo_ocp

CELL = Path("cell")
BASE = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"

params = json.loads((CELL / "r7_E3_params.json").read_text(encoding="utf-8"))
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

print("Nominal cell capacity [A.h]:", pv.get("Nominal cell capacity [A.h]"))
print("Electrode area / heights:", {k: pv.get(k) for k in
      ("Electrode height [m]", "Electrode width [m]", "Positive electrode thickness [m]",
       "Negative electrode thickness [m]")})

options = {"thermal": "lumped", "lithium plating": "irreversible"}
model = pybamm.lithium_ion.SPMe(options=options)
v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", "Charge at 4C until 4.7 V"])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
ap = sol["Negative electrode surface potential difference at separator interface [V]"].entries
i0 = int(min(range(len(V)), key=lambda i: V[i]))


def tof(x):
    v = getattr(x, "value", x)
    return float(v)


def try_var(key):
    try:
        return [tof(x) for x in sol[key].entries]
    except Exception as e:
        return None


current = try_var("Current [A]")
i_n_avg = try_var("Average negative electrode interfacial current density [A.m-2]")
i_n_sep = try_var("Negative electrode interfacial current density at separator interface [A.m-2]")
i_plat = try_var("Average lithium plating interfacial current density [A.m-2]")
dead = try_var("Sum of x-averaged negative electrode volumetric interfacial current densities [A.m-3]")

print("charge-phase: t_ch  Current  V  anode_pot  i_plat_avg(A/m2)")
area = float(pv["Electrode height [m]"]) * float(pv["Electrode width [m]"])
for tch in (0, 100, 300, 700, 1000, 1100, 1180, 1200, 1210, 1215, 1220, 1240):
    target = t[i0] + tch
    i = min(range(len(t)), key=lambda k: abs(t[k] - target))
    c = current[i] if current else None
    ip = i_plat[i] if i_plat else None
    ia = i_n_sep[i] if i_n_sep else None
    print(f"{tch:>7} {c:>9.3f} {tof(V[i]):>7.4f} {tof(ap[i]):>9.4f} "
          f"{ip if ip is None else round(ip,3)}  i_n_sep={ia if ia is None else round(ia,3)}")
print("area m2 =", area)
