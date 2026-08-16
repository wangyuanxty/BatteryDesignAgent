def apply_rules(cands: list[dict], rules: dict) -> list[dict]:
    max_energy = rules.get("max_energy_ev")
    max_homo = rules.get("max_homo_ev")
    out = []
    for c in cands:
        item = dict(c)
        m = item.get("metrics", {})
        if not m.get("converged"):
            item["status"] = "rejected"
        elif max_energy is not None and (m.get("energy_ev") is None or m["energy_ev"] > max_energy):
            item["status"] = "rejected"
        elif max_homo is not None and (m.get("homo_ev") is None or m["homo_ev"] > max_homo):
            item["status"] = "rejected"
        else:
            item["status"] = "passed"
        out.append(item)
    return out
