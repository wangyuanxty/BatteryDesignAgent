"""Dump parameter sets (bda library inspection) — read-only on library, writes workspace work/."""
import json
import os

import pybamm

OUT = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\c1_t1_r1\work\param_dumps"
os.makedirs(OUT, exist_ok=True)

KEYS_OF_INTEREST = [
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Positive electrode maximum concentration [mol.m-3]",
    "Negative electrode maximum concentration [mol.m-3]",
    "Positive electrode conductivity [S.m-1]", "Negative electrode conductivity [S.m-1]",
    "Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]",
    "Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Initial concentration in electrolyte [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
    "Nominal cell capacity [A.h]",
    "Cell cooling surface area [m2]", "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell volume [m3]",
    "SEI kinetic rate constant [m.s-1]", "SEI reaction exchange current density [A.m-2]",
    "Initial inner SEI thickness [m]", "Initial outer SEI thickness [m]",
    "Positive electrode cracking rate", "Negative electrode cracking rate",
    "Positive electrode specific heat capacity [J.kg-1.K-1]",
    "Negative electrode specific heat capacity [J.kg-1.K-1]",
    "Separator specific heat capacity [J.kg-1.K-1]",
    "Positive electrode reaction rate constant [m.s-1]",
    "Negative electrode reaction rate constant [m.s-1]",
    "Positive electrode molar mass [kg.mol-1]", "Negative electrode molar mass [kg.mol-1]",
    "Positive electrode OCP [V]", "Negative electrode OCP [V]",
    "Number of electrodes connected in parallel to make a cell",
    "Number of cells connected in series to make a battery",
]

SETS = ["Chen2020", "OKane2022", "ORegan2022", "Prada2013"]
report = {}
for s in SETS:
    try:
        pv = pybamm.ParameterValues(s)
        keys = pv.keys()
        d = {}
        for k in KEYS_OF_INTEREST:
            if k in keys:
                try:
                    v = pv[k]
                    if hasattr(v, "__len__") and not isinstance(v, str):
                        d[k] = f"<array len={len(v)}> {v[:3]}"
                    else:
                        d[k] = str(v)
                except Exception as e:
                    d[k] = f"<err {e}>"
            else:
                d[k] = None
        report[s] = {"n_keys": len(keys), "values": d}
    except Exception as e:
        report[s] = {"error": str(e)}

with open(os.path.join(OUT, "param_sets.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("written to", os.path.join(OUT, "param_sets.json"))
# compact console echo of the keys that matter most
for s, r in report.items():
    if "error" in r:
        print(s, "ERROR", r["error"])
        continue
    v = r["values"]
    print(s, "| pos_th", v.get("Positive electrode thickness [m]"),
          "| neg_th", v.get("Negative electrode thickness [m]"),
          "| pos_maxc", v.get("Positive electrode maximum concentration [mol.m-3]"),
          "| neg_maxc", v.get("Negative electrode maximum concentration [mol.m-3]"),
          "| nom_cap", v.get("Nominal cell capacity [A.h]"),
          "| up_cut", v.get("Upper voltage cut-off [V]"),
          "| SEI_k", v.get("SEI kinetic rate constant [m.s-1]"),
          "| crack_p", v.get("Positive electrode cracking rate"),
          "| crack_n", v.get("Negative electrode cracking rate"),
          "| htc", v.get("Total heat transfer coefficient [W.m-2.K-1]"),
          "| coolA", v.get("Cell cooling surface area [m2]"),
          "| cellvol", v.get("Cell volume [m3]"),
          "| height", v.get("Electrode height [m]"),
          "| width", v.get("Electrode width [m]"))
