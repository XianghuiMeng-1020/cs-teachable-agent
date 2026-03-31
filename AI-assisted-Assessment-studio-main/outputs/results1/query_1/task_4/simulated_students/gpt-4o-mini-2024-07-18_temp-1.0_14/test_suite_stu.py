from solution_program import *
import pytest
from solution_program import dice_game

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_module():
    yield
    # No file creation involved in this task

def test_basic_case():
    dice_pairs = [(1,6), (5,6), (1,1), (6,5)]
    result = dice_game(4, dice_pairs)
    assert result == [10, 20, 15, 25]

def test_all_neutral():
    dice_pairs = [(3,3), (4,5), (2,4), (1,4)]
    result = dice_game(4, dice_pairs)
    assert result == [0, 0, 0, 0]

def test_all_losses():
    dice_pairs = [(1,1), (1,2), (6,6), (2,1)]
    result = dice_game(4, dice_pairs)
    assert result == [-5, -10, -15, -20]

def test_all_wins():
    dice_pairs = [(6,1), (5,2), (6,5), (4,3)]
    result = dice_game(4, dice_pairs)
    assert result == [10, 20, 30, 40]

def test_mixed_case():
    dice_pairs = [(2,2), (6,1), (1,2), (6,5), (3,3)]
    result = dice_game(5, dice_pairs)
    assert result == [0, 10, 5, 15, 15]