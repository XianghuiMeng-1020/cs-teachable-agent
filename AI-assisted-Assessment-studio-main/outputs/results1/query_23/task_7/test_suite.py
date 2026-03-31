import pytest
import os
from solution import Scoreboard

@pytest.fixture
def setup_module():
    global players
    players = ['Alice', 'Bob', 'Charlie']

def teardown_module(module):
    pass

def test_initial_scores(setup_module):
    scoreboard = Scoreboard(players)
    assert scoreboard.get_score('Alice') == 0
    assert scoreboard.get_score('Bob') == 0
    assert scoreboard.get_score('Charlie') == 0

def test_update_scores(setup_module):
    scoreboard = Scoreboard(players)
    scoreboard.update_score('Alice', 10)
    scoreboard.update_score('Bob', 5)
    assert scoreboard.get_score('Alice') == 10
    assert scoreboard.get_score('Bob') == 5
    assert scoreboard.get_score('Charlie') == 0

def test_get_winner(setup_module):
    scoreboard = Scoreboard(players)
    scoreboard.update_score('Alice', 10)
    scoreboard.update_score('Bob', 10)
    scoreboard.update_score('Charlie', 5)
    winner = scoreboard.get_winner()
    assert winner == 'Alice, Bob'

def test_update_and_retrieve_all_scores(setup_module):
    scoreboard = Scoreboard(players)
    scoreboard.update_score('Charlie', 3)
    scoreboard.update_score('Alice', 5)
    assert scoreboard.get_all_scores() == "Alice:5, Bob:0, Charlie:3"

def test_score_ties(setup_module):
    scoreboard = Scoreboard(players)
    scoreboard.update_score('Alice', 7)
    scoreboard.update_score('Bob', 7)
    assert scoreboard.get_winner() == 'Alice, Bob'