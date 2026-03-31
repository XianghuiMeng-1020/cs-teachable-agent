from solution_program import *
import pytest
import os
from solution_program import BoardGame, BoardGameCollection

def setup_module(module):
    with open('games.txt', 'w') as f:
        f.write('Chess,2,60\n')
        f.write('Monopoly,4,120\n')

def teardown_module(module):
    os.remove('games.txt')

def test_add_game():
    collection = BoardGameCollection([])
    game = BoardGame('Scrabble', 4, 90)
    collection.add_game(game)
    assert len(collection.games) == 1


def test_add_duplicate_game():
    collection = BoardGameCollection([])
    game1 = BoardGame('Chess', 2, 60)
    game2 = BoardGame('Chess', 4, 120)
    collection.add_game(game1)
    collection.add_game(game2)
    assert len(collection.games) == 1


def test_to_file():
    collection = BoardGameCollection([])
    collection.from_file('games.txt')
    collection.to_file('output.txt')
    with open('output.txt', 'r') as f:
        content = f.read().strip()
    os.remove('output.txt')
    assert content == 'Chess,2,60\nMonopoly,4,120'


def test_from_file_with_duplicates():
    collection = BoardGameCollection([])
    with open('games_with_dupes.txt', 'w') as f:
        f.write('Chess,2,60\n')
        f.write('Chess,4,60\n')
        f.write('Monopoly,4,120\n')
    collection.from_file('games_with_dupes.txt')
    os.remove('games_with_dupes.txt')
    assert len(collection.games) == 2


def test_game_to_string():
    game = BoardGame('Risk', 6, 180)
    assert game.to_string() == 'Risk,6,180'