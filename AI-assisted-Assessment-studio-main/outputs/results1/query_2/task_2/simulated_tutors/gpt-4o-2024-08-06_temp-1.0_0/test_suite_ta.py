from program import *
import pytest
import os
from program import find_winning_tickets

winning_numbers_file_path = 'winning_numbers.txt'

winning_numbers_content = '''
1 2 3 4 5
6 7 8 9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
26 27 28 29 30
31 32 33 34 35
36 37 38 39 40
41 42 43 44 45
46 47 48 49 50
'''

def setup_module(module):
    with open(winning_numbers_file_path, 'w') as f:
        f.write(winning_numbers_content)


def teardown_module(module):
    os.remove(winning_numbers_file_path)


def test_no_matching_tickets():
    user_tickets = ["1 1 1 1 1", "6 6 6 6 6"]
    result = find_winning_tickets(winning_numbers_file_path, user_tickets)
    assert result == []


def test_single_matching_ticket():
    user_tickets = ["11 12 13 14 15", "50 49 48 47 46"]
    result = find_winning_tickets(winning_numbers_file_path, user_tickets)
    assert result == ["11 12 13 14 15"]


def test_multiple_matching_tickets():
    user_tickets = ["1 2 3 4 5", "46 47 48 49 50"]
    result = find_winning_tickets(winning_numbers_file_path, user_tickets)
    assert result == ["1 2 3 4 5", "46 47 48 49 50"]


def test_all_tickets_matching_some():
    user_tickets = ["1 2 3 4 5", "11 12 13 14 15", "41 42 43 44 45"]
    result = find_winning_tickets(winning_numbers_file_path, user_tickets)
    assert result == ["1 2 3 4 5", "11 12 13 14 15"]


def test_empty_user_tickets():
    user_tickets = []
    result = find_winning_tickets(winning_numbers_file_path, user_tickets)
    assert result == []
