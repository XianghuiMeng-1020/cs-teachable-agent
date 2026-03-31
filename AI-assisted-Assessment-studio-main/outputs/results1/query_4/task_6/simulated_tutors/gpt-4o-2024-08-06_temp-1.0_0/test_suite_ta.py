from program import *
import pytest
import os
from program import roulette_game

@pytest.mark.parametrize("money, bets, expected", [
    (100, {"even": 50, "odd": 50}, 100), # Even odds: player neither loses nor gains
    (100, {"even": 50}, 150),             # Wins the even bet
    (100, {"odd": 50}, 50),               # Loses the odd bet
    (50, {"even": 50}, 100),              # Wins full even bet
    (75, {"even": 25, "odd": 50}, 75),  # Loses odd, wins even bet
    (200, {"odd": 200}, 0),               # Loses on odd, loses all
    (10, {}, 10),                          # No bets, no change
    (30, {"even": 20, "odd": 10}, 40)   # Wins even, loses odd
])
def test_roulette_game(money, bets, expected):
    result = roulette_game(money, bets)
    assert result == expected
