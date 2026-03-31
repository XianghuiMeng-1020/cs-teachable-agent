def calculate_final_scores(game_log):
    final_scores = {}
    for player, points in game_log.items():
        score = 0
        for point_change in points:
            score += point_change
            if score < 0:
                score = 0
        final_scores[player] = score
    return final_scores