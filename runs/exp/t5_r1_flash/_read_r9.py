import json, os
ws = os.path.dirname(os.path.abspath(__file__))
e = json.load(open(os.path.join(ws, "cell/r9_lnmo_r6_energy_dfn.json"), encoding="utf-8"))
d = json.load(open(os.path.join(ws, "cell/r9_lnmo_r6_1c_dfn.json"), encoding="utf-8"))
print("DFN 1C: model=%s cap=%.4f Ah" % (d.get("model_used"), d["capacity_ah"]))
print("ED(DFN) = %.2f Wh/kg  mass=%.5f kg  E=%.3f Wh  EDvol=%.1f Wh/L"
      % (e["energy_density_wh_kg"], e["mass_kg"], e["energy_wh"], e["energy_density_wh_l"]))
print("midpoint V=%.4f  thickness=%.6f m  DCR=%.3e ohm" % (e["midpoint_voltage_v"], e["thickness_m"], e["dcr_ohm"]))
print("layers kg/m2:", json.dumps(e["layer_kg_m2"]))
print("area=%.4f m2  volume=%.3e m3" % (e["area_m2"], e["volume_m3"]))
