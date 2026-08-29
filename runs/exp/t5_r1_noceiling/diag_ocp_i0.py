# Diagnostic: evaluate Chen2020 OCP functions and exchange-current densities
# over the stoichiometry window relevant to the 4C charge from 2.5 V.
import numpy as np
import pybamm

pv = pybamm.ParameterValues("Chen2020")

ocp_c = pv["Positive electrode OCP [V]"]
ocp_a = pv["Negative electrode OCP [V]"]
i0_n = pv["Negative electrode exchange-current density [A.m-2]"]
i0_p = pv["Positive electrode exchange-current density [A.m-2]"]
c_max_n = float(pv["Maximum concentration in negative electrode [mol.m-3]"])
c_max_p = float(pv["Maximum concentration in positive electrode [mol.m-3]"])

def eval_func(f, *args):
    try:
        syms = [pybamm.Scalar(float(a)) for a in args]
        out = f(*syms)
        return float(np.asarray(out.evaluate()).flatten()[0])
    except Exception as e:
        return f"ERR {type(f).__name__}: {e}"

print("c_max_n =", c_max_n, "c_max_p =", c_max_p)
print("\nOCP positive [V] vs x_c:")
for x in [0.25, 0.35, 0.45, 0.538, 0.6, 0.68, 0.75, 0.85]:
    print(f"  x_c={x:.3f} -> {eval_func(ocp_c, x)}")
print("\nOCP negative [V] vs x_n:")
for x in [0.005, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.54, 0.60, 0.75, 0.88]:
    print(f"  x_n={x:.3f} -> {eval_func(ocp_a, x)}")
print("\ni0 negative [A.m-2] at T=318.15K, c_e=1000, x_n grid:")
for x in [0.02, 0.05, 0.12, 0.20, 0.30, 0.50, 0.70, 0.88]:
    print(f"  x_n={x:.3f} -> {eval_func(i0_n, 1000.0, x * c_max_n, c_max_n, 318.15)}")
print("\ni0 positive [A.m-2] at T=318.15K, c_e=1000, x_c grid:")
for x in [0.25, 0.45, 0.60, 0.70, 0.80, 0.85]:
    print(f"  x_c={x:.3f} -> {eval_func(i0_p, 1000.0, x * c_max_p, c_max_p, 318.15)}")
