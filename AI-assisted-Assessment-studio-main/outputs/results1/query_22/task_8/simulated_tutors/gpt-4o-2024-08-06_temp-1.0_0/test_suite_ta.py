from program import *
import pytest
import os
from program import record_scores, get_scores

def setup_module(module):
    # Create the temporary file with initial data
    with open('test_scores.txt', 'w') as f:
        f.write("Round 1: 10 20 15\n")

    with open('test_empty.txt', 'w') as f:
        f.write("")

def teardown_module(module):
    # Remove the temporary files after tests
    os.remove('test_scores.txt')
    os.remove('test_empty.txt')


def test_initial_file_content():
    record_scores('test_scores.txt', [[30, 40, 25]])
    with open('test_scores.txt', 'r') as f:
        content = f.readlines()
    assert content == ['Round 1: 10 20 15\n', 'Round 2: 30 40 25\n']


def test_append_score_to_existing_file():
    record_scores('test_scores.txt', [[50, 60, 70]])
    with open('test_scores.txt', 'r') as f:
        content = f.readlines()
    assert content == ['Round 1: 10 20 15\n', 'Round 2: 30 40 25\n', 'Round 3: 50 60 70\n']


def test_get_scores():
    expected_scores = ['Round 1: 10 20 15', 'Round 2: 30 40 25', 'Round 3: 50 60 70']
    scores = get_scores('test_scores.txt')
    assert scores == expected_scores


def test_append_to_empty_file():
    record_scores('test_empty.txt', [[10, 20, 30]])
    with open('test_empty.txt', 'r') as f:
        content = f.readlines()
    assert content == ['Round 1: 10 20 30\n']


def test_get_scores_empty_file():
    scores = get_scores('test_empty.txt')
    assert scores == ['Round 1: 10 20 30']
