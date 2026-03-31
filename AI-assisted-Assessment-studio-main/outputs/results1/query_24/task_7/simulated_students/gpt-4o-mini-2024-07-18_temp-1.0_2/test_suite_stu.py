from solution_program import *
import pytest

def test_calculate_score_valid_cases():
    from solution_program import calculate_score
    assert calculate_score(['1', '3', 'skip', '5', '4']) == 13
    assert calculate_score(['2', 'skip', 'skip', '6', '4']) == 12
    assert calculate_score(['1', '2', '3', '4', '5', '6']) == 21


def test_calculate_score_with_invalid_moves():
    from solution_program import calculate_score
    assert calculate_score(['0', '3', '7', 'skip', '4']) == 7
    assert calculate_score(['2', 'bob', 'skip', '6', 'x']) == 8


def test_calculate_score_empty_list():
    from solution_program import calculate_score
    assert calculate_score([]) == 0


def test_calculate_score_all_skips():
    from solution_program import calculate_score
    assert calculate_score(['skip', 'skip', 'skip']) == 0


def test_calculate_score_mixed_invalid_and_valid():
    from solution_program import calculate_score
    assert calculate_score(['1', 'skip', '3', 'text', '4', '12']) == 8
