def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        try:
            winner, score_str = result.split(':')
            score1, score2 = map(int, score_str.split(','))
            if winner in scores:
                scores[winner] += (score1 - score2)
            else:
                scores[winner] = (score1 - score2)
        except (ValueError, IndexError):
            continue
    return scores