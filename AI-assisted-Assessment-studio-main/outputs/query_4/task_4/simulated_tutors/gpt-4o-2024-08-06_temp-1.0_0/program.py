def score_board_games(players, games):
    """
    Updates the `players` dictionary in-place to compute the final scores based on the games provided.
    """
    for game in games:
        winner = game.get("winner")
        
        # Only update if there is a valid winner
        if winner in players:
            players[winner] += 10

# Example usage
players = {"Alice": 100, "Bob": 90, "Charlie": 120}
games = [
    {"round": 1, "player1": "Alice", "player2": "Bob", "winner": "Alice"},
    {"round": 2, "player1": "Charlie", "player2": "Alice", "winner": "Alice"},
    {"round": 3, "player1": "Bob", "player2": "Charlie", "winner": "Charlie"}
]
score_board_games(players, games)
print(players)  # Output should be {"Alice": 120, "Bob": 90, "Charlie": 130}