import json

# Variant J: Higher transport (3x baseline) to push past 0
# Variant K: 2.5x transport (between F and J)
# Variant L: Transport + slightly higher N/P (from D architecture)

D_arch = {
    "Positive electrode thickness [m]": 40e-6,
    "Negative electrode thickness [m]": 60e-6,
    "Positive electrode porosity": 0.33,
    "Negative electrode porosity": 0.40,
    "Positive particle radius [m]": 2e-6,
    "Negative particle radius [m]": 5e-6,
}

variants = {
    "J_high_transport": {
        **D_arch,
        "Electrolyte diffusivity [m2.s-1]": 2.0e-9,    # ~2.9x baseline
        "Electrolyte conductivity [S.m-1]": 2.5,         # ~2.5x baseline
        "Cation transference number": 0.38,
        "SEI kinetic rate constant [m.s-1]": 5e-14,      # Also suppress SEI
    },
    "K_mid_transport": {
        **D_arch,
        "Electrolyte diffusivity [m2.s-1]": 1.8e-9,    # ~2.6x baseline
        "Electrolyte conductivity [S.m-1]": 2.2,         # ~2.2x baseline
        "Cation transference number": 0.36,
        "SEI kinetic rate constant [m.s-1]": 5e-14,
    },
    "L_transport_highNP": {
        "Positive electrode thickness [m]": 38e-6,
        "Negative electrode thickness [m]": 65e-6,       # 1.7x positive
        "Positive electrode porosity": 0.33,
        "Negative electrode porosity": 0.40,
        "Positive particle radius [m]": 2e-6,
        "Negative particle radius [m]": 5e-6,
        "Electrolyte diffusivity [m2.s-1]": 1.5e-9,
        "Electrolyte conductivity [S.m-1]": 1.8,
        "Cation transference number": 0.35,
        "SEI kinetic rate constant [m.s-1]": 5e-14,
    },
}

for name, params in variants.items():
    path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    with open(path, "w") as f:
        json.dump(params, f)
    print(f"Created {path}")

print("Done")
