from bda.funnel.filter import apply_rules

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
