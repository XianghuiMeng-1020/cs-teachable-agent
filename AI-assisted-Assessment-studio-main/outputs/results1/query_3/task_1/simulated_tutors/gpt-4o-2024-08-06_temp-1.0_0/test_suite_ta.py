from program import *
import pytest
from program import lottery_game

def test_exact_match():
    entries = {
        'John': 15,
        'Doe': 15,
    }
    winning_number = 15
    result = lottery_game(entries, winning_number)
    assert result == {
        'John': 'Jackpot',
        'Doe': 'Jackpot'
    }

def test_one_off_match():
    entries = {
        'Emily': 7,
        'Sarah': 9
    }
    winning_number = 8
    result = lottery_game(entries, winning_number)
    assert result == {
        'Emily': 'Half-Pot',
        'Sarah': 'Half-Pot'
    }

def test_two_off_match():
    entries = {
        'Anna': 10,
        'Steve': 14
    }
    winning_number = 12
    result = lottery_game(entries, winning_number)
    assert result == {
        'Anna': 'Quarter-Pot',
        'Steve': 'Quarter-Pot'
    }

def test_no_winnings():
    entries = {
        'Paul': 32,
        'Charles': 7,
    }
    winning_number = 10
    result = lottery_game(entries, winning_number)
    assert result == {
        'Paul': 'No Winnings',
        'Charles': 'No Winnings'
    }

def test_mixture_of_cases():
    entries = {
        'Luke': 5,
        'Leia': 6,
        'Han': 7,
        'Chewie': 10
    }
    winning_number = 7
    result = lottery_game(entries, winning_number)
    assert result == {
        'Luke': 'Quarter-Pot',
        'Leia': 'Half-Pot',
        'Han': 'Jackpot',
        'Chewie': 'No Winnings'
    }
