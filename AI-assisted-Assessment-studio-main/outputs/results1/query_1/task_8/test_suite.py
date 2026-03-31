import pytest
from solution import predict_winnings

@pytest.mark.parametrize("numbers, bet_amounts, expected", [
    ([32], [10], 360),
    ([5, 32, 10], [10, 20, 5], 720),
    ([1, 3, 5, 7, 9, 32], [5, 5, 5, 5, 5, 5], 180),
    ([8, 15, 32, 16], [50, 50, 50, 50], 1800),
    ([0, 1, 6, 10], [0, 0, 0, 0], 0)
])
def test_predict_winnings(numbers, bet_amounts, expected):
    assert predict_winnings(numbers, bet_amounts) == expected

@pytest.mark.parametrize("numbers, bet_amounts, expected", [
    ([32, 32], [10, 20], 360),  # Tests edge case with 32 appearing twice
    ([2], [45], 0),  # Tests case with no winning number
    ([32], [0], 0),  # Tests case with zero bet amount
    ([7, 12, 25, 13], [15, 20, 30, 50], 0),  # No win
    ([32, 10, 25, 19], [1, 2, 3, 4], 36)   # Win with lowest bet amount
])
def test_edge_cases(numbers, bet_amounts, expected):
    assert predict_winnings(numbers, bet_amounts) == expected
