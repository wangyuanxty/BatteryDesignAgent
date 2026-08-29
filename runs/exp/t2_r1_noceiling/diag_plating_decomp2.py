# Decompose the 4C-charge anode potential dive — take 2: surface concentrations + OCP evaluation.
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

def decompose(R_neg, R_pos, label):
    pv = pybamm.ParameterValues("Chen2020")
    pv.update(dict(PV.items()))
    if R_neg: pv.update({"Negative particle radius [m]": R_neg})
    if R_pos: pv.update({"Positive particle radius [m]": R_pos})
    exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", f"Charge at 4C until {v_max} V"])
    model = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible"})
    sim = pybamm.Simulation(model, experiment=exp, parameter_values=pv)
    sol = sim.solve()
    t = np.asarray(sol["Time [s]"].entries)
    c_max_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
    c_max_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])
    # evaluate Chen2020 negative OCP at arbitrary x (using the parameter function directly)
    ocp_neg = pv["Negative electrode OCP [V]"]
    ocp_pos = pv["Positive electrode OCP [V]"]

    # X-averaged concentration variables are saved on their own (coarser) time grid;
    # only the abort state (last point) is needed for the decomposition.
    for lbl, i in [("abort", -1)]:
        xs = float(np.asarray(sol["X-averaged negative particle surface concentration [mol.m-3]"].entries)[i]) / c_max_n
        xb = float(np.asarray(sol["X-averaged negative particle concentration [mol.m-3]"].entries)[i].mean()) / c_max_n
        ys = float(np.asarray(sol["X-averaged positive particle surface concentration [mol.m-3]"].entries)[i]) / c_max_p
        yb = float(np.asarray(sol["X-averaged positive particle concentration [mol.m-3]"].entries)[i].mean()) / c_max_p
        try:
            U_surf = float(ocp_neg(pybamm.Scalar(1e6 * xs)))
            U_pos = float(ocp_pos(pybamm.Scalar(1e6 * ys)))
        except Exception as ex:
            U_surf, U_pos = np.nan, np.nan
        eta = np.asarray(sol["Negative electrode reaction overpotential [V]"].entries)[i, :]
        phi_e = np.asarray(sol["Electrolyte potential [V]"].entries)[i, :]
        spd = float(np.asarray(sol["Negative electrode surface potential difference at separator interface [V]"].entries)[i])
        print(f"[{label}] at {lbl}: x_surf={xs:.4f} x_bulk={xb:.4f} | y_surf={ys:.4f} y_bulk={yb:.4f}")
        print(f"    U_neg(x_surf)~{U_surf:.4f} U_pos(y_surf)~{U_pos:.4f} | surface_potdiff={spd:.4f}")
        print(f"    eta_neg range {eta.min():.4f}..{eta.max():.4f} | phi_e range {phi_e.min():.4f}..{phi_e.max():.4f}")

decompose(None, None, "baseline")
decompose(3.5e-6, None, "R_neg=3.5um")
decompose(None, 2.5e-6, "R_pos=2.5um")
