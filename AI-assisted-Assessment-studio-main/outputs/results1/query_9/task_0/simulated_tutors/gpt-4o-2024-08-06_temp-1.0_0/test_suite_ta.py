from program import *
import pytest

from program import mythical_population_info


def test_mythical_population_info_case_1():
    creatures = [
        {'name': 'Zeus', 'kingdom': 'Olympus', 'power': 100},
        {'name': 'Hades', 'kingdom': 'Underworld', 'power': 95},
        {'name': 'Poseidon', 'kingdom': 'Ocean', 'power': 90},
        {'name': 'Athena', 'kingdom': 'Olympus', 'power': 85}
    ]
    result = mythical_population_info(creatures)
    assert result == {
        'total_creatures': 4,
        'average_power': 92,
        'kingdom_distribution': {
            'Olympus': 2,
            'Underworld': 1,
            'Ocean': 1
        }
    }

def test_mythical_population_info_case_2():
    creatures = [
        {'name': 'Odin', 'kingdom': 'Asgard', 'power': 95},
        {'name': 'Thor', 'kingdom': 'Asgard', 'power': 90},
        {'name': 'Loki', 'kingdom': 'Jotunheim', 'power': 85}
    ]
    result = mythical_population_info(creatures)
    assert result == {
        'total_creatures': 3,
        'average_power': 90,
        'kingdom_distribution': {
            'Asgard': 2,
            'Jotunheim': 1
        }
    }

def test_mythical_population_info_case_3():
    creatures = [
        {'name': 'Anubis', 'kingdom': 'Duot', 'power': 80},
        {'name': 'Ra', 'kingdom': 'Sky', 'power': 100}
    ]
    result = mythical_population_info(creatures)
    assert result == {
        'total_creatures': 2,
        'average_power': 90,
        'kingdom_distribution': {
            'Duot': 1,
            'Sky': 1
        }
    }

def test_mythical_population_info_case_4():
    creatures = []
    result = mythical_population_info(creatures)
    assert result == {
        'total_creatures': 0,
        'average_power': 0,
        'kingdom_distribution': {}
    }

def test_mythical_population_info_case_5():
    creatures = [
        {'name': 'Hercules', 'kingdom': 'Earth', 'power': 88}
    ]
    result = mythical_population_info(creatures)
    assert result == {
        'total_creatures': 1,
        'average_power': 88,
        'kingdom_distribution': {
            'Earth': 1
        }
    }