import json
from pathlib import Path

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
cell = WS / "cell"

rows = [("baseline_Chen2020", "baseline"), ("sys_OKane2022", "OKane"), ("archA_EDmax", "archA"), ("archB_4Csafe", "archB"), ("archC_thin", "archC")]
print(f"{'candidate':<20} {'ED Wh/kg':>9} {'cap Ah':>7} {'E Wh':>7} {'mass g':>7} {'Vmid':>6} {'DCR mOhm':>8} {'Tmax K':>7} {'anode min V':>11} {'model':>14}")
for disp, name in rows:
    en = json.loads((cell / f"r1_{name}_energy.json").read_text(encoding="utf-8"))
    try:
        c4 = json.loads((cell / f"r1_{name}_4c_dfn.json").read_text(encoding="utf-8"))
        tmax = c4.get("T_max_K", float("nan"))
        ap = c4.get("anode_potential_v")
        apmin = min(ap) if ap else float("nan")
        model4 = c4.get("model_used", "-")
    except Exception as ex:
        tmax, apmin, model4 = float("nan"), float("nan"), f"ERR {ex}"
    print(f"{disp:<20} {en['energy_density_wh_kg']:9.1f} {en['capacity_ah']:7.3f} {en['energy_wh']:7.2f} "
          f"{en['mass_kg']*1000:7.2f} {en['midpoint_voltage_v']:6.3f} {en['dcr_ohm']*1000:8.2f} "
          f"{tmax:7.2f} {apmin:11.4f} {model4:>14}")

# SPMe vs DFN calibration for baseline/OKane
for name in ("baseline", "OKane"):
    sp = json.loads((cell / f"r1_{name}_1c_spme.json").read_text(encoding="utf-8"))
    df = json.loads((cell / f"r1_{name}_1c_dfn.json").read_text(encoding="utf-8"))
    print(f"[calib] {name}: SPMe cap={sp['capacity_ah']:.3f} Ah vs DFN cap={df['capacity_ah']:.3f} Ah; "
          f"SPMe Tmax={sp.get('T_max_K', float('nan')):.2f} vs DFN Tmax={df.get('T_max_K', float('nan')):.2f}")
