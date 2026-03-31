def calculate_scores(player_scores):
    total_scores = {}
    for player, scores in player_scores.items():
        total_scores[player] = sum(scores)
    return total_scores

# Example usage
player_scores = {
    "Alice": [10, -5, 7],
    "Bob": [20, -10, 5],
    "Charlie": [5, 0, -2, 4]
}

print(calculate_scores(player_scores))