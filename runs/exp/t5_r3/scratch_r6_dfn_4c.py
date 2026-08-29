"""Round-6: DFN 4C results for finalists."""
import json

base = r"runs\exp\t5_r3\cell"
for v in ["y4", "y3"]:
    try:
        s = json.load(open(fr"{base}\r6_{v}_4c_dfn.json", encoding="utf-8"))
    except FileNotFoundError:
        print(f"{v}: 4C DFN not yet present")
        continue
    ap = s.get("anode_potential_v", [0.0])
    print(
        f"{v} 4C DFN: model={s.get('model_used')} T_max={s.get('T_max_K'):.2f}K "
        f"min_ap={min(ap):+.4f}V n_neg={sum(1 for x in ap if x < 0)} cap={s.get('capacity_ah'):.3f}Ah"
    )