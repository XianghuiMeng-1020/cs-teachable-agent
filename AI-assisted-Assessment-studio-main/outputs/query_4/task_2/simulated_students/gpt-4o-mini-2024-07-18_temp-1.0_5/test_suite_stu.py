from solution_program import *
import pytest

from solution_program import register_and_rank

def test_chess_game():
    players = {
        'Alice': {'game': 'Chess', 'score': 200},
        'Bob': {'game': 'Scrabble', 'score': 300},
        'Cathy': {'game': 'Chess', 'score': 250},
        'David': {'game': 'Monopoly', 'score': 150},
    }
    result = register_and_rank(players)
    assert result['Chess'] == ('Cathy', ['Cathy', 'Alice'])

def test_scrabble_game():
    players = {
        'Alice': {'game': 'Chess', 'score': 100},
        'Bob': {'game': 'Scrabble', 'score': 300},
        'Cathy': {'game': 'Scrabble', 'score': 350},
        'David': {'game': 'Monopoly', 'score': 400},
    }
    result = register_and_rank(players)
    assert result['Scrabble'] == ('Cathy', ['Cathy', 'Bob'])

def test_monopoly_game():
    players = {
        'Alice': {'game': 'Chess', 'score': 100},
        'Bob': {'game': 'Scrabble', 'score': 200},
        'Mike': {'game': 'Monopoly', 'score': 250},
        'David': {'game': 'Monopoly', 'score': 400},
    }
    result = register_and_rank(players)
    assert result['Monopoly'] == ('David', ['David', 'Mike'])

def test_single_player_leaderboard():
    players = {
        'Alice': {'game': 'Chess', 'score': 150},
    }
    result = register_and_rank(players)
    assert result['Chess'] == ('Alice', ['Alice'])

def test_multiple_games_single_leader():
    players = {
        'Alice': {'game': 'Chess', 'score': 300},
        'Bob': {'game': 'Scrabble', 'score': 300},
    }
    result = register_and_rank(players)
    assert result['Chess'] == ('Alice', ['Alice'])
    assert result['Scrabble'] == ('Bob', ['Bob'])