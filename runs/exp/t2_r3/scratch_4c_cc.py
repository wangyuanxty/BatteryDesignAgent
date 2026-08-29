import json, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t2_r3\cell\r7_final_4c_dfn.json", encoding="utf-8"))
t, v = d["time_s"], d["voltage_v"]
for i, vi in enumerate(v):
    if vi >= 4.2 - 1e-9:
        print("first time voltage hits 4.2V cut-off: t =", t[i], "s; capacity at that index =", d["capacity_ah"], "(full protocol)")
        print("voltage max =", max(v))
        break
else:
    print("voltage never reached 4.2; max =", max(v))
print("T_max_K =", d["T_max_K"], " ; final V =", v[-1])