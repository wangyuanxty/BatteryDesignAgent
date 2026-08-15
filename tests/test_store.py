from bda.store import CaseWorkspace, cache_key, cache_get, cache_put

def test_workspace_creates_dirs(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    assert (ws.path / "log.jsonl").parent.exists()

def test_cache_roundtrip(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    params = {"porosity": 0.25, "thickness": 7.5e-5}
    assert cache_get(ws, params) is None
    cache_put(ws, params, {"capacity_ah": 2.1})
    assert cache_get(ws, params)["capacity_ah"] == 2.1

def test_cache_key_order_invariant():
    assert cache_key({"a": 1, "b": 2}) == cache_key({"b": 2, "a": 1})
