# -*- coding: utf-8 -*-
"""SEI-growth response proportionality across PyBaMM SEI options.
Chen2020, SPMe, 1C, 100 cycles, isothermal. SEI read at the LAST time point of the last
cycle -- the same convention as bda's run-pyamm `sei_thickness_nm_end` (entries[-1]).
"""
import io, sys, numpy as np, pybamm
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

exp = pybamm.Experiment([("Discharge at 1C until 2.5 V", "Charge at 1C until 4.2 V")] * 100)

def run(option, key, value):
    pv = pybamm.ParameterValues('Chen2020')
    pv.update({key: value})
    pv.update({"Ambient temperature [K]": 298.15}, check_already_exists=False)
    model = pybamm.lithium_ion.SPMe(options={"SEI": option, "thermal": "isothermal"})
    sol = pybamm.Simulation(model, experiment=exp, parameter_values=pv).solve()
    L = float(np.asarray(sol.cycles[-1]["Negative SEI thickness [m]"].entries[-1]).max())
    return L * 1e9

CASES = [
    ("reaction limited",         "SEI reaction exchange current density [A.m-2]", 1.5e-7),
    ("ec reaction limited",      "SEI kinetic rate constant [m.s-1]",             1e-12),
    ("solvent-diffusion limited","SEI solvent diffusivity [m2.s-1]",              2.5e-22),
]
for option, key, base in CASES:
    print(f"== {option}   (scaling: {key}) ==")
    ref = None
    for m in [1.0, 0.5, 0.2, 0.1, 0.01]:
        L = run(option, key, base * m)
        g = L - 5.0                      # growth above the 5 nm initial SEI
        if ref is None: ref = g
        print(f"   x{m:<6g} SEI={L:8.2f} nm   growth={g:9.2f} nm   growth/growth(base)={g/ref:8.4f}   (proportional = {m})")
