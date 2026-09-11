import pybamm

pv = pybamm.ParameterValues("OKane2022")
keys = list(pv.keys())
with open("param_keys.txt", "w", encoding="utf-8") as out:
    for k in keys:
        if any(s in k.lower() for s in ["capacity", "stoichiometry", "maximum concentration", "molar mass", "initial concentration", "volume fraction", "surface area"]):
            out.write(k + " = " + str(pv[k]) + "\n")
print("done")
