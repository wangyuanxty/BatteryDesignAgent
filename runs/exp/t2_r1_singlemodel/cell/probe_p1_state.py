"""Diagnostic v2: dump SPMe internal state (robust shape handling)."""
import pybamm
import numpy as np

pv = pybamm.ParameterValues("Chen2020")
pv.update({
    "Negative electrode thickness [m]": 2.5e-4,
    "Positive electrode thickness [m]": 1.0e-4,
    "Positive particle radius [m]": 3.0e-6,
    "Negative particle radius [m]": 3.5e-6,
})
v_min = float(pv["Lower voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V"])
model = pybamm.lithium_ion.SPMe()
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

T = np.asarray(sol["Time [s]"].entries).ravel()
V = np.asarray(sol["Terminal voltage [V]"].entries).ravel()
i_cliff = int(np.argmax(V < 3.6))
print(f"t_cliff={T[i_cliff]:.1f}s  t_end={T[-1]:.1f}s")
print(f"model_used_runner_output_is_spme={isinstance(model, pybamm.lithium_ion.SPMe)}")

def last(name):
    """Return flattened final value of a solution variable."""
    try:
        a = np.asarray(sol[name].entries)
        return float(a.ravel()[-1]), a.shape
    except Exception as ex:
        return None, f"{type(ex).__name__}: {ex}"

c_max_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
c_max_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
for name in [
    "X-averaged negative particle concentration [mol.m-3]",
    "X-averaged positive particle concentration [mol.m-3]",
    "Negative particle surface concentration [mol.m-3]",
    "Positive particle surface concentration [mol.m-3]",
    "Negative electrode reaction overpotential [V]",
    "Positive electrode reaction overpotential [V]",
    "Positive electrode surface open-circuit potential [V]",
    "Negative electrode surface open-circuit potential [V]",
    "X-averaged positive electrode open-circuit potential [V]",
    "Positive electrode exchange current density [A.m-2]",
    "Negative electrode exchange current density [A.m-2]",
    "Positive electrode interfacial current density [A.m-2]",
    "Negative electrode interfacial current density [A.m-2]",
]:
    val, shape = last(name)
    if val is None:
        print(f"{name}: UNAVAILABLE ({shape})")
        continue
    line = f"{name}: end={val:.5f} shape={shape}"
    if "concentration [mol.m-3]" in name and val is not None:
        cmax = c_max_n if "egative particle" in name else c_max_p
        line += f"  stoich={val/cmax:.5f}"
    print(line)
