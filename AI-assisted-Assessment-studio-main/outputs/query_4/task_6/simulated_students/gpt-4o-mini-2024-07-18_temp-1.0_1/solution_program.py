def compute_final_scores(moves):
    scores = {}
    for player, positions in moves.items():
        total_score = 0
        for position in positions:
            if position >= 1 and position <= 5:
                total_score += 2
            elif position >= 6 and position <= 10:
                total_score += 3
            elif position > 10:
                total_score += 5
        scores[player] = total_score
    return scores