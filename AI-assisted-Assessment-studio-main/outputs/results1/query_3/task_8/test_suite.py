import pytest
from solution_program import play_game_of_chance


def setup_module(module):
    pass  # No setup required for this test case scenario


def teardown_module(module):
    pass  # No teardown required for this test case scenario


def test_single_roll_per_player():
    result = play_game_of_chance(5, {'Player1': [1], 'Player2': [2]})
    assert result == {'Player1': 1, 'Player2': 2}


def test_multiple_rolls_no_wrap():
    result = play_game_of_chance(10, {'Alice': [3, 4], 'Bob': [2, 3]})
    assert result == {'Alice': 7, 'Bob': 5}
    

def test_wrap_around():
    result = play_game_of_chance(4, {'Charlie': [5, 2], 'Delta': [3, 2, 1]})
    assert result == {'Charlie': 3, 'Delta': 2}


def test_exact_wrap_around():
    result = play_game_of_chance(6, {'Echo': [2, 4], 'Foxtrot': [1, 1, 4]})
    assert result == {'Echo': 0, 'Foxtrot': 0}


def test_large_number_of_rolls():
    result = play_game_of_chance(10, {'Gina': [5, 5, 5, 5], 'Harry': [3, 3, 3, 3]})
    assert result == {'Gina': 0, 'Harry': 2}
