def calculate_final_scores(game_log):
    final_scores = {}
    for player, points in game_log.items():
        score = 0
        for change in points:
            score += change
            if score < 0:
                score = 0
        final_scores[player] = score
    return final_scores