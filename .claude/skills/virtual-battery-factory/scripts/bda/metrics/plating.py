def detect_lithium_plating(anode_potential_v: list[float], t_s: list[float], threshold_v: float = 0.0) -> dict:
    for t, v in zip(t_s, anode_potential_v):
        if v < threshold_v:
            return {"plated": True, "first_time_s": float(t)}
    return {"plated": False, "first_time_s": None}
