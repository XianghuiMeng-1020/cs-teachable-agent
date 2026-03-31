import pytest
import random
from my_module import play_roulette

random.seed(0)  # For consistent testing

@pytest.mark.parametrize("starting_amount, rounds, bets, expected", [
    (100, 5, [('red', 10), ('black', 20), ('red', 30), ('black', 40), ('red', 50)], {'remaining_amount': 30, 'played_rounds': 5}),
    (50, 4, [('red', 5), ('black', 5), ('red', 5), ('black', 5)], {'remaining_amount': 90, 'played_rounds': 4}),
    (20, 6, [('black', 10), ('red', 10), ('black', 5)], {'remaining_amount': 5, 'played_rounds': 3}),
    (10, 3, [('red', 5), ('black', 3), ('red', 3)], {'remaining_amount': 5, 'played_rounds': 3}),
    (200, 2, [('black', 50), ('red', 50)], {'remaining_amount': 100, 'played_rounds': 2})
])
def test_play_roulette(starting_amount, rounds, bets, expected):
    result = play_roulette(starting_amount, rounds, bets)
    assert result == expected
