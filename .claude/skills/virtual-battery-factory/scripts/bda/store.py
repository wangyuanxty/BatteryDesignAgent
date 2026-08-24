import hashlib
import json
from pathlib import Path


def _repo_root() -> Path:
    """仓库根 = 含 .git 或 .claude 的最上层目录（相对路径一律基于它解析，杜绝 cwd 依赖）。"""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists() or (parent / ".claude").exists():
            return parent
    return p.parents[3]


REPO_ROOT = _repo_root()


class CaseWorkspace:
    def __init__(self, case_id: str, root: str = "runs", create: bool = True):
        # 相对 root 基于仓库根解析（t2_r1 实测：agent cd 进工作区后相对路径
        # 拼成 runs/runs/exp/... 双重路径——绝对化后免疫 cwd）
        p = Path(root)
        if not p.is_absolute():
            p = REPO_ROOT / p
        self.path = p / case_id
        if create:
            for sub in ("candidates", "bridge", "cell", "validation", "csv"):
                (self.path / sub).mkdir(parents=True, exist_ok=True)


def cache_key(params: dict) -> str:
    canonical = json.dumps(params, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _cache_path(ws: CaseWorkspace, params: dict) -> Path:
    return ws.path / "cache" / f"{cache_key(params)}.json"


def cache_get(ws: CaseWorkspace, params: dict) -> dict | None:
    p = _cache_path(ws, params)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        # Corrupt cache file: treat as a miss (cache_put will overwrite it).
        return None
    return data if isinstance(data, dict) else None


def cache_put(ws: CaseWorkspace, params: dict, result: dict) -> None:
    p = _cache_path(ws, params)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")


def append_entry(ws: CaseWorkspace, entry: dict) -> None:
    with open(ws.path / "log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
