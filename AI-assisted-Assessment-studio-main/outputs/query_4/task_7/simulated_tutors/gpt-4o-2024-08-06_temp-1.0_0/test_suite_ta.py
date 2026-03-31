from program import *
import pytest

def test_track_wins():
    from program import track_wins
    
    games1 = []
    assert track_wins(games1) == {}
    
    games2 = [('chess', 'Alice')]
    assert track_wins(games2) == {'Alice': {'chess': 1}}
    
    games3 = [
        ('chess', 'Alice'), ('checkers', 'Bob'), ('chess', 'Alice'),
        ('monopoly', 'Bob'), ('checkers', 'Alice')
    ]
    assert track_wins(games3) == {
        'Alice': {'chess': 2, 'checkers': 1},
        'Bob': {'checkers': 1, 'monopoly': 1}
    }

    games4 = [
        ('poker', 'Charlie'), ('poker', 'Charlie'),
        ('monopoly', 'Charlie')
    ]
    assert track_wins(games4) == {
        'Charlie': {'poker': 2, 'monopoly': 1}
    }

    games5 = [
        ('chess', 'David'), ('checkers', 'David'),
        ('checkers', 'David'), ('monopoly', 'David'),
        ('chess', 'Eve'), ('poker', 'Eve')
    ]
    assert track_wins(games5) == {
        'David': {'chess': 1, 'checkers': 2, 'monopoly': 1},
        'Eve': {'chess': 1, 'poker': 1}
    }
