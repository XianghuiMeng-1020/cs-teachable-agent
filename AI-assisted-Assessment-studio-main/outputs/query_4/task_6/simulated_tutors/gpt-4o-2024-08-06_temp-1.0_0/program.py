def compute_final_scores(moves):
    scores = {}
    for player, path in moves.items():
        total_score = 0
        for position in path:
            if 1 <= position <= 5:
                total_score += 2
            elif 6 <= position <= 10:
                total_score += 3
            elif position > 10:
                total_score += 5
        scores[player] = total_score
    return scores

# This implementation uses variables (scores, total_score, player, path, position),
# arithmetic operators (+, +=, <=, and >), selection statements (if/else),
# loops (for), and dictionaries (input moves and output scores).