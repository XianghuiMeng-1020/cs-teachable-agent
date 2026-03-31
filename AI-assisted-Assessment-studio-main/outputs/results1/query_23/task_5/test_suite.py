import pytest

from solution_program import ScoreCard

def test_initial_scores():
    card = ScoreCard(['Alice', 'Bob', 'Charlie'])
    assert card.get_score('Alice') == 0
    assert card.get_score('Bob') == 0
    assert card.get_score('Charlie') == 0

def test_add_score():
    card = ScoreCard(['Alice', 'Bob'])
    card.add_score('Alice', 10)
    assert card.get_score('Alice') == 10
    card.add_score('Bob', 5)
    assert card.get_score('Bob') == 5


def test_nonexistent_player_score():
    card = ScoreCard(['Alice', 'Bob'])
    card.add_score('Charlie', 5)  # Charlie is not in the list
    assert card.get_score('Alice') == 0
    assert card.get_score('Bob') == 0
    assert card.get_score('Charlie') is None


def test_get_winner():
    card = ScoreCard(['Alice', 'Bob', 'Charlie'])
    card.add_score('Alice', 20)
    card.add_score('Bob', 15)
    card.add_score('Charlie', 20)
    assert card.get_winner() == 'Alice'


def test_tie_scenario():
    card = ScoreCard(['Tom', 'Jerry'])
    card.add_score('Tom', 0)
    card.add_score('Jerry', 0)
    assert card.get_winner() == 'Tom'

    card.add_score('Jerry', 5)
    assert card.get_winner() == 'Jerry'

    card.add_score('Tom', 5)
    assert card.get_winner() == 'Jerry'