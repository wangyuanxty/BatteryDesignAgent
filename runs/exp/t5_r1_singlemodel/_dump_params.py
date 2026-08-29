import pybamm

KEYS = [
    "particle radius",
    "current collector",
    "Separator",
    "heat transfer",
    "Electrolyte conductivity",
    "Electrolyte diffusivity",
    "transference",
    "porosity",
    "thickness",
    "Electrode height",
    "Electrode width",
    "Nominal cell capacity",
    "density",
    "maximum concentration",
    "SEI kinetic rate constant",
    "SEI reaction exchange current density",
    "cracking rate",
    "Negative electrode OCP",
    "Positive electrode OCP",
    "entropic",
    "activation energy",
    "reference temperature",
    "Ambient temperature",
    "Initial temperature",
]

for n in ["Chen2020", "OKane2022"]:
    pv = pybamm.ParameterValues(n)
    print("=" * 25, n, "=" * 25)
    for k in pv.keys():
        if any(s in k for s in KEYS):
            v = pv[k]
            print(f"  {k!r}: {v!r}")
