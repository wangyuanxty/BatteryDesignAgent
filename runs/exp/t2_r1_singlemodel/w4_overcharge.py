"""Stage 4: overcharge retry (fresh compute) + TR coupling + nail scenario."""
import json
import subprocess
import sys

CASE = "runs/exp/t2_r1_singlemodel"
CELL = f"{CASE}/cell"


def bda(*args):
    r = subprocess.run([sys.executable, "-m", "bda.cli", *args])
    if r.returncode != 0:
        print(f"FAILED: bda {' '.join(args)}")
        sys.exit(1)


bda("run-pyamm", "--params", f"{CELL}/params_r3.json", "--protocol", "overcharge",
    "--mode", "dfn", "--out", f"{CELL}/r3_overcharge.json")
oc = json.load(open(f"{CELL}/r3_overcharge.json", encoding="utf-8-sig"))
print("OVERCHARGE: cap=%.4f Ah T_max=%.1f K (cap>0.70 => charge phase present)" % (
    oc["capacity_ah"], oc["T_max_K"]))

bda("run-tr", "--sim", f"{CELL}/r3_overcharge.json", "--mass-kg", "0.0699",
    "--out", f"{CELL}/r3_tr.json")
tr = json.load(open(f"{CELL}/r3_tr.json", encoding="utf-8-sig"))
print("TR from overcharge: triggered=%s T_max=%.1f K t_trigger=%s" % (
    tr["triggered"], tr["T_max_K"], tr.get("trigger_time_s")))

bda("run-tr", "--mass-kg", "0.0699", "--q-nail", "5", "--out", f"{CELL}/r3_tr_nail.json")
trn = json.load(open(f"{CELL}/r3_tr_nail.json", encoding="utf-8-sig"))
print("TR nail 5W: triggered=%s T_max=%.1f K t_trigger=%s" % (
    trn["triggered"], trn["T_max_K"], trn.get("trigger_time_s")))
