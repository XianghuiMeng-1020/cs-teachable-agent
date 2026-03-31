from solution_program import *
import pytest
import os
from solution_program import evaluate_lottery_tickets

def setup_module(module):
    with open('input.txt', 'w') as f:
        f.write('123\n456\n579\n632\n')
    with open('input_case2.txt', 'w') as f:
        f.write('111\n222\n333\n444\n')
    with open('input_case3.txt', 'w') as f:
        f.write('777\n888\n999\n513\n666\n')
    with open('input_case4.txt', 'w') as f:
        f.write('080\n143\n379\n632\n000\n')


def teardown_module(module):
    files = ['output.txt', 'input.txt', 'input_case2.txt', 'input_case3.txt', 'input_case4.txt']
    for file in files:
        try:
            os.remove(file)
        except OSError:
            pass


def test_winning_ticket():
    evaluate_lottery_tickets('input.txt', 'output.txt', '632')
    with open('output.txt', 'r') as f:
        result = f.read()
    assert result == 'Tickets evaluated: 4\nWinners: 1\nWinner: 632\n'


def test_no_winners():
    evaluate_lottery_tickets('input_case2.txt', 'output.txt', '800')
    with open('output.txt', 'r') as f:
        result = f.read()
    assert result == 'Tickets evaluated: 4\nNo winners\n'


def test_multiple_winners():
    evaluate_lottery_tickets('input_case3.txt', 'output.txt', '888')
    with open('output.txt', 'r') as f:
        result = f.read()
    assert result == 'Tickets evaluated: 5\nWinners: 1\nWinner: 888\n'


def test_all_same_number_no_winners():
    evaluate_lottery_tickets('input_case4.txt', 'output.txt', '999')
    with open('output.txt', 'r') as f:
        result = f.read()
    assert result == 'Tickets evaluated: 5\nNo winners\n'


def test_non_sequential_winning_number():
    evaluate_lottery_tickets('input.txt', 'output.txt', '579')
    with open('output.txt', 'r') as f:
        result = f.read()
    assert result == 'Tickets evaluated: 4\nWinners: 1\nWinner: 579\n'