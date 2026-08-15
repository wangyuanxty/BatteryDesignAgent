def ie_ea_from_energies(E_neutral_ev: float, E_cation_ev: float, E_anion_ev: float) -> dict:
    return {"IE_ev": E_cation_ev - E_neutral_ev, "EA_ev": E_neutral_ev - E_anion_ev}


def homo_lumo_window(homo_ev: float, lumo_ev: float) -> float:
    return lumo_ev - homo_ev
