def calculate_board_game_score(game_results):
    scores = {}
    
    for result in game_results:
        try:
            winner, scores_str = result.split(':')
            score1, score2 = map(int, scores_str.split(','))
            if winner not in scores:
                scores[winner] = 0
            scores[winner] += (score1 - score2)
        except (ValueError, IndexError):
            continue
    
    return scores