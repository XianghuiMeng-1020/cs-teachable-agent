from solution_program import *
import pytest
import os
from solution_program import luckiest_player

DATA = '''\
Alice 100\nBob 50\nAlice 200\nCharlie 300\nBob 150\n'''

DATA_TIE = '''\
Alice 200\nBob 200\nCharlie 200\nDave 200\n'''  # All should result in Alice

DATA_ONE_PLAYER = '''\
Single 700\n'''

DATA_WITH_NEGATIVE = '''\
Alice -100\nBob 50\nAlice 300\nBob -50\n'''  # Result should be Alice

DATA_SUBTLE_TIE = '''\
Alice 0\nBob 0\nAlice 0\nBob 0\nCharlie 0\n'''  # Result should be Alice


def setup_module(module):
    with open('daily_wins.txt', 'w') as f:
        f.write(DATA)

    with open('daily_wins_tie.txt', 'w') as f:
        f.write(DATA_TIE)

    with open('daily_wins_one_player.txt', 'w') as f:
        f.write(DATA_ONE_PLAYER)

    with open('daily_wins_negative.txt', 'w') as f:
        f.write(DATA_WITH_NEGATIVE)

    with open('daily_wins_subtle_tie.txt', 'w') as f:
        f.write(DATA_SUBTLE_TIE)


def teardown_module(module):
    os.remove('daily_wins.txt')
    os.remove('daily_wins_tie.txt')
    os.remove('daily_wins_one_player.txt')
    os.remove('daily_wins_negative.txt')
    os.remove('daily_wins_subtle_tie.txt')


def test_luckiest_player_normal():
    assert luckiest_player('daily_wins.txt') == 'Alice'


def test_luckiest_player_tie():
    assert luckiest_player('daily_wins_tie.txt') == 'Alice'


def test_luckiest_player_one_player():
    assert luckiest_player('daily_wins_one_player.txt') == 'Single'


def test_with_negative_winnings():
    assert luckiest_player('daily_wins_negative.txt') == 'Alice'


def test_subtle_tie():
    assert luckiest_player('daily_wins_subtle_tie.txt') == 'Alice'
