# Diagnostic: decompose the 4C charge terminal voltage of R3C into physical terms.
import sys, json
import numpy as np
import pybamm

sys.path.insert(0, r".claude/skills/virtual-battery-factory/scripts")
from bda.simulators import pybamm_runner as R

params = json.load(open("runs/exp/t5_r1_noceiling/candidates/r3_C_params.json", encoding="utf-8"))
p = dict(R.PROTOCOLS["4C_charge_45C"])
pv0 = pybamm.ParameterValues("Chen2020")
pv0.update(params)
pv0.update({"Ambient temperature [K]": p["T_amb_K"]}, check_already_exists=False)
pv0.update(R.PLATING_PARAM_DEFAULTS, check_already_exists=False)
for name, value in R.THERMAL_PARAM_DEFAULTS.items():
    if name not in pv0:
        pv0.update({name: value}, check_already_exists=False)
if "Cell volume [m3]" not in pv0:
    pv0.update({"Cell volume [m3]": R._cell_volume_default(pv0)}, check_already_exists=False)

options = {"thermal": "lumped", "lithium plating": "irreversible"}
v_min = float(pv0["Lower voltage cut-off [V]"])
v_max = float(pv0["Upper voltage cut-off [V]"])
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", f"Charge at 4C until {v_max} V"])
model = pybamm.lithium_ion.SPMe(options=options)
sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv0)
sol = sim.solve()

t = sol["Time [s]"].entries
V = sol["Terminal voltage [V]"].entries
i_end = int(np.argmin(V))
t_c0 = float(t[i_end])
print("discharge end at t =", round(t_c0, 1), "s, V =", round(float(V[i_end]), 3))
print("charge segment length =", round(float(t[-1] - t_c0), 1), "s")

def proc(name):
    try:
        return sol[name]
    except Exception as e:
        print("MISSING VAR:", name, "->", str(e).split(". Best matches")[0])
        return None

names = [
    "Terminal voltage [V]",
    "Negative electrode surface potential difference at separator interface [V]",
    "Negative electrode surface potential difference [V]",
    "Positive electrode surface potential difference at separator interface [V]",
    "Positive electrode surface potential difference [V]",
    "X-averaged negative electrode open-circuit potential [V]",
    "X-averaged positive electrode open-circuit potential [V]",
    "X-averaged negative electrode reaction overpotential [V]",
    "X-averaged positive electrode reaction overpotential [V]",
    "X-averaged battery concentration overpotential [V]",
    "X-averaged electrolyte ohmic losses [V]",
    "X-averaged negative electrode ohmic losses [V]",
    "X-averaged positive electrode ohmic losses [V]",
    "X-averaged electrolyte concentration [mol.m-3]",
    "X-averaged negative particle concentration [mol.m-3]",
    "X-averaged positive particle concentration [mol.m-3]",
    "X-averaged cell temperature [K]",
]
series = {n: proc(n) for n in names}
c_max_n = float(pv0["Maximum concentration in negative electrode [mol.m-3]"])
c_max_p = float(pv0["Maximum concentration in positive electrode [mol.m-3]"])

def ev(s, tt):
    if s is None:
        return None
    try:
        return float(np.asarray(s(tt)).flatten()[0])
    except Exception:
        return None

def fmt(name, tt, nd=3):
    v = ev(series[name], tt)
    return f"{v:.{nd}f}" if v is not None else "NA"

cols = ["t_s", "V", "an_sep", "an_cc", "cat_sep", "cat_cc",
        "OCP_c", "OCP_a", "eta_rx_c", "eta_rx_a", "eta_conc_batt",
        "elyte_ohm", "c_e_avg", "x_n_avg", "x_c_avg", "T_K"]
print(" | ".join(cols))
fracs = [0.0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.85, 0.97, 1.0]
for f in fracs:
    tt = t_c0 + (float(t[-1]) - t_c0) * f
    vals = {
        "t_s": f"{tt:.0f}",
        "V": fmt("Terminal voltage [V]", tt),
        "an_sep": fmt("Negative electrode surface potential difference at separator interface [V]", tt),
        "an_cc": fmt("Negative electrode surface potential difference [V]", tt),
        "cat_sep": fmt("Positive electrode surface potential difference at separator interface [V]", tt),
        "cat_cc": fmt("Positive electrode surface potential difference [V]", tt),
        "OCP_c": fmt("X-averaged positive electrode open-circuit potential [V]", tt),
        "OCP_a": fmt("X-averaged negative electrode open-circuit potential [V]", tt),
        "eta_rx_c": fmt("X-averaged positive electrode reaction overpotential [V]", tt),
        "eta_rx_a": fmt("X-averaged negative electrode reaction overpotential [V]", tt),
        "eta_conc_batt": fmt("X-averaged battery concentration overpotential [V]", tt),
        "elyte_ohm": fmt("X-averaged electrolyte ohmic losses [V]", tt),
        "c_e_avg": fmt("X-averaged electrolyte concentration [mol.m-3]", tt, 0),
        "x_n_avg": fmt("X-averaged negative particle concentration [mol.m-3]", tt),
        "x_c_avg": fmt("X-averaged positive particle concentration [mol.m-3]", tt),
        "T_K": fmt("X-averaged cell temperature [K]", tt, 1),
    }
    vn = ev(series["X-averaged negative particle concentration [mol.m-3]"], tt)
    vc = ev(series["X-averaged positive particle concentration [mol.m-3]"], tt)
    vals["x_n_avg"] = f"{vn/c_max_n:.3f}" if vn is not None else "NA"
    vals["x_c_avg"] = f"{vc/c_max_p:.3f}" if vc is not None else "NA"
    print(" | ".join(vals[c] for c in cols))
