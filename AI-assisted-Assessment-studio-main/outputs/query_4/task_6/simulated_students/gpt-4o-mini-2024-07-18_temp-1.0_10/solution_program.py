def compute_final_scores(moves):
    scores = {}
    for player, positions in moves.items():
        total_score = 0
        for pos in positions:
            if 1 <= pos <= 5:
                total_score += 2
            elif 6 <= pos <= 10:
                total_score += 3
            elif pos > 10:
                total_score += 5
        scores[player] = total_score
    return scores