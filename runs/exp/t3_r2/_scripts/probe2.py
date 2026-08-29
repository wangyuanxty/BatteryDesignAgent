"""Probe 2: verify scalar override of function-valued electrolyte keys + initial-state override legality."""
import pybamm

pv = pybamm.ParameterValues("Chen2020")
# 1) scalar override of a function parameter (electrolyte bridge path)
pv.update({"Electrolyte conductivity [S.m-1]": 1.2}, check_already_exists=False)
print("sigma override ->", pv["Electrolyte conductivity [S.m-1]"], type(pv["Electrolyte conductivity [S.m-1]"]).__name__)
# 2) initial-concentration fixture override (values exist as keys)
pv.update({"Initial concentration in positive electrode [mol.m-3]": 63104.0})
pv.update({"Initial concentration in negative electrode [mol.m-3]": 33133.0})
print("init pos ->", pv["Initial concentration in positive electrode [mol.m-3]"])
print("init neg ->", pv["Initial concentration in negative electrode [mol.m-3]"])
# 3) confirm unknown-name detection still works
try:
    pv.update({"Not a real parameter": 1.0})
    print("unknown key accepted (check_already_exists default) ->", pv.get("Not a real parameter"))
except Exception as e:  # noqa: BLE001
    print("unknown key rejected:", type(e).__name__, str(e)[:80])
print("probe2 OK")