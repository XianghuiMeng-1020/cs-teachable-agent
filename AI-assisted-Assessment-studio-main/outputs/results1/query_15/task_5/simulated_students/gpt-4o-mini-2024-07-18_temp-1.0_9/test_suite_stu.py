from solution_program import *
import pytest
from solution_program import calculate_crystal_weights

def test_calculate_crystal_weights_normal_case():
    assert calculate_crystal_weights([4, 9, 6, 3, 10, 15, 2]) == (22, 27)

def test_calculate_crystal_weights_all_glimmer():
    assert calculate_crystal_weights([2, 4, 6]) == (12, 0)

def test_calculate_crystal_weights_all_shadow():
    assert calculate_crystal_weights([1, 3, 5, 7]) == (0, 16)

def test_calculate_crystal_weights_empty_list():
    assert calculate_crystal_weights([]) == (0, 0)

def test_calculate_crystal_weights_mixed_case():
    assert calculate_crystal_weights([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == (20, 25)
