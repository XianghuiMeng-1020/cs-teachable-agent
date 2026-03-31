import pytest
from solution_program import BoardGame

@pytest.fixture
def setup_board_game():
    return BoardGame()

@pytest.mark.parametrize("actions, expected", [
    (["add", "Alice", "get"], "Alice"),
    (["add", "Alice", "add", "Bob", "get"], "Alice, Bob"),
    (["add", "Alice", "add", "Bob", "remove", "Alice", "get"], "Bob"),
    (["add", "Alice", "add", "Bob", "remove", "alice", "get"], "Bob"),
    (["add", "Charlie", "remove", "Alice", "get"], "Charlie"),
    (["add", "Alice", "add", "Alice", "get"], "Alice"),
    (["get"], "No players"),
    (["remove", "Alice", "get"], "No players"),
    (["add", "Ana", "add", "ANA", "get"], "Ana"),
    (["add", "Bob", "add", "Bob", "remove", "Bob", "get"], "No players")
])
def test_board_game(actions, expected, setup_board_game):
    game = setup_board_game
    for i in range(0, len(actions), 2):
        action = actions[i]
        if action == "add":
            game.add_player(actions[i + 1])
        elif action == "remove":
            game.remove_player(actions[i + 1])
        elif action == "get":
            result = game.get_players()
            assert result == expected