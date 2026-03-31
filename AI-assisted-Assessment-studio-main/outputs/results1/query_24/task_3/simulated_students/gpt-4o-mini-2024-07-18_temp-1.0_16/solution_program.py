def calculate_board_game_score(game_results):
    scores = {}
    
    for result in game_results:
        parts = result.split(':')
        if len(parts) != 2:
            continue
        winner, scores_part = parts
        if len(winner) != 1 or not winner.isupper():
            continue
        scores_values = scores_part.split(',')
        if len(scores_values) != 2:
            continue
        try:
            score1 = int(scores_values[0])
            score2 = int(scores_values[1])
        except ValueError:
            continue
        
        score_diff = score1 - score2
        if winner not in scores:
            scores[winner] = 0
        scores[winner] += score_diff
    
    return scores