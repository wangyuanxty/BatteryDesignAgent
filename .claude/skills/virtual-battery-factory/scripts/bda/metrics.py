def cell_mass_kg(layers: dict) -> float:
    total = 0.0
    for layer in layers.values():
        total += layer["thickness_m"] * (1.0 - layer["porosity"]) * layer["density_kg_m3"]
    return total  # per m² of electrode area


def gravimetric_energy_density(energy_wh: float, mass_kg: float) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be positive")
    return energy_wh / mass_kg


def detect_lithium_plating(anode_potential_v: list[float], t_s: list[float], threshold_v: float = 0.0) -> dict:
    for t, v in zip(t_s, anode_potential_v):
        if v < threshold_v:
            return {"plated": True, "first_time_s": float(t)}
    return {"plated": False, "first_time_s": None}


def ie_ea_from_energies(E_neutral_ev: float, E_cation_ev: float, E_anion_ev: float) -> dict:
    return {"IE_ev": E_cation_ev - E_neutral_ev, "EA_ev": E_neutral_ev - E_anion_ev}


def homo_lumo_window(homo_ev: float, lumo_ev: float) -> float:
    return lumo_ev - homo_ev
