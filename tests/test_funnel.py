from bda.funnel import apply_rules

def test_funnel_rules():
    cands = [
        {"smiles": "A", "metrics": {"energy_ev": -10.0, "homo_ev": -7.0, "converged": True}},
        {"smiles": "B", "metrics": {"energy_ev": 5.0, "homo_ev": -7.0, "converged": True}},   # 不稳定
        {"smiles": "C", "metrics": {"energy_ev": -10.0, "homo_ev": -5.0, "converged": True}}, # HOMO 过高
        {"smiles": "D", "metrics": {"energy_ev": None, "homo_ev": None, "converged": False}}, # 未收敛
    ]
    out = apply_rules(cands, {"max_energy_ev": 0.0, "max_homo_ev": -6.0})
    status = {c["smiles"]: c["status"] for c in out}
    assert status == {"A": "passed", "B": "rejected", "C": "rejected", "D": "rejected"}

def test_does_not_mutate_input():
    cands = [{"smiles": "A", "metrics": {"energy_ev": -1.0, "homo_ev": -7.0, "converged": True}}]
    apply_rules(cands, {"max_energy_ev": 0.0, "max_homo_ev": -6.0})
    assert "status" not in cands[0]

from bda.funnel import check_consensus

def test_consensus_flags_rank_disagreement():
    cands = [
        {"smiles": "A", "status": "passed", "metrics": {"mace_energy_ev": -1.0, "chgnet_energy_ev": -1.1, "xtb_homo_ev": -7.0}},
        {"smiles": "B", "status": "passed", "metrics": {"mace_energy_ev": -2.0, "chgnet_energy_ev": -3.0, "xtb_homo_ev": -7.5}},
        {"smiles": "C", "status": "passed", "metrics": {"mace_energy_ev": -1.5, "chgnet_energy_ev": 0.5, "xtb_homo_ev": -8.0}},  # CHGNet 强烈分歧
    ]
    out = check_consensus(cands)
    by_smiles = {c["smiles"]: c for c in out}
    assert by_smiles["C"]["status"] == "disputed"
    assert "dispute_detail" in by_smiles["C"]

def test_consensus_no_false_positive():
    cands = [
        {"smiles": "A", "status": "passed", "metrics": {"mace_energy_ev": -1.0, "chgnet_energy_ev": -1.1, "xtb_homo_ev": -7.0}},
        {"smiles": "B", "status": "passed", "metrics": {"mace_energy_ev": -1.5, "chgnet_energy_ev": -1.6, "xtb_homo_ev": -6.8}},
    ]
    out = check_consensus(cands)
    assert all(c["status"] == "passed" for c in out)
