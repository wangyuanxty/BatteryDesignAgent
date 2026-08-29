import numpy as np
import pybamm

xs = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
for base in ["Chen2020", "OKane2022"]:
    pv = pybamm.ParameterValues(base)
    ocp_n = pv["Negative electrode OCP [V]"]
    print("=" * 10, base, "negative OCP (x_neg = lithiation fraction):")
    vals = []
    for x in xs:
        v = ocp_n(x)
        try:
            vf = float(v)
        except TypeError:
            vf = float(v.evaluate())
        vals.append(vf)
    print("  x:", [f"{x:.2f}" for x in xs])
    print("  V:", [f"{v:.4f}" for v in vals])
    print("  OCP(0.5)=", round(vals[5], 4), " OCP(0.9)=", round(vals[9], 4))
    ocp_p = pv["Positive electrode OCP [V]"]
    print("  positive OCP(0.5)=", round(float(ocp_p(0.5)), 4))