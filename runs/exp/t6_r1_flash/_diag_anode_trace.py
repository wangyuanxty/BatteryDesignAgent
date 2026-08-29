"""Diagnostic v2: trace anode stoichiometry/potential through the whole 4C protocol cycle."""
import json
import numpy as np
import pybamm
from bda.simulators.lnmo_parameters import lnmo_ocp
from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS

base = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
params_file = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t6_r1_flash\_params_superTrans.json"

extra = json.load(open(base, encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp
pv = pybamm.ParameterValues("Chen2020")
pv.update(extra, check_already_exists=False)
pv.update(json.load(open(params_file, encoding="utf-8")))
pv.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
pv.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)

model = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible"})
v_min = float(pv["Lower voltage cut-off [V]"])
exp = pybamm.Experiment([
    f"Discharge at 1C until {v_min} V",
    "Charge at 4C until 4.7 V",
])
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
sol = sim.solve()

cyc = sol.cycles[-1]
t = np.asarray(cyc["Time [s]"].entries)
V = np.asarray(cyc["Terminal voltage [V]"].entries)
ap = np.asarray(cyc["Negative electrode surface potential difference at separator interface [V]"].entries)
sto_avg = np.asarray(cyc["Negative electrode stoichiometry"].entries)
sto_surf = np.asarray(cyc["Negative particle surface stoichiometry"].entries)
u_surf = np.asarray(cyc["Negative electrode open-circuit potential [V]"].entries)
eta = np.asarray(cyc["Negative electrode reaction overpotential [V]"].entries)

# where does the charge leg start? find where current sign flips (voltage passes min)
i_vmin = int(np.argmin(V))
print(f"cycle: {len(t)} points, t_end={t[-1]:.1f}s")
print(f"V_min reached at t={t[i_vmin]:.1f}s (discharge leg end)")
print("at discharge-leg end (start of 4C charge):")
print(f"  V={V[i_vmin]:.4f}  sto_avg={sto_avg[i_vmin]:.4f}  sto_surf={sto_surf[i_vmin]:.4f}  U_neg={u_surf[i_vmin]:.4f}  anode_pot={ap[i_vmin]:.4f}")

print("\n=== trace every ~15th point ===")
print("t[s]   V_cell   anode_pot  U_neg_surf eta_rxn  sto_avg  sto_surf")
for i in range(0, len(t), 15):
    print(f"{t[i]:7.1f} {V[i]:7.4f} {ap[i]:8.4f} {u_surf[i]:7.4f} {eta[i]:8.4f} {sto_avg[i]:6.3f} {sto_surf[i]:6.3f}")
print("...last 6 points:")
for i in range(len(t)-6, len(t)):
    print(f"{t[i]:7.1f} {V[i]:7.4f} {ap[i]:8.4f} {u_surf[i]:7.4f} {eta[i]:8.4f} {sto_avg[i]:6.3f} {sto_surf[i]:6.3f}")

j = int(np.argmin(ap))
print(f"\nanode_pot min = {ap[j]:.4f} V at t={t[j]:.1f}s: V_cell={V[j]:.4f} U_neg={u_surf[j]:.4f} eta={eta[j]:.4f} sto_surf={sto_surf[j]:.4f}")
print(f"charge leg delivered: (t[-1]-t[i_vmin])*4/3600 = {(t[-1]-t[i_vmin])*4/3600:.3f} Ah")
