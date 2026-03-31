import pytest
from solution import count_creature_types

def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_creature_count_case_1():
    creatures = ['Human', 'Robot', 'Alien', 'Human', 'Robot', 'Alien', 'Alien']
    result = count_creature_types(creatures)
    assert result == {'Human': 2, 'Robot': 2, 'Alien': 3}


def test_creature_count_case_2():
    creatures = ['Alien', 'Alien', 'Alien', 'Robot']
    result = count_creature_types(creatures)
    assert result == {'Alien': 3, 'Robot': 1}


def test_creature_count_case_3():
    creatures = ['Human']
    result = count_creature_types(creatures)
    assert result == {'Human': 1}


def test_creature_count_case_4():
    creatures = ['Robot', 'Robot', 'Robot']
    result = count_creature_types(creatures)
    assert result == {'Robot': 3}


def test_creature_count_case_5():
    creatures = ['Martian', 'Venusian', 'Martian', 'Human', 'Martian']
    result = count_creature_types(creatures)
    assert result == {'Martian': 3, 'Venusian': 1, 'Human': 1}