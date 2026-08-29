# Per-cycle breakdown of the aging experiment: step durations, voltage windows,
# and the runner's exact capacity metric ("Discharge capacity [A.h]").entries[-1].
import pybamm
import numpy as np

PV = pybamm.ParameterValues("Chen2020")
v_min = float(PV["Lower voltage cut-off [V]"])
v_max = float(PV["Upper voltage cut-off [V]"])
exp = pybamm.Experiment(
    [(f"Discharge at 1C until {v_min} V", f"Charge at 1C until {v_max} V")] * 3
)
model = pybamm.lithium_ion.SPMe(options={"SEI": "ec reaction limited", "thermal": "isothermal"})
sim = pybamm.Simulation(model, experiment=exp, parameter_values=PV)
sol = sim.solve()
for i in range(len(sol.cycles)):
    cyc = sol.cycles[i]
    t = cyc["Time [s]"].entries
    V = cyc["Terminal voltage [V]"].entries
    dcap = cyc["Discharge capacity [A.h]"].entries
    ccap = cyc["Throughput capacity [A.h]"].entries
    print(f"cycle {i+1}: t {t[0]:.1f} -> {t[-1]:.1f} s (dt={t[-1]-t[0]:.1f}) "
          f"V {V[0]:.3f} -> {V[-1]:.3f}")
    print(f"   steps: {len(cyc.steps)}  DischargeCap[-1]={dcap[-1]:.4f}  "
          f"ChargeCap[-1]={ccap[-1]:.4f}")
    # step-level detail
    for s, st in enumerate(cyc.steps):
        tt = st["Time [s]"].entries
        VV = st["Terminal voltage [V]"].entries
        dd = st["Discharge capacity [A.h]"].entries
        print(f"   step {s}: {st.operating_conditions_string}  "
              f"dt={tt[-1]-tt[0]:.1f}s  V {VV[0]:.3f}->{VV[-1]:.3f}  "
              f"DisCap step-end={dd[-1]:.4f} (delta={dd[-1]-dd[0]:.4f})")
