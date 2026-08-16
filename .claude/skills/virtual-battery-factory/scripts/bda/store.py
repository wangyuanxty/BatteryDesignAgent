import hashlib
import json
from pathlib import Path


class CaseWorkspace:
    def __init__(self, case_id: str, root: str = "runs", create: bool = True):
        self.path = Path(root) / case_id
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
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        # Corrupt cache file: treat as a miss (cache_put will overwrite it).
        return None
    return data if isinstance(data, dict) else None


def cache_put(ws: CaseWorkspace, params: dict, result: dict) -> None:
    p = _cache_path(ws, params)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
