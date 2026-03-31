import pytest
from solution_program import dice_game_of_chance

def test_valid_win_case_1():
    result = dice_game_of_chance({'bet_on': '7', 'amount': 100})
    expected = {'result': 'win', 'final_amount': 200}
    assert result == expected


def test_valid_lose_case_1():
    result = dice_game_of_chance({'bet_on': '5', 'amount': 50})
    expected = {'result': 'lose', 'final_amount': 0}
    assert result == expected


def test_valid_win_case_2():
    result = dice_game_of_chance({'bet_on': '9', 'amount': 100})
    expected = {'result': 'win', 'final_amount': 200}
    assert result == expected


def test_invalid_bet_amount():
    result = dice_game_of_chance({'bet_on': '7', 'amount': -50})
    expected = {'error': 'Invalid bet amount'}
    assert result == expected


def test_invalid_bet_on_value():
    result = dice_game_of_chance({'bet_on': 'abc', 'amount': 100})
    expected = {'error': 'Invalid bet choice'}
    assert result == expected