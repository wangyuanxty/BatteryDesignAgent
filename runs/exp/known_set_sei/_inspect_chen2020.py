import pybamm
pv = pybamm.ParameterValues("Chen2020")
for key in sorted(pv.keys()):
    if any(s in key.lower() for s in ("sei kinetic", "sei", "nominal cell", "electrode height", "electrode width", "positive electrode thickness", "negative electrode thickness", "separator thickness", "porosity", "density")):
        print(key, "=", pv[key])
