from program import *
import pytest
import os
from program import MythicalCreature, CreatureManager

@pytest.fixture(scope='module', autouse=True)
def setup_module(module):
    with open('test_creatures.txt', 'w') as f:
        f.write("Phoenix,Bird,Egyptian,Rebirth\n")
        f.write("Minotaur,Beast,Greek,Strength\n")

@pytest.fixture(scope='module', autouse=True)
def teardown_module(module):
    os.remove('test_creatures.txt')
    if os.path.exists('output_creatures.txt'):
        os.remove('output_creatures.txt')


def test_add_creature():
    manager = CreatureManager()
    manager.add_creature("Dragon", "Reptile", "Chinese", "Fire Breathing")
    assert len(manager.creatures) == 1
    assert manager.creatures[0].name == "Dragon"


def test_save_file():
    manager = CreatureManager()
    manager.add_creature("Dragon", "Reptile", "Chinese", "Fire Breathing")
    manager.add_creature("Unicorn", "Horse", "Medieval", "Magic Horn")
    manager.save_to_file("output_creatures.txt")
    with open("output_creatures.txt", "r") as f:
        data = f.readlines()
    assert len(data) == 2
    assert data[0].strip() == "Dragon,Reptile,Chinese,Fire Breathing"
    assert data[1].strip() == "Unicorn,Horse,Medieval,Magic Horn"


def test_load_file():
    manager = CreatureManager()
    manager.load_from_file("test_creatures.txt")
    assert len(manager.creatures) == 2
    assert manager.creatures[0].name == "Phoenix"
    assert manager.creatures[1].type == "Beast"


def test_save_and_load_combined():
    manager = CreatureManager()
    manager.load_from_file("test_creatures.txt")
    manager.add_creature("Cerberus", "Dog", "Greek", "Guardian")
    manager.save_to_file("output_creatures.txt")
    manager2 = CreatureManager()
    manager2.load_from_file("output_creatures.txt")
    assert len(manager2.creatures) == 3
    names = [creature.name for creature in manager2.creatures]
    assert "Cerberus" in names


def test_empty_file_load():
    empty_filename = "empty_creatures.txt"
    open(empty_filename, 'w').close()
    manager = CreatureManager()
    manager.load_from_file(empty_filename)
    assert len(manager.creatures) == 0
    os.remove(empty_filename)