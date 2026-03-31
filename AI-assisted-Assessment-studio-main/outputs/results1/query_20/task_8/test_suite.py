import pytest

from solution import check_game_winner

def test_player_one_wins():
    assert check_game_winner(10, 5) == "Player One wins!"

def test_player_two_wins():
    assert check_game_winner(4, 7) == "Player Two wins!"

def test_tie():
    assert check_game_winner(8, 8) == "It's a tie!"

def test_another_player_one_wins():
    assert check_game_winner(15, 14) == "Player One wins!"

def test_player_two_wins_large_score():
    assert check_game_winner(100, 101) == "Player Two wins!"
