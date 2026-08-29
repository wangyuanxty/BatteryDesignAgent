"""Dump the final design parameter set (Chen2020 base + B7 overrides) with all
keys needed for the deliverables, formatted for mechanical transcription."""
import json
import pybamm
import sys

sys.stdout.reconfigure(encoding="utf-8")

base = "Chen2020"
overrides = json.load(open(r"runs\exp\t4_r1_flash\_params_b7.json", encoding="utf-8"))
pv = pybamm.ParameterValues(base)
pv.update(overrides)

want = [
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Nominal cell capacity [A.h]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator porosity",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Positive current collector specific heat capacity [J.kg-1.K-1]",
    "Negative current collector specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Electrolyte specific heat capacity [J.kg-1.K-1]",
    "Positive electrode thermal conductivity [W.m-1.K-1]",
    "Negative electrode thermal conductivity [W.m-1.K-1]",
    "Positive current collector thermal conductivity [W.m-1.K-1]",
    "Negative current collector thermal conductivity [W.m-1.K-1]",
    "Separator thermal conductivity [W.m-1.K-1]",
    "Electrolyte thermal conductivity [W.m-1.K-1]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Cell cooling surface area [m2]",
    "Cell volume [m3]",
    "Cell dry mass [kg]",
    "Positive electrode OCP [V]",
    "Negative electrode OCP [V]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode active material concentration at OCP",
    "Negative electrode active material concentration at OCP",
    "Positive maximum concentration [mol.m-3]",
    "Negative maximum concentration [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Positive electrode exchange-current density [A.m-2]",
    "Negative electrode exchange-current density [A.m-2]",
    "Positive electrode activation energy for exchange-current density [J.mol-1]",
    "Negative electrode activation energy for exchange-current density [J.mol-1]",
    "Electrolyte density [kg.m-3]",
    "Electrolyte concentration [mol.m-3]",
    "Initial SEI thickness [m]",
    "SEI growth activation energy [J.mol-1]",
]

print("=== FINAL DESIGN PARAMETER SET: Chen2020 + B7 overrides ===")
for k in want:
    if k not in pv.keys():
        print(f"[MISSING] {k}")
        continue
    v = pv[k]
    try:
        vs = f"{float(v):.8g}"
    except Exception:
        vs = str(v)[:110]
    print(f"{k} = {vs}")

print()
print("=== keys matching 'density' not captured above ===")
for k in sorted(pv.keys()):
    if "density" in k.lower() and k not in want:
        print("  ", k)
