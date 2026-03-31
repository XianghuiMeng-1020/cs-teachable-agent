def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        parts = result.split(':')
        if len(parts) != 2:
            continue
        winner, scores_part = parts
        if not (winner.isalpha() and len(winner) == 1 and winner.isupper()):
            continue
        score_parts = scores_part.split(',')
        if len(score_parts) != 2:
            continue
        try:
            score1 = int(score_parts[0])
            score2 = int(score_parts[1])
        except ValueError:
            continue
        score_difference = score1 - score2
        if winner not in scores:
            scores[winner] = 0
        scores[winner] += score_difference
    return scores