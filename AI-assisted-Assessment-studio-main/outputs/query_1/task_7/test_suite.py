import pytest
from solution import maximize_favor

def test_example_case():
    challenges = [(3, 2), (5, 4), (7, 6), (1, 1)]
    assert maximize_favor(challenges) == 8

def test_no_challenges():
    challenges = []
    assert maximize_favor(challenges) == 0


def test_single_challenge_under_limit():
    challenges = [(4, 3)]
    assert maximize_favor(challenges) == 4

def test_single_challenge_over_limit():
    challenges = [(5, 11)]
    assert maximize_favor(challenges) == 0

def test_multiple_combinations():
    challenges = [(8, 9), (3, 1), (3, 2), (4, 5), (6, 4)]
    assert maximize_favor(challenges) == 11
