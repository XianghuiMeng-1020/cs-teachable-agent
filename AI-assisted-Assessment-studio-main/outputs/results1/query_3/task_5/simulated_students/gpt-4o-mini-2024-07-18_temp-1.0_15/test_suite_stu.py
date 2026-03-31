from solution_program import *
import pytest

from solution_program import balance_predictor

def test_balance_predictor_1():
    probabilities = {
        'A': (50, 2),
        'B': (25, 3),
        'C': (75, 1.5),
        'D': (10, 5)
    }
    assert balance_predictor(['A', 'B', 'D'], 1000, probabilities) == 950

def test_balance_predictor_2():
    probabilities = {
        'A': (60, 2),
        'B': (30, 3),
        'C': (80, 1.5),
        'D': (20, 5)
    }
    assert balance_predictor(['A', 'C', 'D', 'B', 'A'], 1500, probabilities) == 1350

def test_balance_predictor_3():
    probabilities = {
        'A': (55, 1.8),
        'B': (40, 2.5),
        'C': (70, 1.3),
        'D': (15, 4)
    }
    assert balance_predictor(['C', 'B'], 500, probabilities) == 540

def test_balance_predictor_4():
    probabilities = {
        'A': (52, 1.5),
        'B': (26, 3),
        'C': (77, 1.2),
        'D': (12, 6)
    }
    assert balance_predictor(['B', 'D', 'C', 'A'], 800, probabilities) == 715

def test_balance_predictor_5():
    probabilities = {
        'A': (50, 2),
        'B': (25, 3),
        'C': (75, 1.5),
        'D': (10, 5)
    }
    assert balance_predictor(['C', 'A', 'B'], 900, probabilities) == 915
