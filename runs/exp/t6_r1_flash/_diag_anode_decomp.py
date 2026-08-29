"""Diagnostic: decompose anode potential at 4C cutoff (LNMO + Chen2020, superTrans params).
Mirrors pybamm_runner.run_simulation exactly, then dumps per-component terms at the last
charge timestep: U_neg(sto_surf), eta_rxn_neg, electrolyte potential/concentration shift."""
import json
import numpy as np
import pybamm
from bda.simulators.lnmo_parameters import lnmo_ocp

base = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
params_file = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash\_params_superTrans.json"

extra = json.load(open(base, encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)
params = json.load(open(params_file, encoding="utf-8"))
pv.update(params)
pv.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS
pv.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)

options = {"thermal": "lumped", "lithium plating": "irreversible"}
model = pybamm.lithium_ion.SPMe(options=options)
v_min = float(pv["Lower voltage cut-off [V]"])
v_max = float(pv["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([
    f"Discharge at 1C until {v_min} V",
    "Charge at 4C until 4.7 V",
])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

# last charge cycle = last cycle (charge step)
cyc = sol.cycles[-1]
t = cyc["Time [s]"].entries
vars_ = {
    "terminal_voltage": "Terminal voltage [V]",
    "anode_pot_sep": "Negative electrode surface potential difference at separator interface [V]",
    "U_neg": "Negative electrode open circuit potential [V]",
    "eta_rxn_neg": "Negative electrode reaction overpotential [V]",
    "sto_neg_surf": "Negative electrode surface stoichiometry",
    "sto_neg_avg": "Negative electrode stoichiometry",
    "c_e_neg_surf": "Negative electrolyte concentration [mol.m-3]",
    "phi_e_sep_neg": "Electrolyte potential [V]",
    "phi_s_neg": "Negative electrode potential [V]",
    "T_cell": "Volume-averaged cell temperature [K]",
}
print("=== last timestep of 4C charge ===")
for name, var in vars_.items():
    try:
        v = cyc[var].entries
        print(f"{name}: {float(v[-1]):.5f}")
    except Exception as e:
        print(f"{name}: unavailable ({e})")

# time trace of the anode potential + sto during the charge step (last 20 points)
ap = cyc["Negative electrode surface potential difference at separator interface [V]"].entries
sto = cyc["Negative electrode surface stoichiometry"].entries
u = cyc["Negative electrode open circuit potential [V]"].entries
eta = cyc["Negative electrode reaction overpotential [V]"].entries
print("\n=== charge-step trace (every ~10th point) ===")
print("idx  t[s]   V_cell    anode_pot  U_neg   eta_rxn  sto_surf")
step = max(1, len(t)//30)
for i in range(0, len(t), step):
    print(f"{i:4d} {t[i]:8.2f} {cyc['Terminal voltage [V]'].entries[i]:7.4f} "
          f"{ap[i]:8.4f} {u[i]:7.4f} {eta[i]:8.4f} {sto[i]:6.3f}")
# and the final 5 points
print("...final points:")
for i in range(len(t)-5, len(t)):
    print(f"{i:4d} {t[i]:8.2f} {cyc['Terminal voltage [V]'].entries[i]:7.4f} "
          f"{ap[i]:8.4f} {u[i]:7.4f} {eta[i]:8.4f} {sto[i]:6.3f}")

# anode potential minimum location
j = int(np.argmin(ap))
print(f"\nanode_pot min = {ap[j]:.4f} V at t={t[j]:.2f}s, V_cell={cyc['Terminal voltage [V]'].entries[j]:.4f}, sto_surf={sto[j]:.4f}, U_neg={u[j]:.4f}, eta_rxn={eta[j]:.4f}")
