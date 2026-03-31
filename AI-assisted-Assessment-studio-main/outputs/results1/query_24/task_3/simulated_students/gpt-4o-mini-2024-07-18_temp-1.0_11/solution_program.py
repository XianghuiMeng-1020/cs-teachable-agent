def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        try:
            winner, scores_part = result.split(':')
            score1, score2 = map(int, scores_part.split(','))
            if winner not in scores:
                scores[winner] = 0
            scores[winner] += (score1 - score2)
        except (ValueError, IndexError):
            continue
    return scores