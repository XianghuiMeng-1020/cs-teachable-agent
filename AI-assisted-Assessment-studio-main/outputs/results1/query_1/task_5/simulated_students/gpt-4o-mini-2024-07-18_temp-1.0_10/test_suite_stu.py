from solution_program import *
import pytest

from solution_program import high_or_low_game

def test_high_or_low_game():
    assert high_or_low_game([3, 8, 4], ["high", "low"]) == 2
    assert high_or_low_game([5, 1, 9, 3], ["low", "high", "low"]) == 3
    assert high_or_low_game([7, 6, 5], ["low", "low"]) == 0
    assert high_or_low_game([1, 2, 3, 4, 5], ["high", "high", "high", "high"]) == 4
    assert high_or_low_game([9, 5, 3, 7], ["low", "low", "high"]) == 1