from program import *
import pytest
from program import play_dice_games

def setup_module(module):
    module.test_data_1 = {
        'Alice': [3, 5, 2],
        'Bob': [1, 6, 3],
        'Charlie': [4, 4, 4],
        'David': [2, 2]
    }
    module.test_data_2 = {
        'Eve': [5, 5, 5],
        'Frank': [1, 2, 3],
        'Grace': [6, 6, 6],
        'Heidi': [2, 4, 5, 6]
    }
    module.test_data_3 = {
        'Ivan': [4, 4, 4],
        'Judy': [2],
        'Ken': [3, 3, 3, 1],
        'Leo': [5, 6, 2]
    }
    module.test_data_4 = {
        'Mia': [1, 1, 1],
        'Nina': [0, 5, 6],
        'Oscar': [2, 3]
    }
    module.test_data_5 = {
        'Pat': [3, 3, 3],
        'Quinn': [2, 2, 2],
        'Ralph': [6, 6, 6]
    }

def teardown_module(module):
    del module.test_data_1
    del module.test_data_2
    del module.test_data_3
    del module.test_data_4
    del module.test_data_5

def test_play_dice_games_case_1():
    assert play_dice_games(test_data_1) == {
        'Alice': 10,
        'Bob': 10,
        'Charlie': 12,
        'David': -1
    }

def test_play_dice_games_case_2():
    assert play_dice_games(test_data_2) == {
        'Eve': 15,
        'Frank': 6,
        'Grace': 18,
        'Heidi': -1
    }

def test_play_dice_games_case_3():
    assert play_dice_games(test_data_3) == {
        'Ivan': 12,
        'Judy': -1,
        'Ken': -1,
        'Leo': 13
    }

def test_play_dice_games_case_4():
    assert play_dice_games(test_data_4) == {
        'Mia': 3,
        'Nina': 11,
        'Oscar': -1
    }

def test_play_dice_games_case_5():
    assert play_dice_games(test_data_5) == {
        'Pat': 9,
        'Quinn': 6,
        'Ralph': 18
    }