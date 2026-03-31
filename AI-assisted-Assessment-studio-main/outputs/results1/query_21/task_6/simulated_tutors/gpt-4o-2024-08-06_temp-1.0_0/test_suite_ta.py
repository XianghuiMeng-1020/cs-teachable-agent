from program import *
import pytest
import os
from program import BoardGameScoreboard

def setup_module(module):
    open('test_scoreboard.txt', 'w').close()
    open('another_test_scoreboard.txt', 'w').close()

def teardown_module(module):
    os.remove('test_scoreboard.txt')
    os.remove('another_test_scoreboard.txt')

def test_add_score_for_new_player():
    scoreboard = BoardGameScoreboard('test_scoreboard.txt')
    scoreboard.add_score('Alice', 50)
    assert scoreboard.get_score('Alice') == 50

def test_add_score_for_existing_player():
    scoreboard = BoardGameScoreboard('test_scoreboard.txt')
    scoreboard.add_score('Alice', 25)
    assert scoreboard.get_score('Alice') == 75

def test_get_score_for_nonexistent_player():
    scoreboard = BoardGameScoreboard('test_scoreboard.txt')
    assert scoreboard.get_score('Bob') == 0

def test_persistence_after_save_and_load():
    scoreboard = BoardGameScoreboard('test_scoreboard.txt')
    scoreboard.add_score('Charlie', 30)
    del scoreboard
    new_scoreboard = BoardGameScoreboard('test_scoreboard.txt')
    assert new_scoreboard.get_score('Alice') == 75
    assert new_scoreboard.get_score('Charlie') == 30

def test_different_file():
    scoreboard = BoardGameScoreboard('another_test_scoreboard.txt')
    scoreboard.add_score('Dave', 40)
    assert scoreboard.get_score('Dave') == 40
