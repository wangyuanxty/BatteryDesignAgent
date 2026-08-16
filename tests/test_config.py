from bda.config import load_case_config

def test_loads_valid_config(tmp_path):
    p = tmp_path / "case.yaml"
    p.write_text("""
goal: "设计一种电解液添加剂，改善 4C 快充下的析锂"
system: "EC/EMC+LiPF6"
max_rounds: 30
seed_pool: ["FEC", "VC"]
ablations:
  guardrails: true
  consistency: true
  bridge: true
""", encoding="utf-8")
    cfg = load_case_config(str(p))
    assert cfg.goal.startswith("设计")
    assert cfg.max_rounds == 30
    assert cfg.seed_pool == ["FEC", "VC"]
    assert cfg.ablations["bridge"] is True

def test_rejects_missing_goal(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("system: EC/EMC+LiPF6\n", encoding="utf-8")
    import pytest
    with pytest.raises(ValueError, match="goal"):
        load_case_config(str(p))

def test_loads_real_compute_flag(tmp_path):
    p_true = tmp_path / "true.yaml"
    p_true.write_text("goal: g\nsystem: s\nreal_compute: true\n", encoding="utf-8")
    assert load_case_config(str(p_true)).real_compute is True

    p_default = tmp_path / "default.yaml"
    p_default.write_text("goal: g\nsystem: s\n", encoding="utf-8")
    assert load_case_config(str(p_default)).real_compute is False
