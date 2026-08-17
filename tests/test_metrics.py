from bda.metrics import cell_mass_kg, gravimetric_energy_density

def test_cell_mass_kg():
    layers = {
        "positive": {"thickness_m": 7.5e-5, "porosity": 0.25, "density_kg_m3": 4500.0},
        "negative": {"thickness_m": 8.5e-5, "porosity": 0.30, "density_kg_m3": 2200.0},
    }
    m = cell_mass_kg(layers)
    # 7.5e-5*0.75*4500 + 8.5e-5*0.70*2200
    expected = 0.253125 + 0.1309
    assert abs(m - expected) < 1e-6

def test_gravimetric_energy_density():
    assert gravimetric_energy_density(200.0, 1.0) == 200.0

def test_zero_mass_raises():
    import pytest
    with pytest.raises(ValueError):
        gravimetric_energy_density(200.0, 0.0)

from bda.metrics import detect_lithium_plating
from bda.metrics import ie_ea_from_energies, homo_lumo_window

def test_plating_detected_below_zero():
    t = [0.0, 1.0, 2.0, 3.0]
    v = [0.05, 0.02, -0.01, -0.05]
    r = detect_lithium_plating(v, t)
    assert r["plated"] is True
    assert r["first_time_s"] == 2.0

def test_no_plating():
    r = detect_lithium_plating([0.05, 0.02, 0.01], [0.0, 1.0, 2.0])
    assert r["plated"] is False
    assert r["first_time_s"] is None

def test_ie_ea():
    r = ie_ea_from_energies(E_neutral_ev=0.0, E_cation_ev=8.0, E_anion_ev=-1.5)
    assert abs(r["IE_ev"] - 8.0) < 1e-9
    assert abs(r["EA_ev"] - 1.5) < 1e-9

def test_window():
    assert abs(homo_lumo_window(-6.5, -1.5) - 5.0) < 1e-9
