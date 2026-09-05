import json

# Based on Chen2020 baseline electrolyte transport (EC/EMC + LiPF6)
# Typical values: D ~ 7e-10 m2/s, sigma ~ 1.0 S/m, t+ ~ 0.26
# We'll override with enhanced values

# Variant F: Enhanced transport only (target: eliminate plating)
# Variant G: SEI suppression only (target: SEI@500 < 550nm)
# Variant H: Combined transport + SEI (target: both)
# Variant I: Moderate transport + SEI (balanced approach)

# Using Variant D architecture (thin + high N/P, ED=377) as base for F/G/H
# Variant D params:
D_arch = {
    "Positive electrode thickness [m]": 40e-6,
    "Negative electrode thickness [m]": 60e-6,
    "Positive electrode porosity": 0.33,
    "Negative electrode porosity": 0.40,
    "Positive particle radius [m]": 2e-6,
    "Negative particle radius [m]": 5e-6,
}

variants = {
    "F_transport_only": {
        **D_arch,
        "Electrolyte diffusivity [m2.s-1]": 1.5e-9,   # ~2x baseline (~7e-10)
        "Electrolyte conductivity [S.m-1]": 1.8,       # ~1.8x baseline (~1.0)
        "Cation transference number": 0.35,             # improved from ~0.26
    },
    "G_sei_only": {
        **D_arch,
        "SEI kinetic rate constant [m.s-1]": 5e-14,     # ~10x lower than baseline (~5e-13)
    },
    "H_combined": {
        **D_arch,
        "Electrolyte diffusivity [m2.s-1]": 1.5e-9,
        "Electrolyte conductivity [S.m-1]": 1.8,
        "Cation transference number": 0.35,
        "SEI kinetic rate constant [m.s-1]": 5e-14,
    },
    "I_moderate_combined": {
        **D_arch,
        "Electrolyte diffusivity [m2.s-1]": 1.2e-9,   # ~1.7x baseline
        "Electrolyte conductivity [S.m-1]": 1.5,         # ~1.5x baseline
        "Cation transference number": 0.32,
        "SEI kinetic rate constant [m.s-1]": 1e-13,       # ~5x lower
    },
}

for name, params in variants.items():
    path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    with open(path, "w") as f:
        json.dump(params, f)
    print(f"Created {path}: {len(params)} overrides")

print("Done")
