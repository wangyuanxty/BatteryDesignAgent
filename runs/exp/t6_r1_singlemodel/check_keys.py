"""Check pybamm version, Chen2020 concentration/stoich keys, electrolyte conductivity fn at 298/318 K."""
import pybamm

print("pybamm:", pybamm.__version__)
pv = pybamm.ParameterValues("Chen2020")
hits = [k for k in pv.keys() if "concentration" in k.lower()]
print("concentration keys:", hits)
hits2 = [k for k in pv.keys() if "stoichiometry" in k.lower() or "stoich" in k.lower()]
print("stoich keys:", hits2)
for k in hits:
    print("  ", k, "=", pv[k])
for k in hits2:
    print("  ", k, "=", pv[k])
try:
    f = pv["Electrolyte conductivity [S.m-1]"]
    if callable(f):
        print("electrolyte conductivity @298.15:", f(298.15), " @318.15:", f(318.15))
except KeyError:
    print("no Electrolyte conductivity key in Chen2020")
# graphite OCP type
print("negative OCP type:", type(pv["Negative electrode OCP [V]"]))
print("OCP stoich limits neg:", pv.get("Negative electrode OCP stoich limits"))
print("OCP stoich limits pos:", pv.get("Positive electrode OCP stoich limits"))
