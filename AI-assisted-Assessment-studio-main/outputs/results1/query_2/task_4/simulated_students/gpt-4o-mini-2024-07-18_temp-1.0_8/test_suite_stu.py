from solution_program import *
import pytest
import os
from solution_program import check_winner


def setup_module(module):
    with open('log.txt', 'w') as f:
        f.write("Alice 7\nBob 15\nAlice 23\nCharlie 5\n")
        f.write("dave 19\nALICE 23\nBob 21\n")


def teardown_module(module):
    os.remove('log.txt')


def test_winner_exists():
    assert check_winner('log.txt', 'Alice', 23) == True


def test_winner_not_exists():
    assert check_winner('log.txt', 'Bob', 7) == False


def test_case_insensitivity():
    assert check_winner('log.txt', 'alice', 23) == True


def test_non_existent_player():
    assert check_winner('log.txt', 'John', 15) == False


def test_multiple_occurrences():
    assert check_winner('log.txt', 'Bob', 15) == True
