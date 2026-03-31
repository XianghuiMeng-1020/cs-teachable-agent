from program import *
import pytest
import os
from program import lucky_draw_game

import random
random.seed(0)  # Set seed for reproducibility in random number generation

def test_lucky_draw_single_round_win():
    assert lucky_draw_game([1]) == 10

def test_lucky_draw_single_round_lose():
    assert lucky_draw_game([2]) == 0

def test_lucky_draw_multiple_rounds_mixed():
    assert lucky_draw_game([1, 3, 5, 1, 4]) == 30

def test_lucky_draw_multiple_rounds_all_lose():
    assert lucky_draw_game([3, 3, 3, 3, 3]) == 0

def test_lucky_draw_multiple_rounds_all_win():
    assert lucky_draw_game([4, 4, 4, 4]) == 40
