from solution_program import *
import pytest
import os
from solution_program import simulate_game

def setup_module(module):
    pass

def teardown_module(module):
    pass

# Test cases

def test_correct_bet_win():
    probabilities = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                     6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Assumption: simulate_game is expected to simulate the draw
    assert simulate_game(5, 10, probabilities) in {20, -10}


def test_incorrect_bet_loss():
    probabilities = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                     6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Assumption: simulate_game is expected to simulate the draw
    assert simulate_game(11, 20, probabilities) == -20


def test_edge_case_min_bet():
    probabilities = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                     6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Testing with the minimum bet number 1
    assert simulate_game(1, 1, probabilities) in {2, -1}


def test_invalid_bet_number():
    probabilities = {1: 0.2, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                     6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Betting on a number not in the game
    assert simulate_game(11, 5, probabilities) == -5


def test_all_numbers_equal_probability():
    probabilities = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                     6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Simulating a random draw when all numbers have equal chances
    assert simulate_game(10, 100, probabilities) in {200, -100}