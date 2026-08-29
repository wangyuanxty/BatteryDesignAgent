"""Scratch inspection (t6_r1): dump Chen2020 / LNMO-merged parameter values and verify the
anchor-table discriminant before choosing --base. Read-only; writes nothing to the workspace."""
import json
import pybamm
from bda.simulators.lnmo_parameters import lnmo_ocp

KEYS = [
    "Nominal cell capacity [A.h]",
    "Positive electrode thickness [m]", "Negative electrode thickness [m]", "Separator thickness [m]",
    "Positive electrode porosity", "Negative electrode porosity", "Separator porosity",
    "Positive electrode active material volume fraction", "Negative electrode active material volume fraction",
    "Positive electrode density [kg.m-3]", "Negative electrode density [kg.m-3]", "Separator density [kg.m-3]",
    "Positive electrode maximum concentration [mol.m-3]", "Negative electrode maximum concentration [mol.m-3]",
    "Initial concentration in positive electrode [mol.m-3]", "Initial concentration in negative electrode [mol.m-3]",
    "Electrode height [m]", "Electrode width [m]",
    "Positive current collector thickness [m]", "Negative current collector thickness [m]",
    "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
    "Positive particle radius [m]", "Negative particle radius [m]",
    "Electrolyte conductivity [S.m-1]", "Electrolyte diffusivity [m2.s-1]", "Cation transference number",
    "SEI kinetic rate constant [m.s-1]", "Initial SEI thickness [m]",
    "Total heat transfer coefficient [W.m-2.K-1]", "Cell cooling surface area [m2]",
    "Lower voltage cut-off [V]", "Upper voltage cut-off [V]",
]

pv = pybamm.ParameterValues("Chen2020")
print("=== Chen2020 dump ===")
dump = {}
for k in KEYS:
    try:
        dump[k] = float(pv[k])
    except Exception as e:
        dump[k] = f"MISSING ({type(e).__name__})"
print(json.dumps(dump, indent=1, ensure_ascii=False))

print("=== discriminant check ===")
print("lnmo_ocp(0.5) =", float(lnmo_ocp(0.5)))
try:
    print("Chen2020 pos OCP(0.5) =", float(pv["Positive electrode OCP [V]"](0.5)))
except Exception as e:
    print("Chen2020 pos OCP eval failed:", e)

print("=== LNMO merged set ===")
LNMO = r"D:\research\degradation_prognostics\Battery_Design_Agent\.claude\skills\virtual-battery-factory\scripts\bda\simulators\data\LNMO.json"
extra = json.load(open(LNMO, encoding="utf-8"))
for k in ("Positive electrode OCP [V]", "Positive electrode OCP [V] (from stoich)"):
    if isinstance(extra.get(k), str):
        extra[k] = lnmo_ocp
pv2 = pybamm.ParameterValues("Chen2020")
pv2.update(extra, check_already_exists=False)
print("merged has SEI rate:", "SEI kinetic rate constant [m.s-1]" in pv2)
try:
    keys_like_sto = [k for k in pv2.keys() if "stoichiometry limits" in k]
    print("merged stoich-limit keys:", keys_like_sto)
except Exception as e:
    print("pv2.keys() failed:", e)
def g(name):
    try:
        return float(pv2[name])
    except Exception as e:
        return f"MISSING({type(e).__name__})"
print("merged pos max conc:", g("Positive electrode maximum concentration [mol.m-3]"))
print("merged pos initial conc:", g("Initial concentration in positive electrode [mol.m-3]"))
print("merged neg max conc:", g("Negative electrode maximum concentration [mol.m-3]"))
print("merged neg initial conc:", g("Initial concentration in negative electrode [mol.m-3]"))
print("merged pos thickness:", g("Positive electrode thickness [m]"))
print("merged neg thickness:", g("Negative electrode thickness [m]"))

print("=== areal capacity balance (LNMO-merged defaults) ===")
F_Ah = 26.801  # Ah/mol
h = g("Electrode height [m]"); w = g("Electrode width [m]")
nom_ah = g("Nominal cell capacity [A.h]")
area = h * w
pos_areal_ah_m2 = g("Positive electrode maximum concentration [mol.m-3]") * g("Positive electrode thickness [m]") * (1 - g("Positive electrode porosity")) * g("Positive electrode active material volume fraction") * F_Ah
neg_areal_ah_m2 = g("Negative electrode maximum concentration [mol.m-3]") * g("Negative electrode thickness [m]") * (1 - g("Negative electrode porosity")) * g("Negative electrode active material volume fraction") * F_Ah
print(f"area = {area} m2, nominal areal = {nom_ah/area*10000:.2f} mAh/cm2")
print(f"pos areal = {pos_areal_ah_m2*10000:.2f} mAh/cm2 (initial sto {g('Initial concentration in positive electrode [mol.m-3]')/g('Positive electrode maximum concentration [mol.m-3]'):.3f})")
print(f"neg areal = {neg_areal_ah_m2*10000:.2f} mAh/cm2")
print(f"cell capacity-limited by positive: {pos_areal_ah_m2 < nom_ah/area}")

print("=== misc keys existence in merged set ===")
for k in ["Positive current collector thickness [m]", "Negative current collector thickness [m]",
          "Positive current collector density [kg.m-3]", "Negative current collector density [kg.m-3]",
          "Cell cooling surface area [m2]", "Total heat transfer coefficient [W.m-2.K-1]",
          "Electrolyte conductivity [S.m-1]", "Cation transference number"]:
    print(f"  {k}: {k in pv2}")
