from solution_program import *
import pytest
from solution_program import dice_game


def test_reach_target_exactly():
    assert dice_game(10, [3, 3, 4]) == 'WIN'


def test_exceed_target_with_extra_rolls():
    assert dice_game(15, [4, 5, 6, 1]) == 'WIN'


def test_barely_exceed_target():
    assert dice_game(7, [1, 2, 1, 3]) == 'WIN'


def test_no_reaching_target():
    assert dice_game(12, [1, 2, 3]) == 'LOSE'


def test_single_roll_exact_target():
    assert dice_game(4, [4]) == 'WIN'
