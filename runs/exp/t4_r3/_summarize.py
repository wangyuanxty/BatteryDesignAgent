"""t4_r3 helper: print scalar summary keys of round output JSONs (read command outputs verbatim)."""
import json
from pathlib import Path

ws = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent\runs\exp\t4_r3")

for name in [
    "cell/r1_base_1c_25C_spme.json",
    "cell/r1_base_1c_lowT_spme.json",
    "cell/r1_base_4C_45C_spme.json",
    "cell/r1_base_energy.json",
]:
    p = ws / name
    data = json.loads(p.read_text(encoding="utf-8-sig"))
    print("== " + name)
    for k, v in data.items():
        if isinstance(v, (int, float, bool)) or k in ("model_used", "note", "electrolyte_included"):
            print(f"  {k} = {v}")
        elif isinstance(v, list):
            print(f"  {k} = <list len {len(v)}> first={v[0] if isinstance(v[0], (int, float)) else '...'} last={v[-1] if isinstance(v[-1], (int, float)) else '...'}")
        elif isinstance(v, dict):
            print(f"  {k} = <dict {list(v)[:8]}>")