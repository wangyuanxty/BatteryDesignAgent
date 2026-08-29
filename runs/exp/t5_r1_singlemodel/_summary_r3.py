import json
from pathlib import Path
import numpy as np

WS = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t5_r1_singlemodel")
cell = WS / "cell"

rows = [("archH_transport", "archH"), ("archI_h50", "archI"), ("archJ_npUp", "archJ"), ("archK_particles", "archK")]
print(f"{'candidate':<16} {'ED Wh/kg':>9} {'cap Ah':>7} {'E Wh':>7} {'mass g':>7} {'Vmid':>6} {'Tmax K':>7} {'anode min V':>11} {'model':>12}")
for disp, name in rows:
    en = json.loads((cell / f"r3_{name}_energy.json").read_text(encoding="utf-8"))
    c4 = json.loads((cell / f"r3_{name}_4c_dfn.json").read_text(encoding="utf-8"))
    ap = c4.get("anode_potential_v")
    apmin = min(ap) if ap else float("nan")
    print(f"{disp:<16} {en['energy_density_wh_kg']:9.1f} {en['capacity_ah']:7.3f} {en['energy_wh']:7.2f} "
          f"{en['mass_kg']*1000:7.2f} {en['midpoint_voltage_v']:6.3f} "
          f"{c4.get('T_max_K', float('nan')):7.2f} {apmin:11.4f} {c4.get('model_used', '-'):>12}")

enE = json.loads((cell / "r2_archE_energy_dfn.json").read_text(encoding="utf-8"))
print(f"[archE DFN check] ED={enE['energy_density_wh_kg']:.1f} Wh/kg  cap={enE['capacity_ah']:.3f} Ah  E={enE['energy_wh']:.2f} Wh  mass={enE['mass_kg']*1000:.2f} g")

# where does Tmax occur (discharge vs charge segment)? experiment = 1C discharge (~3600 s) then 4C charge (900 s)
for name in ("archH", "archI", "archJ", "archK"):
    c4 = json.loads((cell / f"r3_{name}_4c_dfn.json").read_text(encoding="utf-8"))
    ap = np.asarray(c4["anode_potential_v"])
    t = np.asarray(c4["time_s"])
    i = int(np.argmin(ap))
    print(f"[{name}] anode min {ap.min():.4f} V at t={t[i]:.0f} s (total {t[-1]:.0f} s); Tmax {c4['T_max_K']:.2f} K")
