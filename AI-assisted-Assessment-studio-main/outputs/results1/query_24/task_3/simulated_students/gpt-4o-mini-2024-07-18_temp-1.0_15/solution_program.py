def calculate_board_game_score(game_results):
    scores = {}

    for result in game_results:
        try:
            winner, scores_str = result.split(':')
            score1, score2 = map(int, scores_str.split(','))
            score_difference = score1 - score2

            if winner not in scores:
                scores[winner] = 0
            scores[winner] += score_difference
        except:
            continue

    return scores