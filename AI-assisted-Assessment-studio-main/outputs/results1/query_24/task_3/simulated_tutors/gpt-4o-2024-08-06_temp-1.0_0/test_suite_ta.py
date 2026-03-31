from program import *
import pytest
from program import calculate_board_game_score

def test_calculate_board_game_score_valid_entries():
    results = ["A:4,2", "B:10,5", "A:8,6"]
    expected = {'A': 4, 'B': 5}
    assert calculate_board_game_score(results) == expected


def test_invalid_entries_ignored():
    results = ["A:4,2", "X:3,3:5", "B:10,5", "A:8,6"]
    expected = {'A': 4, 'B': 5}
    assert calculate_board_game_score(results) == expected


def test_invalid_winner():
    results = ["A:4,2", "B:10,5", "1:8,6"]
    expected = {'A': 2, 'B': 5}
    assert calculate_board_game_score(results) == expected


def test_negative_scores():
    results = ["A:4,2", "B:10,5", "A:5,6"]
    expected = {'A': 1, 'B': 5}
    assert calculate_board_game_score(results) == expected


def test_no_results():
    results = []
    expected = {}
    assert calculate_board_game_score(results) == expected


def setup_module(module):
    print("Setup module")

def teardown_module(module):
    print("Teardown module")
