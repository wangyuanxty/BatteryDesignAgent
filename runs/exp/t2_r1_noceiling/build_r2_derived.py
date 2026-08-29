# Mechanically build derived metric files for round-2 candidates A-D:
#  {cand}_derived_sei.json  <- sei_thickness_nm_end from aging100/aging500 outputs
#  {cand}_derived_lowT.json <- lowT_retention = lowT capacity / 1C capacity (same nominal C-rate)
import json
from pathlib import Path

CELL = Path("runs/exp/t2_r1_noceiling/cell")
CANDS = ["A", "B", "C", "D"]

for cand in CANDS:
    aging100 = json.loads((CELL / f"r2_{cand}_aging100.json").read_text(encoding="utf-8-sig"))
    aging500 = json.loads((CELL / f"r2_{cand}_aging500.json").read_text(encoding="utf-8-sig"))
    lowT = json.loads((CELL / f"r2_{cand}_lowT.json").read_text(encoding="utf-8-sig"))
    # 1C reference: for D use the post-nominal-update 1C run (3.5681 A nominal); others use their own 1C run
    ref = CELL / f"r2_{cand}_1c_spme.json"
    if not ref.exists():
        ref = CELL / f"r2_{cand}_measure_1c_spme.json"
    c1 = json.loads(ref.read_text(encoding="utf-8-sig"))
    sei = {"sei_100cyc_nm": aging100["sei_thickness_nm_end"],
           "sei_500cyc_nm": aging500["sei_thickness_nm_end"]}
    low = {"lowT_retention": lowT["capacity_ah"] / c1["capacity_ah"]}
    (CELL / f"r2_{cand}_derived_sei.json").write_text(json.dumps(sei, indent=1), encoding="utf-8")
    (CELL / f"r2_{cand}_derived_lowT.json").write_text(json.dumps(low, indent=1), encoding="utf-8")
    print(f"r2_{cand}: sei100={sei['sei_100cyc_nm']:.1f} sei500={sei['sei_500cyc_nm']:.1f} "
          f"lowT_ret={low['lowT_retention']:.4f} (lowT {lowT['capacity_ah']:.4f} / 1C {c1['capacity_ah']:.4f})")
