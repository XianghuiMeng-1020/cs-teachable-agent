from solution_program import *
import pytest
from solution_program import calculate_prize

def test_all_dice_same():
    assert calculate_prize(4, 4, 4) == 40
    assert calculate_prize(6, 6, 6) == 60

def test_two_dice_same():
    assert calculate_prize(3, 3, 2) == 15
    assert calculate_prize(5, 3, 5) == 25
    assert calculate_prize(1, 2, 1) == 5

def test_all_dice_different():
    assert calculate_prize(1, 2, 3) == 6
    assert calculate_prize(2, 4, 5) == 11
    assert calculate_prize(4, 5, 6) == 15

def test_edge_case_min_max_rolls():
    assert calculate_prize(1, 1, 1) == 10
    assert calculate_prize(6, 5, 6) == 30
    assert calculate_prize(1, 6, 5) == 12