from solution_program import *
import pytest
from solution_program import best_fruits

@pytest.mark.parametrize("apples, min_value, expected", [
    ([5, 10, 25, 20], 15, 45),  # Normal case with values greater than 15
    ([50, 100, 75, 80], 60, 180), # Normal case with multiple high values
    ([1, 3, 5, 7], 9, 0),        # Case with no values greater than 9
    ([20, 30, 10, 40], 30, 70),   # Case with exactly two values greater than 30
    ([10, 15, 20, 25, 5], 24, 25) # Case with single value above threshold
])
def test_best_fruits(apples, min_value, expected):
    assert best_fruits(apples, min_value) == expected