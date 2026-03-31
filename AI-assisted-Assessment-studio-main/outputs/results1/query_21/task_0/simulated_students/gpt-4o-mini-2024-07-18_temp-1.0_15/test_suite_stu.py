from solution_program import *
import pytest
import os
from solution_program import BoardGameTournament

def setup_module(module):
    with open('test_scores.txt', 'w') as f:
        f.write('Alice: 30\nBob: 45\n')

def teardown_module(module):
    os.remove('test_scores.txt')
    if os.path.exists('output_scores.txt'):
        os.remove('output_scores.txt')

def test_add_participant():
    tournament = BoardGameTournament()
    tournament.add_participant('Charlie')
    assert tournament.get_score('Charlie') == 0


def test_record_score():
    tournament = BoardGameTournament()
    tournament.add_participant('Alice')
    tournament.record_score('Alice', 5)
    assert tournament.get_score('Alice') == 5


def test_get_score_non_existent():
    tournament = BoardGameTournament()
    with pytest.raises(ValueError):
        tournament.get_score('NonExistent')

def test_save_scores():
    tournament = BoardGameTournament()
    tournament.add_participant('Charlie')
    tournament.record_score('Charlie', 10)
    tournament.save_scores('output_scores.txt')
    with open('output_scores.txt', 'r') as f:
        content = f.read()
    assert content.strip() == 'Charlie: 10'


def test_load_scores():
    tournament = BoardGameTournament()
    tournament.load_scores('test_scores.txt')
    assert tournament.get_score('Alice') == 30
    assert tournament.get_score('Bob') == 45