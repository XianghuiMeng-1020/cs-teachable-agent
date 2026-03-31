from program import *
import os
import pytest
from program import ScrabbleScoreCalculator

def setup_module(module):
    """ Setup test environment, if needed, create files."""
    pass


def teardown_module(module):
    """ Remove any files if created."""
    pass


def test_all_lowercase_word():
    calculator = ScrabbleScoreCalculator()
    assert calculator.calculate_score("hello") == 8


def test_mixed_case_word():
    calculator = ScrabbleScoreCalculator()
    assert calculator.calculate_score("SuPerB") == 10


def test_word_with_non_alpha_characters():
    calculator = ScrabbleScoreCalculator()
    assert calculator.calculate_score("Hello, World!") == 17


def test_empty_string():
    calculator = ScrabbleScoreCalculator()
    assert calculator.calculate_score("") == 0


def test_word_with_same_letter_different_cases():
    calculator = ScrabbleScoreCalculator()
    assert calculator.calculate_score("appleApple") == 18
