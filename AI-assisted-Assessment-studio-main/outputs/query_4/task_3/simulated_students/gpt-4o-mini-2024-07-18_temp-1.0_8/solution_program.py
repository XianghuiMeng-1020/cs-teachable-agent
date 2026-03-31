def calculate_player_scores(players, scores):
    total_scores = {}
    for player, player_scores in zip(players, scores):
        total_scores[player] = sum(player_scores)
    return total_scores