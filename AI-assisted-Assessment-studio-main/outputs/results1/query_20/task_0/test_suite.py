import pytest
from solution import determine_turn_winner

def test_player_1_wins():
    assert determine_turn_winner("Alice", 100, "Bob", 90) == "Alice"

def test_player_2_wins():
    assert determine_turn_winner("Alice", 70, "Bob", 75) == "Bob"

def test_draw():
    assert determine_turn_winner("Alice", 50, "Bob", 50) == "Draw"

def test_zero_scores():
    assert determine_turn_winner("Alice", 0, "Bob", 0) == "Draw"

def test_negative_scores_player_1_wins():
    assert determine_turn_winner("Alice", -10, "Bob", -20) == "Alice"

def test_negative_scores_player_2_wins():
    assert determine_turn_winner("Alice", -30, "Bob", -25) == "Bob"

def test_large_scores():
    assert determine_turn_winner("Alice", 1000000, "Bob", 999999) == "Alice"
