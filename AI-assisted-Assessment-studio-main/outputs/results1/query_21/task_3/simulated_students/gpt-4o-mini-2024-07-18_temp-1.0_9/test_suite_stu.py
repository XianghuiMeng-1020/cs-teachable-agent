from solution_program import *
import pytest
import os
from solution_program import BoardGame

# Setup function to create a mock file before tests run

def setup_module(module):
    with open('players.txt', 'w') as f:
        f.write('Alice,10\n')
        f.write('Bob,15\n')
        f.write('Charlie,5\n')

def teardown_module(module):
    if os.path.exists('players.txt'):
        os.remove('players.txt')


def test_add_player():
    game = BoardGame()
    game.add_player("David", 20)
    game = BoardGame()  # Reload to check file persistence
    assert game.get_highest_score() == "David"

def test_update_score():
    game = BoardGame()
    game.update_score("Alice", 10)
    game = BoardGame()  # Reload to check file persistence
    assert game.get_highest_score() == "Alice"

def test_highest_score_tie_scenario():
    game = BoardGame()
    game.update_score("Charlie", 20)
    game = BoardGame()  # Reload to check file persistence
    assert game.get_highest_score() == "Charlie"

def test_non_existent_player_update():
    game = BoardGame()
    game.update_score("Nonexistent", 10)
    game = BoardGame()  # Reload to check file persistence
    assert game.get_highest_score() == "Bob"

def test_adding_existing_player_ignored():
    game = BoardGame()
    game.add_player("Alice", 1000) # Should be ignored since Alice is already there
    game = BoardGame()  # Reload to check file persistence
    assert game.get_highest_score() == "Bob"
