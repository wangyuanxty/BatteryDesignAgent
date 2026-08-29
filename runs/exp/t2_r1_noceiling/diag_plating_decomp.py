# Decompose the 4C-charge anode potential dive: which term drives anode_min to -0.44 V?
# Variables at the final time point of the 4C_charge_45C experiment (SPMe + plating, baseline).
import numpy as np
import pybamm

PV = pybamm.ParameterValues("Chen2020")
PV.update({
    "Initial plated lithium concentration [mol.m-3]": 0.0,
    "Typical plated lithium concentration [mol.m-3]": 1000.0,
    "Lithium plating transfer coefficient": 0.65,
    "Exchange-current density for plating [A.m-2]": 0.001,
    "Exchange-current density for stripping [A.m-2]": 0.001,
    "Ambient temperature [K]": 318.15,
}, check_already_exists=False)

v_min = float(PV["Lower voltage cut-off [V]"])
v_max = float(PV["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([
    f"Discharge at 1C until {v_min} V",
    f"Charge at 4C until {v_max} V",
])
model = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=PV)
sol = sim.solve()
t = sol["Time [s]"].entries
print(f"run time {t[-1]:.1f} s")

def last(name):
    v = sol[name]
    if v.domains or isinstance(v, pybamm.Array):
        e = np.asarray(v.entries)
        return e[-1] if e.ndim == 0 else e[-1, :]
    return v

names = [
    "Negative electrode surface potential difference at separator interface [V]",
    "Negative electrode reaction overpotential [V]",
    "Positive electrode reaction overpotential [V]",
    "Negative electrode open circuit potential [V]",
    "Positive electrode open circuit potential [V]",
    "X-averaged negative particle surface concentration [mol.m-3]",
    "X-averaged negative particle concentration [mol.m-3]",
    "X-averaged positive particle surface concentration [mol.m-3]",
    "X-averaged positive particle concentration [mol.m-3]",
    "Electrolyte potential [V]",
    "Terminal voltage [V]",
    "Volume-averaged cell temperature [K]",
    "X-averaged electrolyte concentration [mol.m-3]",
]
c_max_n = float(PV["Maximum concentration in negative electrode [mol.m-3]"])
c_max_p = float(PV["Maximum concentration in positive electrode [mol.m-3]"])
for n in names:
    try:
        e = np.asarray(sol[n].entries)
        if e.ndim == 1:
            print(f"{n}: last={e[-1]:.4f}  min={e.min():.4f}  max={e.max():.4f}")
        else:
            print(f"{n}: last={e[-1, :]}")
    except Exception as ex:
        print(f"{n}: ERR {ex}")

c_surf_n = float(np.asarray(sol["X-averaged negative particle surface concentration [mol.m-3]"].entries)[-1])
c_bulk_n = float(np.asarray(sol["X-averaged negative particle concentration [mol.m-3]"].entries)[-1])
c_surf_p = float(np.asarray(sol["X-averaged positive particle surface concentration [mol.m-3]"].entries)[-1])
c_bulk_p = float(np.asarray(sol["X-averaged positive particle concentration [mol.m-3]"].entries)[-1])
print(f"anode x_surf={c_surf_n/c_max_n:.4f}  x_bulk={c_bulk_n/c_max_n:.4f}  delta_x={c_surf_n/c_max_n - c_bulk_n/c_max_n:+.4f}")
print(f"cathode y_surf={c_surf_p/c_max_p:.4f}  y_bulk={c_bulk_p/c_max_p:.4f}  delta_y={c_surf_p/c_max_p - c_bulk_p/c_max_p:+.4f}")

# also at charge start (t just after discharge ends)
i_start = int(np.argmax(t > 3523))
for lbl, i in [("charge start", i_start), ("abort", -1)]:
    cs = float(np.asarray(sol["X-averaged negative particle surface concentration [mol.m-3]"].entries)[i])
    print(f"at {lbl}: x_surf={cs/c_max_n:.4f}  anode_surf_potdiff={np.asarray(sol['Negative electrode surface potential difference at separator interface [V]'].entries)[i]:.4f}")
