from program import *
import os
import pytest
from program import Leaderboard

def setup_module(module):
    with open('load_test.txt', 'w') as f:
        f.write('Alice:10\nBob:15\n')
    with open('update_test.txt', 'w') as f:
        f.write('Charlie:20\n')


def teardown_module(module):
    os.remove('load_test.txt')
    os.remove('update_test.txt')
    if os.path.exists('save_test.txt'):
        os.remove('save_test.txt')


def test_add_player():
    leaderboard = Leaderboard()
    leaderboard.add_player('Alice')
    assert leaderboard.get_score('Alice') == 0


def test_update_score_existing_player():
    leaderboard = Leaderboard()
    leaderboard.add_player('Alice')
    leaderboard.update_score('Alice', 20)
    assert leaderboard.get_score('Alice') == 20


def test_get_score_non_existing_player():
    leaderboard = Leaderboard()
    assert leaderboard.get_score('Bob') is None


def test_load_scores():
    leaderboard = Leaderboard()
    leaderboard.load_scores('load_test.txt')
    assert leaderboard.get_score('Alice') == 10
    assert leaderboard.get_score('Bob') == 15


def test_save_scores():
    leaderboard = Leaderboard()
    leaderboard.add_player('Alice')
    leaderboard.add_player('Bob')
    leaderboard.update_score('Alice', 50)
    leaderboard.update_score('Bob', 40)
    leaderboard.save_scores('save_test.txt')
    with open('save_test.txt', 'r') as f:
        content = f.read()
    assert 'Alice:50' in content
    assert 'Bob:40' in content