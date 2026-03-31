import pytest
from spaceship_module import Spaceship

class TestSpaceship:
    def test_high_efficiency(self):
        s = Spaceship('Voyager', 60000, 10000)
        assert s.calculate_fuel_efficiency() == 6.0
        assert s.efficiency_report() == "High Efficiency"

    def test_moderate_efficiency(self):
        s = Spaceship('Pioneer', 3000, 1000)
        assert s.calculate_fuel_efficiency() == 3.0
        assert s.efficiency_report() == "Moderate Efficiency"

    def test_low_efficiency(self):
        s = Spaceship('Galactic Cruiser', 1000, 1000)
        assert s.calculate_fuel_efficiency() == 1.0
        assert s.efficiency_report() == "Low Efficiency"

    def test_zero_fuel_exception(self):
        s = Spaceship('Enterprise', 5000, 0)
        with pytest.raises(ValueError):
            s.calculate_fuel_efficiency()

    def test_boundary_efficiency_high(self):
        s = Spaceship('Boundary High', 5001, 1000)
        assert s.calculate_fuel_efficiency() == 5.001
        assert s.efficiency_report() == "High Efficiency"
