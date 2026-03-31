from program import *
import pytest

from program import find_winner


def test_player_a_wins():
    result = find_winner(300, 150)
    assert result == "Player A wins"

def test_player_b_wins():
    result = find_winner(100, 300)
    assert result == "Player B wins"

def test_tie_score():
    result = find_winner(200, 200)
    assert result == "Tie"

def test_negative_score_a_wins():
    result = find_winner(-50, -100)
    assert result == "Player A wins"

def test_negative_score_b_wins():
    result = find_winner(-100, -50)
    assert result == "Player B wins"
