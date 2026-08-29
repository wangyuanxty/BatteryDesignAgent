import json, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\cell\r7_final_4c_dfn.json", encoding="utf-8"))
t, v = d["time_s"], d["voltage_v"]
print("n =", len(t), "t[0] =", t[0], "t[-1] =", t[-1])
print("v[0] =", v[0])
for i in range(0, len(t), 40):
    print(f"  t={t[i]:9.1f}  V={v[i]:.5f}")
print(f"  t={t[-1]:9.1f}  V={v[-1]:.5f}")
# first crossing of various thresholds
for th in (4.19, 4.195, 4.199, 4.2):
    for i, vi in enumerate(v):
        if vi >= th:
            print(f"first V>={th}: t={t[i]:.2f} s, idx={i}")
            break
        if i == len(v) - 1:
            print(f"V never reaches {th}; max={max(v)}")