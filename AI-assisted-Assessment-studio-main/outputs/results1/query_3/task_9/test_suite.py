import pytest
from roulette import calculate_payout

def test_single_number_bet_wins():
    bets = [
        {"player": "Alice", "bet_type": "number", "amount": 10}
    ]
    winning_number = 7
    result = calculate_payout(bets, winning_number)
    assert result == {"Alice": 0}


def test_single_even_bet_wins():
    bets = [
        {"player": "Bob", "bet_type": "even", "amount": 15}
    ]
    winning_number = 2
    result = calculate_payout(bets, winning_number)
    assert result == {"Bob": 30}


def test_single_odd_bet_wins():
    bets = [
        {"player": "Charlie", "bet_type": "odd", "amount": 20}
    ]
    winning_number = 3
    result = calculate_payout(bets, winning_number)
    assert result == {"Charlie": 40}


def test_multiple_bets_mixed_outcome():
    bets = [
        {"player": "Alice", "bet_type": "number", "amount": 10},
        {"player": "Bob", "bet_type": "even", "amount": 15},
        {"player": "Charlie", "bet_type": "odd", "amount": 5}
    ]
    winning_number = 2
    result = calculate_payout(bets, winning_number)
    assert result == {"Alice": 0, "Bob": 30, "Charlie": 0}


def test_multiple_bets_winning_number():
    bets = [
        {"player": "Alice", "bet_type": "number", "amount": 5},
        {"player": "Bob", "bet_type": "number", "amount": 20},
        {"player": "Charlie", "bet_type": "number", "amount": 15}
    ]
    winning_number = 29
    result = calculate_payout(bets, winning_number)
    assert result == {"Alice": 0, "Bob": 700, "Charlie": 525}