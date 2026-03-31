from program import *
import pytest
import os
from program import MythicalCreature, MythicalDatabase

CREATURES_FILE = 'test_creatures.txt'

# Setup and teardown functions for file creation and removal
def setup_module(module):
    with open(CREATURES_FILE, 'w') as f:
        f.write('Fenrir|Norse|A monstrous wolf\n')
        f.write('Medusa|Greek|A Gorgon with snakes for hair\n')

def teardown_module(module):
    os.remove(CREATURES_FILE)

# Test cases
def test_add_creature():
    db = MythicalDatabase()
    db.add_creature('Phoenix', 'Greek', 'A firebird that regenerates')
    assert len(db.list_creatures()) == 1
    assert db.list_creatures()[0] == 'Name: Phoenix, Origin: Greek, Description: A firebird that regenerates'


def test_list_creatures():
    db = MythicalDatabase()
    db.add_creature('Cerberus', 'Greek', 'A three-headed dog')
    db.add_creature('Jormungandr', 'Norse', 'The world serpent')
    creatures = db.list_creatures()
    assert len(creatures) == 2
    assert creatures[0] == 'Name: Cerberus, Origin: Greek, Description: A three-headed dog'
    assert creatures[1] == 'Name: Jormungandr, Origin: Norse, Description: The world serpent'


def test_save_to_file():
    db = MythicalDatabase()
    db.add_creature('Cerberus', 'Greek', 'A three-headed dog')
    db.add_creature('Jormungandr', 'Norse', 'The world serpent')
    db.save_to_file('output_creatures.txt')
    with open('output_creatures.txt', 'r') as f:
        lines = f.readlines()
    os.remove('output_creatures.txt')
    assert len(lines) == 2
    assert lines[0].strip() == 'Cerberus|Greek|A three-headed dog'
    assert lines[1].strip() == 'Jormungandr|Norse|The world serpent'


def test_load_from_file():
    db = MythicalDatabase()
    db.load_from_file(CREATURES_FILE)
    creatures = db.list_creatures()
    assert len(creatures) == 2
    assert creatures[0] == 'Name: Fenrir, Origin: Norse, Description: A monstrous wolf'
    assert creatures[1] == 'Name: Medusa, Origin: Greek, Description: A Gorgon with snakes for hair'


def test_append_after_loading():
    db = MythicalDatabase()
    db.load_from_file(CREATURES_FILE)
    db.add_creature('Phoenix', 'Greek', 'A firebird that regenerates')
    creatures = db.list_creatures()
    assert len(creatures) == 3
    assert creatures[2] == 'Name: Phoenix, Origin: Greek, Description: A firebird that regenerates'
