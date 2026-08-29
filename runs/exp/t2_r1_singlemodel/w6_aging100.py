"""Re-measure aging100 with final params (D_ec=1e-19) -> cell/r3_aging100.json."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(r"D:\research\degradation_prognostics\Battery_Design_Agent")
CELL = REPO / "runs" / "exp" / "t2_r1_singlemodel" / "cell"
PY = REPO / ".venv" / "Scripts" / "python.exe"

r = subprocess.run([str(PY), "-m", "bda.cli", "run-pyamm",
                    "--params", str(CELL / "params_r3.json"),
                    "--protocol", "aging_1C_100cyc",
                    "--mode", "dfn",
                    "--out", str(CELL / "r3_aging100.json")])
if r.returncode != 0:
    print("run-pyamm FAILED", r.returncode)
    sys.exit(1)
out = json.loads((CELL / "r3_aging100.json").read_text(encoding="utf-8-sig"))
print("AGING100 @1e-19: cycles=%d SEI=%.2f nm cap_last=%.4f"
      % (len(out["cycle_numbers"]), out["sei_thickness_nm_end"],
         out["capacity_ah_per_cycle"][-1]))
