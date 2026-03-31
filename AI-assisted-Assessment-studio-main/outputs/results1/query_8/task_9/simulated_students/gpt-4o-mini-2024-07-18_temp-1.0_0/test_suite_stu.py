from solution_program import *
import pytest

from solution_program import mythical_character_power

def test_known_character_zeus():
    assert mythical_character_power('Zeus') == 'Thunder'

def test_known_character_poseidon():
    assert mythical_character_power('Poseidon') == 'Sea'

def test_known_character_athena():
    assert mythical_character_power('Athena') == 'Wisdom'

def test_known_character_hades():
    assert mythical_character_power('Hades') == 'Underworld'

def test_unknown_character():
    assert mythical_character_power('UnknownCharacter') == 'Unknown'

def test_known_character_apollo():
    assert mythical_character_power('Apollo') == 'Sun'

def test_uppercase_character():
    assert mythical_character_power('zeus') == 'Unknown'

def test_empty_string():
    assert mythical_character_power('') == 'Unknown'