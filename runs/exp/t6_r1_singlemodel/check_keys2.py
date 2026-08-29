"""Check current key names for diffusivity / particle radius / AM fraction in Chen2020 + model requirements."""
import pybamm

pv = pybamm.ParameterValues("Chen2020")
for k in ("Positive particle diffusivity [m2.s-1]",
          "Negative particle diffusivity [m2.s-1]",
          "Positive particle radius [m]",
          "Negative particle radius [m]",
          "Positive electrode active material volume fraction",
          "Negative electrode active material volume fraction",
          "Positive electrode porosity",
          "Negative electrode porosity",
          "Positive electrode conductivity [S.m-1]"):
    try:
        print(f"{k} = {pv[k]}")
    except KeyError:
        print(f"{k} = <MISSING>")
m = pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible", "SEI": "ec reaction limited"})
req = m.default_parameter_values
print("--- model-required names containing particle/radius/fraction/porosity:")
for k in sorted(req.keys()):
    if any(s in k.lower() for s in ("radius", "fraction", "porosity", "diffusivity")):
        print("  ", k)
