from solution_program import *
import pytest

def test_calculate_dish_time():
    from solution_program import calculate_dish_time

    # Test with all valid integer strings
    assert calculate_dish_time(['30', '45', '20', 5, 10]) == 110
    
    # Test with a mix of valid and invalid strings
    assert calculate_dish_time(['60', 'abc', '90', 'def']) == 150

    # Test with all invalid entries
    assert calculate_dish_time(['xyz', [], {}, None, '']) == 0

    # Test with some valid and some invalid entries
    assert calculate_dish_time([80, '40mins', '100', False, [10]]) == 180

    # Test with an empty list
    assert calculate_dish_time([]) == 0
