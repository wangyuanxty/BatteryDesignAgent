def cell_mass_kg(layers: dict) -> float:
    total = 0.0
    for layer in layers.values():
        total += layer["thickness_m"] * (1.0 - layer["porosity"]) * layer["density_kg_m3"]
    return total  # per m² of electrode area


def gravimetric_energy_density(energy_wh: float, mass_kg: float) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be positive")
    return energy_wh / mass_kg
