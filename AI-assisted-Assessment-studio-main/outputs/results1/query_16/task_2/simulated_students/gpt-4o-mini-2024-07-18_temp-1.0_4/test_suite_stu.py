from solution_program import *
import pytest
import os
from solution_program import Lasergun

@pytest.fixture(scope="module")
def setup_module(module):
    # No files to setup within this particular problem
    pass

@pytest.fixture(scope="module")
def teardown_module(module):
    # No files to teardown in this particular problem
    pass

@pytest.mark.parametrize("total_energy, shot_times, expected", [
    (100, 5, "Remaining energy: 50"),
    (50, 5, "Out of energy!"),
    (30, 2, "Remaining energy: 10"),
    (10, 1, "Remaining energy: 0"),
    (10, 2, "Out of energy!")
])
def test_lasergun_functionality(total_energy, shot_times, expected):
    gun = Lasergun(total_energy)
    for _ in range(shot_times):
        result = gun.shoot()
    assert result == expected


@pytest.mark.parametrize("total_energy, error_message", [
    (0, "Invalid energy value."),
    (-10, "Invalid energy value."),
])
def test_invalid_initialization(total_energy, error_message):
    with pytest.raises(ValueError) as e:
        Lasergun(total_energy)
    assert str(e.value) == error_message


def test_reload_functionality():
    gun = Lasergun(50)
    for _ in range(5):
        gun.shoot()
    gun.reload()
    assert gun.remaining_energy() == "Remaining energy: 50"
