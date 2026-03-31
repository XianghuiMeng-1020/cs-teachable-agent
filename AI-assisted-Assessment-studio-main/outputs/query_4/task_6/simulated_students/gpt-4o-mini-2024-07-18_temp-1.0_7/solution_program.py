def compute_final_scores(moves):
    scores = {}
    for player, positions in moves.items():
        score = 0
        for position in positions:
            if 1 <= position <= 5:
                score += 2
            elif 6 <= position <= 10:
                score += 3
            elif position > 10:
                score += 5
        scores[player] = score
    return scores