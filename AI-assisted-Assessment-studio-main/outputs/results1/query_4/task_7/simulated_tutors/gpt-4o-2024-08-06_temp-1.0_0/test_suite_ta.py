from program import *
import pytest


def test_dice_probability_lowest_score():
    from program import dice_probability
    assert dice_probability(2) == 0.0278

def test_dice_probability_highest_score():
    from program import dice_probability
    assert dice_probability(12) == 0.0278

def test_dice_probability_most_common_score():
    from program import dice_probability
    assert dice_probability(7) == 0.1667

def test_dice_probability_out_of_bounds_low():
    from program import dice_probability
    assert dice_probability(1) == 0

def test_dice_probability_out_of_bounds_high():
    from program import dice_probability
    assert dice_probability(13) == 0

def test_dice_probability_less_common_score():
    from program import dice_probability
    assert dice_probability(4) == 0.1111
