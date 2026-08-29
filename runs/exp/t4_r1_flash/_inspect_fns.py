import pybamm, inspect, numpy as np

pv = pybamm.ParameterValues("Chen2020")

def show(name):
    v = pv[name]
    print(f"\n=== {name} ===")
    print("  type:", type(v).__name__)
    if callable(v) and not isinstance(v, (int, float)):
        try:
            print("  signature:", inspect.signature(v))
        except Exception as e:
            print("  sig err:", e)
        # evaluate at 298.15 vs 253.15 where possible
        args = {}
        for pname, par in inspect.signature(v).parameters.items():
            if pname == "c_e":
                args[pname] = 1000.0
            elif pname == "c_s_surf":
                args[pname] = 20000.0
            elif pname == "c_s_max":
                args[pname] = 50000.0
            elif pname == "T":
                args[pname] = 298.15
            elif pname.startswith("T"):
                args[pname] = 298.15
        try:
            base_val = v(**args)
            if "T" in args:
                args2 = dict(args); args2["T"] = 253.15
                val_lo = v(**args2)
                print(f"  value at T=298.15: {base_val}")
                print(f"  value at T=253.15: {val_lo}")
                if base_val != 0:
                    print(f"  ratio(253/298): {val_lo/base_val:.4f}")
            else:
                print(f"  value: {base_val}")
        except Exception as e:
            print("  eval err:", e)

for n in [
    "Electrolyte conductivity [S.m-1]",
    "Electrolyte diffusivity [m2.s-1]",
    "Positive electrode exchange-current density [A.m-2]",
    "Negative electrode exchange-current density [A.m-2]",
]:
    show(n)

# all keys containing diffusivity / temperature / activation
keys = sorted(pv.keys())
for p in ["iffusiv", "emperature", "ctivation", "reaction"]:
    hits = [k for k in keys if p.lower() in k.lower()]
    print(f"\n--- '{p}':", hits)
    for h in hits:
        v = pv[h]
        if callable(v) and not isinstance(v, (int, float)):
            try:
                print("   ", h, "sig:", inspect.signature(v))
            except Exception:
                print("   ", h, "callable")
        else:
            print("   ", h, "=", v)

# Initial temperature?
print("\nInitial temperature in set:", "Initial temperature [K]" in pv, pv.get("Initial temperature [K]"))
