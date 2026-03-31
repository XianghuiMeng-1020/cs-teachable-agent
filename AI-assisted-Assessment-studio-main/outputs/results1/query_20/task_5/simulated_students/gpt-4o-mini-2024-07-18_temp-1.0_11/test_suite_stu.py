from solution_program import *
import pytest

from solution_program import calculate_score


def test_player_a_wins():
    assert calculate_score("101010", "010101", "0S0S0S") == "A"

def test_player_b_wins():
    assert calculate_score("010000", "001010", "S0S0S0") == "B"

def test_tie_game():
    assert calculate_score("1100", "1100", "00S0") == "Tie"

def test_no_special_locations():
    assert calculate_score("1111", "0000", "0000") == "Tie"

def test_special_locations_without_settlements():
    assert calculate_score("0000", "0000", "SSSS") == "Tie"
