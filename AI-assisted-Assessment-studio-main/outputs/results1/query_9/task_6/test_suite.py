import pytest

from solution import mythological_creatures_info

def test_single_creature_with_strength():
    creatures = [
        {'name': 'Sphinx', 'attributes': {'type': 'Mystic', 'origin': 'Egypt', 'strength': 'Intelligent'}}
    ]
    result = mythological_creatures_info(creatures)
    assert result == {
        'Sphinx': {'origin': 'Egypt', 'type_strength': ['Mystic: Intelligent']}
    }

def test_single_creature_without_strength():
    creatures = [
        {'name': 'Phoenix', 'attributes': {'type': 'Bird', 'origin': 'Egypt'}}
    ]
    result = mythological_creatures_info(creatures)
    assert result == {
        'Phoenix': {'origin': 'Egypt', 'type_strength': ['Bird: unknown']}
    }

def test_multiple_creatures_mixed_strengths():
    creatures = [
        {'name': 'Cyclops', 'attributes': {'type': 'Giant', 'origin': 'Greece', 'strength': 'Very Strong'}},
        {'name': 'Hydra', 'attributes': {'type': 'Serpent', 'origin': 'Greece'}}
    ]
    result = mythological_creatures_info(creatures)
    assert result == {
        'Cyclops': {'origin': 'Greece', 'type_strength': ['Giant: Very Strong']},
        'Hydra': {'origin': 'Greece', 'type_strength': ['Serpent: unknown']}
    }

def test_empty_list_of_creatures():
    creatures = []
    result = mythological_creatures_info(creatures)
    assert result == {}

def test_no_attributes_key_creature():
    creatures = [
        {'name': 'Harpy', 'attributes': {}}
    ]
    result = mythological_creatures_info(creatures)
    assert result == {
        'Harpy': {'origin': None, 'type_strength': [None]}
    }
