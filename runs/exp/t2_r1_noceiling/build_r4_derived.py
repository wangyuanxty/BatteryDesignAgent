# Mechanically build derived metric files for round-4 candidates I-L (same pattern as R3).
import json
from pathlib import Path

CELL = Path("runs/exp/t2_r1_noceiling/cell")
CANDS = ["I", "J", "K", "L"]

for cand in CANDS:
    aging100 = json.loads((CELL / f"r4_{cand}_aging100.json").read_text(encoding="utf-8-sig"))
    aging500 = json.loads((CELL / f"r4_{cand}_aging500.json").read_text(encoding="utf-8-sig"))
    lowT = json.loads((CELL / f"r4_{cand}_lowT.json").read_text(encoding="utf-8-sig"))
    c1 = json.loads((CELL / f"r4_{cand}_1c_spme.json").read_text(encoding="utf-8-sig"))
    sei = {"sei_100cyc_nm": aging100["sei_thickness_nm_end"],
           "sei_500cyc_nm": aging500["sei_thickness_nm_end"]}
    low = {"lowT_retention": lowT["capacity_ah"] / c1["capacity_ah"]}
    (CELL / f"r4_{cand}_derived_sei.json").write_text(json.dumps(sei, indent=1), encoding="utf-8")
    (CELL / f"r4_{cand}_derived_lowT.json").write_text(json.dumps(low, indent=1), encoding="utf-8")
    print(f"r4_{cand}: sei100={sei['sei_100cyc_nm']:.1f} sei500={sei['sei_500cyc_nm']:.1f} "
          f"lowT_ret={low['lowT_retention']:.4f} (lowT {lowT['capacity_ah']:.4f} / 1C {c1['capacity_ah']:.4f})")
