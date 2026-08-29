"""Round-5 params: V12 (high-porosity + fine particles + fast D + h=25)."""
import json
from pathlib import Path

p = {
    "Electrolyte conductivity [S.m-1]": 1.5,
    "Cation transference number": 0.35,
    "Electrolyte diffusivity [m2.s-1]": 8.0e-10,
    "Positive current collector thickness [m]": 8e-6,
    "Negative current collector thickness [m]": 6e-6,
    "Separator porosity": 0.5,
    "Positive electrode thickness [m]": 5.13912e-05,
    "Positive electrode porosity": 0.55,
    "Negative electrode thickness [m]": 7.64241e-05,
    "Negative electrode porosity": 0.5,
    "Positive particle radius [m]": 0.8e-6,
    "Negative particle radius [m]": 1.0e-6,
    "Total heat transfer coefficient [W.m-2.K-1]": 25.0,
}
out = Path("runs/exp/t3_r3/cell/r5_v12_hip_final_params.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(p, f, indent=2, ensure_ascii=False)
print(out.name, "written")