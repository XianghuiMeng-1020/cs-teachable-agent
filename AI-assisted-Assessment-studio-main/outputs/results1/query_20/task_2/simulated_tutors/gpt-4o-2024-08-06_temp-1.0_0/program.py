def chess_game_outcome(score_player1, score_player2, player1_name, player2_name):
    if score_player1 > score_player2:
        return f"{player1_name} is victorious!"
    elif score_player2 > score_player1:
        return f"{player2_name} is victorious!"
    else:
        return "The game is a draw!"

# Test the function with the provided test cases
import pytest

@pytest.mark.parametrize("score_player1, score_player2, player1_name, player2_name, expected", [
    (3, 2, "Alice", "Bob", "Alice is victorious!"),
    (1, 4, "Carlos", "Diana", "Diana is victorious!"),
    (5, 5, "Eve", "Frank", "The game is a draw!"),
    (0, 0, "George", "Helen", "The game is a draw!"),
    (10, 9, "Ian", "Judy", "Ian is victorious!")
])
def test_chess_game_outcome(score_player1, score_player2, player1_name, player2_name, expected):
    assert chess_game_outcome(score_player1, score_player2, player1_name, player2_name) == expected

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    print("Setup for module executed.")
    
@pytest.fixture(scope="module", autouse=True)
def teardown_module():
    print("Teardown for module executed.")