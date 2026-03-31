from solution_program import *
import pytest
import os
from solution_program import BoardGame

def setup_module(module):
    # Setup runs before any tests
    pass

def teardown_module(module):
    # Teardown runs after all tests
    pass

# Test cases

def test_initialization():
    bg = BoardGame("Monopoly", ["john", "jane"], "ongoing")
    assert bg.game_summary() == "Game: monopoly, Players: 2, List: [john, jane], Status: ongoing"


def test_add_player():
    bg = BoardGame("Chess", [], "ongoing")
    bg.add_player("alice")
    assert bg.game_summary() == "Game: chess, Players: 1, List: [alice], Status: ongoing"
    bg.add_player("bob")
    assert bg.game_summary() == "Game: chess, Players: 2, List: [alice, bob], Status: ongoing"
    bg.add_player("bob")  # Trying to add the same player
    assert bg.game_summary() == "Game: chess, Players: 2, List: [alice, bob], Status: ongoing"


def test_remove_player():
    bg = BoardGame("Risk", ["alice", "bob", "charlie"], "ongoing")
    bg.remove_player("bob")
    assert bg.game_summary() == "Game: risk, Players: 2, List: [alice, charlie], Status: ongoing"
    bg.remove_player("bob")  # Trying to remove a non-existent player
    assert bg.game_summary() == "Game: risk, Players: 2, List: [alice, charlie], Status: ongoing"


def test_finish_game():
    bg = BoardGame("Catan", ["alice", "bob"], "ongoing")
    bg.finish_game()
    assert bg.game_summary() == "Game: catan, Players: 2, List: [alice, bob], Status: completed"


def test_cannot_add_players_when_completed():
    bg = BoardGame("Checkers", ["alex"], "completed")
    bg.add_player("blake")
    assert bg.game_summary() == "Game: checkers, Players: 1, List: [alex], Status: completed"