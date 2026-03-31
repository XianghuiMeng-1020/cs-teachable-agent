from program import *
import pytest
from program import mythical_creature_classification

def test_basic_classification():
    creatures = {
        "Minotaur": {"type": "monstrous", "danger_level": 5, "favored_by": "Ares"},
        "Cyclops": {"type": "monstrous", "danger_level": 7, "favored_by": "Zeus"},
        "Pegasus": {"type": "divine", "danger_level": 2, "favored_by": "Athena"}
    }
    expected = {
        "Minotaur": "Moderately Threatening",
        "Cyclops": "Highly Threatening - Zeus' favorite",
        "Pegasus": "Not Threatening"
    }
    assert mythical_creature_classification(creatures) == expected

def test_zeus_favored():
    creatures = {
        "Cerberus": {"type": "monstrous", "danger_level": 6, "favored_by": "Zeus"},
        "Harpy": {"type": "monstrous", "danger_level": 4, "favored_by": "Ares"}
    }
    expected = {
        "Cerberus": "Moderately Threatening - Zeus' favorite",
        "Harpy": "Moderately Threatening"
    }
    assert mythical_creature_classification(creatures) == expected

def test_low_danger():
    creatures = {
        "Satyr": {"type": "divine", "danger_level": 1, "favored_by": "Dionysus"}
    }
    expected = {
        "Satyr": "Not Threatening"
    }
    assert mythical_creature_classification(creatures) == expected

def test_high_danger_non_zeus():
    creatures = {
        "Typhon": {"type": "monstrous", "danger_level": 10, "favored_by": "Hera"}
    }
    expected = {
        "Typhon": "Highly Threatening"
    }
    assert mythical_creature_classification(creatures) == expected

def test_empty_creatures():
    creatures = {}
    expected = {}
    assert mythical_creature_classification(creatures) == expected
