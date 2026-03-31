from solution_program import *
import pytest
import os
from solution_program import analyse_dice_game

def setup_module(module):
    with open('test_input_1.txt', 'w') as f:
        f.write('win\nlose\nwin\ndraw\nwin\nlose\n')
    with open('test_input_2.txt', 'w') as f:
        f.write('draw\n') 
    with open('test_input_3.txt', 'w') as f:
        f.write('lose\nwin\nlose\nwin\n')
    with open('test_input_4.txt', 'w') as f:
        f.write('')  # Empty input file
    with open('test_input_5.txt', 'w') as f:
        f.write('draw\ndraw\ndraw\n')

def teardown_module(module):
    try:
        os.remove('test_input_1.txt')
        os.remove('test_input_2.txt')
        os.remove('test_input_3.txt')
        os.remove('test_input_4.txt')
        os.remove('test_input_5.txt')
        os.remove('test_output_1.txt')
        os.remove('test_output_2.txt')
        os.remove('test_output_3.txt')
        os.remove('test_output_4.txt')
        os.remove('test_output_5.txt')
    except FileNotFoundError:
        pass

@pytest.mark.parametrize("input_file,output_file,expected", [
    ('test_input_1.txt', 'test_output_1.txt', "Wins: 3\nLoses: 2\nDraws: 1\n"),
    ('test_input_2.txt', 'test_output_2.txt', "Wins: 0\nLoses: 0\nDraws: 1\n"),
    ('test_input_3.txt', 'test_output_3.txt', "Wins: 2\nLoses: 2\nDraws: 0\n"),
    ('test_input_4.txt', 'test_output_4.txt', "Wins: 0\nLoses: 0\nDraws: 0\n"),
    ('test_input_5.txt', 'test_output_5.txt', "Wins: 0\nLoses: 0\nDraws: 3\n")
])
def test_analyse_dice_game(input_file, output_file, expected):
    analyse_dice_game(input_file, output_file)
    with open(output_file, 'r') as f:
        result = f.read()
    assert result == expected