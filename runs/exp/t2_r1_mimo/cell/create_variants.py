import json

# From calc-energy output:
# layer_kg_m2: pos_electrode=0.1640, neg_electrode=0.1059, pos_cc=0.0432, neg_cc=0.1075, separator=0.00252
# thickness_m total=0.0002008
# area_m2=0.1027
# capacity_ah=4.948

# Chen2020 typical values (from PyBaMM parameter set):
# pos electrode: ~75.6e-6 m thick, 0.332 porosity
# neg electrode: ~85.2e-6 m thick, 0.332 porosity
# separator: ~25e-6 m thick, 0.47 porosity
# pos CC (Al): ~16e-6 m
# neg CC (Cu): ~12e-6 m  (wait, need to check)

# Let me compute from mass/area/density:
# pos electrode active: rho=3100 kg/m3 (NMC811), mass/area=0.1640
#   If thickness=t, porosity=eps: 0.1640 = t * (1-eps) * 3100 * 0.1027... no
#   Actually: mass/area = t * (1-eps) * rho  (per unit area, total mass = mass/area * area)
#   So: 0.1640 = t * (1-0.332) * 3100 => t = 0.1640 / (0.668 * 3100) = 79.7e-6 m

# neg electrode active: rho=2600 kg/m3 (graphite), mass/area=0.1059
#   0.1059 = t * (1-0.332) * 2600 => t = 0.1059 / (0.668 * 2600) = 60.5e-6 m
#   Hmm, that's less than pos electrode. For N/P balance, neg should be > pos.

# Let me try with neg porosity = 0.485:
#   0.1059 = t * (1-0.485) * 2600 => t = 0.1059 / (0.515 * 2600) = 79.1e-6 m
#   That gives pos/neg ~ 79.7/79.1 = 1.01 N/P ratio... still low

# Actually, for Chen2020 the standard values are:
# pos electrode thickness: 75.6e-6 m
# neg electrode thickness: 85.2e-6 m
# pos porosity: 0.332
# neg porosity: 0.485 (wait, that's unusual)

# Let me just use common values and see what happens
# The key is to try different configurations

# Baseline: use the values that produce the observed output
# Variant A: Thinner electrodes
# Variant B: Thinner + higher porosity + smaller particles
# Variant C: Very thin + optimal for rate

# Create params files
variants = {
    "baseline": {},  # empty = use defaults

    "A_thin_electrodes": {
        "Positive electrode thickness [m]": 50e-6,  # was ~76e-6
        "Negative electrode thickness [m]": 55e-6,  # was ~85e-6
    },

    "B_thin_high_porosity": {
        "Positive electrode thickness [m]": 40e-6,
        "Negative electrode thickness [m]": 45e-6,
        "Positive electrode porosity": 0.35,
        "Negative electrode porosity": 0.40,
        "Positive particle radius [m]": 2e-6,   # smaller particles
        "Negative particle radius [m]": 5e-6,   # smaller particles
    },

    "C_thin_optimal": {
        "Positive electrode thickness [m]": 35e-6,
        "Negative electrode thickness [m]": 40e-6,
        "Positive electrode porosity": 0.30,
        "Negative electrode porosity": 0.35,
        "Positive particle radius [m]": 1.5e-6,
        "Negative particle radius [m]": 3e-6,
        "Separator thickness [m]": 15e-6,  # thinner separator
        "Separator porosity": 0.45,
    },
}

for name, params in variants.items():
    path = f"runs/exp/t2_r1_mimo/cell/params_{name}.json"
    with open(path, "w") as f:
        json.dump(params, f)
    print(f"Created {path}: {len(params)} overrides")

print("\nDone creating parameter files")
