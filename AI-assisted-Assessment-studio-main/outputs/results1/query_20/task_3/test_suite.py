import pytest

from solution_program import determine_winner

def test_all_draws():
    assert determine_winner("123", "321") == "Draw"
    
def test_alice_wins():
    assert determine_winner("456", "123") == "Alice"
    
def test_bob_wins():
    assert determine_winner("123", "456") == "Bob"
    
def test_empty_rolls():
    assert determine_winner("", "") == "Draw"
    
def test_large_numbers():
    assert determine_winner("666", "555") == "Alice"