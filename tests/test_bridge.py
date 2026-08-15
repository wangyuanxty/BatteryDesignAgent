from bda.bridge.mapper import map_micro_to_pybamm

def test_maps_known_props():
    out = map_micro_to_pybamm({"D_electrolyte_m2_s": 3e-10, "conductivity_S_m": 1.1})
    assert out["Electrolyte diffusivity [m2.s-1]"] == 3e-10
    assert out["Electrolyte conductivity [S.m-1]"] == 1.1

def test_unknown_key_fails_fast():
    import pytest
    with pytest.raises(ValueError, match="D_electrolyte_m2_s"):
        map_micro_to_pybamm({"bogus_key": 1.0})
