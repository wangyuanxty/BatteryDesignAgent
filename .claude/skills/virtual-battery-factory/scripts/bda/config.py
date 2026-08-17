from dataclasses import dataclass, field
import yaml


@dataclass
class CaseConfig:
    goal: str
    system: str
    max_rounds: int = 30
    seed_pool: list[str] = field(default_factory=list)
    ablations: dict[str, bool] = field(default_factory=dict)
    base_params: str = "Chen2020"
    real_compute: bool = False
    start_stage: int = 1  # 1=全流程（阶段1 材料设计起）；2=从阶段2 结构设计起（材料用体系基线）


def load_case_config(path: str) -> CaseConfig:
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if not isinstance(raw, dict) or not raw.get("goal"):
        raise ValueError("case config requires a 'goal' field")
    if not raw.get("system"):
        raise ValueError("case config requires a 'system' field")
    cfg = CaseConfig(
        goal=str(raw["goal"]),
        system=str(raw["system"]),
        max_rounds=int(raw.get("max_rounds", 30)),
        seed_pool=list(raw.get("seed_pool", [])),
        ablations=dict(raw.get("ablations", {})),
        base_params=str(raw.get("base_params", "Chen2020")),
        real_compute=bool(raw.get("real_compute", False)),
        start_stage=int(raw.get("start_stage", 1)),
    )
    if cfg.max_rounds < 1:
        raise ValueError("max_rounds must be >= 1")
    if cfg.start_stage not in (1, 2):
        raise ValueError("start_stage must be 1 or 2")
    return cfg
