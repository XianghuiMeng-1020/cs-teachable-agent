import pytest
import os
from solution import MythologicalCreature, CreaturesRepository

def setup_module(module):
    with open('test_creatures.txt', 'w') as file:
        file.write("Dragon;European;A large, serpentine legendary creature that appears in the folklore of many cultures worldwide.\n")
        file.write("Phoenix;Egyptian;A long-lived bird that cyclically regenerates or is otherwise born again.\n")
        file.write("Unicorn;Western;A legendary animal that has been described since antiquity as a beast with a single large, pointed, spiraling horn projecting from its forehead.\n")

def teardown_module(module):
    os.remove('test_creatures.txt')
    if os.path.exists('output_creatures.txt'):
        os.remove('output_creatures.txt')

def test_add_creature():
    repo = CreaturesRepository()
    creature = MythologicalCreature("Cerberus", "Greek", "A multi-headed dog that guards the gates of the Underworld.")
    repo.add_creature(creature)
    assert any(c.name == "Cerberus" for c in repo.creatures)

def test_remove_creature():
    repo = CreaturesRepository()
    creature = MythologicalCreature("Minotaur", "Greek", "A creature with the head of a bull and the body of a man.")
    repo.add_creature(creature)
    repo.remove_creature("Minotaur")
    assert not any(c.name == "Minotaur" for c in repo.creatures)

def test_load_from_file():
    repo = CreaturesRepository()
    repo.load_from_file('test_creatures.txt')
    assert any(c.name == "Dragon" for c in repo.creatures)
    assert any(c.name == "Phoenix" for c in repo.creatures)
    assert any(c.name == "Unicorn" for c in repo.creatures)

def test_save_to_file():
    repo = CreaturesRepository()
    repo.load_from_file('test_creatures.txt')
    repo.save_to_file('output_creatures.txt')
    with open('output_creatures.txt', 'r') as file:
        content = file.read()
    assert "Dragon;European;" in content
    assert "Phoenix;Egyptian;" in content
    assert "Unicorn;Western;" in content

def test_empty_removal_handling():
    repo = CreaturesRepository()
    repo.remove_creature("NonExistent")  # Attempting to remove a non-existent creature
    assert len(repo.creatures) == 0