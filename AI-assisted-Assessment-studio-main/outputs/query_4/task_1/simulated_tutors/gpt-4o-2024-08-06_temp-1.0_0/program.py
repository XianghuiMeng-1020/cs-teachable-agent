def update_leaderboard(rounds):
    # Dictionary to maintain the cumulative scores of each player
    leaderboard = {}
    
    # Accumulate scores over all rounds
    for round in rounds:
        for player, score in round.items():
            if player in leaderboard:
                leaderboard[player] += score
            else:
                leaderboard[player] = score
                
    # Sort the leaderboard by score in descending order, alphabetically for ties
    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda x: (-x[1], x[0])))
    return sorted_leaderboard

# Sample input for testing
rounds = [
    {'Alice': 10, 'Bob': 15, 'Charlie': 5},
    {'Alice': 20, 'Bob': 10, 'Charlie': 15},
    {'Alice': 5, 'Bob': 25, 'Charlie': 10}
]

# Testing the function
print(update_leaderboard(rounds))