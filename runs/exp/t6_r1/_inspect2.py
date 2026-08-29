"""Scratch inspection 2 (t6_r1): key-name compatibility of LNMO.json overrides vs Chen2020,
and numeric evaluation of the LNMO OCP (discriminant verification)."""
import re
import pybamm
from bda.simulators.lnmo_parameters import lnmo_ocp

print("=== lnmo_ocp sweep (numeric) ===")
for x in (0.0, 0.08, 0.3, 0.5, 0.7, 0.9, 0.92, 1.0):
    print(f"  sto={x:.2f}  OCP={float(lnmo_ocp(x).value):.4f} V")

pv = pybamm.ParameterValues("Chen2020")
keys = list(pv.keys())
print(f"Chen2020 n_keys = {len(keys)}")
for pat in ("maximum concentration", "molar mass", "OCP", "stoich", "volume fraction"):
    print(f"--- keys matching '{pat}'")
    for k in keys:
        if re.search(pat, k, re.I):
            v = pv[k]
            if callable(v) and not isinstance(v, (int, float)):
                print(f"   {k} -> callable {type(v).__name__}")
            else:
                print(f"   {k} = {v}")

LNMO = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
import json
extra = json.load(open(LNMO, encoding="utf-8"))
print("=== LNMO.json override keys ===")
for k, v in extra.items():
    mark = "EXISTS-in-Chen2020" if k in pv else "ADDED (may be inert)"
    print(f"  [{mark}] {k} = {str(v)[:60]}")

print("=== pybamm version ===")
print(pybamm.__version__)

# What does the installed pybamm's model actually read for max conc? Check standard parameters symbol names.
import pybamm as pb
print("DFN max-conc parameter name used by installed pybamm:",
      [str(s) for s in pb.lithium_ion.DFN().parameters if "maximum concentration" in str(s).lower()][:6])
