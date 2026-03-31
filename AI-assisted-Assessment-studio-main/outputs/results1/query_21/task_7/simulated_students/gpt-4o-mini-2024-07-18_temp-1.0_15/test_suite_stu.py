from solution_program import *
import pytest
import os
from solution_program import BoardGame, save_board_games, load_board_games


def setup_module(module):
    games_data = [
        "Chess,2,2\n",
        "Monopoly,2,6\n",
        "Pandemic,2,4\n",
        "Catan,3,4\n"
    ]
    with open('board_games.txt', 'w') as f:
        f.writelines(games_data)


def teardown_module(module):
    if os.path.exists('board_games.txt'):
        os.remove('board_games.txt')


def test_board_game_str_method():
    game = BoardGame("Chess", 2, 2)
    assert str(game) == "Chess (2:2 players)"


def test_load_board_games():
    games = load_board_games()
    assert len(games) == 4
    assert str(games[0]) == "Chess (2:2 players)"
    assert str(games[1]) == "Monopoly (2:6 players)"


def test_save_board_games():
    new_games = [
        BoardGame("Risk", 2, 6),
        BoardGame("Scrabble", 2, 4)
    ]
    save_board_games(new_games)
    with open('board_games.txt') as f:
        lines = f.readlines()
    assert lines[0].strip() == "Risk,2,6"
    assert lines[1].strip() == "Scrabble,2,4"


def test_save_and_load_board_games():
    new_games = [
        BoardGame("Ticket to Ride", 2, 5),
        BoardGame("Azul", 2, 4)
    ]
    save_board_games(new_games)
    loaded_games = load_board_games()
    assert len(loaded_games) == 2
    assert str(loaded_games[0]) == "Ticket to Ride (2:5 players)"
    assert str(loaded_games[1]) == "Azul (2:4 players)"


def test_file_not_found_exception_handling():
    os.remove('board_games.txt')
    games = load_board_games()
    assert games == []