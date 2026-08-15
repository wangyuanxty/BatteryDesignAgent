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
    )
    if cfg.max_rounds < 1:
        raise ValueError("max_rounds must be >= 1")
    return cfg
