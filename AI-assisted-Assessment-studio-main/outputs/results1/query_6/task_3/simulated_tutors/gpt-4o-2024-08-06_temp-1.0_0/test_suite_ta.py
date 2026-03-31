from program import *
import pytest
import os
from program import MythicalCreature

def setup_module(module):
    with open('test_creature.txt', 'w') as f:
        f.write('Minotaur,Beast,Greek,Maze Navigation,Immense Strength\n')

def teardown_module(module):
    os.remove('test_creature.txt')

class TestMythicalCreature:
    def test_describe(self):
        creature = MythicalCreature('Pegasus','Horse','Greek',['Flight'])
        assert creature.describe() == 'Pegasus is a Horse from Greek. Powers: Flight'

    def test_save_to_file(self):
        creature = MythicalCreature('Cerberus','Beast','Greek',['Guarding','Multiple Heads'])
        creature.save_to_file('cerberus.txt')
        with open('cerberus.txt', 'r') as f:
            data = f.read()
        assert data == 'Cerberus,Beast,Greek,Guarding,Multiple Heads\n'
        os.remove('cerberus.txt')

    def test_load_from_file(self):
        creature = MythicalCreature.load_from_file('test_creature.txt')
        assert creature.name == 'Minotaur'
        assert creature.creature_type == 'Beast'
        assert creature.origin == 'Greek'
        assert creature.powers == ['Maze Navigation', 'Immense Strength']

    def test_end_to_end(self):
        creature = MythicalCreature('Fenrir','Wolf','Norse',['Enormous Size','Great Strength'])
        creature.save_to_file('fenrir.txt')
        loaded_creature = MythicalCreature.load_from_file('fenrir.txt')
        assert loaded_creature.describe() == 'Fenrir is a Wolf from Norse. Powers: Enormous Size, Great Strength'
        os.remove('fenrir.txt')

    def test_empty_powers(self):
        creature = MythicalCreature('Sphinx','Creature','Egypt',[])
        assert creature.describe() == 'Sphinx is a Creature from Egypt. Powers: '
