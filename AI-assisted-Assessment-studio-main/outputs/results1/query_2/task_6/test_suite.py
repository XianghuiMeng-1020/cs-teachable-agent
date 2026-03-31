import pytest
import os
from solution import generate_slots, determine_outcome, read_words_from_file, spin_and_check

file_content = """apple
banana
cherry
grape
orange"""

def setup_module(module):
    with open('words.txt', 'w') as file:
        file.write(file_content)

def teardown_module(module):
    os.remove('words.txt')

# Test cases

def test_read_words_from_file():
    result = read_words_from_file('words.txt')
    expected = ['apple', 'banana', 'cherry', 'grape', 'orange']
    assert result == expected

# Since generate_slots gives random outcomes, we focus on testing its results with determine_outcome

def test_determine_outcome_win():
    assert determine_outcome('apple apple apple') == 'WIN'

def test_determine_outcome_lose():
    assert determine_outcome('apple banana apple') == 'LOSE'

def test_spin_and_check_win():
    for _ in range(100):
        result = spin_and_check('words.txt', 1)  # If num_slots is 1, it's always a win
        assert result == 'WIN'

def test_spin_and_check_lose_with_multiple_slots():
    lose = False
    for _ in range(100):
        if spin_and_check('words.txt', 3) == 'LOSE':
            lose = True
            break
    assert lose