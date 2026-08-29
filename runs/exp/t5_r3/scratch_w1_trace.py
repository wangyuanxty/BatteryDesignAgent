"""Inspect W1 4C trajectory in detail."""
import json

s = json.load(open(r"runs\exp\t5_r3\cell\r3_w1_4c_45c.json", encoding="utf-8"))
t, v, ap = s["time_s"], s["voltage_v"], s["anode_potential_v"]
print("n:", len(t), "t0:", t[0], "t_end:", t[-1])
# locate steps: v < 4.0 = discharge-ish; find where voltage jumps above 4.0 again = charge
starts = [i for i in range(1, len(v)) if v[i] - v[i - 1] > 0.05]
print("up-jump indices:", starts[:6])
i_last = starts[-1] if starts else None
print("charge start t:", t[i_last] if i_last else None, "v:", round(v[i_last], 3) if i_last else None)
if i_last is not None:
    print("charge end t:", t[-1], "v_end:", round(v[-1], 3), "ap_end:", round(ap[-1], 4))
    print("charge duration s:", round(t[-1] - t[i_last], 1))
    # capacity by duration x 4C
    print("charge Ah (duration x 4C):", round((t[-1] - t[i_last]) * 4 / 3600, 4))
print("ap min:", round(min(ap), 4), "at t:", t[ap.index(min(ap))])
# T_max is scalar only; find voltage at end of discharge
vd = [v[i] for i in range(len(v)) if t[i] < (t[i_last] if i_last else 0)]
print("v at end of discharge:", round(vd[-1], 3) if vd else None)