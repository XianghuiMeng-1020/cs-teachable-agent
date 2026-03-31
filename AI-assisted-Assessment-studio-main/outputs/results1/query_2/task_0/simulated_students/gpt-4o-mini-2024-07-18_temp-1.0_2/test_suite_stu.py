from solution_program import *
import pytest
import os
from solution_program import get_lucky_winner

def setup_module(module):
    with open('tickets1.txt', 'w') as f:
        f.write('Alice:12345\nBob:67890\nCharlie:24680')
    with open('tickets2.txt', 'w') as f:
        f.write('Anna:12\nEli:3456\nOwen:789')
    with open('tickets3.txt', 'w') as f:
        f.write('Kate:111\nMilo:2222\nToby:33333')

def teardown_module(module):
    os.remove('tickets1.txt')
    os.remove('tickets2.txt')
    os.remove('tickets3.txt')

def test_winner_case1():
    winner = get_lucky_winner('tickets1.txt')
    assert winner == 'Charlie'


def test_winner_case2():
    winner = get_lucky_winner('tickets2.txt')
    assert winner == 'Eli'


def test_winner_case3():
    winner = get_lucky_winner('tickets3.txt')
    assert winner == 'Toby'


def test_winner_single_entry():
    with open('single_ticket.txt', 'w') as f:
        f.write('Solo:5555')
    winner = get_lucky_winner('single_ticket.txt')
    assert winner == 'Solo'
    os.remove('single_ticket.txt')


def test_empty_file():
    with open('empty_tickets.txt', 'w') as f:
        pass
    winner = get_lucky_winner('empty_tickets.txt')
    assert winner is None
    os.remove('empty_tickets.txt')