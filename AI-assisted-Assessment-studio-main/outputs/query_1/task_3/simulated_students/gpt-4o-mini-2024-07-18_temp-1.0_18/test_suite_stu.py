from solution_program import *
import pytest
from solution_program import calculate_awards

def test_calculate_awards_base_cases():
    # Test with each tier
    assert calculate_awards([0]) == ['Novice']
    assert calculate_awards([3]) == ['Adept']
    assert calculate_awards([8]) == ['Veteran']
    assert calculate_awards([15]) == ['Elite']

def test_calculate_awards_mixed_tiers():
    # Mixed tiers
    assert calculate_awards([0, 2, 6, 11]) == ['Novice', 'Adept', 'Veteran', 'Elite']
    
def test_calculate_awards_alternating_values():
    # Alternating values
    assert calculate_awards([5, 10, 11, 0, 1]) == ['Adept', 'Veteran', 'Elite', 'Novice', 'Adept']

def test_calculate_awards_multiple_mixed_tiers():
    # Common multiple mixed tiers
    assert calculate_awards([1, 5, 0, 7, 12, 9, 4]) == ['Adept', 'Adept', 'Novice', 'Veteran', 'Elite', 'Veteran', 'Adept']

def test_calculate_awards_empty():
    # Test empty list
    assert calculate_awards([]) == []