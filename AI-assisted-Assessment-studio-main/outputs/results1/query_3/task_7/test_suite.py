import pytest

from solution import simulate_lottery


def test_all_losses():
    player_numbers = [1, 2, 3, 4, 5, 6]
    rounds = {
        1: [7, 8, 9, 10, 11, 12],
        2: [13, 14, 15, 16, 17, 18]
    }
    assert simulate_lottery(player_numbers, rounds) == 0


def test_all_wins():
    player_numbers = [10, 20, 30, 40, 50, 1]
    rounds = {
        1: [10, 20, 30, 40, 50, 1],
        2: [10, 20, 30, 40, 50, 1]
    }
    assert simulate_lottery(player_numbers, rounds) == 2


def test_some_wins():
    player_numbers = [3, 6, 23, 45, 19, 21]
    rounds = {
        1: [3, 6, 24, 44, 19, 21],
        2: [1, 2, 23, 45, 19, 21],
        3: [3, 6, 23, 45, 19, 21]  # All matches
    }
    assert simulate_lottery(player_numbers, rounds) == 2


def test_invalid_player_numbers():
    player_numbers = [3, 6, 23, 45, 19, 50] # Invalid player numbers (number out of range)
    rounds = {
        1: [3, 6, 25, 45, 20, 22],
        2: [1, 2, 23, 45, 19, 21]
    }
    assert simulate_lottery(player_numbers, rounds) == 0


def test_invalid_round_numbers():
    player_numbers = [3, 6, 23, 45, 19, 21]
    rounds = {
        1: [3, 6, 23, 49, 45, 21],
        2: [1, 2, 50, 45, 19, 21] # Invalid round numbers (number out of range)
    }
    assert simulate_lottery(player_numbers, rounds) == 0