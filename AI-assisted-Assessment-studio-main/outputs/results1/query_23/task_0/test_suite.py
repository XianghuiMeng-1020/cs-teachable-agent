import pytest
from solution import BoardGame

def setup_module(module):
    pass

def teardown_module(module):
    pass

class TestBoardGame:
    def test_add_player_and_get_player_total_score(self):
        game = BoardGame()
        game.add_player("Alice")
        assert game.get_player_total_score("Alice") == 0
        
    def test_record_score_single_player(self):
        game = BoardGame()
        game.add_player("Bob")
        game.record_score("Bob", 10)
        assert game.get_player_total_score("Bob") == 10

    def test_multiple_scores_single_player(self):
        game = BoardGame()
        game.add_player("Charlie")
        game.record_score("Charlie", 5)
        game.record_score("Charlie", 15)
        assert game.get_player_total_score("Charlie") == 20

    def test_get_winner_single_winner(self):
        game = BoardGame()
        game.add_player("Dave")
        game.add_player("Eve")
        game.record_score("Dave", 30)
        game.record_score("Eve", 25)
        assert game.get_winner() == "Dave"

    def test_get_winner_tie(self):
        game = BoardGame()
        game.add_player("Frank")
        game.add_player("Grace")
        game.record_score("Frank", 25)
        game.record_score("Grace", 25)
        assert game.get_winner() == "Frank"