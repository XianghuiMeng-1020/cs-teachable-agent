from program import *
import pytest
import os
from program import check_winner

PARTICIPANTS_FILE = 'test_participants.txt'
WINNER_FILE = 'test_winner.txt'


def setup_module(module):
    with open(PARTICIPANTS_FILE, 'w') as f:
        f.write("A1234\nB5678\nC9012\n")
    with open('test_participants_2.txt', 'w') as f:
        f.write("A1234\nC9012\nE3456\n")
    with open('test_participants_3.txt', 'w') as f:
        f.write("X1234\nY5678\nZ9012\n")
    with open(WINNER_FILE, 'w') as f:
        f.write("B5678")
    with open('test_winner_2.txt', 'w') as f:
        f.write("E3456")
    with open('test_winner_3.txt', 'w') as f:
        f.write("Z9012")


def teardown_module(module):
    os.remove(PARTICIPANTS_FILE)
    os.remove('test_participants_2.txt')
    os.remove('test_participants_3.txt')
    os.remove(WINNER_FILE)
    os.remove('test_winner_2.txt')
    os.remove('test_winner_3.txt')


def test_valid_winner():
    assert check_winner(PARTICIPANTS_FILE, WINNER_FILE) == True

def test_invalid_winner():
    assert check_winner('test_participants_2.txt', WINNER_FILE) == False

def test_different_winner_from_participants_2():
    assert check_winner('test_participants_2.txt', 'test_winner_2.txt') == True

def test_different_files_no_winner():
    assert check_winner(PARTICIPANTS_FILE, 'test_winner_2.txt') == False

def test_different_file_sets_valid_winner():
    assert check_winner('test_participants_3.txt', 'test_winner_3.txt') == True
