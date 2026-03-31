import pytest
from solution_program import game_of_chance

def test_game_of_chance_basic_win_lose():
    assert game_of_chance([10, 20, 15], [4, 3, 6]) == 130

def test_game_of_chance_all_win():
    assert game_of_chance([10, 20, 15], [4, 5, 6]) == 145

def test_game_of_chance_all_lose():
    assert game_of_chance([10, 20, 15], [1, 2, 3]) == 55

def test_game_of_chance_just_enough_balance():
    assert game_of_chance([100, 10, 15], [4, 5, 6]) == 230

def test_game_of_chance_not_enough_balance():
    assert game_of_chance([100, 150, 20], [3, 4, 2]) == 0