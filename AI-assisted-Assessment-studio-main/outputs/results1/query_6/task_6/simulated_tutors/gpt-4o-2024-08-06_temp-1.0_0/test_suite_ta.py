from program import *
import pytest
import os
from program import Creature, read_creatures_from_file, save_creatures_to_file

def setup_module(module):
    with open('creatures.txt', 'w') as f:
        f.write("Cerberus,Greek,A three-headed dog
")
        f.write("Sirens,Greek,Creatures who lure sailors
")
        f.write("Fenrir,Norse,A monstrous wolf
")
        f.write("Anansi,Akan,A spider god
")
        f.write("Ganesha,Hindu,God with an elephant head
")

def teardown_module(module):
    os.remove('creatures.txt')
    if os.path.exists('output_creatures.txt'):
        os.remove('output_creatures.txt')

def test_creature_initialization():
    creature = Creature("Phoenix", "Egyptian", "A fire bird")
    assert creature.name == "Phoenix"
    assert creature.origin == "Egyptian"
    assert creature.description == "A fire bird"


def test_creature_string_representation():
    creature = Creature("Phoenix", "Egyptian", "A fire bird")
    assert str(creature) == "Phoenix from Egyptian: A fire bird"


def test_read_creatures_from_file():
    creatures = read_creatures_from_file('creatures.txt')
    assert len(creatures) == 5
    assert creatures[0].name == "Cerberus"
    assert creatures[0].origin == "Greek"
    assert creatures[0].description == "A three-headed dog"


def test_save_creatures_to_file():
    creatures = read_creatures_from_file('creatures.txt')
    save_creatures_to_file(creatures, 'output_creatures.txt')
    with open('output_creatures.txt', 'r') as f:
        lines = f.readlines()
    assert len(lines) == 5
    assert lines[0].strip() == "Cerberus,Greek,A three-headed dog"


def test_file_round_trip():
    initial_creatures = read_creatures_from_file('creatures.txt')
    save_creatures_to_file(initial_creatures, 'output_creatures.txt')
    round_trip_creatures = read_creatures_from_file('output_creatures.txt')
    assert len(round_trip_creatures) == len(initial_creatures)
    for ic, rtc in zip(initial_creatures, round_trip_creatures):
        assert ic.name == rtc.name
        assert ic.origin == rtc.origin
        assert ic.description == rtc.description
