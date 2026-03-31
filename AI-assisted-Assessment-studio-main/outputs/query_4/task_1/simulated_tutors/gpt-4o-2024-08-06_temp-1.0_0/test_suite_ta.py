from program import *
import pytest
from program import update_leaderboard

# Test case 1: Basic input with three rounds
@pytest.mark.parametrize("rounds, expected", [
    ([{'Alice': 10, 'Bob': 15, 'Charlie': 5}, {'Alice': 20, 'Bob': 10, 'Charlie': 15}, {'Alice': 5, 'Bob': 25, 'Charlie': 10}], {'Bob': 50, 'Alice': 35, 'Charlie': 30}),

    # Test case 2: All players score the same
    ([{'Alice': 10, 'Bob': 10, 'Charlie': 10}, {'Alice': 10, 'Bob': 10, 'Charlie': 10}], {'Alice': 20, 'Bob': 20, 'Charlie': 20}),

    # Test case 3: A single player dominates
    ([{'Alice': 30, 'Bob': 0, 'Charlie': 0}, {'Alice': 20, 'Bob': 0, 'Charlie': 0}], {'Alice': 50, 'Bob': 0, 'Charlie': 0}),

    # Test case 4: Two players tie and should sort alphabetically by name
    ([{'Alice': 10, 'Bob': 10, 'Charlie': 0}, {'Alice': 0, 'Bob': 0, 'Charlie': 0}], {'Alice': 10, 'Bob': 10, 'Charlie': 0}),

    # Test case 5: Incremental increase for all players each round
    ([{'Alice': 1, 'Bob': 1, 'Charlie': 1}, {'Alice': 2, 'Bob': 2, 'Charlie': 2}], {'Alice': 3, 'Bob': 3, 'Charlie': 3})
])
def test_update_leaderboard(rounds, expected):
    assert update_leaderboard(rounds) == expected