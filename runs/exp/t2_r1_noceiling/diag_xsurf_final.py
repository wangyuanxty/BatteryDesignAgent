# Final mechanism check: exact anode surface stoichiometry + OCP at the 4C abort.
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
exp = pybamm.Experiment([f"Discharge at 1C until {v_min} V", f"Charge at 4C until {v_max} V"])
model = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=PV)
sol = sim.solve()

c_max_n = float(PV["Maximum concentration in negative electrode [mol.m-3]"])
ocp = PV["Negative electrode OCP [V]"]
xs = float(np.asarray(sol["X-averaged negative particle surface concentration [mol.m-3]"].entries)[-1])
xb = float(np.asarray(sol["X-averaged negative particle concentration [mol.m-3]"].entries)[-1].mean())
print(f"abort state: x_surf={xs/c_max_n:.4f}  x_bulk={xb/c_max_n:.4f}")
for name in ["Negative electrode open-circuit potential [V]",
             "Negative electrode bulk open-circuit potential [V]"]:
    e = np.asarray(sol[name].entries)
    if e.ndim == 1:
        print(f"{name}: scalar last={float(e[-1]):+.4f} min={float(e.min()):+.4f}")
    else:
        row = e[-1, :]
        print(f"{name}: n={len(row)} first5={np.round(row[:5],3)} last5={np.round(row[-5:],3)} "
              f"min={row.min():+.4f} at idx {int(row.argmin())} max={row.max():+.4f} at idx {int(row.argmax())}")
spd = np.asarray(sol["Negative electrode surface potential difference at separator interface [V]"].entries)
eta = np.asarray(sol["Negative electrode reaction overpotential [V]"].entries)[-1, :]
# neg electrode block: find its extent (values < 0); first neg point = sep interface
negvals = eta[eta < 0]
print(f"surface potdiff min={spd.min():.4f} at t_end")
print(f"eta_neg: sep-side={negvals[0]:.4f} ... CC-side={negvals[-1]:.4f}  (n_neg_points={len(negvals)})")
print(f"check(sep): spd_end - eta_neg_sep = {spd[-1]:.4f} - ({negvals[0]:.4f}) = {spd[-1]-negvals[0]:.4f}")
print(f"check(CC) : spd_end - eta_neg_CC  = {spd[-1]:.4f} - ({negvals[-1]:.4f}) = {spd[-1]-negvals[-1]:.4f}")
# U(c_s_surf) processed variable vs the OCP at x_surf
u_surf_proc = float(np.asarray(sol["Negative electrode open-circuit potential [V]"].entries)[-1])
print(f"consistency: U_surf(processed)={u_surf_proc:+.4f} vs spd-eta_neg_sep={spd[-1]-negvals[0]:.4f}")
