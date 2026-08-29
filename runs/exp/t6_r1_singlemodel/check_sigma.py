"""Evaluate Chen2020 electrolyte conductivity function vs c_e and T."""
import pybamm

pv = pybamm.ParameterValues("Chen2020")
f = pv["Electrolyte conductivity [S.m-1]"]
import inspect
print("sig:", inspect.signature(f))
print("doc:", (f.__doc__ or "")[:200])
for T in (298.15, 318.15):
    for c in (500.0, 1000.0, 2000.0):
        try:
            v = f(c, T)
        except TypeError:
            try:
                v = f(T)
            except Exception as e:
                v = f"ERR {e}"
        print(f"  sigma(c={c}, T={T}) = {v}")
# diffusivity function too
d = pv["Electrolyte diffusivity [m2.s-1]"]
print("dif:", inspect.signature(d))
for T in (298.15, 318.15):
    try:
        print(f"  D(c=1000, T={T}) = {d(1000.0, T)}")
    except TypeError:
        print(f"  D(c=1000, T={T}) = {d(1000.0, T)} -- try other signature")
        try:
            print("   D(T):", d(T))
        except Exception as e:
            print("   ERR", e)
