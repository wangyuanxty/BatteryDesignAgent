"""Scratch: evaluate Chen2020/OKane2022 electrolyte transport functions at reference states."""
import pybamm

for name in ["Chen2020", "OKane2022"]:
    pv = pybamm.ParameterValues(name)
    for key in ["Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]"]:
        f = pv[key]
        if callable(f):
            try:
                v25 = f(1000.0, 298.15)
                v45 = f(1000.0, 318.15)
            except Exception as e:
                v25 = v45 = f"err {e}"
            print(f"{name} {key}: func -> c=1000 T=298: {v25}, T=318: {v45}")
        else:
            print(f"{name} {key}: scalar {f}")
    print(f"{name} Cation transference number: {pv['Cation transference number']}")
