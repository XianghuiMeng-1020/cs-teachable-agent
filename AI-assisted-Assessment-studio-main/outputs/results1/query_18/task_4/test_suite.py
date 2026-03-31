import pytest
import os
from solution_program import calculate_power

# Setting up and tearing down test files

def setup_module(module):
    with open('energy1.txt', 'w') as f:
        f.write('20,30,-10,5')

    with open('energy2.txt', 'w') as f:
        f.write('-100,-50,-150')

    with open('energy3.txt', 'w') as f:
        f.write('50,50,50,50,50')

    with open('energy4.txt', 'w') as f:
        f.write('0')

    with open('energy5.txt', 'w') as f:
        f.write('')

def teardown_module(module):
    os.remove('energy1.txt')
    os.remove('energy2.txt')
    os.remove('energy3.txt')
    os.remove('energy4.txt')
    os.remove('energy5.txt')

# Test cases

def test_calculate_power_with_positive_changes():
    result = calculate_power('energy1.txt')
    assert result == 1045  # 1000 + 20 + 30 - 10 + 5

def test_calculate_power_with_negative_changes():
    result = calculate_power('energy2.txt')
    assert result == 700  # 1000 - 100 - 50 - 150

def test_calculate_power_with_consistent_positive_changes():
    result = calculate_power('energy3.txt')
    assert result == 1250  # 1000 + 50 + 50 + 50 + 50 + 50

def test_calculate_power_with_zero_changes():
    result = calculate_power('energy4.txt')
    assert result == 1000  # 1000 + 0

# Edge Case: Test with No Changes

def test_calculate_power_with_no_changes():
    result = calculate_power('energy5.txt')
    assert result == 1000  # 1000 + 0 (no change)
