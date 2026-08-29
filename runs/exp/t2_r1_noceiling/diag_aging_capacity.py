# Diagnostic: why does the aging protocol's cycle-1 discharge deliver ~1.65 Ah while
# the 1C_discharge protocol (same step, same initial state) delivers ~4.94 Ah?
# Isolate the two model-option differences: SEI (ec reaction limited) and thermal (isothermal).
import pybamm
import numpy as np

PV = pybamm.ParameterValues("Chen2020")
v_min = float(PV["Lower voltage cut-off [V]"])
v_max = float(PV["Upper voltage cut-off [V]"])

def run(opts, steps, label):
    model = pybamm.lithium_ion.SPMe(options=opts)
    sim = pybamm.Simulation(model, experiment=pybamm.Experiment(steps), parameter_values=PV)
    sol = sim.solve()
    t = sol["Time [s]"].entries
    V = sol["Terminal voltage [V]"].entries
    print(f"{label}: t_end={t[-1]:.1f}s  V_end={V[-1]:.3f}  "
          f"(1C discharge capacity proxy = {t[-1]*5.0/3600:.3f} Ah)")

steps1 = [f"Discharge at 1C until {v_min} V"]
run({}, steps1, "noSEI+lumped   : 1C discharge step")
run({"thermal": "isothermal"}, steps1, "noSEI+isother  : 1C discharge step")
run({"SEI": "ec reaction limited"}, steps1, "SEI+lumped     : 1C discharge step")
run({"SEI": "ec reaction limited", "thermal": "isothermal"}, steps1, "SEI+isother    : 1C discharge step")
run({"SEI": "ec reaction limited", "thermal": "isothermal"},
    [("Discharge at 1C until %s V" % v_min, "Charge at 1C until %s V" % v_max)] * 2,
    "SEI+iso 2-cycle: aging-style experiment (whole run)")
