import json
# Read one of the simulation outputs to understand the parameter set
# Let's look at the bda library for Chen2020 defaults
import sys
sys.path.insert(0, ".")
from bda.simulators.pyamm_sim import load_base_params
params = load_base_params("Chen2020")
# Print architecture-relevant params
arch_keys = [
    "Positive electrode thickness [m]",
    "Negative electrode thickness [m]",
    "Positive electrode porosity",
    "Negative electrode porosity",
    "Separator thickness [m]",
    "Separator porosity",
    "Positive current collector thickness [m]",
    "Negative current collector thickness [m]",
    "Positive particle radius [m]",
    "Negative particle radius [m]",
    "Positive electrode active material volume fraction",
    "Negative electrode active material volume fraction",
    "Nominal cell capacity [A.h]",
    "Electrode height [m]",
    "Electrode width [m]",
]
for k in arch_keys:
    if k in params:
        v = params[k]
        print(f"  {k}: {v}")
    else:
        print(f"  {k}: NOT FOUND")
