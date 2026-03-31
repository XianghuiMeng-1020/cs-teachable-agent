def calculate_scores(player_scores):
    total_scores = {}
    for player, scores in player_scores.items():
        total_scores[player] = sum(scores)
    return total_scores