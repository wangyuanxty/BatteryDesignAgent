# Read all r3 outputs: aging SEI, energy, lowT, 1C refs, 4C anode min.
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

d = Path("runs/exp/t2_r1_noceiling/cell")
print("cand  sei100   sei500   lowTcap   1Ccap   lowTret  ED(Wh/kg)  anode_min")
for c in "EFGH":
    a100 = json.loads((d / f"r3_{c}_aging100.json").read_text(encoding="utf-8-sig"))
    a500 = json.loads((d / f"r3_{c}_aging500.json").read_text(encoding="utf-8-sig"))
    lt = json.loads((d / f"r3_{c}_lowT.json").read_text(encoding="utf-8-sig"))
    c1 = json.loads((d / f"r3_{c}_1c_spme.json").read_text(encoding="utf-8-sig"))
    en = json.loads((d / f"r3_{c}_energy.json").read_text(encoding="utf-8-sig"))
    p4 = json.loads((d / f"r3_{c}_4c45.json").read_text(encoding="utf-8-sig"))
    s100 = a100["sei_thickness_nm_end"]
    s500 = a500["sei_thickness_nm_end"]
    ret = lt["capacity_ah"] / c1["capacity_ah"]
    ed = en.get("energy_density_wh_kg", list(en.values())[0] if len(en) == 1 else en)
    amin = min(p4["anode_potential_v"])
    print(f"r3_{c}  {s100:7.1f} {s500:8.1f}  {lt['capacity_ah']:8.4f} {c1['capacity_ah']:7.4f}  {ret:7.4f}  {ed}  {amin:+.4f}")
    # also cycle-1 net capacity of aging run (artifact check)
    cap1 = a100.get("capacity_ah")
    print(f"      aging100 cap1(net)={cap1}  Tmax_lowT={lt.get('T_max_K')}  Vmin_lowT={lt.get('voltage_v',[None])[0] if lt.get('voltage_v') else None}")
