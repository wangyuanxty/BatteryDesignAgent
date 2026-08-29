"""Dump Chen2020 parameter set keys of design interest (anchor verification + ceiling grounding)."""
import json
import pybamm

pv = pybamm.ParameterValues("Chen2020")
interesting = [k for k in pv.keys() if any(
    s in k.lower() for s in [
        "electrode thickness", "porosity", "particle radius", "current collector",
        "separator", "electrolyte", "transference", "sei", "density", "capacity",
        "initial concentration in negative", "initial concentration in positive",
        "maximum concentration", "cracking", "heat transfer", "height", "width",
        "nominal cell capacity", "lower voltage", "upper voltage"
    ]
)]
out = {k: (pv[k] if not isinstance(pv[k], (list, tuple)) else "ARRAY") for k in sorted(interesting)}
print(json.dumps(out, indent=1, default=str))
