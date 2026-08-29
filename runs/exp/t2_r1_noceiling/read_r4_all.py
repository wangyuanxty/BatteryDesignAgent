# Read all r4 outputs: energy, lowT details, 4C details.
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

d = Path("runs/exp/t2_r1_noceiling/cell")
for c in "IJKL":
    en = json.loads((d / f"r4_{c}_energy.json").read_text(encoding="utf-8-sig"))
    lt = json.loads((d / f"r4_{c}_lowT.json").read_text(encoding="utf-8-sig"))
    p4 = json.loads((d / f"r4_{c}_4c45.json").read_text(encoding="utf-8-sig"))
    a = p4["anode_potential_v"]
    print(f"r4_{c}: ED={en}  lowT_Tmax={lt.get('T_max_K')}  "
          f"4C_Tmax={p4['T_max_K']:.1f}  anode_min={min(a):+.4f}  charge_cap={p4['capacity_ah']:.4f}")
    print(f"     4C currents: nominal->4C = (see params); t_end={p4['time_s'][-1]:.1f}s")
