import pytest
from solution import calculate_score

def test_calculate_score_basic():
    assert calculate_score(0, [1, 2]) == 30

def test_calculate_score_zero_position():
    assert calculate_score(0, [3, 4]) == 70

def test_calculate_score_single_roll():
    assert calculate_score(10, [6]) == 160

def test_calculate_score_multiple_rolls():
    assert calculate_score(5, [3, 2]) == 100

def test_calculate_score_invalid_roll_raises_exception():
    try:
        calculate_score(5, [3, 7])
        assert False, "Exception not raised"
    except ValueError:
        pass

def test_calculate_score_negative_position_raises_exception():
    try:
        calculate_score(-1, [3, 2])
        assert False, "Exception not raised"
    except ValueError:
        pass

def test_calculate_score_no_rolls():
    assert calculate_score(0, []) == 0