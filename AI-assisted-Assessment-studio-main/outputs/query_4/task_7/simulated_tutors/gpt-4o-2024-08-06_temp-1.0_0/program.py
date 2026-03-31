def track_wins(games):
    # Initialize the main dictionary to track players and their victories
    victory_tracker = {}
    
    # Iterate over each game in the list of games
    for game_name, winner_name in games:
        # If the winner is not already in the tracker, add them
        if winner_name not in victory_tracker:
            victory_tracker[winner_name] = {}
        # If the game is not already in the player's dictionary, add it
        if game_name not in victory_tracker[winner_name]:
            victory_tracker[winner_name][game_name] = 0
        # Increment the number of wins for the current game
        victory_tracker[winner_name][game_name] += 1
    
    return victory_tracker

# Test cases to check the implementation
if __name__ == "__main__":
    # Run the provided tests within the script for manual verification
    assert track_wins([]) == {}
    assert track_wins([('chess', 'Alice')]) == {'Alice': {'chess': 1}}
    assert track_wins([
        ('chess', 'Alice'), ('checkers', 'Bob'), ('chess', 'Alice'),
        ('monopoly', 'Bob'), ('checkers', 'Alice')
    ]) == {
        'Alice': {'chess': 2, 'checkers': 1},
        'Bob': {'checkers': 1, 'monopoly': 1}
    }
    assert track_wins([
        ('poker', 'Charlie'), ('poker', 'Charlie'),
        ('monopoly', 'Charlie')
    ]) == {
        'Charlie': {'poker': 2, 'monopoly': 1}
    }
    assert track_wins([
        ('chess', 'David'), ('checkers', 'David'),
        ('checkers', 'David'), ('monopoly', 'David'),
        ('chess', 'Eve'), ('poker', 'Eve')
    ]) == {
        'David': {'chess': 1, 'checkers': 2, 'monopoly': 1},
        'Eve': {'chess': 1, 'poker': 1}
    }