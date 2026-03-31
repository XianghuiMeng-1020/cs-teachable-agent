def play_dice_games(games):
    scores = {}
    for player, rolls in games.items():
        if len(rolls) != 3:
            # Set score to -1 if number of dice rolls is not 3
            scores[player] = -1
        else:
            # Sum the valid rolls
            scores[player] = sum(rolls)
    return scores

# Example of how this would work
example_games = {
    'Alice': [3, 5, 2],
    'Bob': [1, 6, 3],
    'Charlie': [4, 4, 4],
    'David': [2, 2]
}

print(play_dice_games(example_games))
# Output should be {'Alice': 10, 'Bob': 10, 'Charlie': 12, 'David': -1}