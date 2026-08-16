RANK_KEYS = ("mace_energy_ev", "chgnet_energy_ev", "xtb_homo_ev")


def _ranks(cands: list[dict], key: str) -> dict:
    values = [(c["smiles"], c["metrics"][key]) for c in cands]
    ordered = sorted(values, key=lambda kv: kv[1])  # 能量/轨道能越低越优，统一升序排名
    return {smiles: i for i, (smiles, _) in enumerate(ordered)}


def check_consensus(cands: list[dict], rank_spread: int | None = None) -> list[dict]:
    n = len(cands)
    if n < 3:
        return [dict(c) for c in cands]
    spread_threshold = rank_spread if rank_spread is not None else max(2, int(0.3 * n))
    rank_lists = {key: _ranks(cands, key) for key in RANK_KEYS}
    out = []
    for c in cands:
        item = dict(c)
        ranks = [rank_lists[key][c["smiles"]] for key in RANK_KEYS]
        if max(ranks) - min(ranks) >= spread_threshold:
            item["status"] = "disputed"
            item["dispute_detail"] = {"ranks": dict(zip(RANK_KEYS, ranks))}
        out.append(item)
    return out
