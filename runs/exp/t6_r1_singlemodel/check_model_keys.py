"""Check which parameter names the PyBaMM 26.7 models actually consume (new vs old convention)."""
import pybamm

for name, model in [
    ("SPMe", pybamm.lithium_ion.SPMe(options={"thermal": "lumped", "lithium plating": "irreversible", "SEI": "ec reaction limited"})),
    ("DFN", pybamm.lithium_ion.DFN(options={"thermal": "lumped", "lithium plating": "irreversible", "SEI": "ec reaction limited"})),
]:
    pv = model.default_parameter_values
    print("=" * 70)
    print("MODEL:", name, "| n params:", len(pv.keys()))
    for k in sorted(pv.keys()):
        if any(s in k.lower() for s in ("concentration", "stoich", "ocp", "open")):
            print("   REQ:", k)
