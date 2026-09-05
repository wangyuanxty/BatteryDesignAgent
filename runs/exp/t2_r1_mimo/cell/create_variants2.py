import json

# Variant D: Thin electrodes + higher N/P ratio (thicker negative)
# Also try Variant E: moderate thickness + high N/P + smaller particles
variants = {
    "D_thin_highNP": {
        "Positive electrode thickness [m]": 40e-6,
        "Negative electrode thickness [m]": 60e-6,  # 1.5x positive for high N/P
        "Positive electrode porosity": 0.33,
        "Negative electrode porosity": 0.40,
        "Positive particle radius [m]": 2e-6,
        "Negative particle radius [m]": 5e-6,
    },
    "E_moderate_highNP": {
        "Positive electrode thickness [m]": 50e-6,
        "Negative electrode thickness [m]": 75e-6,  # 1.5x positive
        "Positive electrode porosity": 0.32,
        "Negative electrode porosity": 0.38,
        "Positive particle radius [m]": 2e-6,
        "Negative particle radius [m]": 4e-6,
    },
}

for name, params in variants.items():
    path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    with open(path, "w") as f:
        json.dump(params, f)
    print(f"Created {path}")

print("Done")
