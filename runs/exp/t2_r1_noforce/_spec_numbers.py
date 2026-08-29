"""Extract all numbers needed for the closing deliverables (F1 + Chen2020 parameter set)."""
import json
import pybamm

def load(p):
    with open(p, encoding="utf-8-sig") as f:
        return json.load(f)

en = load("cell/r5_f1_energy.json")
fc = load("cell/r5_f1_4c_dfn.json")
a100 = load("cell/r5_f1_aging100_spme.json")
a500 = load("cell/r5_f1_aging500_spme.json")
lowt = load("cell/r5_f1_lowT_spme.json")
one = load("cell/r5_f1_1c_spme.json")

print("== F1 outputs ==")
print("energy:", json.dumps({k: en[k] for k in ["capacity_ah", "energy_wh", "mass_kg", "energy_density_wh_kg",
      "volume_m3", "energy_density_wh_l", "thickness_m", "midpoint_voltage_v", "dcr_ohm", "power_density_w_kg", "area_m2"]}, indent=1))
print("layer_kg_m2:", json.dumps(en["layer_kg_m2"]))
charge_in = fc["capacity_ah"][-1] if isinstance(fc["capacity_ah"], list) else fc["capacity_ah"]
print("4C: T_max_K =", fc["T_max_K"], " min_anode =", min(fc["anode_potential_v"]), " charge_in =", charge_in)
print("1C cap =", one["capacity_ah"], " lowT cap =", lowt["capacity_ah"])
print("SEI100 =", a100["sei_thickness_nm_end"], " SEI500 =", a500["sei_thickness_nm_end"])

print("== Chen2020 params (F1 overrides applied where noted) ==")
pv = pybamm.ParameterValues("Chen2020")
keys = ["Nominal cell capacity [A.h]", "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
        "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
        "Positive current collector thickness [m]", "Negative current collector thickness [m]",
        "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
        "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
        "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
        "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
        "Separator density [kg.m-3]", "Electrode height [m]", "Electrode width [m]",
        "Maximum concentration in positive electrode [mol.m-3]", "Maximum concentration in negative electrode [mol.m-3]",
        "Initial concentration in positive electrode [mol.m-3]", "Initial concentration in negative electrode [mol.m-3]",
        "Cation transference number", "Typical electrolyte concentration [mol.m-3]",
        "EC initial concentration in electrolyte [mol.m-3]", "Positive particle radius [m]",
        "Negative particle radius [m]", "SEI kinetic rate constant [m.s-1]",
        "Total heat transfer coefficient [W.m-2.K-1]"]
for k in keys:
    v = pv[k]
    print(f"  {k} = {v if not hasattr(v, 'name') else type(v).__name__}")
print("F1 overrides: Negative particle radius 3e-6, Negative electrode porosity 0.42, SEI kinetic rate constant 4e-13")
# N/P calculation (capacity density x thickness ratio)
F = 96485.0 / 3600.0  # Ah per mol e-
cneg = 33133.0 * F * 0.75 * (1 - 0.42) * 85.2e-6
cpos = 63104.0 * F * 0.665 * (1 - float(pv["Positive electrode porosity"])) * 75.6e-6
print(f"neg areal capacity = {cneg:.3f} Ah/m2, pos areal capacity = {cpos:.3f} Ah/m2, N/P = {cneg/cpos:.3f}")
