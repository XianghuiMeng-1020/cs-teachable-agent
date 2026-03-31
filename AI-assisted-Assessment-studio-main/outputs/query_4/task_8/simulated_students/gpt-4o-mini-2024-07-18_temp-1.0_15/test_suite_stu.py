from solution_program import *
import pytest

from solution_program import calculate_final_scores

# Test cases
def test_case_1():
    result = calculate_final_scores({'Alice': [10, -5, 20, -30, 5], 'Bob': [-10, 20, 15, -5, 10]})
    assert result == {'Alice': 5, 'Bob': 30}

def test_case_2():
    result = calculate_final_scores({'Max': [0, -50, 50, 20], 'John': [-20, 30, -10, 0, 50]})
    assert result == {'Max': 20, 'John': 50}

def test_case_3():
    result = calculate_final_scores({'Charlie': [5, 5, 5, -15, 10], 'David': [5, -5, 5, -5]})
    assert result == {'Charlie': 10, 'David': 0}

def test_case_4():
    result = calculate_final_scores({'Eve': [-10, -20, 40, -10, 10], 'Frank': [30, -10, 5]})
    assert result == {'Eve': 20, 'Frank': 25}

def test_case_5():
    result = calculate_final_scores({'Tom': [100, -50, -30, 10, -20], 'Jerry': [25, -25, 25, -25]})
    assert result == {'Tom': 10, 'Jerry': 0}