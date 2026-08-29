import sys, json
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts")
sys.path.insert(0, r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators")
from pybamm_runner import run_simulation  # may not be importable; fallback below

keys = [
    "EC diffusivity [m2.s-1]",
    "EC initial concentration in electrolyte [mol.m-3]",
    "SEI open-circuit potential [V]",
    "SEI resistivity [Ohm.m]",
    "Initial SEI thickness [m]",
    "Negative electrode exchange-current density [A.m-2]",
    "Lower voltage cut-off [V]",
    "Upper voltage cut-off [V]",
]
try:
    from pybamm_runner import load_parameter_set
except Exception:
    load_parameter_set = None

base = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
if load_parameter_set is not None:
    pv = load_parameter_set(base)
else:
    import pybamm
    pv = pybamm.ParameterValues("Chen2020")
    with open(base, encoding="utf-8") as fh:
        over = json.load(fh)
    for k, v in over.items():
        try:
            pv.update({k: v}, check_already_exists=False)
        except ValueError:
            pass  # function-valued keys (OCP) are bound by run_simulation

print("has:", [k for k in keys if k in pv])
for k in keys:
    if k in pv:
        print(k, "=", pv[k])
