def calculate_board_game_score(game_results):
    scores = {}
    
    for result in game_results:
        try:
            winner, score_str = result.split(':')
            score1, score2 = map(int, score_str.split(','))
            score_diff = score1 - score2
            
            if winner in scores:
                scores[winner] += score_diff
            else:
                scores[winner] = score_diff
        except (ValueError, IndexError):
            continue
    
    return scores