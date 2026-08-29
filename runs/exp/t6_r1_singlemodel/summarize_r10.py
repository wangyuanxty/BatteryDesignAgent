"""Summarize R10 G1/G2/G3 metrics for the evaluate notes."""
import json
from pathlib import Path

CELL = Path("cell")
for tag in ("G1", "G2", "G3"):
    try:
        e = json.loads((CELL / f"r10_{tag}_energy.json").read_text(encoding="utf-8"))
        c4 = json.loads((CELL / f"r10_{tag}_4c_spme.json").read_text(encoding="utf-8"))
        ag = json.loads((CELL / f"r10_{tag}_aging_spme.json").read_text(encoding="utf-8"))
        ap = c4["anode_potential_v"]
        V = c4["voltage_v"]
        t = c4["time_s"]
        mn = min(ap)
        plated = mn < 0
        imin = int(min(range(len(V)), key=lambda i: V[i]))
        t_dis = t[imin]
        t_trip = next((t[i] for i in range(len(V)) if V[i] >= 4.6999), None)
        t_ch = (t_trip - t_dis) if t_trip else None
        dur_s = (c4.get("capacity_ah") or 0) * 3600 / 4.0
        fill = (t_ch or 0) * 4.0 / 3600 / e["capacity_ah"]
        print(f"== {tag}: ED={e['energy_density_wh_l']:.2f} mid={e['midpoint_voltage_v']:.4f} "
              f"cap={e['capacity_ah']:.4f} thick={e['thickness_m']}")
        print(f"   4C: T={c4['T_max_K']:.3f} trip_t={t_trip:.1f}s t_dis={t_dis:.1f}s t_ch={t_ch:.1f}s "
              f"fill={fill*100:.2f}% anode_min={mn:.4f} plated={plated} cap_ah={c4['capacity_ah']:.4f}")
        print(f"   aging SEI={ag['sei_thickness_nm_end']:.2f}")
    except Exception as ex:
        print(f"== {tag}: ERROR {ex}")
