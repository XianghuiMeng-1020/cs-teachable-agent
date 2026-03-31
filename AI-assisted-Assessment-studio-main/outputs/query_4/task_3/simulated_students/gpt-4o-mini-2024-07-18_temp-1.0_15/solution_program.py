def calculate_player_scores(players, scores):
    total_scores = {}
    for player, score_list in zip(players, scores):
        total_scores[player] = sum(score_list)
    return total_scores