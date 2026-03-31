from program import *
import pytest
import os
from winner_selection import select_winner

participants_content = """
Alice 12 34 22 55 17 9
Bob 11 22 33 44 55 66
Charlie 12 34 22 55 17 9
Dave 10 20 30 40 50 60
Eve 11 22 33 44 55 66
"""

single_participant_content = """
Alice 12 34 22 55 17 9
"""

empty_content = """"""

def setup_module(module):
    with open('participants.txt', 'w') as file:
        file.write(participants_content)

    with open('single_participant.txt', 'w') as file:
        file.write(single_participant_content)

    with open('empty.txt', 'w') as file:
        file.write(empty_content)


def teardown_module(module):
    os.remove('participants.txt')
    os.remove('single_participant.txt')
    os.remove('empty.txt')
    if os.path.exists('winner.txt'):
        os.remove('winner.txt')


def test_random_winner_selection():
    select_winner('participants.txt', 'winner.txt')
    assert os.path.exists('winner.txt')
    with open('winner.txt', 'r') as file:
        winner = file.read().strip()
    assert winner in {'Alice', 'Bob', 'Charlie', 'Dave', 'Eve'}


def test_single_participant():
    select_winner('single_participant.txt', 'winner.txt')
    assert os.path.exists('winner.txt')
    with open('winner.txt', 'r') as file:
        winner = file.read().strip()
    assert winner == 'Alice'


def test_no_participants():
    select_winner('empty.txt', 'winner.txt')
    assert os.path.exists('winner.txt')
    with open('winner.txt', 'r') as file:
        winner = file.read().strip()
    assert winner == ''


def test_consistency_with_no_change():
    select_winner('participants.txt', 'winner.txt')
    with open('winner.txt', 'r') as file:
        first_winner = file.read().strip()

    select_winner('participants.txt', 'winner.txt')
    with open('winner.txt', 'r') as file:
        second_winner = file.read().strip()
    # In case of handling state, ensure a reset doesn't cause persistent state
    assert first_winner == second_winner


def test_fresh_run_after_delete():
    select_winner('participants.txt', 'winner.txt')
    os.remove('winner.txt')
    select_winner('participants.txt', 'winner.txt')
    assert os.path.exists('winner.txt')