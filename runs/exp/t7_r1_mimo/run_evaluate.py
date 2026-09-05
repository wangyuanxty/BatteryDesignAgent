"""Write evaluate entries for all candidates using log-evaluate batch mode."""
import os, sys, json, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CASE_DIR = "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo"

# Create batch file for log-evaluate
batch = [
    {
        "candidate": "baseline_Chen2020",
        "outputs": [
            "cell/baseline_energy.json",
            "cell/aging_45c.json",
            "cell/4c_charge_45c.json",
            "cell/nail_tr.json"
        ],
        "note": "Baseline Chen2020: ED=400 Wh/kg (PASS), SEI=476nm (PASS), 4C plating (FAIL anode_min=-0.438V), nail TR triggered=true (numerical instability, not genuine TR)"
    },
    {
        "candidate": "V_K_extreme_transport",
        "outputs": [
            "cell/V_K_extreme_transport_energy.json",
            "cell/V_K_aging_45c.json",
            "cell/V_K_extreme_transport_4c_dfn.json",
            "cell/V_K_nail_hA05.json"
        ],
        "note": "V_K: ED=419 Wh/kg (PASS), SEI=536nm (PASS, tight margin), 4C no plating anode_min=+0.005V (PASS), nail hA=0.5 no TR (PASS)"
    }
]

batch_file = "cell/eval_batch.json"
with open(batch_file, "w", encoding="utf-8") as f:
    json.dump(batch, f, indent=2)

# Run log-evaluate batch
cmd = [PYTHON, "-m", "bda", "log-evaluate",
       "--case-dir", CASE_DIR,
       "--round", "1",
       "--batch-file", batch_file]
print("Running log-evaluate batch...")
r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if r.returncode != 0:
    print(f"ERROR: {r.stderr[:500]}")
else:
    print(f"STDOUT: {r.stdout[:500]}")
    print("Log-evaluate batch completed")
