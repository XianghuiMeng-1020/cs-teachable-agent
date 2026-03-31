from solution_program import *
import pytest

from solution_program import board_game_feedback


def test_board_game_master():
    assert board_game_feedback(90) == "You're a board game master!"
    assert board_game_feedback(95) == "You're a board game master!"


def test_great_job():
    assert board_game_feedback(75) == "Great job! You're on the way to mastery."
    assert board_game_feedback(80) == "Great job! You're on the way to mastery."


def test_good_effort():
    assert board_game_feedback(50) == "Good effort. Keep practicing!"
    assert board_game_feedback(60) == "Good effort. Keep practicing!"


def test_room_for_improvement():
    assert board_game_feedback(25) == "Not bad, but there's room for improvement."
    assert board_game_feedback(40) == "Not bad, but there's room for improvement."


def test_needs_more_practice():
    assert board_game_feedback(0) == "Needs more practice to improve."
    assert board_game_feedback(20) == "Needs more practice to improve."
