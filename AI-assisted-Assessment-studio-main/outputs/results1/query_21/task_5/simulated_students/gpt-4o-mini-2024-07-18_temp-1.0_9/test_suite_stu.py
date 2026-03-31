from solution_program import *
import pytest
import os
from leaderboard import BoardGameLeaderboard

leaderboard_file = 'leaderboard.txt'


def setup_module(module):
    with open(leaderboard_file, 'w') as f:
        f.write("Alice:50\nBob:40\nCharlie:30\n")


def teardown_module(module):
    os.remove(leaderboard_file)


def test_add_score_new_player():
    leaderboard = BoardGameLeaderboard()
    leaderboard.load_from_file()
    leaderboard.add_score("David", 25)
    assert leaderboard.get_score("David") == 25
    leaderboard.save_to_file()


def test_add_score_existing_player():
    leaderboard = BoardGameLeaderboard()
    leaderboard.load_from_file()
    leaderboard.add_score("Alice", 20)
    assert leaderboard.get_score("Alice") == 70
    leaderboard.save_to_file()


def test_get_score_nonexistent_player():
    leaderboard = BoardGameLeaderboard()
    leaderboard.load_from_file()
    score = leaderboard.get_score("Eve")
    assert score == 0


def test_get_top_player():
    leaderboard = BoardGameLeaderboard()
    leaderboard.load_from_file()
    assert leaderboard.get_top_player() == "Alice"


def test_save_and_load_consistency():
    leaderboard = BoardGameLeaderboard()
    leaderboard.load_from_file()
    leaderboard.add_score("David", 100)
    leaderboard.save_to_file()
    new_leaderboard = BoardGameLeaderboard()
    new_leaderboard.load_from_file()
    assert new_leaderboard.get_score("David") == 100
