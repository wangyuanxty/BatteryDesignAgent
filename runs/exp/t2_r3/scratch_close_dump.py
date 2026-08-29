# One-off closing data dump for t2_r3 deliverables (audit trace: values read from tool outputs / pybamm Chen2020 set)
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\cell"

import pybamm
pv = pybamm.ParameterValues("Chen2020")
KEYS = [
 "Electrode height [m]","Electrode width [m]","Nominal cell capacity [A.h]",
 "Lower voltage cut-off [V]","Upper voltage cut-off [V]",
 "Positive electrode thickness [m]","Negative electrode thickness [m]",
 "Separator thickness [m]","Separator porosity",
 "Positive electrode porosity","Negative electrode porosity",
 "Positive current collector thickness [m]","Negative current collector thickness [m]",
 "Positive current collector density [kg.m-3]","Negative current collector density [kg.m-3]",
 "Positive electrode density [kg.m-3]","Negative electrode density [kg.m-3]",
 "Positive electrode active material volume fraction","Negative electrode active material volume fraction",
 "Positive electrode conductive additive volume fraction","Positive electrode binder volume fraction",
 "Negative electrode conductive additive volume fraction","Negative electrode binder volume fraction",
 "Positive particle radius [m]","Negative particle radius [m]",
 "Maximum concentration in positive electrode [mol.m-3]","Maximum concentration in negative electrode [mol.m-3]",
 "Initial concentration in positive electrode [mol.m-3]","Initial concentration in negative electrode [mol.m-3]",
 "Electrolyte conductivity [S.m-1]","Electrolyte diffusivity [m2.s-1]","Cation transference number",
 "SEI kinetic rate constant [m.s-1]","SEI reaction exchange current density [A.m-2]",
 "SEI partial molar volume [m3.mol-1]","Initial SEI thickness [m]",
 "Total heat transfer coefficient [W.m-2.K-1]","Reference temperature [K]","Ambient temperature [K]",
 "Positive electrode surface area [m2]","Negative electrode surface area [m2]",
 "Positive current collector surface area [m2]","Number of electrodes connected in parallel to make a cell",
 "Number of cells connected in series to make a battery",
]
print("=== CHEN2020 BASELINE PARAMS ===")
for k in KEYS:
    try:
        v = pv[k]
        if hasattr(v, "value"):
            v = v.value
        print(f"{k} = {v}")
    except Exception as e:
        print(f"{k} = ABSENT ({type(e).__name__})")

def scalars(path, label, extra_min_keys=()):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    print(f"\n=== {label} ({path.split(chr(92))[-1]}) scalar keys ===")
    for k, v in d.items():
        if isinstance(v, (int, float, bool, str)):
            print(f"  {k} = {v}")
    for k in extra_min_keys:
        if k in d and isinstance(d[k], list):
            a = [x for x in d[k] if isinstance(x, (int, float))]
            print(f"  {k}: len={len(d[k])} min={min(a):.6g} max={max(a):.6g} first={d[k][:3]}")
    return d

scalars(f"{ROOT}\\r7_final_1c_dfn.json", "r7 1C DFN")
d4 = scalars(f"{ROOT}\\r7_final_4c_dfn.json", "r7 4C DFN", ("anode_potential_v",))
try:
    t = d4.get("time_s") or d4.get("Time [s]")
except Exception:
    pass
ag100 = scalars(f"{ROOT}\\r6_combo-v5-final_aging100_spme.json", "r6 aging100")
ag500 = scalars(f"{ROOT}\\r6_combo-v5-final_aging500_spme.json", "r6 aging500")