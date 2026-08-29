"""Diagnostic v3: trace anode sto for NPup (L_neg 120um + archThin + hiTrans) and L_neg 150um."""
import json
import numpy as np
import pybamm
from bda.simulators.lnmo_parameters import lnmo_ocp
from bda.simulators.pybamm_runner import PLATING_PARAM_DEFAULTS

base = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
extra = json.load(open(base, encoding="utf-8"))
for key in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(key), str):
        extra[key] = lnmo_ocp

def trace(label, overrides):
    pv = pybamm.ParameterValues("Chen2020")
    pv.update(extra, check_already_exists=False)
    pv.update(overrides)
    pv.update({"Ambient temperature [K]": 318.15}, check_already_exists=False)
    pv.update(PLATING_PARAM_DEFAULTS, check_already_exists=False)
    model = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible"})
    v_min = float(pv["Lower voltage cut-off [V]"])
    exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", "Charge at 4C until 4.7 V"])
    sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
    sol = sim.solve()
    cyc = sol.cycles[-1]
    def r(x): return np.asarray(x.entries).ravel()
    t = r(cyc["Time [s]"]); V = r(cyc["Terminal voltage [V]"])
    ap = r(cyc["Negative electrode surface potential difference at separator interface [V]"])
    sto_avg = r(cyc["Negative electrode stoichiometry"])
    sto_surf = r(cyc["Negative particle surface stoichiometry"])
    u_surf = r(cyc["Negative electrode open-circuit potential [V]"])
    eta = r(cyc["Negative electrode reaction overpotential [V]"])
    print(f"\n=== {label} ===")
    print(f"charge leg: {t[-1]:.0f}s = {(t[-1])*18/3600:.2f} Ah @18A; anode_pot min={ap.min():.4f} at t={t[int(np.argmin(ap))]:.0f}s")
    j = int(np.argmin(ap))
    print(f"  at min: V_cell={V[j]:.4f} U_neg={u_surf[j]:.4f} eta={eta[j]:.4f} sto_surf={sto_surf[j]:.4f} sto_avg={sto_avg[j]:.4f}")
    # when does sto_surf cross 0.95?
    k = np.argmax(sto_surf > 0.95) if np.any(sto_surf > 0.95) else -1
    if k >= 0:
        print(f"  sto_surf crosses 0.95 at t={t[k]:.0f}s: V_cell={V[k]:.4f} anode_pot={ap[k]:.4f}")
    else:
        print("  sto_surf never exceeds 0.95")
    # end-of-charge values
    print(f"  at cutoff: V={V[-1]:.4f} anode_pot={ap[-1]:.4f} sto_surf={sto_surf[-1]:.4f} U_neg={u_surf[-1]:.4f} eta={eta[-1]:.4f}")
    return sol

archthin_hiTrans = {
    "Separator thickness [m]": 8e-6, "Positive current collector thickness [m]": 8e-6,
    "Negative current collector thickness [m]": 6e-6, "Cation transference number": 0.45,
    "Electrolyte conductivity [S.m-1]": 1.5, "Electrolyte diffusivity [m2.s-1]": 4e-10,
}
trace("NPup (L_neg 120um)", {**archthin_hiTrans, "Negative electrode thickness [m]": 1.2e-4})
trace("L_neg 150um", {**archthin_hiTrans, "Negative electrode thickness [m]": 1.5e-4})
trace("L_neg 180um", {**archthin_hiTrans, "Negative electrode thickness [m]": 1.8e-4})
