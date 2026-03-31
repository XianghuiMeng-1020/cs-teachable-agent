import pytest

def test_find_winner():
    from solution import find_winner
    
    # Case where Player 1 wins
    result = find_winner('3 5', '4 2')
    assert result == 'Player 1 Wins'
    
    # Case where Player 2 wins
    result = find_winner('2 2', '5 1')
    assert result == 'Player 2 Wins'
    
    # Case where both scores draw
    result = find_winner('6 3', '5 4')
    assert result == 'Draw'
    
    # Case with minimum scores
    result = find_winner('1 1', '1 1')
    assert result == 'Draw'
    
    # Case with maximum possible, Player 1 win
    result = find_winner('6 6', '6 5')
    assert result == 'Player 1 Wins'