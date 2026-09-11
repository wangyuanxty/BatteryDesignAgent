"""Emit funnel_summary.json + cell_summary.json mechanically from the run artifacts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FUNNEL = ROOT / "funnel"
CELL = ROOT / "cell"
ENV = ROOT / "envelope"

from rdkit import Chem

funnel = []
for k in ["pfta", "pfhex", "pftea", "pfpent", "ncf3", "sf6"]:
    m = json.loads((FUNNEL / f"{k}_mace.json").read_text(encoding="utf-8"))["candidates"][0]
    c = json.loads((FUNNEL / f"{k}_chgnet.json").read_text(encoding="utf-8"))["candidates"][0]
    x = json.loads((FUNNEL / f"{k}_xtb.json").read_text(encoding="utf-8"))["candidates"][0]
    n = Chem.MolFromSmiles(m["smiles"]).GetNumAtoms()
    row = {
        "key": k, "name": json.loads((FUNNEL / f"{k}_in.json").read_text(encoding="utf-8"))["candidates"][0]["name"],
        "smiles": m["smiles"], "n_atoms": n,
        "mace_energy_ev": m["metrics"]["energy_ev"], "mace_converged": m["metrics"]["converged"],
        "chgnet_energy_ev": c["metrics"]["energy_ev"], "chgnet_converged": c["metrics"]["converged"],
        "xtb_homo_ev": x["metrics"]["homo_ev"], "xtb_lumo_ev": x["metrics"]["lumo_ev"],
        "mace_per_atom": m["metrics"]["energy_ev"] / n,
        "chgnet_per_atom": c["metrics"]["energy_ev"] / n,
    }
    env_path = ENV / f"{k}_envelope.json"
    if env_path.exists():
        e = json.loads(env_path.read_text(encoding="utf-8"))
        row.update({"in_envelope": e["in_envelope"], "families_matched": e["families_matched"],
                    "point_per_atom": e["point_per_atom"]})
    funnel.append(row)
(ROOT / "funnel_summary.json").write_text(json.dumps(funnel, indent=2, ensure_ascii=False), encoding="utf-8")

cell = {}
for k in ["pfta", "pfhex", "pftea", "pfpent", "ncf3"]:
    a = json.loads((CELL / f"aging_{k}.json").read_text(encoding="utf-8"))
    mp = json.loads((CELL / "mapping.json").read_text(encoding="utf-8"))
    rec = [r for r in mp["candidates"] if r["candidate"] == k][0]
    cell[k] = {"sei_thickness_nm_end": a["sei_thickness_nm_end"], "k_m_s": rec["k_m_s"],
               "k_over_k0": rec["k_over_k0"], "homo_ev": rec["homo_ev_xtb"]}
cell["pfta_cell_window"] = {
    "energy_density_wh_kg": json.loads((CELL / "energy_pfta.json").read_text(encoding="utf-8"))["energy_density_wh_kg"],
    "mass_kg": json.loads((CELL / "energy_pfta.json").read_text(encoding="utf-8"))["mass_kg"],
    "charge4c_T_max_K": json.loads((CELL / "charge_4c_45c_pfta.json").read_text(encoding="utf-8"))["T_max_K"],
    "anode_potential_min_v": min(json.loads((CELL / "charge_4c_45c_pfta.json").read_text(encoding="utf-8"))["anode_potential_v"]),
    "run_tr_triggered": json.loads((CELL / "runtr_pfta.json").read_text(encoding="utf-8"))["triggered"],
}
cell["window_edge_check"] = {
    "k_at_homo_minus13p74": json.loads((CELL / "params_window_edge.json").read_text(encoding="utf-8"))["SEI kinetic rate constant [m.s-1]"],
    "sei_thickness_nm_end": json.loads((CELL / "aging_window_edge.json").read_text(encoding="utf-8"))["sei_thickness_nm_end"],
}
cell["calibration_replication"] = {
    "baseline_k0_sei_nm": json.loads((ROOT / "calib" / "aging_baseline_k0.json").read_text(encoding="utf-8"))["sei_thickness_nm_end"],
    "k0p1x_sei_nm": json.loads((ROOT / "calib" / "aging_0p1x.json").read_text(encoding="utf-8"))["sei_thickness_nm_end"],
    "contract_reference": "449.12 nm (k0), 385.10 nm (0.1x k0)",
}
(ROOT / "cell_summary.json").write_text(json.dumps(cell, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote funnel_summary.json, cell_summary.json")
