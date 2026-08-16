from bda.store import CaseWorkspace, cache_key, cache_get, cache_put

def test_workspace_creates_dirs(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    assert (ws.path / "log.jsonl").parent.exists()

def test_workspace_no_create_leaves_dir_empty(tmp_path):
    root = tmp_path / "outdir"
    root.mkdir()
    ws = CaseWorkspace(".", root=str(root), create=False)
    assert ws.path == root
    assert list(root.iterdir()) == []  # no subdir side effects at the out-parent

def test_cache_roundtrip(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    params = {"porosity": 0.25, "thickness": 7.5e-5}
    assert cache_get(ws, params) is None
    cache_put(ws, params, {"capacity_ah": 2.1})
    assert cache_get(ws, params)["capacity_ah"] == 2.1

def test_cache_key_order_invariant():
    assert cache_key({"a": 1, "b": 2}) == cache_key({"b": 2, "a": 1})

def test_corrupt_cache_file_is_treated_as_miss(tmp_path):
    """Invalid JSON in the cache file must be a miss, then overwritten on put."""
    ws = CaseWorkspace("case1", root=str(tmp_path))
    params = {"porosity": 0.25}
    cache_put(ws, params, {"capacity_ah": 2.1})
    cache_path = ws.path / "cache" / f"{cache_key(params)}.json"
    cache_path.write_text("{not valid json", encoding="utf-8")
    assert cache_get(ws, params) is None  # corrupt -> miss, no crash
    cache_put(ws, params, {"capacity_ah": 3.3})  # overwrite the corrupt file
    assert cache_get(ws, params)["capacity_ah"] == 3.3

def test_non_dict_cache_file_is_treated_as_miss(tmp_path):
    ws = CaseWorkspace("case1", root=str(tmp_path))
    params = {"porosity": 0.25}
    cache_put(ws, params, {"capacity_ah": 2.1})
    cache_path = ws.path / "cache" / f"{cache_key(params)}.json"
    cache_path.write_text('[1, 2, 3]', encoding="utf-8")
    assert cache_get(ws, params) is None
