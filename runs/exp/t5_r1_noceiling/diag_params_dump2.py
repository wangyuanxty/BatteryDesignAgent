import json
import pybamm

# 1) keys present in the R4A DFN 4C tool output
with open("runs/exp/t5_r1_noceiling/cell/r4_A_4c_dfn.json", encoding="utf-8") as f:
    d = json.load(f)
print("R4A 4C DFN keys:", sorted(d.keys()))
for k in d:
    v = d[k]
    if isinstance(v, list):
        print(f"  {k}: list len={len(v)}, first={v[0] if v else None}, last={v[-1] if v else None}")

# 2) electrolyte / thermal parameter-set values
pv = pybamm.ParameterValues("Chen2020")
keys = [
    "Initial concentration in electrolyte [mol.m-3]",
    "Typical electrolyte concentration [mol.m-3]",
    "Cation transference number",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Ambient temperature [K]",
    "Reference temperature [K]",
    "Nominal cell capacity [A.h]",
    "Typical current [A]",
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Separator thickness [m]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive electrode specific capacity [A.h.kg-1]",
    "Negative electrode specific capacity [A.h.kg-1]",
    "Positive electrode OCV at 100% SOC [V]",
    "Positive electrode OCV at 0% SOC [V]",
    "Negative electrode OCV at 100% SOC [V]",
    "Negative electrode OCV at 0% SOC [V]",
    "Positive electrode surface area to volume ratio [m-1]",
    "Negative electrode surface area to volume ratio [m-1]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode thermal conductivity [W.m-1.K-1]",
    "Negative electrode thermal conductivity [W.m-1.K-1]",
    "Separator thermal conductivity [W.m-1.K-1]",
]
for k in keys:
    try:
        print(f"{k} = {pv[k]}")
    except Exception as e:
        print(f"{k} = MISSING ({type(e).__name__})")
