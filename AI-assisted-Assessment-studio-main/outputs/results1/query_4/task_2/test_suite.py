import pytest
from solution import play_dice_game

def test_reach_minimum_target():
    assert play_dice_game(1) == 1

def test_exact_roll_few_turns():
    actual = play_dice_game(6)
    assert actual == 1

def test_target_with_many_rolls():
    actual = play_dice_game(20)
    assert actual >= 4

def test_large_target_exact_case():
    actual = play_dice_game(30)
    assert actual >= 5  # Should be 5 if player always rolls 6

def test_nontrivial_case():
    actual = play_dice_game(15)
    assert actual >= 3  # Minimum of 3 rolls of 6 each
