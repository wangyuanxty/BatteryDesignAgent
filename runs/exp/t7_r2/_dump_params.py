import pybamm

keys = [
    "Electrode height [m]", "Electrode width [m]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]",
    "Separator thickness [m]", "Positive electrode porosity", "Negative electrode porosity",
    "Separator porosity", "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]",
    "Separator density [kg.m-3]", "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Nominal cell capacity [A.h]", "Negative electrode active material volume fraction",
    "Positive electrode active material volume fraction", "Positive particle radius [m]", "Negative particle radius [m]",
    "Cell volume [m3]", "Cell cooling surface area [m2]", "Total heat transfer coefficient [W.m-2.K-1]",
    "SEI kinetic rate constant [m.s-1]", "SEI reaction exchange current density [A.m-2]",
    "Electrolyte conductivity [S.m-1]", "Cation transference number",
    "Upper voltage cut-off [V]", "Lower voltage cut-off [V]",
    "Positive electrode cracking rate", "Negative electrode cracking rate",
    "Maximum concentration in negative electrode [mol.m-3]",
    "Initial concentration in negative electrode [mol.m-3]",
]

for base in ["Chen2020", "OKane2022", "ORegan2022"]:
    pv = pybamm.ParameterValues(base)
    print("=" * 20, base)
    for k in keys:
        try:
            v = pv[k]
            if callable(v):
                try:
                    v = f"callable(f(1.0)={v(1.0):.4g})"
                except Exception:
                    try:
                        v = f"callable()"
                    except Exception:
                        v = "callable(?)"
            elif isinstance(v, (tuple, list)):
                v = repr(v)
            print(f"  {k} = {v}")
        except Exception:
            print(f"  {k} = MISSING")