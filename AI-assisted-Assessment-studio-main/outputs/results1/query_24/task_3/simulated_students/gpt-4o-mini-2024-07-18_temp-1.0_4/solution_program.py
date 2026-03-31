def calculate_board_game_score(game_results):
    scores = {}
    for result in game_results:
        parts = result.split(':')
        if len(parts) != 2:
            continue
        winner, score_part = parts[0], parts[1]
        if winner not in scores:
            scores[winner] = 0
        score_parts = score_part.split(',')
        if len(score_parts) != 2:
            continue
        try:
            score1 = int(score_parts[0])
            score2 = int(score_parts[1])
        except ValueError:
            continue
        if score1 > score2:
            scores[winner] += (score1 - score2)
    return scores