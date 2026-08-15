from bda.metrics.energy_density import cell_mass_kg, gravimetric_energy_density

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
