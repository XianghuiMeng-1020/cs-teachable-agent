from solution_program import *
import pytest
import os
from solution_program import simulate_turn

@pytest.fixture(autouse=True)
def setup_teardown():
    yield
    # No file operations needed for this task

def test_valid_turn():
    board_state = [4, 5, 2, 8, 1]
    assert simulate_turn(board_state, 3) == 11
    assert board_state == [0, 0, 0, 8, 1]

def test_roll_exceeds_board():
    board_state = [1, 1, 1, 1, 1]
    assert simulate_turn(board_state, 6) == 5
    assert board_state == [0, 0, 0, 0, 0]

def test_zeroed_board_state():
    board_state = [0, 0, 0]
    assert simulate_turn(board_state, 2) == 0
    assert board_state == [0, 0, 0]

def test_invalid_roll():
    board_state = [3, 3, 3]
    assert simulate_turn(board_state, 0) == 0
    assert board_state == [3, 3, 3]

def test_invalid_board_state():
    board_state = [3, 'a', 3]
    assert simulate_turn(board_state, 3) == 0
    assert board_state == [3, 'a', 3]
