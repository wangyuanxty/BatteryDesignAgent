"""Diagnose 5C bottleneck: solve DFN 5C discharge for ~30 s, inspect state variables.

Answers: (1) does Chen2020 have separate active-material-volume-fraction keys;
(2) where does the terminal voltage sit at t~0 and t~30 s (V, cathode OCP, anode OCP,
overpotential-ish decomposition); (3) electrolyte c_e min/max (salt depletion index);
(4) negative particle surface concentration (solid-diffusion saturation index).
"""
import pybamm
import numpy as np

pv = pybamm.ParameterValues("Chen2020")
for k in ["Positive electrode active material volume fraction",
          "Negative electrode active material volume fraction",
          "Positive electrode surface area to volume ratio [m-1]",
          "Negative electrode surface area to volume ratio [m-1]"]:
    try:
        print(f"{k!r}: {pv[k]}")
    except KeyError:
        print(f"{k!r}: MISSING")

pv.update({"Ambient temperature [K]": 298.15}, check_already_exists=False)
options = {"thermal": "isothermal"}
model = pybamm.lithium_ion.DFN(options=options)
# 5C: current = 5 * nominal capacity / hour
i_cell = 5.0 * float(pv["Nominal cell capacity [A.h]"])
c_rate = i_cell / (float(pv["Electrode height [m]"]) * float(pv["Electrode width [m]"]))
print(f"i_cell={i_cell:.2f} A, current density={c_rate:.2f} A/m2")

v_min = float(pv["Lower voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 5C until {v_min} V"])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()
t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries

for ts in [0.0, 10.0, 30.0, 60.0, t[-1]]:
    idx = int(np.argmin(np.abs(t - ts)))
    tt = t[idx]
    print(f"--- t={tt:.1f} s")
    print(f"  V={V[idx]:.3f}")
    try:
        print(f"  c_e: min={sol['Electrolyte concentration [M]'].entries[:,idx].min():.3f} "
              f"max={sol['Electrolyte concentration [M]'].entries[:,idx].max():.3f}")
    except Exception as e:
        print("  c_e err", e)
    try:
        xn = sol["Negative particle surface concentration [mol.m-3]"].entries
        xn_max = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
        print(f"  neg surf conc: min={xn[:,idx].min():.0f} max={xn[:,idx].max():.0f} / c_max={xn_max:.0f}")
    except Exception as e:
        print("  neg surf err", e)
    try:
        xp = sol["Positive particle surface concentration [mol.m-3]"].entries
        xp_max = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
        print(f"  pos surf conc: min={xp[:,idx].min():.0f} max={xp[:,idx].max():.0f} / c_max={xp_max:.0f}")
    except Exception as e:
        print("  pos surf err", e)
print(f"END: t={t[-1]:.1f} s, V={V[-1]:.3f}, cap={sol.cycles[-1]['Discharge capacity [A.h]'].entries[-1]:.3f} Ah")