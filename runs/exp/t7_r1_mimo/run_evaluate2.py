"""Run log-evaluate directly."""
import os, sys, subprocess

os.chdir("D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo")
PYTHON = "D:/research/degradation_prognostics/Battery_Design_Agent/.venv/Scripts/python.exe"
CASE_DIR = "D:/research/degradation_prognostics/Battery_Design_Agent/runs/exp/t7_r1_mimo"

# Run baseline evaluation
cmd = [
    PYTHON, "-m", "bda", "log-evaluate",
    "--case-dir", CASE_DIR,
    "--round", "0",
    "--outputs",
    "cell/baseline_energy.json",
    "cell/aging_45c.json",
    "cell/4c_charge_45c.json",
    "cell/nail_tr.json",
    "--candidate", "baseline_Chen2020",
    "--note", "Baseline: ED=400 PASS, SEI=476 PASS, 4C plating FAIL, nail TR numerical instability"
]

print("Running baseline evaluation...")
proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
print(f"Return code: {proc.returncode}")
if proc.stdout:
    print(f"Stdout: {proc.stdout[:500]}")
if proc.stderr:
    print(f"Stderr: {proc.stderr[:500]}")

# Run V_K evaluation
cmd2 = [
    PYTHON, "-m", "bda", "log-evaluate",
    "--case-dir", CASE_DIR,
    "--round", "1",
    "--outputs",
    "cell/V_K_extreme_transport_energy.json",
    "cell/V_K_aging_45c.json",
    "cell/V_K_extreme_transport_4c_dfn.json",
    "cell/V_K_nail_hA05.json",
    "--candidate", "V_K_extreme_transport",
    "--note", "V_K: ED=419 PASS, SEI=536 PASS, 4C no plating PASS, nail no TR PASS (hA=0.5)"
]

print("\nRunning V_K evaluation...")
proc2 = subprocess.run(cmd2, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
print(f"Return code: {proc2.returncode}")
if proc2.stdout:
    print(f"Stdout: {proc2.stdout[:500]}")
if proc2.stderr:
    print(f"Stderr: {proc2.stderr[:500]}")
