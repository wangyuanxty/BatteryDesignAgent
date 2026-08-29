import json, os
ws = os.path.dirname(os.path.abspath(__file__))
for fn in ["cell/r7_lnmo_r4_4c45_dfn.json", "cell/r8_lnmo_r5_4c45_dfn.json", "cell/r9_lnmo_r6_4c45_dfn.json"]:
    d = json.load(open(os.path.join(ws, fn), encoding="utf-8"))
    t, v, a = d["time_s"], d["voltage_v"], d["anode_potential_v"]
    # find the charge step: the rise of V from discharge floor toward max
    # locate max V index and look backwards to where V starts rising steeply
    imax = max(range(len(v)), key=v.__getitem__)
    # charge start: last point before imax where dV/dt is small/negative (rest after discharge)
    start = None
    for i in range(imax - 1, 0, -1):
        if v[i] < 4.0 and v[i + 1] - v[i] > 0.05:
            start = i
            break
    if start is None:
        start = 0
    # approximate capacity in charge via current assumed constant 18 A -> Ah = A * dt/3600
    dt_charge = t[imax] - t[start]
    print("%s: t_start=%.0f t_maxV=%.0f dt=%.0f s  V_start=%.3f  V_max=%.3f  charge_ah_est=%.2f  cap_ah=%.2f  anode_min=%.4f"
          % (fn, t[start], t[imax], dt_charge, v[start], v[imax], 18.0 * dt_charge / 3600.0, d.get("capacity_ah"), min(a)))
    # anode potential at the moment of max V
    print("   anode at maxV: %.4f  ; anode min overall: %.4f" % (a[imax], min(a)))
