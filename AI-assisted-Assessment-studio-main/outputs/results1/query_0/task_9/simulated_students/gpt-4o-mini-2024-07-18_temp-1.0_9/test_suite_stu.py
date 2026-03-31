from solution_program import *
import pytest
import os
from random import seed
from game_of_chance import lucky_draw

def setup_module(module):
    with open('player_choice.txt', 'w') as f:
        f.write('5')

def teardown_module(module):
    os.remove('player_choice.txt')
    if os.path.exists('outcome.txt'):
        os.remove('outcome.txt')

def test_winning_case():
    seed(1)
    lucky_draw()
    with open('outcome.txt', 'r') as f:
        assert f.read().strip() == 'Congratulations! You won! Lucky number: 5'

def test_losing_case_1():
    with open('player_choice.txt', 'w') as f:
        f.write('2')
    seed(2)
    lucky_draw()
    with open('outcome.txt', 'r') as f:
        assert f.read().strip() == 'Sorry! Better luck next time. Chosen number: 2, Generated number: 1'

def test_losing_case_2():
    with open('player_choice.txt', 'w') as f:
        f.write('10')
    seed(3)
    lucky_draw()
    with open('outcome.txt', 'r') as f:
        assert f.read().strip() == 'Sorry! Better luck next time. Chosen number: 10, Generated number: 1'

def test_correct_file_update():
    seed(4)
    lucky_draw()
    with open('player_choice.txt', 'r') as f:
        choice = f.read().strip()
    with open('outcome.txt', 'r') as f:
        outcome = f.read().strip()
    assert choice in outcome

def test_boundaries_handling():
    with open('player_choice.txt', 'w') as f:
        f.write('1')
    seed(5)
    lucky_draw()
    with open('outcome.txt', 'r') as f:
        assert f.read().strip() == 'Sorry! Better luck next time. Chosen number: 1, Generated number: 3'