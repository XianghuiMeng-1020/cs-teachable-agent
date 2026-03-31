from solution_program import *
import os
import pytest
from solution_program import MythologyManager

def setup_module(module):
    with open('test_mythology.txt', 'w') as file:
        file.write('')

def teardown_module(module):
    os.remove('test_mythology.txt')

def test_add_and_get_story():
    manager = MythologyManager('test_mythology.txt')
    manager.add_story('Zeus', 'Ruler of the Olympian gods.')
    assert manager.get_story('Zeus') == 'Ruler of the Olympian gods.'


def test_get_nonexistent_story():
    manager = MythologyManager('test_mythology.txt')
    assert manager.get_story('Poseidon') == ''


def test_remove_story():
    manager = MythologyManager('test_mythology.txt')
    manager.add_story('Hades', 'God of the underworld.')
    manager.remove_story('Hades')
    assert manager.get_story('Hades') == ''


def test_persistence_across_sessions():
    manager = MythologyManager('test_mythology.txt')
    manager.add_story('Athena', 'Goddess of wisdom and war.')
    manager.save()

    new_manager = MythologyManager('test_mythology.txt')
    assert new_manager.get_story('Athena') == 'Goddess of wisdom and war.'


def test_overwrite_existing_file():
    manager = MythologyManager('test_mythology.txt')
    manager.add_story('Hermes', 'Messenger of the gods.')
    manager.save()

    overwrite_manager = MythologyManager('test_mythology.txt')
    assert overwrite_manager.get_story('Hermes') == 'Messenger of the gods.'

    overwrite_manager.add_story('Apollo', 'God of the sun.')
    overwrite_manager.save()

    final_manager = MythologyManager('test_mythology.txt')
    assert final_manager.get_story('Apollo') == 'God of the sun.'
    assert final_manager.get_story('Hermes') == 'Messenger of the gods.'
