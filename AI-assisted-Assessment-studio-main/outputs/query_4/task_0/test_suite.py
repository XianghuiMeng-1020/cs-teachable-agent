import pytest
from solution import calculate_scores

# Setup Module (Optional, Structure Add-on if needed)
def setup_module(module):
    pass

def teardown_module(module):
    pass

def test_base_case1():
    player_scores = {
        "Alice": [10, -5, 7],
        "Bob": [20, -10, 5],
        "Charlie": [5, 0, -2, 4]
    }
    expected = {
        "Alice": 12,
        "Bob": 15,
        "Charlie": 7
    }
    assert calculate_scores(player_scores) == expected

def test_base_case2():
    player_scores = {
        "Dave": [3, 3, 3],
        "Eva": [-2, 2, -1, 1]
    }
    expected = {
        "Dave": 9,
        "Eva": 0
    }
    assert calculate_scores(player_scores) == expected

def test_mixed_scores():
    player_scores = {
        "Frank": [-1, -2, -3]
    }
    expected = {
        "Frank": -6
    }
    assert calculate_scores(player_scores) == expected

def test_single_player_single_score():
    player_scores = {
        "George": [10]
    }
    expected = {
        "George": 10
    }
    assert calculate_scores(player_scores) == expected

def test_no_scores():
    player_scores = {
        "Helen": []
    }
    expected = {
        "Helen": 0
    }
    assert calculate_scores(player_scores) == expected