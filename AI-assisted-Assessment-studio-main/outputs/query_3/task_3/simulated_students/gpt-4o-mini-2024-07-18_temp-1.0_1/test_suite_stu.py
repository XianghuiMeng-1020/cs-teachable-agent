from solution_program import *
import pytest
from solution_program import alien_population_change

def setup_module(module):
    # Prepare environment, if necessary
    pass

def teardown_module(module):
    # Clean up environment, if necessary
    pass

def test_single_planet():
    data = {"Mercury": ["2022:10"]}
    assert alien_population_change(data) == {"Mercury": 1.01}


def test_multiple_years():
    data = {"Earth": ["2021:30", "2022:-10", "2023:5"]}
    assert alien_population_change(data) == {"Earth": 1.025}


def test_negative_change():
    data = {"Pluto": ["2021:-10", "2022:-10", "2023:-10"]}
    assert alien_population_change(data) == {"Pluto": 0.97}


def test_multiple_planets():
    data = {
        "Jupiter": ["2021:25", "2022:15"],
        "Saturn": ["2021:-5", "2022:10"]
    }
    assert alien_population_change(data) == {"Jupiter": 1.04, "Saturn": 1.05}


def test_no_change():
    data = {"Neptune": ["2021:0", "2022:0"]}
    assert alien_population_change(data) == {"Neptune": 1.0}