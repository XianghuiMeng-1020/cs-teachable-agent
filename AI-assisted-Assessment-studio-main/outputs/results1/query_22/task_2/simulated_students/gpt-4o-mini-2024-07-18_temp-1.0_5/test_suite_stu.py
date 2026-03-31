from solution_program import *
import os
import pytest
from solution_program import count_games_with_letter

# Creation of a sample games.txt file for testing

def setup_module(module):
    with open('games.txt', 'w') as f:
        f.write("Chess\n")
        f.write("Checkers\n")
        f.write("Catan\n")
        f.write("Battleship\n")
        f.write("Carcassonne\n")
        f.write("Monopoly\n")
        f.write("Dominion\n")
        f.write("Risk\n")
        f.write("Clue\n")
        f.write("Azul\n")

# Removal of the sample games.txt file after testing

def teardown_module(module):
    os.remove('games.txt')


def test_count_games_with_letter_C():
    assert count_games_with_letter('games.txt', 'C') == 4

def test_count_games_with_letter_B():
    assert count_games_with_letter('games.txt', 'B') == 1

def test_count_games_with_letter_M():
    assert count_games_with_letter('games.txt', 'M') == 1

def test_count_games_with_letter_D():
    assert count_games_with_letter('games.txt', 'D') == 1

def test_count_games_with_letter_R():
    assert count_games_with_letter('games.txt', 'R') == 1