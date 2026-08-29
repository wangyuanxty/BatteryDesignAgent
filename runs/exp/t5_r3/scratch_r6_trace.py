"""4C charge-step trace analysis: where did the charge start/end, what current, what voltage."""
import json

files = [
    "r1_baseline_4c_45c.json",
    "r5_y1_4c_45c.json",
    "r5_y2_4c_45c.json",
    "r5_y3_4c_45c.json",
    "r5_y4_4c_45c.json",
    "r6_y3_4c_dfn.json",
    "r6_y4_4c_dfn.json",
]
base = r"runs\exp\t5_r3\cell"
I = 20.0  # 4C of nominal 5 Ah
for f in files:
    try:
        s = json.load(open(fr"{base}\{f}", encoding="utf-8"))
    except FileNotFoundError:
        print(f"{f}: missing")
        continue
    t = s["time_s"]; v = s["voltage_v"]; ap = s.get("anode_potential_v", [])
    vmin_i = min(range(len(v)), key=lambda i: v[i])
    # charge step = from voltage minimum onward
    t0 = t[vmin_i]; t_end = t[-1]
    dur = t_end - t0
    ah = dur * I / 3600.0
    print(
        f"{f}: model={s.get('model_used')} n={len(t)} vmin={v[vmin_i]:.3f}V@{t0:.0f}s "
        f"v_end={v[-1]:.3f}V charge_dur={dur:.0f}s -> {ah:.3f}Ah (I={I:.0f}A) "
        f"min_ap={min(ap) if ap else float('nan'):+.4f}V ap_end={ap[-1] if ap else float('nan'):+.4f}V "
        f"capacity_ah_field={s.get('capacity_ah'):.3f}"
    )

# detail on y4 dfn: voltage/AP evolution over charge
s = json.load(open(fr"{base}\r6_y4_4c_dfn.json", encoding="utf-8"))
t = s["time_s"]; v = s["voltage_v"]; ap = s["anode_potential_v"]
vmin_i = min(range(len(v)), key=lambda i: v[i])
print("\nY4-DFN charge step evolution (20A assumed):")
for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
    i = vmin_i + int((len(t) - 1 - vmin_i) * frac)
    print(f"@{frac:.2f}: t={(t[i]-t[vmin_i]):5.0f}s V={v[i]:.3f} ap={ap[i]:+.4f} Ah={(t[i]-t[vmin_i])*I/3600:.3f}")