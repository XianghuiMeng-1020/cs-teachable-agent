from solution_program import *
import pytest

from solution_program import dice_game

def test_dice_game_win_conditions():
    assert dice_game([(3, 4), (5, 6)]) == ['Win', 'Win']


def test_dice_game_lose_conditions():
    assert dice_game([(1, 1), (1, 2), (6, 6)]) == ['Lose', 'Lose', 'Lose']


def test_dice_game_neutral_conditions():
    assert dice_game([(2, 2), (3, 4), (4, 5)]) == ['Neutral', 'Win', 'Win']


def test_dice_game_mixed_conditions():
    assert dice_game([(3, 3), (2, 2), (5, 6), (1, 3)]) == ['Neutral', 'Neutral', 'Win', 'Neutral']


def test_dice_game_edge_case_empty_list():
    assert dice_game([]) == []
