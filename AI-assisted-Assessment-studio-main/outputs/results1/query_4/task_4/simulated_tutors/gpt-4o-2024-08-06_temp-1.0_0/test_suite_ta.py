from program import *
import pytest
from program import lucky_number_game

def test_positive_ending_rolls():
    rolls = lucky_number_game()
    assert isinstance(rolls, int)
    assert rolls > 0

def test_multiple_runs_consistency():
    roll_counts = [lucky_number_game() for _ in range(10)]
    assert all(isinstance(count, int) and count > 0 for count in roll_counts)

def test_low_roll_count_eventually():
    # Expect a positive score usually within a reasonable range
    assert any(lucky_number_game() < 10 for _ in range(20))

@pytest.mark.parametrize('iteration', range(5))
def test_higher_number_of_trials(iteration):
    assert lucky_number_game() > 0

@pytest.mark.parametrize('iteration', range(5))
def test_game_completes(iteration):
    score_sum = 0
    score_map = {1: 0, 2: 10, 3: -5, 4: 5, 5: 20, 6: -10}
    rolls = 0
    while score_sum <= 0:
        rolls += 1
        score_sum += score_map[iteration % 6 + 1]
    assert rolls == lucky_number_game()