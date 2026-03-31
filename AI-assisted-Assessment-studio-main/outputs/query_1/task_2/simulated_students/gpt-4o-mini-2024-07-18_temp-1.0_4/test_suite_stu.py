from solution_program import *
import pytest

# Import the function from the solution program
from solution_program import creature_balance

# Test cases

def test_balanced():
    assert creature_balance([5, 10, 5], [7, 13]) == 'Balanced'

def test_greater_side_a():
    assert creature_balance([10, 20], [5, 5]) == 'Side A'

def test_greater_side_b():
    assert creature_balance([5, 8], [10, 5]) == 'Side A'

def test_greater_side_b_large_values():
    assert creature_balance([12, 15], [25, 3]) == 'Side B'

def test_another_balanced_case():
    assert creature_balance([7, 8], [9, 6]) == 'Balanced'