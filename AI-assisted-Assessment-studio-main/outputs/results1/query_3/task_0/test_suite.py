import pytest
from solution import calculate_winnings

@pytest.mark.parametrize("bets, roll, expected", [
    ({1: 10, 2: 20, 3: 0, 4: 15, 5: 5, 6: 0}, 3, -50),
    ({1: 0, 2: 0, 3: 20, 4: 0, 5: 0, 6: 0}, 3, 60),
    ({1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10}, 6, -40),
    ({1: 0, 2: 0, 3: 0, 4: 0, 5: 100, 6: 0}, 5, 300),
    ({1: 100, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100}, 1, -400)
])
def test_calculate_winnings(bets, roll, expected):
    assert calculate_winnings(bets, roll) == expected