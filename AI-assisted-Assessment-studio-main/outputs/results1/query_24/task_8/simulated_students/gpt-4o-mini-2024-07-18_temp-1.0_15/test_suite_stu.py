from solution_program import *
import pytest

from solution_program import update_leaderboard

def test_update_leaderboard_basic():
    entries = [
        "Alice,10",
        "Bob,15",
        "Alice,5",
        "Charlie,20"
    ]
    result = update_leaderboard(entries)
    assert result == {"Alice": 15, "Bob": 15, "Charlie": 20}

def test_update_leaderboard_with_malformed_entries():
    entries = [
        "Alice,10",
        "Bob,15",
        "Alice-5",
        "Charlie,20a",
        "David,30"
    ]
    result = update_leaderboard(entries)
    assert result == {"Alice": 10, "Bob": 15, "David": 30}

def test_update_leaderboard_empty_entries():
    entries = []
    result = update_leaderboard(entries)
    assert result == {}

def test_update_leaderboard_no_valid_scores():
    entries = [
        "Alice-Ten",
        "Bob-Fifteen",
        "AliceFifteen",
        "Charlie:Twenty"
    ]
    result = update_leaderboard(entries)
    assert result == {}

def test_update_leaderboard_large_numbers():
    entries = [
        "Alice,1000000",
        "Bob,-5000",
        "Alice,2000000",
        "Charlie,0"
    ]
    result = update_leaderboard(entries)
    assert result == {"Alice": 3000000, "Bob": -5000, "Charlie": 0}