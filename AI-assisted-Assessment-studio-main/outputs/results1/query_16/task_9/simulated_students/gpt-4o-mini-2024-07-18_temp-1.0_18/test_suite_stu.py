from solution_program import *
import pytest
import os
from solution_program import Starship

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_module():
    yield

@pytest.mark.parametrize("initial_time, velocity, intensity, expected", [
    (10, 1.0, 2, "20.00 years"),
    (15, 0.5, 4, "30.00 years"),
    (5, 2.0, 3, "30.00 years"),
    (0, 1.5, 3, "0.00 years"),
    (10, 1.1, 0, "0.00 years")
])
def test_travel_through_wormhole(initial_time, velocity, intensity, expected):
    ship = Starship(initial_time, velocity)
    ship.travel_through_wormhole(intensity)
    assert ship.get_effective_time() == expected


def test_handle_exception_test():
    ship = Starship(0, 0)
    assert ship.handle_exception_test() == 'Handled Exception: Division by zero.'