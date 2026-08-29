"""Preparation step (Stage 1, zero simulation budget): dump Chen2020 parameter set
keys relevant to this case to (a) verify the deterministic base mapping (anchor table:
task names no electrode system -> Chen2020) and (b) inventory available design levers."""
import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
keys = sorted(pv.keys())

interesting = [
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "SEI kinetic rate constant [m.s-1]",
    "SEI reaction exchange current density [A.m-2]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator porosity",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Electrode height [m]",
    "Electrode width [m]",
    "Nominal cell capacity [A.h]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Maximum concentration in positive electrode [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Cell volume [m3]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Positive electrode OCP [V]",
    "Negative electrode OCP [V]",
]

out = {"total_key_count": len(keys), "items": {}}
for name in interesting:
    if name in pv:
        v = pv[name]
        if callable(v):
            out["items"][name] = {"type": "function", "repr": str(v)}
        else:
            out["items"][name] = {"type": type(v).__name__, "value": v}

# Which thermal/geometry keys are missing (runner would inject defaults)?
thermal_needed = [
    "Cell cooling surface area [m2]",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Positive current collector conductivity [S.m-1]",
    "Negative current collector conductivity [S.m-1]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]",
    "Negative current collector density [kg.m-3]",
    "Positive current collector specific heat capacity [J.kg-1.K-1]",
    "Negative current collector specific heat capacity [J.kg-1.K-1]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Cell volume [m3]",
]
out["thermal_missing"] = [n for n in thermal_needed if n not in pv]

plating_needed = [
    "Initial plated lithium concentration [mol.m-3]",
    "Typical plated lithium concentration [mol.m-3]",
    "Lithium plating transfer coefficient",
    "Exchange-current density for plating [A.m-2]",
    "Exchange-current density for stripping [A.m-2]",
]
out["plating_missing"] = [n for n in plating_needed if n not in pv]

out["has_sei_kinetics"] = "SEI kinetic rate constant [m.s-1]" in pv
out["negative_contains_siox"] = any(
    "Si" in k and "negative" in k.lower() for k in keys
)
out["all_key_names"] = keys

with open("runs/exp/t2_r1_singlemodel/prep_chen2020_dump.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False, default=str)
print("dumped", len(keys), "keys; missing thermal:", len(out["thermal_missing"]),
      "; missing plating:", len(out["plating_missing"]),
      "; has SEI kinetics:", out["has_sei_kinetics"],
      "; SiOx keys:", out["negative_contains_siox"])
