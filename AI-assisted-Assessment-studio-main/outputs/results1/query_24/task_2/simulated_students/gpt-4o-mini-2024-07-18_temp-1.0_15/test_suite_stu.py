from solution_program import *
import pytest
import os
from solution_program import calculate_winner_score

filename = "test_file.txt"


def setup_module(module):
    with open(filename, 'w') as f:
        f.write("Alice 20\nBob 35\nAlice 30\nCharlie 25\nBob 40\n")

def teardown_module(module):
    os.remove(filename)


def test_calculate_winner_score_base_case():
    assert calculate_winner_score(filename) == ('Bob', 75)


def test_calculate_winner_score_different_file():
    with open('temp_test_file.txt', 'w') as f:
        f.write("Dana 10\nEva 15\nDana 20\nEva 15\n")
    assert calculate_winner_score('temp_test_file.txt') in [('Dana', 30), ('Eva', 30)]
    os.remove('temp_test_file.txt')


def test_calculate_winner_score_single_entry():
    with open('temp_test_file.txt', 'w') as f:
        f.write("Frank 40\n")
    assert calculate_winner_score('temp_test_file.txt') == ('Frank', 40)
    os.remove('temp_test_file.txt')


def test_calculate_winner_score_file_not_found():
    assert calculate_winner_score('non_existent_file.txt') == None


def test_calculate_winner_score_invalid_data():
    with open('bad_data_file.txt', 'w') as f:
        f.write("Invalid Data\nMore Bad Data\n")
    assert calculate_winner_score('bad_data_file.txt') == None
    os.remove('bad_data_file.txt')