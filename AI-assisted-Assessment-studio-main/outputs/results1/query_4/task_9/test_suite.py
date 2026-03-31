import pytest
from solution import game_of_chance

def test_game_of_chance_player_wins():
    initial_scores = {'Alice': 2, 'Computer': 1}
    final_scores = game_of_chance(dict(initial_scores))
    assert 'Alice' in final_scores
    assert final_scores['Alice'] > initial_scores['Alice']


def test_game_of_chance_computer_wins():
    initial_scores = {'Bob': 0}
    final_scores = game_of_chance(dict(initial_scores))
    assert 'Computer' in final_scores
    assert final_scores['Computer'] > initial_scores.get('Computer', 0)


def test_game_of_chance_tie():
    initial_scores = {'Tom': 5, 'Computer': 3}
    for _ in range(100):  # Increase chance to detect tie
        trial_scores = game_of_chance(dict(initial_scores))
        if trial_scores == initial_scores:
            assert trial_scores == initial_scores
            return
    assert False, "A tie was never detected"


def test_game_of_chance_no_previous_computer_score():
    initial_scores = {'Carol': 3}
    final_scores = game_of_chance(dict(initial_scores))
    assert 'Computer' in final_scores


def test_game_of_chance_no_previous_scores():
    initial_scores = {}
    final_scores = game_of_chance(dict(initial_scores))
    assert 'Computer' in final_scores or any(
        score > 0 for score in final_scores.values()
    )
