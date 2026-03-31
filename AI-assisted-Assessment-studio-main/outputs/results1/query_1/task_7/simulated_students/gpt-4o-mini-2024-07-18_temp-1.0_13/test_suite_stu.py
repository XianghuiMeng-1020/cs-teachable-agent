from solution_program import *
import pytest

from solution_program import lucky_draw

def test_lucky_draw_base_case():
    assert lucky_draw([1, 2, 3, 4, 5, 6, 7, 8, 9], 3) == True

def test_lucky_draw_case_not_in_first_five():
    assert lucky_draw([1, 2, 3, 4, 5, 6, 7, 8, 9], 8) == False

def test_lucky_draw_insufficient_cards():
    assert lucky_draw([1, 2, 3], 2) == False

def test_lucky_draw_exactly_five_cards():
    assert lucky_draw([10, 20, 30, 40, 50], 50) == True

def test_lucky_draw_no_match():
    assert lucky_draw([11, 12, 13, 14, 15], 9) == False