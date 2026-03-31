import pytest
import os
from solution import BoardGame

@pytest.fixture(autouse=True)
def setup_class():
    BoardGame.games = []

@pytest.mark.parametrize("title, min_players, max_players", [
    ("Chess", 2, 2), 
    ("Monopoly", 2, 6), 
    ("Pandemic", 2, 4), 
    ("Codenames", 2, 8)
])
def test_add_game(title, min_players, max_players):
    BoardGame.add_game(title, min_players, max_players)
    assert any(game.title == title for game in BoardGame.games)

@pytest.mark.parametrize("num, expected_titles", [
    (2, ["Chess", "Monopoly", "Pandemic", "Codenames"]),
    (3, ["Monopoly", "Pandemic", "Codenames"]),
    (4, ["Monopoly", "Pandemic", "Codenames"]),
    (6, ["Monopoly", "Codenames"]),
    (8, ["Codenames"])
])
def test_games_with_min_players(num, expected_titles):
    BoardGame.add_game("Chess", 2, 2)
    BoardGame.add_game("Monopoly", 2, 6)
    BoardGame.add_game("Pandemic", 2, 4)
    BoardGame.add_game("Codenames", 2, 8)
    assert BoardGame.games_with_min_players(num) == expected_titles

@pytest.mark.parametrize("num, expected_titles", [
    (2, ["Chess", "Monopoly", "Pandemic"]),
    (4, ["Chess", "Monopoly", "Pandemic"]),
    (5, ["Chess", "Monopoly", "Pandemic"]),
    (6, ["Chess", "Monopoly"]),
    (8, ["Chess", "Monopoly", "Codenames"])
])
def test_games_with_max_players(num, expected_titles):
    BoardGame.add_game("Chess", 2, 2)
    BoardGame.add_game("Monopoly", 2, 6)
    BoardGame.add_game("Pandemic", 2, 4)
    BoardGame.add_game("Codenames", 2, 8)
    assert BoardGame.games_with_max_players(num) == expected_titles