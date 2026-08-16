import json
import subprocess
import sys

PY = sys.executable

def test_unknown_command_fails_fast():
    r = subprocess.run([PY, "-m", "bda", "nonsense"], capture_output=True, text=True)
    assert r.returncode != 0
    assert "command" in r.stderr.lower() or "usage" in r.stderr.lower()

def test_bridge_roundtrip(tmp_path):
    props = tmp_path / "p.json"
    props.write_text(json.dumps({"D_electrolyte_m2_s": 3e-10}), encoding="utf-8")
    out = tmp_path / "o.json"
    r = subprocess.run([PY, "-m", "bda", "bridge", "--props", str(props), "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["Electrolyte diffusivity [m2.s-1]"] == 3e-10

def test_bridge_bad_key_exit_1(tmp_path):
    props = tmp_path / "p.json"
    props.write_text(json.dumps({"bogus": 1.0}), encoding="utf-8")
    out = tmp_path / "o.json"
    r = subprocess.run([PY, "-m", "bda", "bridge", "--props", str(props), "--out", str(out)],
                       capture_output=True, text=True)
    assert r.returncode == 1
    assert "bogus" in r.stderr
