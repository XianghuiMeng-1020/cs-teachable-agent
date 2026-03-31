import pytest
from solution import lucky_dice

def test_all_7s_and_11s():
    outcomes = [(3, 4), (5, 6), (6, 1), (2, 5)]  # sums: 7, 11, 7, 7
    result = lucky_dice(outcomes)
    assert result['total_score'] == 40
    assert result['rolls'] == [10, 10, 10, 10]

def test_all_not_scoring():
    outcomes = [(1, 1), (2, 2), (3, 4), (3, 5)]  # sums: 2, 4, 7, 8
    result = lucky_dice(outcomes)
    assert result['total_score'] == 15
    assert result['rolls'] == [5, 0, 10, 0]

def test_all_lows():
    outcomes = [(1, 1), (1, 2), (6, 6)]  # sums: 2, 3, 12
    result = lucky_dice(outcomes)
    assert result['total_score'] == 15
    assert result['rolls'] == [5, 5, 5]

def test_mixed_scores():
    outcomes = [(1, 6), (2, 3), (5, 5)]  # sums: 7, 5, 10
    result = lucky_dice(outcomes)
    assert result['total_score'] == 10
    assert result['rolls'] == [10, 0, 0]

def test_empty_outcomes():
    outcomes = []
    result = lucky_dice(outcomes)
    assert result['total_score'] == 0
    assert result['rolls'] == []
