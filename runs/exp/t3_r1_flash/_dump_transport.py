import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
out = {}
for k in [
    "Initial concentration in electrolyte [mol.m-3]",
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Positive electrode diffusivity [m2.s-1]",
    "Negative electrode diffusivity [m2.s-1]",
    "Positive electrode exchange-current density [A.m-2]",
    "Negative electrode exchange-current density [A.m-2]",
    "Positive electrode OCP [V]",
    "Negative electrode OCP [V]",
]:
    v = pv[k]
    if callable(v):
        try:
            v = float(v(0.5))
        except Exception:
            v = "<function>"
    out[k] = v
# sample concentration-dependent functions at c=1000 mol/m3 (try (c,T) then (c) signature)
def sample(f, x):
    try:
        return float(f(x, 298.15))
    except TypeError:
        return float(f(x))

for k in ["Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]"]:
    f = pv[k]
    if callable(f):
        out[k + "@1000"] = sample(f, 1000.0)
        out[k + "@2000"] = sample(f, 2000.0)
for k in ["Positive electrode diffusivity [m2.s-1]", "Negative electrode diffusivity [m2.s-1]"]:
    f = pv[k]
    if callable(f):
        out[k + "@c0.5"] = sample(f, 0.5)
        out[k + "@c0.9"] = sample(f, 0.9)
print(json.dumps(out, indent=1, default=str))
