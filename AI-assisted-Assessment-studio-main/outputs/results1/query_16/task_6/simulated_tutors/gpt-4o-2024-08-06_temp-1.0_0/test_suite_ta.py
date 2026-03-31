from program import *
import pytest
from program import Spaceship

@pytest.fixture(scope='module')
def setup_module():
    pass

def teardown_module(module):
    pass

class TestSpaceship:
    def test_valid_travel_time(self):
        ship = Spaceship(100.0, 2.0)
        assert ship.calculate_travel_time(100.0) == 50.0

    def test_zero_distance(self):
        ship = Spaceship(100.0, 2.0)
        with pytest.raises(ValueError, match="Distance must be positive"):
            ship.calculate_travel_time(0)

    def test_non_positive_fuel_multiplier(self):
        with pytest.raises(ValueError, match="Hyperdrive multiplier must be positive"):
            Spaceship(100.0, 0)

    def test_negative_fuel_level(self):
        with pytest.raises(ValueError, match="Fuel level must be non-negative"):
            Spaceship(-10.0, 1.0)

    def test_valid_edge_case_large_distance(self):
        ship = Spaceship(50.0, 1.5)
        assert ship.calculate_travel_time(150.0) == 2.0
