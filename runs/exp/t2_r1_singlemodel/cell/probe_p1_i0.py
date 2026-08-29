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
sim = pybamm.Simulation(pybamm.lithium_ion.SPMe(), experiment=exp, parameter_values=pv)
sol = sim.solve()

T = np.asarray(sol["Time [s]"].entries).ravel()
V = np.asarray(sol["Terminal voltage [V]"].entries).ravel()
i0p = np.asarray(sol["Positive electrode exchange current density [A.m-2]"].entries)
print("i0p raw shape:", i0p.shape)
i0p = i0p.reshape(-1, len(T))
ce_avg = np.asarray(sol["X-averaged electrolyte concentration [mol.m-3]"].entries).ravel()
try:
    Temp = np.asarray(sol["Volume-averaged cell temperature [K]"].entries).ravel()
except KeyError:
    Temp = np.full(len(T), 298.15)
print("t     V      i0p(r0)   i0p(rR)   ce_avg    T")
for k in [0, 20, 40, 55, 65, 70, 75, 80, 84]:
    print("%6.1f %6.3f %9.5f %9.5f %8.1f %7.2f" % (T[k], V[k], i0p[0, k], i0p[-1, k], ce_avg[k], Temp[k]))
