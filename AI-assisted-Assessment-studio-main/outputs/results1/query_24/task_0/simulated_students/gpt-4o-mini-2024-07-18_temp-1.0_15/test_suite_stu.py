from solution_program import *
import pytest
from solution_program import board_game_summary

class InvalidFormatError(Exception):
    pass

def test_board_game_summary_valid_input():
    assert board_game_summary("A12B4A3B10C1") == {'A': 15, 'B': 14, 'C': 1}


def test_board_game_summary_single_player():
    assert board_game_summary("Z50") == {'Z': 50}


def test_board_game_summary_multiple_awards_per_player():
    assert board_game_summary("D2D3D5") == {'D': 10}


def test_board_game_summary_invalid_input_non_numeric():
    try:
        board_game_summary("E3F2GZ")
    except ValueError as e:
        assert str(e) == "Invalid format in results string"


def test_board_game_summary_invalid_input_empty_string():
    try:
        board_game_summary("")
    except ValueError as e:
        assert str(e) == "Invalid format in results string"