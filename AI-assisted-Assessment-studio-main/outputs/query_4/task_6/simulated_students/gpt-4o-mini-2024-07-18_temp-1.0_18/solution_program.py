def compute_final_scores(moves):
    scores = {}
    for player, positions in moves.items():
        score = 0
        for pos in positions:
            if 1 <= pos <= 5:
                score += 2
            elif 6 <= pos <= 10:
                score += 3
            elif pos > 10:
                score += 5
        scores[player] = score
    return scores