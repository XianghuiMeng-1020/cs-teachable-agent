import pytest
import os
from solution_program import log_scores, top_score

FILENAME = 'test_game_scores.txt'


def setup_module(module):
    with open(FILENAME, 'w') as f:
        f.write('')


def teardown_module(module):
    if os.path.exists(FILENAME):
        os.remove(FILENAME)


def test_single_high_score():
    log_scores(FILENAME, ['Alice', 'Bob', 'Charlie'], [10, 15, 20])
    result = top_score(FILENAME)
    assert result == ['Charlie']


def test_multiple_high_scores():
    log_scores(FILENAME, ['Dan', 'Eve', 'Frank'], [20, 20, 5])
    result = top_score(FILENAME)
    assert result == ['Dan', 'Eve']


def test_tie_scores_same_order():
    log_scores(FILENAME, ['George', 'Hannah', 'Ian'], [20, 20, 20])
    result = top_score(FILENAME)
    assert result == ['George', 'Hannah', 'Ian']


def test_no_score():
    log_scores(FILENAME, [], [])
    result = top_score(FILENAME)
    assert result == []


def test_all_unique_scores():
    log_scores(FILENAME, ['Jack', 'Karen'], [8, 20])
    result = top_score(FILENAME)
    assert result == ['Karen']
