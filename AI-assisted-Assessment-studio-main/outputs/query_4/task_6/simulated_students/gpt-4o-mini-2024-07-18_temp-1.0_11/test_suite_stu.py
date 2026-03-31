from solution_program import *
import pytest
from solution_program import compute_final_scores


def test_single_player():
    result = compute_final_scores({"Alice": [1, 2, 3, 4]})
    assert result == {"Alice": 8}


def test_multiple_players():
    players = {
        "Alice": [2, 6, 8, 10, 11],
        "Bob": [5, 6, 10, 11],
        "Charlie": [1, 3, 9, 15]
    }
    result = compute_final_scores(players)
    assert result == {"Alice": 15, "Bob": 13, "Charlie": 15}


def test_empty_path():
    result = compute_final_scores({"Alice": []})
    assert result == {"Alice": 0}


def test_no_players():
    result = compute_final_scores({})
    assert result == {}


def test_varied_paths():
    players = {
        "Alice": [5, 5, 5],
        "Bob": [0, 11, 12],
        "Charlie": [4, 7, 13]
    }
    result = compute_final_scores(players)
    assert result == {"Alice": 6, "Bob": 10, "Charlie": 10}