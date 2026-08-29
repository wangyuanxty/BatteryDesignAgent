import pybamm
pv = pybamm.ParameterValues("OKane2022")
keys = [
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Separator thickness [m]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Cation transference number",
    "Total heat transfer coefficient [W.m-2.K-1]",
    "Cell cooling surface area [m2]",
    "Positive electrode density [kg.m-3]",
    "Negative electrode density [kg.m-3]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Positive electrode active material volume fraction",
    "Negative particle radius [m]",
    "Positive particle radius [m]",
    "Upper voltage cut-off [V]",
    "Lower voltage cut-off [V]",
    "Electrode height [m]",
    "Electrode width [m]",
]
for k in keys:
    v = pv.get(k) if k in pv.keys() else "<MISSING>"
    print(k, "=", repr(v)[:80])