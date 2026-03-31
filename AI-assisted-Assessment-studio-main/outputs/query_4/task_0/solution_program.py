def calculate_scores(player_scores):
    total_scores = {}
    for player, scores in player_scores.items():
        total = 0
        for score in scores:
            total += score
        total_scores[player] = total
    return total_scores