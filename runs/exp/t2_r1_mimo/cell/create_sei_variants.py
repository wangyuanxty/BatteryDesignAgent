import json

# Variant M: Lower SEI rate (2e-14) with same transport as J
# Variant N: Even lower SEI rate (1e-14)
# Variant O: Moderate SEI reduction (3e-14) - might be enough

J_base = {
    "Positive electrode thickness [m]": 40e-6,
    "Negative electrode thickness [m]": 60e-6,
    "Positive electrode porosity": 0.33,
    "Negative electrode porosity": 0.40,
    "Positive particle radius [m]": 2e-6,
    "Negative particle radius [m]": 5e-6,
    "Electrolyte diffusivity [m2.s-1]": 2.0e-9,
    "Electrolyte conductivity [S.m-1]": 2.5,
    "Cation transference number": 0.38,
}

variants = {
    "M_low_sei": {**J_base, "SEI kinetic rate constant [m.s-1]": 2e-14},
    "N_min_sei": {**J_base, "SEI kinetic rate constant [m.s-1]": 1e-14},
    "O_mod_sei": {**J_base, "SEI kinetic rate constant [m.s-1]": 3e-14},
}

for name, params in variants.items():
    path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    with open(path, "w") as f:
        json.dump(params, f)
    print(f"Created {path}")
print("Done")
