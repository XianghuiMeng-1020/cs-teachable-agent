import pytest
import os
from solution import GameBoard

def setup_module(module):
    with open('players_input.txt', 'w') as file:
        file.write('Alice\nBob\nCharlie\n')

def teardown_module(module):
    os.remove('players_input.txt')
    if os.path.exists('scores_output.txt'):
        os.remove('scores_output.txt')

def test_total_score_and_winner():
    game = GameBoard('players_input.txt')
    game.add_round_scores('Alice', 10, 20)
    game.add_round_scores('Bob', 15, 15)
    game.add_round_scores('Charlie', 8, 12)
    assert game.get_total_score('Alice') == 30
    assert game.get_total_score('Bob') == 30
    assert game.get_winner() in ['Alice', 'Bob']

def test_non_existent_player():
    game = GameBoard('players_input.txt')
    game.add_round_scores('Dave', 10, 20)
    assert game.get_total_score('Dave') == 0

def test_write_scores_to_file():
    game = GameBoard('players_input.txt')
    game.add_round_scores('Alice', 5, 10)
    game.add_round_scores('Bob', 3, 7)
    game.add_round_scores('Charlie', 2, 8)
    game.write_scores_to_file('scores_output.txt')
    with open('scores_output.txt', 'r') as file:
        lines = file.readlines()
    assert 'Alice: 15\n' in lines
    assert 'Bob: 10\n' in lines
    assert 'Charlie: 10\n' in lines

def test_edge_empty_scores_file():
    game = GameBoard('players_input.txt')
    game.write_scores_to_file('scores_output.txt')
    with open('scores_output.txt', 'r') as file:
        lines = file.readlines()
    assert 'Alice: 0\n' in lines
    assert 'Bob: 0\n' in lines
    assert 'Charlie: 0\n' in lines

def test_tie_handling():
    game = GameBoard('players_input.txt')
    game.add_round_scores('Alice', 10, 10)
    game.add_round_scores('Bob', 20, 0)
    game.add_round_scores('Charlie', 5, 15)
    assert game.get_winner() in ['Alice', 'Bob', 'Charlie']
