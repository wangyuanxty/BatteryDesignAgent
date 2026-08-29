import sys, json
sys.stdout.reconfigure(encoding="utf-8")
import pybamm
pv = pybamm.ParameterValues("Chen2020")
sig = pv["Electrolyte conductivity [S.m-1]"]
diff = pv["Electrolyte diffusivity [m2.s-1]"]
c = pv["Initial concentration in electrolyte [mol.m-3]"]
cc = getattr(c, "value", 1000.0)
print("typ c =", cc)
print("sigma(1M,298.15) =", sig(cc, 298.15))
print("D(1M,298.15) =", diff(cc, 298.15))
d = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\cell\r7_final_4c_dfn.json", encoding="utf-8"))
print("4c keys:", list(d.keys()))
t = d.get("time_s") or d.get("Time [s]")
if t is not None:
    print("4c last time =", t[-1], "n =", len(t))
else:
    for k, v in d.items():
        if isinstance(v, list):
            print("list key", k, "len", len(v), "last", v[-1])
lt = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\cell\r7_final_lowT_dfn.json", encoding="utf-8"))
print("lowT dfn capacity_ah =", lt.get("capacity_ah"))