from solution_program import *
import pytest
import os
from solution_program import play_game_of_chance

file_content = """
5
7
3
9
1
2
4
5
8
9
""".strip()


def setup_module(module):
    with open('file_game.txt', 'w') as f:
        f.write(file_content)


def teardown_module(module):
    os.remove('file_game.txt')


def test_single_match():
    assert play_game_of_chance('file_game.txt', 50, 5) == 50


def test_multiple_match():
    assert play_game_of_chance('file_game.txt', 100, 9) == 190


def test_no_match():
    assert play_game_of_chance('file_game.txt', 50, 11) == -50


def test_no_match_larger_bet():
    assert play_game_of_chance('file_game.txt', 200, 11) == -200


def test_all_entries_different_than_guess():
    assert play_game_of_chance('file_game.txt', 100, 6) == -100
